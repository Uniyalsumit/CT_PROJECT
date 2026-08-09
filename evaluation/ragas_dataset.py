import sys
from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))
from datasets import Dataset
from rag_pipeline import ask
from .benchmark import BENCHMARK

questions = []
answers = []
contexts = []

for item in BENCHMARK:
    q = item["question"]
    result = ask(q)

    questions.append(q)
    answers.append(result["answer"])
    contexts.append([d.page_content for d in result["documents"]])

data = {
    "question": questions,
    "answer": answers,
    "contexts": contexts,
}

dataset = Dataset.from_dict(data)
save_path = Path(__file__).resolve().parent / "ragas_eval_dataset"
dataset.save_to_disk(str(save_path))
print(f"Built dataset with {len(dataset)} examples")