import os
import sys
import json
import re
import argparse
from pathlib import Path
from flask import Flask, render_template, abort, redirect, url_for
import markdown
from dotenv import load_dotenv

# Ensure sync_data helper imports work by adding workspace root to sys.path
WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
if str(WORKSPACE_ROOT) not in sys.path:
    sys.path.append(str(WORKSPACE_ROOT))

# Load environment variables
load_dotenv(dotenv_path=WORKSPACE_ROOT / ".env")
AIRTABLE_PAT = os.getenv("AIRTABLE_PAT")
AIRTABLE_BASE_ID = os.getenv("AIRTABLE_BASE_ID")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")

from scripts.sync_data import load_schema_map, slugify, hash_id, get_record_title

CACHE_PATH = WORKSPACE_ROOT / "preview_app" / "airtable_cache.json"

app = Flask(__name__)
app.jinja_env.add_extension('jinja2.ext.do')

from markupsafe import Markup

# Custom Jinja2 filters for Jekyll Liquid compatibility
@app.template_filter('markdownify')
def markdownify_filter(s):
    if not s:
        return ""
    return Markup(markdown.markdown(str(s)))

@app.template_filter('downcase')
def downcase_filter(s):
    if not s:
        return ""
    return str(s).lower()

@app.template_filter('truncatewords')
def truncatewords_filter(s, num):
    if not s:
        return ""
    words = str(s).split()
    if len(words) > num:
        return " ".join(words[:num]) + "..."
    return " ".join(words)

def fetch_and_cache_data():
    from pyairtable import Api
    if not AIRTABLE_PAT or not AIRTABLE_BASE_ID:
        raise Exception("Error: AIRTABLE_PAT and AIRTABLE_BASE_ID must be set in your environment or .env file.")
    
    api = Api(AIRTABLE_PAT)
    base = api.base(AIRTABLE_BASE_ID)
    schema_map = load_schema_map()
    
    print("Fetching data from Airtable...")
    TABLE_NAMES = ["Cases", "Organisations", "Resources", "Participants", "Locations", "Messages"]
    name_to_id = {table_data["name"]: t_id for t_id, table_data in schema_map.items()}
    
    records_cache = {}
    id_to_slug = {}
    used_slugs_by_table = {}
    
    for name in TABLE_NAMES:
        if name not in name_to_id:
            continue
        t_id = name_to_id[name]
        print(f"  Fetching {name} ({t_id})...")
        records = base.table(t_id).all(use_field_ids=True)
        records_cache[t_id] = {r["id"]: r["fields"] for r in records}
        
        # Generate slugs for all records in the table
        used_slugs_by_table[t_id] = set()
        for rec_id, fields in records_cache[t_id].items():
            title = get_record_title(fields, t_id, schema_map, rec_id)
            base_slug = slugify(title)
            if not base_slug:
                base_slug = hash_id(rec_id)
            
            slug = base_slug
            counter = 1
            while slug in used_slugs_by_table[t_id]:
                slug = f"{base_slug}-{counter}"
                counter += 1
            used_slugs_by_table[t_id].add(slug)
            id_to_slug[rec_id] = slug

    cache_data = {
        "records": records_cache,
        "id_to_slug": id_to_slug
    }
    
    CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with open(CACHE_PATH, "w") as f:
        json.dump(cache_data, f, indent=2)
    print(f"Cache successfully saved to {CACHE_PATH}")
    return cache_data

def load_cache(force_refresh=False):
    if force_refresh or not CACHE_PATH.exists():
        return fetch_and_cache_data()
    with open(CACHE_PATH, "r") as f:
        return json.load(f)

