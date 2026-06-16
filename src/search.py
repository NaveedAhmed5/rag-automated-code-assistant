import os
import json
from pinecone import Pinecone
import cohere

def test_metadata_filter():
    pinecone_key = os.environ.get("PINECONE_API_KEY", "")
    pc = Pinecone(api_key=pinecone_key)
    index = pc.Index("repo-commit-history")
    
    # Let's filter for commits that modified cart_screen.dart
    filter_dict = {
        "file_paths": {"$in": ["lib/screens/cart_screen.dart"]}
    }
    
    print(f"Searching for commits that modified 'lib/screens/cart_screen.dart'...")
    
    # Provide a dummy zero vector since we only want to filter by metadata
    # The dimension matches Cohere's embed-english-v3.0 output (1024)
    dummy_vector = [0.0] * 1024
    
    response = index.query(
        vector=dummy_vector,
        filter=filter_dict,
        top_k=10,
        include_metadata=True
    )
    
    matches = response.matches
    print(f"Total matches found: {len(matches)}")
    for match in matches:
        print(f" - Commit Hash: {match.id}")
        print(f"   Date: {match.metadata.get('date')}")
        print(f"   Message: {match.metadata.get('text').split('Diff:')[0].strip()}")

if __name__ == "__main__":
    print("Initializing Pinecone Metadata Search...")
    test_metadata_filter()
