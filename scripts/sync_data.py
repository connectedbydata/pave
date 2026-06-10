import os
import requests
import yaml
import json
import re
import hashlib
from dotenv import load_dotenv
from pyairtable import Api
from pathlib import Path

# Load environment variables
load_dotenv()

AIRTABLE_PAT = os.getenv("AIRTABLE_PAT")
AIRTABLE_BASE_ID = os.getenv("AIRTABLE_BASE_ID")
SCHEMA_PATH = Path("_data/schema_map.yml")

if not AIRTABLE_PAT or not AIRTABLE_BASE_ID:
    print("Error: AIRTABLE_PAT and AIRTABLE_BASE_ID must be provided.")
    print("Ensure they are set in your .env file (local) or added as Repository Secrets (GitHub Actions).")
    exit(1)

if not SCHEMA_PATH.exists():
    print(f"Error: Schema map not found at {SCHEMA_PATH}. Run scripts/sync_schema.py first.")
    exit(1)

api = Api(AIRTABLE_PAT)
base = api.base(AIRTABLE_BASE_ID)

# Target tables
TABLE_CONFIG = {
    "Cases": {"dir": Path("_cases"), "collection": "cases"},
    "Organisations": {"dir": Path("_organisations"), "collection": "organisations"},
    "Resources": {"dir": Path("_resources"), "collection": "resources"},
    "Participants": {"dir": Path("_participants"), "collection": "participants"},
    "Locations": {"dir": Path("_locations"), "collection": "locations"},
    "Messages": {"dir": Path("_messages"), "collection": "messages"}
}
TABLE_NAMES = list(TABLE_CONFIG.keys())
ATTACHMENT_DIR = Path("assets/attachments")

# Sync Settings
FILTER_FIELD_ID = "fldrM6RRk8easAxSq"  # Default: Workflow: Status
FILTER_VALUES = ["Completed","Draft","Nomination","Submission"]           # Only sync records with these status values

def slugify(text):
    text = str(text).lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text)
    text = text.strip('-')
    return text[:100].rstrip('-')

def hash_id(record_id):
    if not record_id:
        return record_id
    return hashlib.sha256(record_id.encode()).hexdigest()[:16]

def is_record_id(value):
    """Check if a value looks like a raw Airtable record ID."""
    if isinstance(value, str):
        return value.startswith("rec") and len(value) >= 14
    if isinstance(value, list) and len(value) > 0:
        return all(isinstance(v, str) and v.startswith("rec") and len(v) >= 14 for v in value)
    return False

def load_schema_map():
    with open(SCHEMA_PATH, "r") as f:
        return yaml.safe_load(f)

def download_attachment(url, filename, record_id, field_id, suffix="", attachment_id=None):
    ATTACHMENT_DIR.mkdir(parents=True, exist_ok=True)
    
    hashed_rec_id = hash_id(record_id)
    ext = Path(filename).suffix
    if attachment_id:
        local_filename = f"{hashed_rec_id}_{field_id}_{attachment_id}_{suffix}{ext}" if suffix else f"{hashed_rec_id}_{field_id}_{attachment_id}{ext}"
    else:
        local_filename = f"{hashed_rec_id}_{field_id}_{suffix}_{filename}" if suffix else f"{hashed_rec_id}_{field_id}_{filename}"
    
    local_path = ATTACHMENT_DIR / local_filename
    
    if not local_path.exists():
        print(f"    Downloading {attachment_id or filename} {suffix}..." if suffix else f"    Downloading {attachment_id or filename}...")
        r = requests.get(url, stream=True)
        if r.status_code == 200:
            with open(local_path, 'wb') as f:
                for chunk in r.iter_content(1024):
                    f.write(chunk)
    return f"/assets/attachments/{local_filename}"