def resolve_fields_for_preview(rec_fields, current_table_id, schema_map, id_to_slug):
    resolved = {}
    table_fields = schema_map.get(current_table_id, {}).get("fields", {})
    
    for field_id, value in rec_fields.items():
        field_info = table_fields.get(field_id)
        if not field_info or not field_info.get("sync", False):
            continue
            
        key_name = field_info.get("slug", field_id)
        
        # Resolve record links
        if field_info["type"] == "multipleRecordLinks":
            linked_slugs = []
            for l_rec_id in value:
                if l_rec_id in id_to_slug:
                    linked_slugs.append(id_to_slug[l_rec_id])
            resolved[key_name] = linked_slugs
        # Leave attachments as is (direct Airtable links)
        else:
            resolved[key_name] = value
            
    return resolved

def get_resolved_collections(cache, schema_map):
    collections_config = {
        "Organisations": "organisations",
        "Resources": "resources",
        "Participants": "participants",
        "Locations": "locations",
        "Messages": "messages"
    }
    name_to_id = {table_data["name"]: t_id for t_id, table_data in schema_map.items()}
    id_to_slug = cache["id_to_slug"]
    
    collections = {}
    for t_name, col_key in collections_config.items():
        t_id = name_to_id.get(t_name)
        if not t_id or t_id not in cache["records"]:
            collections[col_key] = {}
            continue
            
        resolved_col = {}
        for rec_id, rec_fields in cache["records"][t_id].items():
            slug = id_to_slug.get(rec_id)
            if slug:
                resolved_rec = resolve_fields_for_preview(rec_fields, t_id, schema_map, id_to_slug)
                title = get_record_title(rec_fields, t_id, schema_map, rec_id)
                resolved_rec["title"] = title
                resolved_rec["slug"] = slug
                resolved_rec["airtable_id"] = hash_id(rec_id)
                resolved_col[slug] = resolved_rec
        collections[col_key] = resolved_col
    return collections

@app.route('/case/<record_id>')
def preview_case(record_id):
    cache = load_cache()
    schema_map = load_schema_map()
    
    # Locate Cases table ID
    case_table_id = None
    for t_id, table_data in schema_map.items():
        if table_data["name"] == "Cases":
            case_table_id = t_id
            break
            
    if not case_table_id or record_id not in cache["records"].get(case_table_id, {}):
        abort(404, description=f"Case record with ID '{record_id}' not found in cache. Try running with --refresh or visiting /refresh/{record_id}.")
        
    rec_fields = cache["records"][case_table_id][record_id]
    id_to_slug = cache["id_to_slug"]
    
    # Resolve fields for Case
    resolved_case = resolve_fields_for_preview(rec_fields, case_table_id, schema_map, id_to_slug)
    title = get_record_title(rec_fields, case_table_id, schema_map, record_id)
    resolved_case["title"] = title
    resolved_case["slug"] = id_to_slug.get(record_id)
    resolved_case["airtable_id"] = hash_id(record_id)
    
    # Get other collections
    collections = get_resolved_collections(cache, schema_map)
    
    return render_template(
        'case.html',
        page=resolved_case,
        site=collections,
        record_id=record_id
    )

@app.route('/refresh/<record_id>')
def refresh_case(record_id):
    load_cache(force_refresh=True)
    return redirect(url_for('preview_case', record_id=record_id))

