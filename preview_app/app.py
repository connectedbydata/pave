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

# Serve compiled Jekyll assets (CSS) and other static files locally
@app.route('/pave/assets/<path:filename>')
@app.route('/assets/<path:filename>')
def serve_assets(filename):
    for folder in ["_site/assets", "assets"]:
        target_dir = WORKSPACE_ROOT / folder
        if (target_dir / filename).exists():
            from flask import send_from_directory
            return send_from_directory(str(target_dir), filename)
    abort(404)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Standalone Flask preview application.")
    parser.add_argument("--refresh", action="store_true", help="Force refresh Airtable cache on startup")
    parser.add_argument("--port", type=int, default=8000, help="Port to run Flask app on (default: 8000)")
    args = parser.parse_args()
    
    if args.refresh or not CACHE_PATH.exists():
        load_cache(force_refresh=True)
        
    app.run(debug=True, port=args.port)
