import requests
from datetime import datetime, timedelta

import os

# 1. Credentials
API_KEY = os.environ.get("TRELLO_API_KEY", "")
TOKEN = os.environ.get("TRELLO_TOKEN", "")

# TARGET BOARD NAME
TARGET_BOARD_NAME = "RepoRAG Project"

# 2. Sequential Tasks matching your precise layout
PLAN = [
    {
        "sequence": 1,
        "tasks": [
            {
                "name": "Trello Plan",
                "desc": "Establish agile project workflow tracking. Create the standard column states: To Do, Doing, and Done to organize daily deliverables.",
                "checklists": []
            },
            {
                "name": "VSCode Setup",
                "desc": "Initialize workspace directory tree structure, set up a locally isolated virtual environment, and install dependencies.",
                "checklists": ["Create folder structure", "Initialize myvenv", "Install requirements"]
            }
        ]
    },
    {
        "sequence": 2,
        "tasks": [
            {
                "name": "Implement GitPython Connection in src/extractor.py",
                "desc": "Establish core repository hook pipeline. Write Python code leveraging GitPython library utilities to target and programmatically mount a local git repository.",
                "checklists": []
            },
            {
                "name": "Extract Raw Commit Messages and Patch Diffs",
                "desc": "Build text data generation sequence. Implement processing loops to crawl target branch tracking logs, pulling out commit messages along with structural code diff comparisons.",
                "checklists": []
            }
        ]
    },
    {
        "sequence": 3,
        "tasks": [
            {
                "name": "Parse Commit Structural Metadata Attributes",
                "desc": "Create indexing parameters for structural scoping. Inject extraction attributes to isolate categorical details: file extensions, primary directory parent paths, and lines changed metrics.",
                "checklists": []
            },
            {
                "name": "Export Extracted Git History to data/raw_commits.json",
                "desc": "Form data storage contract layer. Format unified payload dictionaries containing raw text fragments combined with parsed metadata tables, exporting them cleanly into data/raw_commits.json.",
                "checklists": []
            }
        ]
    },
    {
        "sequence": 4,
        "tasks": [
            {
                "name": "Initialize Local ChromaDB Database in src/ingest.py",
                "desc": "Provision localized multi-modal vector cluster. Write core layout setup logic to instantiate, configure, and initialize a local collection storage pool inside ChromaDB.",
                "checklists": []
            },
            {
                "name": "Configure Text Embedding Model Pipeline",
                "desc": "Hook vector transformation models. Configure a structural embedding pipeline standard (e.g., OpenAI API or local Hugging Face instances) to convert language fragments to vectors.",
                "checklists": []
            }
        ]
    },
    {
        "sequence": 5,
        "tasks": [
            {
                "name": "Generate Embeddings from Extracted Git JSON",
                "desc": "Execute numerical matrix transformations. Run batch extraction calculations over target database blocks from raw_commits.json, feeding raw strings into the embedding model layer.",
                "checklists": []
            },
            {
                "name": "Save Vector Arrays and Metadata Payloads to ChromaDB",
                "desc": "Commit index vectors to persistent storage layer. Load the generated vector embeddings array maps along with corresponding schema payload structures directly to ChromaDB.",
                "checklists": []
            }
        ]
    },
    {
        "sequence": 6,
        "tasks": [
            {
                "name": "Implement Hard Metadata Filtering in src/search.py",
                "desc": "Code precision scoping rules. Write syntax filters to search inside specific directories (e.g., folders containing src/auth) to isolate target files directly during search execution.",
                "checklists": []
            },
            {
                "name": "Verify Metadata Query Space Narrowing Performance",
                "desc": "Validate search array limits. Verify performance boundaries to ensure hard relational parameters successfully drop unrelated entries and constrain database operations.",
                "checklists": []
            }
        ]
    },
    {
        "sequence": 7,
        "tasks": [
            {
                "name": "Combine Metadata Filters with Vector Similarity Search",
                "desc": "Implement multi-tier hybrid index engine. Unify literal hard criteria restrictions with text semantic math matching algorithms inside single search query blocks.",
                "checklists": []
            },
            {
                "name": "Verify Multi-Modal Extraction of Diffs and Line Counts",
                "desc": "Test input query scenarios. Type raw software error messages to ensure retrieval systems reliably extract top 2 relevant structural file paths, patch diff contexts, and lines_changed.",
                "checklists": []
            }
        ]
    },
    {
        "sequence": 8,
        "tasks": [
            {
                "name": "Design Context-Grounded LLM Prompt Template",
                "desc": "Form prompt blueprint boundaries. Initialize structured prompt layout formatting schemas within Python to direct generation contexts cleanly.",
                "checklists": []
            },
            {
                "name": "Inject Structural Constraint Safeguards into LLM Prompt",
                "desc": "Enforce context anchoring logic. Set explicit prompt rules: 'Answer using only the provided context. Notice the original fix size (lines changed) to guide your recommendation.'",
                "checklists": []
            }
        ]
    },
    {
        "sequence": 9,
        "tasks": [
            {
                "name": "Construct Interactive CLI Terminal Wrapper in src/main.py",
                "desc": "Write entry interface. Build operational command-line loops inside main.py to handle developer text terminal query inputs fluidly.",
                "checklists": []
            },
            {
                "name": "Wire End-to-End Pipeline Retrieval to LLM Generation",
                "desc": "Complete overall engine pipeline loops. Link search output context pipes cleanly to the LLM completion engine so entering any raw crash snippet drops working solution recommendations.",
                "checklists": []
            }
        ]
    },
    {
        "sequence": 10,
        "tasks": [
            {
                "name": "Execute End-to-End System Demo with 3 Real-World Bugs",
                "desc": "Perform acceptance criteria test suite execution. Run 3 diagnostic production repo crash sequences through the CLI to verify data routing efficiency and eliminate hallucinations.",
                "checklists": []
            },
            {
                "name": "Complete Sprint Retrospective and Document Bottlenecks",
                "desc": "Conduct a sprint self-evaluation. Document memory barriers or file chunk processing thresholds inside project materials to serve as a strong portfolio interview discussion point.",
                "checklists": []
            }
        ]
    }
]