@app.route('/describe/<record_id>')
def describe_case(record_id):
    if not GEMINI_API_KEY:
        return {"status": "error", "message": "GEMINI_API_KEY environment variable not configured. Please set it in your .env file."}, 500

    # 1. Refresh cache
    try:
        cache = load_cache(force_refresh=True)
        schema_map = load_schema_map()
    except Exception as e:
        return {"status": "error", "message": f"Failed to refresh cache from Airtable: {str(e)}"}, 500
    
    # 2. Locate Cases table ID
    case_table_id = None
    for t_id, table_data in schema_map.items():
        if table_data["name"] == "Cases":
            case_table_id = t_id
            break
            
    if not case_table_id or record_id not in cache["records"].get(case_table_id, {}):
        abort(404, description=f"Case record with ID '{record_id}' not found.")

    rec_fields = cache["records"][case_table_id][record_id]
    id_to_slug = cache["id_to_slug"]
    
    # Resolve fields for Case
    resolved_case = resolve_fields_for_preview(rec_fields, case_table_id, schema_map, id_to_slug)
    title = get_record_title(rec_fields, case_table_id, schema_map, record_id)
    slug = id_to_slug.get(record_id)
    
    if not slug:
        return {"status": "error", "message": "Slug for case not found."}, 500

    # Get other collections
    collections = get_resolved_collections(cache, schema_map)

    # Extract timeline dates
    start_year = resolved_case.get('what-year-did-the-project-start')
    end_year = resolved_case.get('what-year-did-the-project-conclude')

    # Resolve lead organisations
    lead_org_slugs = resolved_case.get('lead-organisations') or []
    lead_org_names = []
    for o_slug in lead_org_slugs:
        org = collections.get('organisations', {}).get(o_slug)
        if org and org.get('title'):
            lead_org_names.append(org['title'])
        else:
            lead_org_names.append(o_slug)
    lead_orgs_str = ", ".join(lead_org_names) if lead_org_names else "Unknown organization"

    # Initiation method
    initiation_list = resolved_case.get('how-was-the-project-initiated') or []
    initiation_str = ", ".join(initiation_list) if initiation_list else "initiated"

    # Aggregate methods, participants, and descriptions
    methods = set()
    total_participants = 0
    group_descriptions = []
    
    part_slugs = resolved_case.get('participants') or []
    for p_slug in part_slugs:
        part = collections.get('participants', {}).get(p_slug)
        if part:
            p_methods = part.get('which-of-the-following-methods-were-used-to')
            if isinstance(p_methods, list):
                methods.update(p_methods)
            elif p_methods:
                methods.add(p_methods)
            
            count = part.get('how-many-people-took-part')
            if count:
                try:
                    total_participants += int(count)
                except ValueError:
                    pass
            
            desc = part.get('group-description')
            if desc:
                group_descriptions.append(desc)
    
    methods_str = ", ".join(sorted(list(methods))) if methods else "various methods"

    # Construct the prompt for Gemini
    prompt = f"""You are an expert editor for the PAVE (Participation and Voicing Engagement) Case Book.
Your task is to generate two, natural-sounding prose descriptions of a public participation project about AI.

The first description MUST exactly follow this sentence structure template:
In/between dates, lead organisation {{commissioned / initiated etc}} a process that used {{methods}} to involve approximately {{N}} people in {{kind of activity}} to {{purpose}} with {{intended outcomes}}.

Here are the guidelines for each part of the sentence:
1. "In/between dates": Describe the time period. E.g., "In 2024", "Between 2023 and 2024", "Beginning in 2025".
2. "lead organisation": The name of the organization leading the process. Nicely prefix it with "the" if appropriate (e.g., "the Stanford Deliberative Democracy Lab", "Connected by Data").
3. "{{commissioned / initiated etc}}": A verb representing how the project was started, like "commissioned", "initiated", "co-created", "hosted", "piloted". Choose the best fit based on the initiation method.
4. "{{methods}}": Natural phrasing listing the participation methods used (e.g., "surveys and focus groups", "a citizens' assembly", "deliberative community gatherings").
5. "approximately {{N}} people": Specify the count of participants (e.g., "approximately 207 people" or "approximately 1,545 participants"). If no count is available, write "an unrecorded number of citizens" or similar.
6. "in {{kind of activity}}": Describe the activity/setting (e.g., "in public consultations across Morocco and Paraguay", "in video design sessions", "in classroom workshops").
7. "to {{purpose}}": The goal or target of the involvement (e.g., "to inform policy-making and build community power with respect to AI", "to shape the deployment of risk prediction algorithms").
8. "with {{intended outcomes}}": The expected results (e.g., "with the intended outcome of creating re-usable participation tools and methods", "with the goal of guiding industry product decisions").

The second description, separated from the first by line breaks and ------ may summarise methods, and vary the placement of the key facts, in order to draw attention to significant aspects of the case. Do not use hyperbole or make unsubstantianted claims about the importance of the case. 

Each description should be one or two sentences long, and should flow naturally and grammatically. Do not include any explanations, markdown code blocks, or additional text. Just output the sentence.

Here is the data for this case study:
- Project Title: {title}
- Timeline: Start Year: {start_year}, End Year: {end_year}
- Lead Organisation(s): {lead_orgs_str}
- Initiation Method: {initiation_str}
- Methods Used: {methods_str}
- Total Participants: {total_participants if total_participants > 0 else 'Unknown'}
- Participant Group Descriptions: {"; ".join(group_descriptions) if group_descriptions else 'Unknown'}
- Goals: {resolved_case.get('project-goals')}
- Brief Description: {resolved_case.get('provide-a-brief-description-of-the-project')}
- Inclusion Efforts: {resolved_case.get('inclusion-efforts')}
- Project Limitations: {resolved_case.get('what-limitations-to-the-project-should-be-noted')}
- Subject Matter Focus: {resolved_case.get('describe-the-subject-matter-in-your-own-words-one')}

Generate the single conforming sentence:"""

    # Call Gemini API via requests
    import requests
    models_to_try = [GEMINI_MODEL]
    if GEMINI_MODEL != "gemini-2.5-flash":
        models_to_try.append("gemini-2.5-flash")
    
    last_error = None
    prose_desc = None
    for model in models_to_try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={GEMINI_API_KEY}"
        headers = {"Content-Type": "application/json"}
        payload = {
            "contents": [{
                "parts": [{
                    "text": prompt
                }]
            }],
            "generationConfig": {
                "temperature": 0.2
            }
        }
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            resp_json = response.json()
            prose_desc = resp_json["candidates"][0]["content"]["parts"][0]["text"].strip()
            break  # Success!
        except Exception as e:
            last_error = str(e)
            if hasattr(e, "response") and e.response is not None:
                try:
                    last_error = f"{e.response.status_code} Server Error: {e.response.json().get('error', {}).get('message', str(e))}"
                except:
                    pass
            continue
            
    if not prose_desc:
        return {"status": "error", "message": f"Gemini API request failed: {last_error}"}, 500

    # Clean prose
    prose_desc = prose_desc.strip().strip('"').strip("'")
    if prose_desc.startswith("`") and prose_desc.endswith("`"):
        prose_desc = prose_desc.strip("`").strip()

    return {
        "status": "success",
        "slug": slug,
        "description": prose_desc
    }


