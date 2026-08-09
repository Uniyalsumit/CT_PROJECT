import re 
import sys
from pathlib import Path
from sentence_transformers import CrossEncoder
sys.path.append(str(Path(__file__).resolve().parent.parent))
from config import NLI_MODEL_NAME, NLI_ENTAILMENT_THRESHOLD

_nli_model = None
print(CrossEncoder(NLI_MODEL_NAME).config.id2label)
CITATION_PATTERN = re.compile(
    r"\[(commit\s+[a-f0-9]{7,40}|PR\s+#\d+|issue\s+#\d+)\]",
    re.IGNORECASE,
)

def _load_nli_model()->CrossEncoder:
    global _nli_model
    if _nli_model is None:
        _nli_model = CrossEncoder(NLI_MODEL_NAME)
    return _nli_model

def split_into_claims(answer: str) -> list[str]:
    cleaned = CITATION_PATTERN.sub("", answer).strip()
    sentence = re.split(r"(?<=[.!?])\s+", cleaned)
    return [s.strip() for s in sentence if len(s.strip()) > 10]

def check_entailment(claim : str , document : list):
    model = _load_nli_model()
    pairs = [(d.page_content , claim) for d in document]
    scores = model.predict(pairs ,apply_softmax=True)
    best_score = float(max(s[1] for s in scores))
    return {
        "claim" : claim,
        "entailment_score" : best_score,
        "supported" : best_score >=NLI_ENTAILMENT_THRESHOLD
    }

def run_hallunication_guard(answer : str , documents : list):
    claims = split_into_claims(answer)
    results = [check_entailment(c, documents) for c in claims]
    unsupported = [r for r in results if not r["supported"]]
    return {
        "all_supported": len(unsupported) == 0,
        "unsupported_claims": unsupported,
        "results": results,
    }

def extract_citation(answer : str)->list[str]:
    return [m.group(1) for m in CITATION_PATTERN.finditer(answer)]

def validate_citations(answer: str, documents: list) -> dict:
    # Confirms every citation in the answer maps to a chunk that was actually retrieved — catches fabricated SHAs/PR#/issue#.
    valid_shas = {d.metadata.get("sha", "")[:7] for d in documents if d.metadata.get("sha")}
    valid_prs = {str(d.metadata.get("pr_number")) for d in documents if d.metadata.get("pr_number")}
    valid_issues = {str(d.metadata.get("issue_number")) for d in documents if d.metadata.get("issue_number")}

    citations = extract_citation(answer)
    invalid = []
    for c in citations:
        c_lower = c.lower()
        if c_lower.startswith("commit"):
            sha = c_lower.replace("commit", "").strip()
            if sha not in valid_shas:
                invalid.append(c)
        elif c_lower.startswith("pr"):
            num = re.search(r"\d+", c).group()
            if num not in valid_prs:
                invalid.append(c)
        elif c_lower.startswith("issue"):
            num = re.search(r"\d+", c).group()
            if num not in valid_issues:
                invalid.append(c)

    return {
        "all_valid": len(invalid) == 0,
        "invalid_citations": invalid,
        "total_citations": len(citations),
    }

def guard_answer(answer: str, documents: list) -> dict:
    # Runs both guardrail checks and returns a combined verdict.
    hallucination_result = run_hallunication_guard(answer, documents)
    citation_result = validate_citations(answer, documents)

    passed = hallucination_result["all_supported"] and citation_result["all_valid"]

    return {
        "passed": passed,
        "hallucination_check": hallucination_result,
        "citation_check": citation_result,
    }
