"""
Automated Zenodo Version Publisher for Alternative Life Manuscript.

Uses the Zenodo InvenioRDM REST API to:
  1. Create a new draft version from record 23574418.
  2. Upload the updated 'Alternative Life Manuscript.docx' and 'Alternative Life Manuscript.pdf'.
  3. Update version metadata to 'v1.1'.
  4. Publish the new version.

Usage:
  python scripts/publish_zenodo_v2.py --token <YOUR_ZENODO_TOKEN>
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path
import httpx


ZENODO_API_BASE = "https://zenodo.org/api"
RECORD_ID = "23574418"


def publish_new_zenodo_version(token: str, publish: bool = True) -> None:
    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json"
    }

    print(f"[*] Contacting Zenodo for record {RECORD_ID}...")
    with httpx.Client(base_url=ZENODO_API_BASE, headers=headers, timeout=60.0) as client:
        # Step 1: Create a new draft version
        print("[*] Creating new version draft on Zenodo...")
        resp = client.post(f"/records/{RECORD_ID}/versions")
        if resp.status_code not in (200, 201):
            print(f"[!] Error creating new version: HTTP {resp.status_code} - {resp.text}", file=sys.stderr)
            sys.exit(1)

        draft_data = resp.json()
        draft_id = draft_data.get("id")
        draft_links = draft_data.get("links", {})
        print(f"[+] Draft version created successfully! Draft ID: {draft_id}")

        # Step 2: Prepare file list
        docx_path = Path("Alternative Life Manuscript.docx").resolve()
        pdf_path = Path("Alternative Life Manuscript.pdf").resolve()
        files_to_upload = [docx_path, pdf_path]

        for file_path in files_to_upload:
            if not file_path.exists():
                print(f"[!] File not found: {file_path}", file=sys.stderr)
                sys.exit(1)

            file_key = file_path.name
            print(f"[*] Initializing upload for: {file_key}...")
            # Init file entry
            init_resp = client.post(f"/records/{draft_id}/draft/files", json=[{"key": file_key}])
            if init_resp.status_code not in (200, 201):
                # If already exists in draft, proceed
                pass

            # Upload raw file content
            print(f"[*] Uploading bytes ({file_path.stat().st_size} bytes) for {file_key}...")
            with open(file_path, "rb") as f:
                upload_resp = client.put(
                    f"/records/{draft_id}/draft/files/{file_key}/content",
                    content=f.read(),
                    headers={"Content-Type": "application/octet-stream"}
                )
            if upload_resp.status_code not in (200, 201):
                print(f"[!] Failed to upload content for {file_key}: {upload_resp.text}", file=sys.stderr)
                sys.exit(1)

            # Commit the file
            print(f"[*] Committing {file_key}...")
            commit_resp = client.post(f"/records/{draft_id}/draft/files/{file_key}/commit")
            if commit_resp.status_code not in (200, 201):
                print(f"[!] Warning committing {file_key}: {commit_resp.text}")

        # Step 3: Update metadata
        print("[*] Updating metadata for version v1.1...")
        meta_payload = draft_data.get("metadata", {})
        meta_payload["version"] = "v1.1"
        meta_resp = client.put(f"/records/{draft_id}/draft", json={"metadata": meta_payload})
        if meta_resp.status_code not in (200, 200):
            print(f"[!] Warning updating metadata: {meta_resp.status_code} - {meta_resp.text}")

        # Step 4: Publish
        if publish:
            print("[*] Publishing new version on Zenodo...")
            pub_resp = client.post(f"/records/{draft_id}/draft/actions/publish")
            if pub_resp.status_code in (200, 201, 202):
                pub_data = pub_resp.json()
                new_doi = pub_data.get("doi")
                print("\n" + "=" * 65)
                print(f"[SUCCESS] Zenodo Version 1.1 published successfully!")
                print(f"New Version DOI: {new_doi}")
                print(f"Record URL: {pub_data.get('links', {}).get('self_html')}")
                print("=" * 65 + "\n")
            else:
                print(f"[!] Error publishing: HTTP {pub_resp.status_code} - {pub_resp.text}", file=sys.stderr)
        else:
            print(f"[*] Draft {draft_id} updated and ready for manual review at: {draft_links.get('self_html')}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Publish v1.1 to Zenodo via API")
    parser.add_argument("--token", type=str, default=os.getenv("ZENODO_TOKEN"), help="Zenodo Personal Access Token")
    parser.add_argument("--no-publish", action="store_true", help="Prepare draft without publishing")
    args = parser.parse_args()

    if not args.token:
        print("[!] Error: Zenodo Personal Access Token is required.", file=sys.stderr)
        print("    Pass --token <TOKEN> or set the ZENODO_TOKEN environment variable.", file=sys.stderr)
        print("    Generate one here: https://zenodo.org/account/settings/applications/tokens/new/", file=sys.stderr)
        sys.exit(1)

    publish_new_zenodo_version(args.token, publish=not args.no_publish)


if __name__ == "__main__":
    main()
