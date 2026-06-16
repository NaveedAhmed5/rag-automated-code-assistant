import os
import json
from pinecone import Pinecone
import cohere

def setup_pinecone():
    """
    Initializes Pinecone client and Cohere embedding client.
    """
    pinecone_key = os.environ.get("PINECONE_API_KEY", "")
    pc = Pinecone(api_key=pinecone_key)
    index = pc.Index("repo-commit-history")
    
    cohere_key = os.environ.get("COHERE_API_KEY", "")
    co = cohere.Client(cohere_key)
    return index, co

def ingest_commits(json_path, index, co):
    print("Loading target data from: " + json_path)
    if not os.path.exists(json_path):
        print("Error: " + json_path + " does not exist.")
        return

    with open(json_path, "r", encoding="utf-8") as f:
        commits = json.load(f)

    vectors_to_upsert = []

    for commit in commits:
        commit_hash = commit.get("commit_id")
        message = commit.get("message", "")
        
        raw_diff_parts = []
        for file in commit.get("modified_files", []):
            file_path = file.get("file_path", "")
            raw_diff_parts.append(f"--- a/{file_path}")
            raw_diff_parts.append(f"+++ b/{file_path}")
            for line in file.get("deleted_lines", []):
                raw_diff_parts.append(f"-{line}")
            for line in file.get("added_lines", []):
                raw_diff_parts.append(f"+{line}")
        raw_diff = "\n".join(raw_diff_parts)

        document_text = f"Message: {message}\nDiff:\n{raw_diff}"
        
        # Pinecone metadata doesn't need json.dumps, but we'll keep the same shape
        metrics = {
            "total_lines_added": commit.get("total_lines_added", 0),
            "total_lines_deleted": commit.get("total_lines_deleted", 0),
            "modified_files_count": len(commit.get("modified_files", []))
        }
        
        file_paths = [file.get("file_path", "") for file in commit.get("modified_files", [])]
        
        # Truncate text to fit Pinecone's 40KB metadata limit
        truncated_text = document_text if len(document_text) <= 30000 else document_text[:30000] + "\n...[TRUNCATED FOR METADATA]..."

        metadata = {
            "author": commit.get("author", "Unknown"),
            "date": commit.get("date", ""),
            "commit_hash": commit_hash,
            "metrics": json.dumps(metrics),
            "file_paths": file_paths,
            "text": truncated_text
        }

        # Embed using Cohere
        response = co.embed(
            texts=[document_text],
            model="embed-english-v3.0",
            input_type="search_document"
        )
        embedding = response.embeddings[0]

        vectors_to_upsert.append({
            "id": commit_hash,
            "values": embedding,
            "metadata": metadata
        })

    print(f"Ingesting {len(vectors_to_upsert)} commits into Pinecone Cloud Database...")
    
    # Upsert in batch
    index.upsert(vectors=vectors_to_upsert)

if __name__ == "__main__":
    BASE_DIR = r"C:\Career\Summer_Projects\RepoRAG\Sprint_1\Project"
    JSON_PATH = os.path.join(BASE_DIR, "data", "raw_commits.json")
    
    print("Initializing Pinecone Cloud Database setup...")
    try:
        index, co = setup_pinecone()
        print("Pinecone client initialized successfully.")
        
        ingest_commits(JSON_PATH, index, co)
        print("Data successfully ingested into the Pinecone database!")
        stats = index.describe_index_stats()
        print(f"Total documents now in collection: {stats.total_vector_count}")
        
    except Exception as e:
        print(f"Ingestion failed. Error: {e}")
