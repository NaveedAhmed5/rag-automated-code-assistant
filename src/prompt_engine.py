def build_rag_prompt(user_query, retrieved_contexts):
    prompt_parts = []
    
    system_rule = (
        "System Rule: You are an expert coding assistant. Assume the provided code context is the EXACT proven solution "
        "to the user's bug. Do not mention or show the actual commits, commit hashes, or raw diffs to the user. "
        "Instead, provide an extremely concise summary structured exactly with the following headers: "
        "'1) The Issue', '2) The Reasons', and '3) The Solutions'. "
        "Act as if you are instructing the user on how to apply this specific fix to resolve their issue. "
        "CRITICAL: Do NOT list changes file-by-file. Group similar modifications across all files into a single, high-level, generalized step. "
        "Never repeat the same instructions. Keep the solution highly concise and deduplicate any redundant context.\n"
    )
    prompt_parts.append(system_rule)
    
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
