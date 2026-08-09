import sys
import types

# fake_vertexai_module = types.ModuleType("langchain_community.chat_models.vertexai")

# class ChatVertexAI:
#     """Stub — never actually used, just satisfies ragas's import."""
#     pass

# fake_vertexai_module.ChatVertexAI = ChatVertexAI
# sys.modules["langchain_community.chat_models.vertexai"] = fake_vertexai_module


from pathlib import Path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from datasets import load_from_disk
from ragas import evaluate
from ragas.metrics import faithfulness, AnswerRelevancy
from ragas.run_config import RunConfig
from ragas.llms import LangchainLLMWrapper
from ragas.embeddings import LangchainEmbeddingsWrapper

from langchain_groq import ChatGroq
from langchain_huggingface import HuggingFaceEmbeddings

from config import GROQ_API_KEY, EMBEDDING_MODEL

JUDGE_MODEL = "openai/gpt-oss-120b"
judge_llm = ChatGroq(model=JUDGE_MODEL, api_key=GROQ_API_KEY, temperature=0,max_tokens=1596)
ragas_llm = LangchainLLMWrapper(judge_llm)

embeddings_model = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)
ragas_embeddings = LangchainEmbeddingsWrapper(embeddings_model)


answer_relevancy = AnswerRelevancy(strictness=1)


run_config = RunConfig(max_workers=2, timeout=120 , max_retries=5, max_wait=90,)


TEST_ON_SMALL_SUBSET = True
SUBSET_SIZE = 5


def main():
    dataset = load_from_disk(str(Path(__file__).resolve().parent / "ragas_eval_dataset"))
    print(f"Loaded {len(dataset)} examples for evaluation")
    print(f"Judge model: {JUDGE_MODEL}")

    result = evaluate(
        dataset,
        metrics=[faithfulness, answer_relevancy],
        llm=ragas_llm,
        embeddings=ragas_embeddings,
        run_config=run_config,
    )

    print("RAGAs Results")
    print(result)

    df = result.to_pandas()
    results_dir = Path(__file__).resolve().parent / "results"
    results_dir.mkdir(exist_ok=True)
    suffix = "_test" if TEST_ON_SMALL_SUBSET else ""
    out_path = results_dir / f"ragas_results{suffix}.csv"
    df.to_csv(out_path, index=False)
    print(f"\nSaved detailed results to {out_path}")

    print("Averages")
    for col in ["faithfulness", "answer_relevancy"]:
        if col in df.columns:
            print(f"{col}: {df[col].mean():.3f}")


if __name__ == "__main__":
    main()