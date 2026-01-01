#!/usr/bin/env python3
"""
Import old Paperless-ngx documents to new instance with proper metadata mapping.
"""

import os
import sqlite3
import requests
import time
from pathlib import Path

# Configuration
PAPERLESS_URL = "http://192.168.1.221:8010"
API_TOKEN = "b808c2de4a3de3b44559585d846517c76402c8ed"
OLD_DB_PATH = r"X:\paperless-ngx\config\db.sqlite3"
OLD_ORIGINALS_PATH = r"X:\paperless-ngx\data\media\documents\originals"

HEADERS = {"Authorization": f"Token {API_TOKEN}"}

# Tag mappings: old_name -> new_id
TAG_MAPPING = {
    "Family": 5,      # Family tag exists
    "Finance": 14,    # Financial
    "School": 17,     # Education
    "Tax": 15,        # Tax
}

# Correspondent mappings: old_name -> new_id
CORRESPONDENT_MAPPING = {
    "Los Angeles Unified School District": 15,  # LAUSD
    "LA Superior Court": 10,                     # Los Angeles Superior Court
}

# Document type mappings: old_name -> new_id
DOCTYPE_MAPPING = {
    "General": None,       # No direct mapping
    "Receipts": 37,        # Receipt
    "Tax Return": 30,      # Tax Return
    "W-2": 31,             # W-2
}


def get_existing_documents():
    """Get list of existing document titles to avoid duplicates."""
    response = requests.get(
        f"{PAPERLESS_URL}/api/documents/?page_size=500",
        headers=HEADERS
    )
    data = response.json()
    # Return both titles and original filenames for duplicate checking
    existing = {
        "titles": set(d["title"] for d in data["results"]),
        "filenames": set(d["original_file_name"] for d in data["results"])
    }
    return existing


def get_old_documents():
    """Extract documents and their metadata from old database."""
    conn = sqlite3.connect(OLD_DB_PATH)

    # Get documents
    docs = conn.execute('''
        SELECT id, title, correspondent_id, document_type_id, filename, created
        FROM documents_document
    ''').fetchall()

    # Get tags
    tags = {t[0]: t[1] for t in conn.execute('SELECT id, name FROM documents_tag').fetchall()}

    # Get correspondents
    correspondents = {c[0]: c[1] for c in conn.execute('SELECT id, name FROM documents_correspondent').fetchall()}

    # Get document types
    doc_types = {d[0]: d[1] for d in conn.execute('SELECT id, name FROM documents_documenttype').fetchall()}

    # Get document-tag mappings
    doc_tags = {}
    for dt in conn.execute('SELECT document_id, tag_id FROM documents_document_tags').fetchall():
        if dt[0] not in doc_tags:
            doc_tags[dt[0]] = []
        doc_tags[dt[0]].append(dt[1])

    conn.close()

    # Build document list with metadata
    documents = []
    for doc in docs:
        doc_id, title, corr_id, dtype_id, filename, created = doc

        # Get correspondent name
        corr_name = correspondents.get(corr_id) if corr_id else None

        # Get document type name
        dtype_name = doc_types.get(dtype_id) if dtype_id else None

        # Get tag names
        tag_names = [tags[tid] for tid in doc_tags.get(doc_id, [])]

        # Build full file path
        file_path = os.path.join(OLD_ORIGINALS_PATH, filename)

        documents.append({
            "id": doc_id,
            "title": title,
            "correspondent": corr_name,
            "document_type": dtype_name,
            "tags": tag_names,
            "filename": filename,
            "file_path": file_path,
            "created": created
        })

    return documents