# Serve compiled Jekyll assets (CSS) and other static files locally
@app.route('/pave/assets/<path:filename>')
@app.route('/assets/<path:filename>')
def serve_assets(filename):
    candidates = []
    
    # Candidate 1: Local self-contained static folder
    static_dir = Path(__file__).resolve().parent / "static"
    static_path = static_dir / filename
    if static_path.exists():
        candidates.append(static_path)
        
    # Candidates 2: Parent repo folders (Jekyll workspace)
    for folder in ["_site/assets", "assets"]:
        parent_path = WORKSPACE_ROOT / folder / filename
        if parent_path.exists():
            candidates.append(parent_path)
            
    if not candidates:
        abort(404)
        
    # Serve the candidate with the latest modification time to prevent serving stale assets
    newest_path = max(candidates, key=lambda p: p.stat().st_mtime)
    
    from flask import send_from_directory
    return send_from_directory(str(newest_path.parent), newest_path.name)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Standalone Flask preview application.")
    parser.add_argument("--refresh", action="store_true", help="Force refresh Airtable cache on startup")
    parser.add_argument("--port", type=int, default=8000, help="Port to run Flask app on (default: 8000)")
    args = parser.parse_args()
    
    if args.refresh or not CACHE_PATH.exists():
        load_cache(force_refresh=True)
        
    app.run(debug=True, port=args.port)
