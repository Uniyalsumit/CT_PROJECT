import os
import sys 
import re
import json
from pathlib import Path
from langchain_text_splitters import RecursiveCharacterTextSplitter
from tqdm import tqdm

sys.path.append(str(Path(__file__).resolve().parent.parent))
from config import RAW_DIR, PROCESSED_DIR, CHUNK_SIZE, CHUNK_OVERLAP

RAW_DATA_PATH = RAW_DIR / "raw_data.json"


def load_raw_data() -> dict:
    if not RAW_DATA_PATH.exists():
        raise FileNotFoundError(
            f"{RAW_DATA_PATH} not found. Run data_ingestion/ingest.py first."
        )
    with open(RAW_DATA_PATH) as f:
        return json.load(f)


splitter = RecursiveCharacterTextSplitter(
    chunk_size = CHUNK_SIZE,
    chunk_overlap = CHUNK_OVERLAP,
    separators=["\n\n", "\n", ". ", " ", ""],
)



def clean_text(text : str)->str:
    if not text:
        return ""
    text = re.sub(r"<!--.*?-->", "", text, flags=re.DOTALL)  #remove html comments
    text = re.sub(r"```[\s\S]*?```", "", text)                    # fenced code blocks (kept short-form only)
    text = re.sub(r"\r\n", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r"\s+$", "", text, flags=re.MULTILINE)
    return text.strip()

def process_commits(commits : list ) -> list:
    chunks = []
    for data in tqdm(commits , desc = "Processing comments"): 
        sha = data["sha"] #extract useful fields from files
        message = clean_text(data.get("commit" , {}).get("message",""))
        author = data.get("commit",{}).get("author",{}).get("name" ,"unknown")
        date = data.get("commit", {}).get("author", {}).get("date", "")
        url = data.get("html_url", "")

        if not message: continue

        for i , piece in enumerate(splitter.split_text(message)): #message is split into some portion ex ["Fix bug in API", "update docs", "refactor code"]
            chunks.append({  #append it tot chunk
                "text": piece,
                "source_type": "commit",
                "sha": sha,
                "author": author,
                "date": date,
                "url": url,
                "chunk_id": f"commit-{sha}-{i}",
            })
    return chunks

def process_pr(pull_req : list) -> list:
    chunks = []
    for data in tqdm(pull_req, desc="Processing PRs"):
        number = data["number"]
        title = data.get("title", "")
        body = clean_text(data.get("body", ""))
        author = data.get("user", {}).get("login", "unknown")
        date = data.get("created_at", "")
        url = data.get("html_url", "")
 
        full_text = f"PR #{number}: {title}\n\n{body}"
        for i, piece in enumerate(splitter.split_text(full_text)):
             chunks.append({
                 "text": piece,
                 "source_type": "pull_request",
                 "pr_number": number,
                 "author": author,
                 "date": date,
                 "url": url,
                 "chunk_id": f"pr-{number}-{i}",
             })
    return chunks


def process_issues(issue : list)-> list:
    chunks = []
    for data in tqdm(issue , desc = "Processing issues"):
        number = data["number"]
        title = data.get("title", "")
        body = clean_text(data.get("body", ""))
        author = data.get("user", {}).get("login", "unknown")
        date = data.get("created_at", "")
        url = data.get("html_url", "")
        full_text = f"Issue #{number}: {title}\n\n{body}"

        for i, piece in enumerate(splitter.split_text(full_text)):
            chunks.append({
                "text": piece,
                "source_type": "issue",
                "issue_number": number,
                "author": author,
                "date": date,
                "url": url,
                "chunk_id": f"issue-{number}-{i}",
            })
    return chunks


def process_running():
    raw_data = load_raw_data()
    all_chunks =(
        process_commits(raw_data.get("commits",[]))
        + process_pr(raw_data.get("pull_requests",[]))
        + process_issues(raw_data.get("issues" , []))
    )
    out_path = PROCESSED_DIR / "chunks.jsonl"
    with open(out_path, "w") as f:
        for chunk in all_chunks:
            f.write(json.dumps(chunk) + "\n")
    print(f"Wrote {len(all_chunks)} chunks to {out_path}")
    return all_chunks

if __name__ == "__main__":
    process_running()



 
