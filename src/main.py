import os
import sys
import json
import cohere
from dotenv import load_dotenv

# Ensure the src directory is in the path to import local modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from search import semantic_search
from prompt_engine import build_rag_prompt

def main():
    print("Loading environment variables...")
    load_dotenv()
    
    cohere_key = os.environ.get("COHERE_API_KEY")
    if not cohere_key:
        print("Error: COHERE_API_KEY environment variable not found.")
        sys.exit(1)
        
    print("Initializing Cohere client...")
    co = cohere.Client(cohere_key)
    
    print("\n" + "="*50)
    print("  Welcome to RepoRAG: Automated Code Assistant")
    print("="*50 + "\n")
    
    while True:
        try:
            query = input("Enter a bug description (or type 'exit' to quit): ").strip()
            
            if not query:
                continue
                
            if query.lower() in ['exit', 'quit']:
                print("Exiting RepoRAG. Goodbye!")
                break
                
            print("\n[1/4] Searching database for related historical commits...")
            matches = semantic_search(query_text=query, top_k=2)
            
            if not matches:
                print("No related commits found in the history. Try expanding your query.")
                continue
                
            print(f"[2/4] Retrieved {len(matches)} relevant commits. Formatting context...")
            
            retrieved_contexts = []
            for match in matches:
                metadata = match.metadata
                metrics_str = metadata.get("metrics", "{}")
                
                lines_added = 0
                lines_deleted = 0
                try:
                    metrics = json.loads(metrics_str)
                    lines_added = metrics.get('total_lines_added', 0)
                    lines_deleted = metrics.get('total_lines_deleted', 0)
                except Exception:
                    pass
                    
                context_dict = {
                    "commit_hash": match.id,
                    "text": metadata.get("text", ""),
                    "lines_added": lines_added,
                    "lines_deleted": lines_deleted
                }
                retrieved_contexts.append(context_dict)
                
            print("[3/4] Generating structured RAG prompt...")
            final_prompt = build_rag_prompt(query, retrieved_contexts)
            
            print("[4/4] Querying LLM for fix recommendation...\n")
            response = co.chat(
                message=final_prompt,
                model="command-r"
            )
            
            print("="*50)
            print("  AI FIX RECOMMENDATION")
            print("="*50)
            print(response.text.strip())
            print("="*50 + "\n")
            
        except KeyboardInterrupt:
            print("\nOperation cancelled by user. Exiting...")
            break
        except Exception as e:
            print(f"\nAn error occurred during execution: {e}")
            print("Please try a different query or check your API quotas.\n")

if __name__ == "__main__":
    main()
