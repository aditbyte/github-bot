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
    
    # Ensure we're in the correct directory
    original_dir = os.getcwd()
    os.chdir(repo_path)
    
    try:
        # Create the directory if it doesn't exist
        Path(repo_path).mkdir(parents=True, exist_ok=True)
        
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
    finally:
        os.chdir(original_dir)

def create_contribution_pattern(repo_path, pattern_type="consistent"):
    """
    Creates different patterns of contributions.
    
    Args:
        repo_path (str): Path to the Git repository
        pattern_type (str): Type of pattern - "consistent", "random", "streaks"
    """
    import random
    
    # Define date range (last 365 days)
    end_date = datetime.date.today()
    start_date = end_date - datetime.timedelta(days=365)
    
    original_dir = os.getcwd()
    os.chdir(repo_path)
    
    try:
        Path(repo_path).mkdir(parents=True, exist_ok=True)
        
        if not os.path.exists('.git'):
            subprocess.run(['git', 'init'], check=True)
        
        current_date = start_date
        
        while current_date <= end_date:
            commits_today = 0
            
            if pattern_type == "consistent":
                # 1-3 commits most days, skip some weekends
                if current_date.weekday() < 5:  # Weekday
                    commits_today = random.randint(1, 3)
                elif random.random() < 0.3:  # 30% chance on weekends
                    commits_today = random.randint(1, 2)
                    
            elif pattern_type == "random":
                # Random commits, some days empty
                commits_today = random.choices([0, 1, 2, 3, 4, 5], 
                                             weights=[30, 25, 20, 15, 7, 3])[0]
                                             
            elif pattern_type == "streaks":
                # Create streaks and gaps
                if random.random() < 0.7:  # 70% active days
                    commits_today = random.randint(1, 4)
            
            # Create the commits for this day
            for i in range(commits_today):
                filename = f"daily_work_{current_date.strftime('%Y%m%d')}_{i}.py"
                
                # Create some variety in file content
                content = f"""# Daily work for {current_date}
# File {i + 1} of {commits_today}

def work_function_{current_date.strftime('%Y%m%d')}_{i}():
    '''
    Function created on {current_date}
    '''
    return "Work completed on {current_date}"

if __name__ == "__main__":
    result = work_function_{current_date.strftime('%Y%m%d')}_{i}()
    print(result)
"""
                
                with open(filename, 'w') as f:
                    f.write(content)
                
                subprocess.run(['git', 'add', filename], check=True)
                
                # Vary the time of day for commits
                hour = random.randint(9, 18)
                minute = random.randint(0, 59)
                date_string = f"{current_date.strftime('%Y-%m-%d')} {hour:02d}:{minute:02d}:00"
                
                env = os.environ.copy()
                env['GIT_AUTHOR_DATE'] = date_string
                env['GIT_COMMITTER_DATE'] = date_string
                
                commit_messages = [
                    "Fix bug in user authentication",
                    "Add new feature for data processing",
                    "Update documentation",
                    "Refactor code for better performance",
                    "Add unit tests",
                    "Fix typo in comments",
                    "Optimize database queries",
                    "Update dependencies"
                ]
                
                message = random.choice(commit_messages)
                
                subprocess.run([
                    'git', 'commit', 
                    '-m', message
                ], env=env, check=True)
            
            current_date += datetime.timedelta(days=1)
        
        print(f"Created contribution pattern: {pattern_type}")
        
    finally:
        os.chdir(original_dir)

# Example usage
if __name__ == "__main__":
    # Example 1: Simple backdated commits
    repo_path = "./GITHUB-BOT"
    start_date = datetime.date(2025, 8, 1)
    end_date = datetime.date(2025, 8, 31)
    
    print("Creating backdated contributions...")
    create_backdated_commits(repo_path, start_date, end_date, commits_per_day=1)
    
    # Example 2: Create realistic contribution pattern
    # create_contribution_pattern("./realistic_contributions", "consistent")
