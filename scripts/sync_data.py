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
    print("Error: AIRTABLE_PAT and AIRTABLE_BASE_ID must be set in .env")
    exit(1)

if not SCHEMA_PATH.exists():
    print(f"Error: Schema map not found at {SCHEMA_PATH}. Run scripts/sync_schema.py first.")
    exit(1)

api = Api(AIRTABLE_PAT)
base = api.base(AIRTABLE_BASE_ID)

# Target tables
TABLE_NAMES = ["Cases", "Organisations", "Resources", "Participants", "Locations"]
ATTACHMENT_DIR = Path("assets/attachments")
CASES_DIR = Path("_cases")

# Sync Settings
FILTER_FIELD_ID = "fldrM6RRk8easAxSq"  # Default: Workflow: Status
FILTER_VALUES = ["Completed"]           # Only sync records with these status values

def slugify(text):
    text = str(text).lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_-]+', '-', text)
    text = text.strip('-')
    return text

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

def resolve_nested(data, all_tables_data, schema_map, current_table_id, rec_id):
    resolved = {}
    table_fields = schema_map.get(current_table_id, {}).get("fields", {})
    
    for field_id, value in data.items():
        field_info = table_fields.get(field_id)
        
        # Only process if field is in schema and marked for sync
        if not field_info or not field_info.get("sync", False):
            continue

        # Skip if value is solely a record ID and not resolved
        if is_record_id(value) and field_info["type"] != "multipleRecordLinks":
            continue

        # Check if it's a multiple record link
        if field_info["type"] == "multipleRecordLinks":
            linked_table_id = field_info.get("options", {}).get("linkedTableId")
            if linked_table_id and linked_table_id in all_tables_data:
                nested_records = []
                for l_rec_id in value:
                    if l_rec_id in all_tables_data[linked_table_id]:
                        l_rec_fields = all_tables_data[linked_table_id][l_rec_id]
                        processed_l_rec = resolve_nested_simple(l_rec_fields, all_tables_data, schema_map, linked_table_id, l_rec_id)
                        nested_records.append({**processed_l_rec, "id": hash_id(l_rec_id)})
                resolved[field_id] = nested_records
            # If we don't resolve it, we don't output the raw IDs
        
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
            resolved[field_id] = local_attachments
        else:
            resolved[field_id] = value
    return resolved

def resolve_nested_simple(data, all_tables_data, schema_map, current_table_id, rec_id):
    """Simplified version for nested records to prevent deep recursion but handle attachments and sync status."""
    resolved = {}
    table_fields = schema_map.get(current_table_id, {}).get("fields", {})
    
    for field_id, value in data.items():
        field_info = table_fields.get(field_id)
        if not field_info or not field_info.get("sync", False):
            continue

        # Skip if value is solely a record ID
        if is_record_id(value):
            continue
            
        if field_info["type"] == "multipleAttachments":
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
            resolved[field_id] = local_attachments
        else:
            resolved[field_id] = value
    return resolved

def annotate_yaml(yaml_str, field_map):
    lines = yaml_str.splitlines()
    new_lines = []
    for line in lines:
        # Match "fldXXXX:" or "  fldXXXX:" or "- fldXXXX:" or "  - fldXXXX:"
        match = re.search(r'^(\s*)(?:-\s+)?(fld[a-zA-Z0-9]+):', line)
        if match:
            indent, f_id = match.groups()
            if f_id in field_map:
                # Always prepend the comment on the line before
                new_lines.append(f"{indent}# {field_map[f_id]}")
        new_lines.append(line)
    return "\n".join(new_lines)

def main():
    schema_map = load_schema_map()
    
    # Map all field IDs to names for comment addition
    field_id_to_name = {}
    for t_data in schema_map.values():
        for f_id, f_info in t_data.get("fields", {}).items():
            field_id_to_name[f_id] = f_info["name"]

    # Map names to IDs for easier fetching
    name_to_id = {table_data["name"]: t_id for t_id, table_data in schema_map.items()}
    
    print("Fetching records from Airtable...")
    all_tables_data = {}
    for name in TABLE_NAMES:
        if name in name_to_id:
            t_id = name_to_id[name]
            print(f"  Fetching {name} ({t_id})...")
            records = base.table(t_id).all(use_field_ids=True)
            all_tables_data[t_id] = {r["id"]: r["fields"] for r in records}
        else:
            print(f"  Warning: Table '{name}' not found in schema map.")

    # Process Cases
    case_table_id = name_to_id.get("Cases")
    if not case_table_id:
        print("Error: 'Cases' table not found in schema map.")
        return

    CASES_DIR.mkdir(exist_ok=True)
    # Clear existing cases to avoid duplicates or orphaned files
    for f in CASES_DIR.glob("*.md"):
        f.unlink()
    
    print("Processing Cases...")
    sync_count = 0
    used_slugs = set()

    for rec_id, fields in all_tables_data[case_table_id].items():
        # Apply filtering
        if FILTER_FIELD_ID:
            current_status = fields.get(FILTER_FIELD_ID)
            if isinstance(current_status, list):
                if not any(s in FILTER_VALUES for s in current_status):
                    continue
            elif current_status not in FILTER_VALUES:
                continue

        print(f"  Processing Case {rec_id}...")
        
        # Resolve nesting and attachments (recursive, respects sync: true)
        final_data = resolve_nested(fields, all_tables_data, schema_map, case_table_id, rec_id)
        
        # Title logic
        title = rec_id
        for f_id, f_val in final_data.items():
            f_info = schema_map[case_table_id]["fields"].get(f_id)
            if f_info:
                clean_name = f_info["name"].strip().lower().replace("\ufeff", "")
                if clean_name in ["title", "name", "project title", "case name"]:
                    title = f_val
                    break

        # Generate unique slug
        base_slug = slugify(title)
        if not base_slug:
            base_slug = rec_id
        
        slug = base_slug
        counter = 1
        while slug in used_slugs:
            slug = f"{base_slug}-{counter}"
            counter += 1
        used_slugs.add(slug)

        front_matter = {
            "layout": "case",
            "title": title,
            "airtable_id": hash_id(rec_id),
            "slug": slug,
            **final_data
        }
        
        file_path = CASES_DIR / f"{slug}.md"
        with open(file_path, "w") as f:
            f.write("---\n")
            fm_yaml = yaml.dump(front_matter, sort_keys=False)
            f.write(annotate_yaml(fm_yaml, field_id_to_name))
            f.write("\n---\n")
        sync_count += 1

    print(f"Sync complete! {sync_count} records processed.")

if __name__ == "__main__":
    main()
