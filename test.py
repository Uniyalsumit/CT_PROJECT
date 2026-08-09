import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from rag_pipeline import ask   # only need this once


result = ask("Explain dependency injection in FastAPI")
guard = result["guard"]

print("Answer:", result["answer"])
print("\nGuard passed:", guard["passed"])
print("Unsupported claims:", len(guard["hallucination_check"]["unsupported_claims"]))

for c in guard["hallucination_check"]["unsupported_claims"]:
    print(f"[{c['entailment_score']:.3f}] {c['claim']}")

# test_cases = [
#     {
#         "question": "Does FastAPI use blockchain to validate requests?",
#         "expect": "should_abstain_or_deny",   
#     },
#     {
#         "question": "What does the class FastAPISuperRouter do?",
#         "expect": "should_abstain",            
#     },
#     {
#         "question": "Why was APIRouter changed to store the entire object instead of copying routes?",
#         "expect": "should_answer_grounded",   
#     },
#     {
#         "question": "What does per-route middleware do in APIRouter?",
#         "expect": "should_answer_grounded",
#     },
#     {
#         "question": "Why is FastAPI popular?",
#         "expect": "should_answer_or_abstain",
#     },
# ]

# for case in test_cases:
#     q = case["question"]
#     print(f"\n{'='*70}")
#     print(f"Q: {q}")
#     print(f"Expected: {case['expect']}")
#     print('='*70)

#     result = ask(q)

#     print(f"Answer: {result['answer'][:300]}")
#     print(f"Docs retrieved: {len(result['documents'])}")

#     if result["guard"] is None:
#         print("Guard: N/A (abstained before generation)")
#     else:
#         guard = result["guard"]
#         print(f"Guard passed: {guard['passed']}")
#         if not guard["hallucination_check"]["all_supported"]:
#             print("  Unsupported claims:")
#             for c in guard["hallucination_check"]["unsupported_claims"]:
#                 print(f"    [{c['entailment_score']:.2f}] {c['claim']}")
#         if not guard["citation_check"]["all_valid"]:
#             print("  Invalid citations:", guard["citation_check"]["invalid_citations"])