def upload_document(doc, existing):
    """Upload a single document to Paperless-ngx."""
    # Check for duplicates by title
    if doc["title"] in existing["titles"]:
        print(f"  SKIPPING (duplicate title): {doc['title']}")
        return False

    # Check for duplicates by filename
    original_filename = os.path.basename(doc["file_path"])
    if original_filename in existing["filenames"]:
        print(f"  SKIPPING (duplicate filename): {original_filename}")
        return False

    # Check if file exists
    if not os.path.exists(doc["file_path"]):
        print(f"  SKIPPING (file not found): {doc['file_path']}")
        return False

    # Map correspondent
    correspondent_id = None
    if doc["correspondent"]:
        correspondent_id = CORRESPONDENT_MAPPING.get(doc["correspondent"])
        if not correspondent_id:
            print(f"  WARNING: No mapping for correspondent '{doc['correspondent']}'")

    # Map document type
    document_type_id = None
    if doc["document_type"]:
        document_type_id = DOCTYPE_MAPPING.get(doc["document_type"])
        if document_type_id is None and doc["document_type"] != "General":
            print(f"  WARNING: No mapping for document type '{doc['document_type']}'")

    # Map tags
    tag_ids = []
    for tag_name in doc["tags"]:
        tag_id = TAG_MAPPING.get(tag_name)
        if tag_id:
            tag_ids.append(tag_id)
        else:
            print(f"  WARNING: No mapping for tag '{tag_name}'")

    # Determine additional tags based on content/path
    # Add Education tag for LAUSD documents
    if doc["correspondent"] == "Los Angeles Unified School District":
        if 17 not in tag_ids:
            tag_ids.append(17)  # Education

    # Add IEP tag for IEP documents
    if "IEP" in doc["title"].upper() or "Individualized Education Program" in doc["title"]:
        if 11 not in tag_ids:
            tag_ids.append(11)  # IEP tag
        if not document_type_id:
            document_type_id = 23  # IEP Document type

    # Add Tax tag for tax-related documents
    if "Tax" in doc["filename"] or "W2" in doc["title"] or "1099" in doc["title"]:
        if 15 not in tag_ids:
            tag_ids.append(15)  # Tax

    # Add Financial tag for financial documents
    if "Robinhood" in doc["title"] or "Withdrawal" in doc["title"]:
        if 14 not in tag_ids:
            tag_ids.append(14)  # Financial

    # Add person tags based on title
    if "Devin Stokes" in doc["title"]:
        if 1 not in tag_ids:
            tag_ids.append(1)  # Devin Stokes
    if "Amy Stokes" in doc["title"]:
        if 2 not in tag_ids:
            tag_ids.append(2)  # Amy Stokes

    # Prepare the upload
    print(f"  Uploading: {doc['title']}")
    print(f"    File: {original_filename}")
    print(f"    Correspondent ID: {correspondent_id}")
    print(f"    Document Type ID: {document_type_id}")
    print(f"    Tag IDs: {tag_ids}")

    # Build the multipart form data
    with open(doc["file_path"], "rb") as f:
        files = {"document": (original_filename, f, "application/pdf")}

        data = {"title": doc["title"]}

        if correspondent_id:
            data["correspondent"] = correspondent_id

        if document_type_id:
            data["document_type"] = document_type_id

        if tag_ids:
            data["tags"] = tag_ids

        if doc["created"]:
            # Format: YYYY-MM-DD
            created_date = doc["created"].split("T")[0].split(" ")[0]
            data["created"] = created_date

        response = requests.post(
            f"{PAPERLESS_URL}/api/documents/post_document/",
            headers=HEADERS,
            files=files,
            data=data
        )

        if response.status_code in [200, 201, 202]:
            print(f"    SUCCESS: Document queued for processing")
            return True
        else:
            print(f"    ERROR: {response.status_code} - {response.text}")
            return False


def main():
    print("=" * 60)
    print("Paperless-ngx Document Import Tool")
    print("=" * 60)
    print()

    # Get existing documents to avoid duplicates
    print("Fetching existing documents...")
    existing = get_existing_documents()
    print(f"  Found {len(existing['titles'])} existing documents")
    print()

    # Get old documents
    print("Reading old database...")
    documents = get_old_documents()
    print(f"  Found {len(documents)} documents to potentially import")
    print()

    # Process each document
    print("Processing documents...")
    print("-" * 60)

    success_count = 0
    skip_count = 0
    error_count = 0

    for doc in documents:
        print(f"\nDocument: {doc['title']}")

        result = upload_document(doc, existing)

        if result is True:
            success_count += 1
            # Add to existing to prevent re-upload if there are duplicates in source
            existing["titles"].add(doc["title"])
            existing["filenames"].add(os.path.basename(doc["file_path"]))
            # Small delay to not overwhelm the server
            time.sleep(1)
        elif result is False:
            skip_count += 1
        else:
            error_count += 1

    print()
    print("=" * 60)
    print("Import Summary")
    print("=" * 60)
    print(f"  Successfully uploaded: {success_count}")
    print(f"  Skipped (duplicates/not found): {skip_count}")
    print(f"  Errors: {error_count}")
    print()


if __name__ == "__main__":
    main()
