import os
import requests
import yaml
import argparse
import re
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
load_dotenv()

AIRTABLE_PAT = os.getenv("AIRTABLE_PAT")
AIRTABLE_BASE_ID = os.getenv("AIRTABLE_BASE_ID")
SCHEMA_PATH = Path("_data/schema_map.yml")

def generate_field_slug(name):
    # Remove BOM and other weird characters
    name = name.replace("\ufeff", "")
    # Lowercase
    name = name.lower()
    # Keep only letters, numbers, spaces, and hyphens
    name = re.sub(r'[^a-z0-9\s-]', '', name)
    # Replace spaces and underscores/hyphens with a single hyphen
    slug = re.sub(r'[\s_-]+', '-', name).strip('-')
    # Limit to 50 characters
    if len(slug) > 50:
        truncated = slug[:50]
        if '-' in truncated:
            slug = truncated.rsplit('-', 1)[0]
        else:
            slug = truncated
    return slug

def fetch_schema():
    url = f"https://api.airtable.com/v0/meta/bases/{AIRTABLE_BASE_ID}/tables"
    headers = {"Authorization": f"Bearer {AIRTABLE_PAT}"}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()["tables"]

def main():
    parser = argparse.ArgumentParser(description="Sync Airtable schema and manage field sync status.")
    parser.add_argument("--default-sync", choices=["on", "off"], default="off", help="Set default sync status for new fields (default: off)")
    parser.add_argument("--reset-all", choices=["on", "off"], help="Force reset all fields to on or off")
    args = parser.parse_args()

    if not AIRTABLE_PAT or not AIRTABLE_BASE_ID:
        print("Error: AIRTABLE_PAT and AIRTABLE_BASE_ID must be provided.")
        print("Ensure they are set in your .env file (local) or added as Repository Secrets (GitHub Actions).")
        exit(1)

    print("Fetching schema from Airtable...")
    tables_schema = fetch_schema()
    
    # Load existing schema map if it exists
    existing_schema = {}
    if SCHEMA_PATH.exists():
        with open(SCHEMA_PATH, "r") as f:
            existing_schema = yaml.safe_load(f) or {}

    new_schema = {}
    default_sync_bool = (args.default_sync == "on")
    
    for table in tables_schema:
        t_id = table["id"]
        t_name = table["name"]
        
        # Preserve or create table entry
        existing_table = existing_schema.get(t_id, {})
        primary_field_id = table["fields"][0]["id"] if table["fields"] else None
        
        # First pass to collect and reserve all existing slugs
        used_slugs = set()
        for f in table["fields"]:
            f_id = f["id"]
            existing_field = existing_table.get("fields", {}).get(f_id, {})
            existing_slug = existing_field.get("slug")
            if existing_slug:
                used_slugs.add(existing_slug)

        new_table_fields = {}
        for f in table["fields"]:
            f_id = f["id"]
            existing_field = existing_table.get("fields", {}).get(f_id, {})
            
            # Determine sync status
            sync_status = existing_field.get("sync", default_sync_bool)
            if args.reset_all:
                sync_status = (args.reset_all == "on")
            
            # Slug generation / preservation
            slug = existing_field.get("slug")
            if not slug:
                base_slug = generate_field_slug(f["name"])
                if not base_slug:
                    base_slug = "field"
                slug = base_slug
                counter = 1
                while slug in used_slugs:
                    slug = f"{base_slug}-{counter}"
                    counter += 1
                used_slugs.add(slug)

            field_data = {
                "name": f["name"],
                "type": f["type"],
                "sync": sync_status,
                "slug": slug
            }
            
            # Check for name change
            existing_name = existing_field.get("name")
            new_name = f["name"]
            if existing_name and existing_name != new_name:
                field_data["comment"] = f"Name changed from \"{existing_name}\" - field slug not updated yet"
            elif "comment" in existing_field:
                field_data["comment"] = existing_field["comment"]
            
            # Include choices
            if "choices" in f.get("options", {}):
                field_data["choices"] = [c["name"] for c in f["options"]["choices"]]
            
            # Include linkedTableId
            if "linkedTableId" in f.get("options", {}):
                field_data["options"] = {"linkedTableId": f["options"]["linkedTableId"]}
            
            new_table_fields[f_id] = field_data
            
        new_schema[t_id] = {
            "name": t_name,
            "primaryFieldId": primary_field_id,
            "fields": new_table_fields
        }

    # Save the updated schema
    SCHEMA_PATH.parent.mkdir(exist_ok=True)
    with open(SCHEMA_PATH, "w") as f:
        yaml.dump(new_schema, f, sort_keys=False)

    print(f"Schema map updated at {SCHEMA_PATH}")
    if args.reset_all:
        print(f"All fields have been forced to: {args.reset_all}")
    else:
        print(f"New fields default to: {args.default_sync}")

if __name__ == "__main__":
    main()
