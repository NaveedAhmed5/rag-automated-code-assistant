def build_rag_prompt(user_query, retrieved_contexts):
    prompt_parts = []
    
    # 1. Enforce the strict system rule exactly as requested
    prompt_parts.append("System Rule: Answer using only the provided context. Notice the original fix size (lines changed) to guide your recommendation.\n")
    
    # 2. Append Context Data
    prompt_parts.append("--- RETRIEVED CONTEXT START ---")
    for ctx in retrieved_contexts:
        prompt_parts.append(f"\nCommit Hash: {ctx.get('commit_hash', 'Unknown')}")
        prompt_parts.append(f"Lines Added: {ctx.get('lines_added', 0)}")
        prompt_parts.append(f"Lines Deleted: {ctx.get('lines_deleted', 0)}")
        prompt_parts.append("Code Diff:")
        prompt_parts.append(ctx.get('text', ''))
        prompt_parts.append("-" * 40)
    prompt_parts.append("--- RETRIEVED CONTEXT END ---\n")
    
    # 3. Append the User Query
    prompt_parts.append("User Query:")
    prompt_parts.append(user_query)
    
    return "\n".join(prompt_parts)

if __name__ == "__main__":
    # Mock data for testing the formatting
    mock_contexts = [
        {
            "commit_hash": "a1b2c3d4e5f6",
            "lines_added": 12,
            "lines_deleted": 3,
            "text": "--- a/src/auth.py\n+++ b/src/auth.py\n-def login(): pass\n+def login():\n+    print('secure')"
        },
        {
            "commit_hash": "f9e8d7c6b5a4",
            "lines_added": 2,
            "lines_deleted": 0,
            "text": "--- a/src/db.py\n+++ b/src/db.py\n+import pinecone"
        }
    ]
    
    mock_query = "How do we initialize the database and secure the login?"
    
    final_prompt = build_rag_prompt(mock_query, mock_contexts)
    
    print("=== FINAL CONSTRUCTED PROMPT ===\n")
    print(final_prompt)