def calculate_due_dates(start_date):
    """Calculates due dates starting exactly on start_date, skipping Sundays."""
    day_map = {}
    current_date = start_date
    
    for item in PLAN:
        seq_num = item["sequence"]
        
        # If the date landing position falls on a Sunday, bump it to Monday
        while (current_date.weekday() == 5 or current_date.weekday() == 6):
            current_date += timedelta(days=1)
            
        due_datetime = current_date.replace(hour=23, minute=30, second=0, microsecond=0)
        
        # FIX: Append '+05:00' to explicitly force Pakistan Standard Time offset
        day_map[seq_num] = f"{due_datetime.isoformat()}+05:00"
        
        # Advance to the next calendar date for the NEXT sequence block
        current_date += timedelta(days=1)
        
    return day_map

def get_or_create_board():
    base_url = "https://api.trello.com/1"
    query = {"key": API_KEY, "token": TOKEN}

    # Timeline anchors exactly on Thursday, June 11, 2026
    start_date = datetime(2026, 6, 11)
    due_dates = calculate_due_dates(start_date)

    print(f"🔍 Scanning account for an existing board named '{TARGET_BOARD_NAME}'...")
    boards_url = f"{base_url}/members/me/boards"
    boards = requests.get(boards_url, params=query).json()
    
    board_id = None
    short_url = None
    
    for b in boards:
        if b["name"] == TARGET_BOARD_NAME:
            board_id = b["id"]
            short_url = b["shortUrl"]
            print(f"🎯 Found existing board! (ID: {board_id})")
            break

    # If the board doesn't exist, build a brand new one
    if not board_id:
        print(f"✨ Board '{TARGET_BOARD_NAME}' not found. Creating a new one...")
        board_url = f"{base_url}/boards/"
        board_query = {**query, "name": TARGET_BOARD_NAME, "defaultLists": "false"}
        
        response = requests.post(board_url, params=board_query)
        if response.status_code != 200:
            print(f"❌ Trello Authentication Failed (Status {response.status_code}): {response.text}")
            return
            
        board_resp = response.json()
        board_id = board_resp.get("id")
        short_url = board_resp.get("shortUrl")

    # Fetch active lists to either reuse or configure fresh columns
    lists_url = f"{base_url}/boards/{board_id}/lists"
    lists = requests.get(lists_url, params=query).json()
    
    list_ids = {l["name"]: l["id"] for l in lists}
    columns = ["Done", "Doing", "To Do"]

    # Ensure all required layout columns exist on the board
    for col_name in columns:
        if col_name not in list_ids:
            list_url = f"{base_url}/boards/{board_id}/lists"
            list_query = {**query, "name": col_name, "pos": "top"}
            list_resp = requests.post(list_url, params=list_query).json()
            list_ids[col_name] = list_resp["id"]

    todo_list_id = list_ids["To Do"]

    # Clear existing cards in 'To Do' list to prevent duplicate item packing
    print("🧹 Cleaning out old/outdated items from the 'To Do' column...")
    cards_url = f"{base_url}/lists/{todo_list_id}/cards"
    existing_cards = requests.get(cards_url, params=query).json()
    for card in existing_cards:
        requests.delete(f"{base_url}/cards/{card['id']}", params=query)

    print("🚀 Populating cards top-down (closest deadline absolute first)...")
    card_url = f"{base_url}/cards"
    
    for item in PLAN:
        seq_num = item["sequence"]
        iso_due_date = due_dates[seq_num]
        
        for task in item["tasks"]:
            card_query = {
                **query,
                "name": task["name"],
                "desc": task["desc"],
                "idList": todo_list_id,
                "due": iso_due_date,
                "pos": "bottom"  # Top-down order matching closest deadline first
            }
            card_resp = requests.post(card_url, params=card_query).json()
            card_id = card_resp.get("id")
            
            # Append requirements checklist items where applicable
            if card_id and task["checklists"]:
                chk_url = f"{base_url}/cards/{card_id}/checklists"
                chk_resp = requests.post(chk_url, params={**query, "name": "Requirements"}).json()
                chk_id = chk_resp.get("id")
                
                if chk_id:
                    item_url = f"{base_url}/checklists/{chk_id}/checkitems"
                    for check_item in task["checklists"]:
                        requests.post(item_url, params={**query, "name": check_item, "pos": "bottom"})

    print(f"\n🎉 Process complete! Your board workspace is perfectly configured.")
    print(f"🔗 Direct board access link: {short_url}")

if __name__ == "__main__":
    get_or_create_board()