def get_record_title(fields, table_id, schema_map, record_id):
    """Determine the title for a record based on schema and common field names."""
    table_fields = schema_map.get(table_id, {}).get("fields", {})
    
    # Try primary field
    primary_id = schema_map.get(table_id, {}).get("primaryFieldId")
    if primary_id and primary_id in fields:
        return str(fields[primary_id])
        
    # Fallback to common name fields
    for f_id, f_val in fields.items():
        f_info = table_fields.get(f_id)
        if f_info:
            clean_name = f_info["name"].strip().lower().replace("\ufeff", "")
            if clean_name in ["title", "name", "project title", "case name"]:
                return str(f_val)
    
    return record_id

def resolve_fields(data, schema_map, current_table_id, rec_id, id_to_slug, synced_ids):
    resolved = {}
    table_fields = schema_map.get(current_table_id, {}).get("fields", {})
    
    for field_id, value in data.items():
        field_info = table_fields.get(field_id)
        
        # Only process if field is in schema and marked for sync
        if not field_info or not field_info.get("sync", False):
            continue

        # Skip if value is solely a record ID and not a link
        if is_record_id(value) and field_info["type"] != "multipleRecordLinks":
            continue

        key_name = field_info.get("slug", field_id)

        # Check if it's a multiple record link
        if field_info["type"] == "multipleRecordLinks":
            linked_slugs = []
            for l_rec_id in value:
                # ONLY include links to records that are actually being synced
                if l_rec_id in synced_ids and l_rec_id in id_to_slug:
                    linked_slugs.append(id_to_slug[l_rec_id])
            resolved[key_name] = linked_slugs
        
        # Handle attachments
        elif field_info["type"] == "multipleAttachments":
            local_attachments = []
            for att in value:
                att_id = att.get("id")
                local_url = download_attachment(att["url"], att["filename"], rec_id, field_id, attachment_id=att_id)
                new_att = {**att, "url": local_url}
                if "thumbnails" in att:
                    new_thumbnails = {}
                    for size, thumb in att["thumbnails"].items():
                        thumb_url = download_attachment(thumb["url"], att["filename"], rec_id, field_id, suffix=size, attachment_id=att_id)
                        new_thumbnails[size] = {**thumb, "url": thumb_url}
                    new_att["thumbnails"] = new_thumbnails
                local_attachments.append(new_att)
            resolved[key_name] = local_attachments
        else:
            resolved[key_name] = value
    return resolved

def annotate_yaml(yaml_str, field_map):
    lines = yaml_str.splitlines()
    new_lines = []
    skip_keys = {"layout", "title", "airtable_id", "slug", "redirect_from"}
    for line in lines:
        # Match "some-key:" or "  some-key:" or "- some-key:"
        match = re.search(r'^(\s*)(?:-\s+)?([a-zA-Z0-9_-]+):', line)
        if match:
            indent, key = match.groups()
            if key not in skip_keys and key in field_map:
                # Always prepend the comment on the line before
                new_lines.append(f"{indent}# {field_map[key]}")
        new_lines.append(line)
    return "\n".join(new_lines)

