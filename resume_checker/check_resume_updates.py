import os
import subprocess
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv(os.path.expanduser(".env"))

resume_path = os.getenv("RESUME_PATH")
parse_cv_script = os.getenv("PARSE_CV_SCRIPT")
portfolio_path = os.getenv("PORTFOLIO_PATH")

if not all([resume_path, parse_cv_script, portfolio_path]):
    print("Error: One or more required environment variables are missing.")
    exit(1)


def get_last_sunday():
    today = datetime.now()
    last_sunday = today - timedelta(days=(today.weekday() + 1) % 7)
    return last_sunday


def has_been_modified(file_path, last_sunday):
    try:
        last_modified_time = datetime.fromtimestamp(os.path.getmtime(file_path))
        return last_modified_time > last_sunday
    except FileNotFoundError:
        print(f"Error: The file {file_path} does not exist.")
        return False
    except Exception as e:
        print(f"Error: Could not determine if {file_path} has been modified. {e}")
        return False


def run_python_script():
    try:
        subprocess.run(["python3", parse_cv_script], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while running the script: {e}")
        return False
    except FileNotFoundError:
        print(f"Error: The script {parse_cv_script} does not exist.")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False


def check_git_status(file_path):
    try:
        os.chdir(portfolio_path)
        result = subprocess.run(
            ["git", "status", "--short"], capture_output=True, text=True, check=True
        )
        return file_path in result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while checking git status: {e}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False


def commit_changes():
    original_dir = os.getcwd()
    try:
        subprocess.run(["git", "add", "experience.html", "workData.js"], check=True)
        subprocess.run(
            ["git", "commit", "-m", "auto updated content from resume"], check=True
        )
        subprocess.run(["git", "push"], check=True)
    except FileNotFoundError:
        print(f"Error: The directory {portfolio_path} does not exist.")
    except subprocess.CalledProcessError as e:
        print(f"Error occurred during git operations: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
    finally:
        os.chdir(original_dir)


if __name__ == "__main__":
    last_sunday = get_last_sunday()
    print(f"Last Sunday: {last_sunday}")
    if has_been_modified(resume_path, last_sunday):
        print("Resume file has updates")
        if run_python_script():
            print("Successfully parsed resume.")
            if check_git_status("workData.js"):
                print("workData has local changes")
                commit_changes()
                print("Local changes pushed to github. Done.")
            else:
                print("workData has no changes. Done.")
