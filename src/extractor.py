import os
import json
from git import Repo

# Force Python to find your Git installation path directly on Windows
os.environ["GIT_PYTHON_GIT_EXECUTABLE"] = r"C:\Softwares\Git\cmd\git.exe"

def clone_or_load_github_repo(username, repo_name, token, local_storage_dir):
    """
    Connects to GitHub using your token and clones the repository.
    If it is already downloaded, it opens it up instantly!
    """
    repo_folder_path = os.path.join(local_storage_dir, repo_name)
    
    if os.path.exists(os.path.join(repo_folder_path, ".git")):
        print(f"Repository already exists locally at: {repo_folder_path}")
        print("Opening existing local copy...")
        return Repo(repo_folder_path)
    
    authenticated_url = f"https://{token}@github.com/{username}/{repo_name}.git"
    
    print(f"Connecting to GitHub to download: {username}/{repo_name}...")
    try:
        # Clone ONLY the text tree history, optimization to handle network timeouts
        repo = Repo.clone_from(
            authenticated_url, 
            repo_folder_path, 
            multi_options=["--filter=blob:none"]
        )
        print("Download complete! Successfully connected to remote Git repository.")
        return repo
    except Exception as e:
        print(f"Failed to download from GitHub. Error details: {e}")
        return None

def extract_commit_history(repo):
    """Loops through commits and extracts text messages and plain code diffs."""
    if not repo:
        return []

    print("\nStarting extraction of commit history...")
    # Grab the last 50 historical updates to analyze
    commits = list(repo.iter_commits(max_count=50))
    print(f"Found {len(commits)} historical commits to analyze.\n")

    # List of common binary file extensions we want to skip reading text for
    BINARY_EXTENSIONS = ('.png', '.jpg', '.jpeg', '.gif', '.mp4', '.mov', '.zip', '.pdf', '.exe', '.ttf', '.woff')

    commits_data = []

    for commit in commits:
        commit_entry = {
            "commit_id": commit.hexsha,
            "author": commit.author.name,
            "date": str(commit.authored_datetime),
            "message": commit.summary,
            "total_lines_added": 0,
            "total_lines_deleted": 0,
            "modified_files": []
        }

        # Skip parent comparison if it is the root initial commit
        if not commit.parents:
            commits_data.append(commit_entry)
            continue

        # Compare this commit with its parent to capture code diff modifications
        parent = commit.parents[0]
        diffs = parent.diff(commit, create_patch=True)

        for d in diffs:
            file_path = d.b_path if d.b_path else d.a_path
            
            # Optimization: Skip trying to read raw lines if it's a known binary media file
            if file_path.lower().endswith(BINARY_EXTENSIONS):
                continue

            _, ext = os.path.splitext(file_path)
            
            file_metrics = {
                "file_path": file_path,
                "file_extension": ext.lower(),
                "lines_added": 0,
                "lines_deleted": 0,
                "added_lines": [],
                "deleted_lines": []
            }

            try:
                # Decode the text metrics cleanly
                diff_text = d.diff.decode('utf-8', errors='ignore')
                
                for line in diff_text.splitlines():
                    if line.startswith('+') and not line.startswith('+++'):
                        file_metrics["lines_added"] += 1
                        file_metrics["added_lines"].append(line[1:])  # Strip the '+' prefix
                    elif line.startswith('-') and not line.startswith('---'):
                        file_metrics["lines_deleted"] += 1
                        file_metrics["deleted_lines"].append(line[1:])  # Strip the '-' prefix
                
                # Aggregate to commit level
                commit_entry["total_lines_added"] += file_metrics["lines_added"]
                commit_entry["total_lines_deleted"] += file_metrics["lines_deleted"]
                
                commit_entry["modified_files"].append(file_metrics)
                
            except Exception:
                pass
                
        commits_data.append(commit_entry)

    return commits_data

if __name__ == "__main__":
    # --- CONFIGURATION SETTINGS ---
    GITHUB_USERNAME = "NaveedAhmed5"
    GITHUB_REPO_NAME = "Shopiz-E_Clothing-Store-Mobile-App"
    GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "") # Paste your GitHub Personal Access Token here
    
    # Define local execution directory routing layout parameters
    BASE_DIR = r"C:\Career\Summer_Projects\RepoRAG\Sprint_1\Project"
    STORAGE_DIR = os.path.join(BASE_DIR, "cloned_repos")
    
    # Target path layout modification for output json structured data
    DATA_DIR = os.path.join(BASE_DIR, "data")
    # ------------------------------
    
    # Output File Configuration
    output_filename = "raw_commits.json"
    output_filepath = os.path.join(DATA_DIR, output_filename)
    
    # Safety Check: Ensure the targeted data directory is created before running
    os.makedirs(DATA_DIR, exist_ok=True)
    
    # Simple console alert to communicate script execution has started
    print(f"Processing history... Writing metrics directly to:\n {output_filepath}")
    
    # Execution pipeline trigger
    git_repo = clone_or_load_github_repo(GITHUB_USERNAME, GITHUB_REPO_NAME, GITHUB_TOKEN, STORAGE_DIR)
    if git_repo:
        commits_data = extract_commit_history(git_repo)
        
        with open(output_filepath, "w", encoding="utf-8") as json_file:
            json.dump(commits_data, json_file, indent=4, ensure_ascii=False)
            
        print("Extraction complete. JSON metrics saved successfully.")