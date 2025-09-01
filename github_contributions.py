import os
import subprocess
import datetime
from pathlib import Path

def create_backdated_commits(repo_path, start_date, end_date, commits_per_day=1):
    """
    Creates backdated commits in a Git repository.
    
    Args:
        repo_path (str): Path to the Git repository
        start_date (datetime.date): Start date for backdated commits
        end_date (datetime.date): End date for backdated commits
        commits_per_day (int): Number of commits to create per day
    """
    
    # Create the directory if it doesn't exist BEFORE changing directory
    Path(repo_path).mkdir(parents=True, exist_ok=True)
    
    # Change to the repo directory
    os.chdir(repo_path)
    
    try:
        # Initialize git repo if not already initialized
        if not os.path.exists('.git'):
            subprocess.run(['git', 'init'], check=True)
            print("Initialized new Git repository")
        
        current_date = start_date
        commit_count = 0
        
        while current_date <= end_date:
            for commit_num in range(commits_per_day):
                # Create or modify a file
                filename = f"contribution_{current_date.strftime('%Y%m%d')}_{commit_num}.txt"
                with open(filename, 'w') as f:
                    f.write(f"Contribution on {current_date} - Commit {commit_num + 1}\n")
                    f.write(f"Timestamp: {datetime.datetime.now()}\n")
                
                # Add file to git
                subprocess.run(['git', 'add', filename], check=True)
                
                # Create commit with custom date
                commit_message = f"Daily contribution - {current_date}"
                date_string = current_date.strftime('%Y-%m-%d 12:00:00')
                
                # Set both author and committer dates
                env = os.environ.copy()
                env['GIT_AUTHOR_DATE'] = date_string
                env['GIT_COMMITTER_DATE'] = date_string
                
                subprocess.run([
                    'git', 'commit', 
                    '-m', commit_message
                ], env=env, check=True)
                
                commit_count += 1
                print(f"Created commit {commit_count}: {commit_message}")
            
            # Move to next day
            current_date += datetime.timedelta(days=1)
        
        print(f"\nSuccessfully created {commit_count} backdated commits!")
        print("To push to GitHub:")
        print("1. Create a new repository on GitHub")
        print("2. Add remote: git remote add origin <your-repo-url>")
        print("3. Push: git push -u origin main")
        
    except subprocess.CalledProcessError as e:
        print(f"Git command failed: {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    # Customize your repository path and desired date range here
    repo_path = "./github-bot"  # Folder to hold the git repo
    start_date = datetime.date(2024, 1, 1)  # Start date for commits
    end_date = datetime.date(2024, 1, 7)    # End date for commits (one week example)
    commits_per_day = 2                      # Number of commits per day
    
    print("Creating backdated contributions...")
    create_backdated_commits(repo_path, start_date, end_date, commits_per_day)
