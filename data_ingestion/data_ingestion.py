import json
import sys
import time
from pathlib import Path
from github import Github, RateLimitExceededException, GithubException
from tqdm import tqdm

sys.path.append(str(Path(__file__).resolve().parent))
from config import GITHUB_TOKEN , REPO_OWNER , REPO_NAME , RAW_DIR

RAW_DATA_PATH = RAW_DIR / "raw_data.json"

def get_repo():
    if not GITHUB_TOKEN:
        print("Error git token is not present")
        gt = Github()
    else:
        gt = Github(GITHUB_TOKEN)

    repo = gt.get_repo(f"{REPO_OWNER}/{REPO_NAME}")
    return gt , repo


def fetch_commit(gt , repo , max_items :int = None) -> list:
    print("Fetching the commits")
    # out_dir = RAW_DIR/"commits"
    # out_dir.mkdir(exist_ok = True)

    
    result = []
    commits = repo.get_commits()

    for commit in tqdm(commits , total = max_items):
        try:
            result.append({
                "sha": commit.sha,
                "html_url": commit.html_url,
                "commit": {
                        "message": commit.commit.message,
                        "author": {
                                "name": commit.commit.author.name if commit.commit.author else "unknown",
                                "date": commit.commit.author.date.isoformat() if commit.commit.author else "",
                            },
                        },
                })
            if max_items and len(result) >= max_items:
                break
        except RateLimitExceededException:
            _wait_for_rate_limit(gt)
        except GithubException as e:
            print(f"API error git hub is not initalize")
    print(f"Saved {len(result)} commits")
    return result


def _wait_for_rate_limit(gt : Github):
    rate = gt.get_rate_limit().core
    wait = max((rate.reset.timestamp() - time.time()) , 1)
    print(f"Rate limit hit Sleeping{wait:.0f}s until resets" )
    time.sleep(wait)


def fetch_pull_request(gt , repo , max_items:int = None) -> list:
    print("fetch request")
    # out_dir = RAW_DIR / "pull_requests"
    # out_dir.mkdir(exist_ok=True)

    result = []
    prs = repo.get_pulls(state = "all")

    for pr in tqdm(prs ,total = max_items):
        try:
            result.append({
                 "number": pr.number,
                  "title": pr.title,
                  "body": pr.body or "",
                  "user": {"login": pr.user.login if pr.user else "unknown"},
                  "created_at": pr.created_at.isoformat() if pr.created_at else "",
                  "html_url": pr.html_url,
                  "state": pr.state,
                        })
            if max_items and len(result) >= max_items:
                break
        except RateLimitExceededException:
            _wait_for_rate_limit(gt)
        except GithubException as e:
             print(f"Skipping a PR due to API error: {e}")
    print(f"Saved {len(result)} pull request")
    return result

def fetch_issues(gt , repo , max_items : int= None) -> list:
    print("Fetch issues")
    # out_dir = RAW_DIR / "issues"
    # out_dir.mkdir(exist_ok=True)

    result = []
    issues = repo.get_issues(state = "all")
    for issue in tqdm(issues , total=max_items):
        if issue.pull_request is not None:
            continue
        try:
            result.append({
                "number" : issue.number,
                "title" : issue.title,
                "body": issue.body or "",
                "user": {"login": issue.user.login if issue.user else "unknown"},
                "created_at": issue.created_at.isoformat() if issue.created_at else "",
                "html_url": issue.html_url,
                "state": issue.state,
            })
            if max_items and len(result) >= max_items:
                break
        except RateLimitExceededException:
            _wait_for_rate_limit(gt)
        except GithubException as e:
            print(f"Skipping an issue due to API error: {e}")

    print(f"Saved {len(result)} issues.")
    return result


def run_ingestion(max_items : int = None):#if no value is given use none 
    gt , repo = get_repo()
    commits = fetch_commit(gt ,repo , max_items=max_items)
    issues = fetch_issues(gt ,repo , max_items=max_items)
    pull_req = fetch_pull_request(gt ,repo , max_items=max_items)

    consolidated = {
            "commits": commits,
            "pull_requests": pull_req,
            "issues": issues,
    }
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    with open(RAW_DATA_PATH, "w") as f:
        json.dump(consolidated, f, indent=4)

    total = len(commits) + len(pull_req) + len(issues)
    print(f"Saved {total} total records ({len(commits)} commits, "
          f"{len(pull_req)} PRs, {len(issues)} issues) to {RAW_DATA_PATH}")
    return consolidated 
    
if __name__ == "__main__":
    run_ingestion(max_items=None)