def main():
    schema_map = load_schema_map()
    
    # Map all field slugs and IDs to names for comment addition
    field_slug_to_name = {}
    for t_data in schema_map.values():
        for f_id, f_info in t_data.get("fields", {}).items():
            slug = f_info.get("slug")
            if slug:
                field_slug_to_name[slug] = f_info["name"]
            else:
                field_slug_to_name[f_id] = f_info["name"]

    # Map names to IDs for easier fetching
    name_to_id = {table_data["name"]: t_id for t_id, table_data in schema_map.items()}
    
    print("Fetching records from Airtable...")
    all_tables_data = {}
    id_to_slug = {}
    used_slugs_by_table = {}

    for name in TABLE_NAMES:
        if name in name_to_id:
            t_id = name_to_id[name]
            print(f"  Fetching {name} ({t_id})...")
            records = base.table(t_id).all(use_field_ids=True)
            all_tables_data[t_id] = {r["id"]: r["fields"] for r in records}
            
            # Generate slugs first for cross-referencing
            used_slugs_by_table[t_id] = set()
            for rec_id, fields in all_tables_data[t_id].items():
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
        else:
            print(f"  Warning: Table '{name}' not found in schema map.")

    # 1. Identify active cases
    case_table_id = name_to_id.get("Cases")
    active_case_ids = set()
    
    if case_table_id and case_table_id in all_tables_data:
        for rec_id, fields in all_tables_data[case_table_id].items():
            # Apply filtering
            if FILTER_FIELD_ID:
                current_status = fields.get(FILTER_FIELD_ID)
                if isinstance(current_status, list):
                    if not any(s in FILTER_VALUES for s in current_status):
                        continue
                elif current_status not in FILTER_VALUES:
                    continue
            active_case_ids.add(rec_id)

    # 2. Recursively find all reachable non-case records
    referenced_ids = set(active_case_ids)
    to_expand = list(active_case_ids)
    
    while to_expand:
        current_id = to_expand.pop()
        
        # Find which table this record belongs to
        found_fields = None
        found_table_id = None
        for t_id, t_data in all_tables_data.items():
            if current_id in t_data:
                found_fields = t_data[current_id]
                found_table_id = t_id
                break
        
        if found_fields:
            table_fields = schema_map.get(found_table_id, {}).get("fields", {})
            for f_id, f_val in found_fields.items():
                f_info = table_fields.get(f_id)
                # Only follow links if the field itself is marked for sync
                if f_info and f_info.get("sync") and f_info["type"] == "multipleRecordLinks" and isinstance(f_val, list):
                    for ref in f_val:
                        # Determine if the reference is to a Case or something else
                        is_ref_case = False
                        for t_id, t_data in all_tables_data.items():
                            if ref in t_data:
                                if t_id == case_table_id:
                                    is_ref_case = True
                                break
                        
                        # Rules:
                        # - If it's a Case, only include if it's already an ACTIVE case
                        # - If it's not a Case, include it and continue expanding
                        if is_ref_case:
                            if ref in active_case_ids:
                                referenced_ids.add(ref)
                        else:
                            if ref not in referenced_ids:
                                referenced_ids.add(ref)
                                to_expand.append(ref)

    # 3. Process each table and write only referenced records
    for table_name, config in TABLE_CONFIG.items():
        t_id = name_to_id.get(table_name)
        if not t_id or t_id not in all_tables_data:
            continue

        print(f"Processing {table_name}...")
        config["dir"].mkdir(exist_ok=True)
        # Clear existing
        for f in config["dir"].glob("*.md"):
            f.unlink()
        
        sync_count = 0
        for rec_id, fields in all_tables_data[t_id].items():
            # Only sync if it's in our discovered referenced set
            if rec_id not in referenced_ids:
                continue

            # Resolve fields (cross-references use slugs, filtered by referenced_ids)
            final_data = resolve_fields(fields, schema_map, t_id, rec_id, id_to_slug, referenced_ids)
            
            title = get_record_title(fields, t_id, schema_map, rec_id)
            slug = id_to_slug[rec_id]

            if table_name == "Cases":
                layout = "case"
                redirects = [f"/c/{hash_id(rec_id)}/"]
            elif table_name == "Organisations":
                layout = "organisation"
                redirects = None
            else:
                layout = "generic"
                redirects = None
            
            front_matter = {
                "layout": layout,
                "title": title,
                "airtable_id": hash_id(rec_id),
                "slug": slug,
            }
            if redirects:
                front_matter["redirect_from"] = redirects
            front_matter.update(final_data)
            
            file_path = config["dir"] / f"{slug}.md"
            with open(file_path, "w") as f:
                f.write("---\n")
                fm_yaml = yaml.dump(front_matter, sort_keys=False)
                f.write(annotate_yaml(fm_yaml, field_slug_to_name))
                f.write("\n---\n")
            sync_count += 1
        print(f"  {sync_count} records processed for {table_name}.")

    print(f"Sync complete!")

if __name__ == "__main__":
    main()
