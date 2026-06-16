import os
import json
from pinecone import Pinecone
import cohere
from dotenv import load_dotenv

load_dotenv()

def get_clients():
    pinecone_key = os.environ.get("PINECONE_API_KEY", "")
    pc = Pinecone(api_key=pinecone_key)
    index = pc.Index("repo-commit-history")
    
    cohere_key = os.environ.get("COHERE_API_KEY", "")
    co = cohere.Client(cohere_key)
    return index, co

def semantic_search(query_text, metadata_filter=None, top_k=2):
    index, co = get_clients()
    
    print(f"Generating embeddings for query: '{query_text}'...")
    response = co.embed(
        texts=[query_text],
        model="embed-english-v3.0",
        input_type="search_query"
    )
    query_vector = response.embeddings[0]
    
    print("Executing semantic search against Pinecone Index...")
    query_args = {
        "vector": query_vector,
        "top_k": top_k,
        "include_metadata": True
    }
    if metadata_filter:
        query_args["filter"] = metadata_filter
        
    search_results = index.query(**query_args)
    return search_results.matches

if __name__ == "__main__":
    print("Initializing Pinecone Semantic Search...")
    
    # Define a mock bug description
    mock_bug_query = "Fix cart screen rendering issue"
    
    # Execute semantic search
    matches = semantic_search(query_text=mock_bug_query, top_k=2)
    
    print(f"Total semantic matches found: {len(matches)}")
    for i, match in enumerate(matches, 1):
        print(f"\n--- Match {i} ---")
        print(f"Commit Hash: {match.id}")
        print(f"Similarity Score: {match.score:.4f}")
        
        metadata = match.metadata
        print(f"Date: {metadata.get('date')}")
        
        # Extract and parse metrics
        metrics_str = metadata.get("metrics", "{}")
        try:
            metrics = json.loads(metrics_str)
            print(f"Lines Added: {metrics.get('total_lines_added', 0)}")
            print(f"Lines Deleted: {metrics.get('total_lines_deleted', 0)}")
        except json.JSONDecodeError:
            print("Lines Added: Unknown")
            print("Lines Deleted: Unknown")
            
        # Extract and print raw diff cleanly
        full_text = metadata.get("text", "")
        if "Diff:\n" in full_text:
            diff = full_text.split("Diff:\n")[1]
        else:
            diff = full_text
            
        added_lines = []
        deleted_lines = []
        
        for line in diff.splitlines():
            if line.startswith('+') and not line.startswith('+++'):
                added_lines.append(line)
            elif line.startswith('-') and not line.startswith('---'):
                deleted_lines.append(line)
                
        print("\nExact Lines Added:")
        if added_lines:
            for l in added_lines[:15]: # Show up to 15 lines to prevent terminal overflow
                print(f"  {l}")
            if len(added_lines) > 15:
                print(f"  ... (+ {len(added_lines) - 15} more lines)")
        else:
            print("  None")
            
        print("\nExact Lines Deleted:")
        if deleted_lines:
            for l in deleted_lines[:15]:
                print(f"  {l}")
            if len(deleted_lines) > 15:
                print(f"  ... (+ {len(deleted_lines) - 15} more lines)")
        else:
            print("  None")
