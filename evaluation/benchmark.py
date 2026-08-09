BENCHMARK = [
    # ---------- GROUNDED: real entities, should answer + pass guard (20) ----------
    {"id": 1, "category": "grounded", "question": "Why was APIRouter changed to store the entire object instead of copying routes?", "expected_behavior": "answer_and_pass", "ground_truth_ref": "PR #15745"},
    {"id": 2, "category": "grounded", "question": "What does per-route middleware do in APIRouter?", "expected_behavior": "answer_and_pass", "ground_truth_ref": "issue #4437"},
    {"id": 3, "category": "grounded", "question": "Why is per-route and per-APIRouter middleware useful compared to global middleware?", "expected_behavior": "answer_and_pass", "ground_truth_ref": "issue #4437"},
    {"id": 4, "category": "grounded", "question": "Why does middleware execute even when there's no matching route?", "expected_behavior": "answer_and_pass", "ground_truth_ref": "PR #4794"},
    {"id": 5, "category": "grounded", "question": "What logging changes were made for debugging request validation?", "expected_behavior": "answer_and_pass", "ground_truth_ref": "issue #14078"},
    {"id": 6, "category": "grounded", "question": "How does FastAPI use Pydantic models for request validation?", "expected_behavior": "answer_and_pass", "ground_truth_ref": "issue #14078 -- VERIFY"},
    {"id": 7, "category": "grounded", "question": "What validation happens in the FastAPI response handler?", "expected_behavior": "answer_and_pass", "ground_truth_ref": "issue #1359"},
    {"id": 8, "category": "grounded", "question": "Why can subrouters now be included in main routers before adding routes?", "expected_behavior": "answer_and_pass", "ground_truth_ref": "PR #15745"},
    {"id": 9, "category": "grounded", "question": "What are the new .matches() and .handle() methods on APIRouter for?", "expected_behavior": "answer_and_pass", "ground_truth_ref": "PR #15745"},
    {"id": 10, "category": "grounded", "question": "Why does router.routes now return a tree instead of a plain list?", "expected_behavior": "answer_and_pass", "ground_truth_ref": "PR #15745"},
    {"id": 11, "category": "grounded", "question": "What happens to code that iterates directly over router.routes after this change?", "expected_behavior": "answer_and_pass", "ground_truth_ref": "PR #15745"},
    {"id": 12, "category": "grounded", "question": "Why are custom APIRoute subclasses now possible?", "expected_behavior": "answer_and_pass", "ground_truth_ref": "PR #15745"},
    {"id": 13, "category": "grounded", "question": "What memory benefit comes from not copying routes?", "expected_behavior": "answer_and_pass", "ground_truth_ref": "PR #15745"},
    {"id": 14, "category": "grounded", "question": "Is the alpha feature of customizing APIRoute and APIRouter instances officially supported?", "expected_behavior": "answer_and_pass", "ground_truth_ref": "PR #15745"},
    {"id": 15, "category": "grounded", "question": "Why did FastAPI add dependency execution per router even without a matching route?", "expected_behavior": "answer_and_pass", "ground_truth_ref": "PR #4794"},
    {"id": 16, "category": "grounded", "question": "How were duplicate route definitions handled before the APIRouter change?", "expected_behavior": "answer_and_pass", "ground_truth_ref": "PR #15745 -- VERIFY"},
    {"id": 17, "category": "grounded", "question": "What was the original bug report that led to per-route middleware support?", "expected_behavior": "answer_and_pass", "ground_truth_ref": "issue #4437"},
    {"id": 18, "category": "grounded", "question": "Why should router.routes be treated as an internal implementation detail?", "expected_behavior": "answer_and_pass", "ground_truth_ref": "PR #15745"},
    {"id": 19, "category": "grounded", "question": "What issue prompted better logging around Pydantic validation errors?", "expected_behavior": "answer_and_pass", "ground_truth_ref": "issue #14078"},
    {"id": 20, "category": "grounded", "question": "Why was response validation added to the FastAPI response handler?", "expected_behavior": "answer_and_pass", "ground_truth_ref": "issue #1359"},

    # ---------- ADVERSARIAL: nonexistent/fake entities, should abstain (8) ----------
    {"id": 21, "category": "adversarial_fake_entity", "question": "What does the class FastAPISuperRouter do?", "expected_behavior": "abstain", "ground_truth_ref": None},
    {"id": 22, "category": "adversarial_fake_entity", "question": "How does PydanticStrictValidator work in FastAPI?", "expected_behavior": "abstain", "ground_truth_ref": None},
    {"id": 23, "category": "adversarial_fake_entity", "question": "What is the purpose of the FastAPIAsyncMiddlewareChain class?", "expected_behavior": "abstain", "ground_truth_ref": None},
    {"id": 24, "category": "adversarial_fake_entity", "question": "Explain how RouteCacheManager improves FastAPI performance.", "expected_behavior": "abstain", "ground_truth_ref": None},
    {"id": 25, "category": "adversarial_fake_entity", "question": "What does `APIRouterV2` add compared to the original APIRouter?", "expected_behavior": "abstain", "ground_truth_ref": None},
    {"id": 26, "category": "adversarial_fake_entity", "question": "How does the DependencyGraphResolver class work?", "expected_behavior": "abstain", "ground_truth_ref": None},
    {"id": 27, "category": "adversarial_fake_entity", "question": "What bug did the SchemaAutoMigrator fix?", "expected_behavior": "abstain", "ground_truth_ref": None},
    {"id": 28, "category": "adversarial_fake_entity", "question": "Why was the RequestThrottlePolicy class deprecated?", "expected_behavior": "abstain", "ground_truth_ref": None},

    # ---------- OFF-TOPIC / ABSURD PREMISE: should deny or abstain (5) ----------
    {"id": 29, "category": "off_topic", "question": "Does FastAPI use blockchain to validate requests?", "expected_behavior": "deny_or_abstain", "ground_truth_ref": None},
    {"id": 30, "category": "off_topic", "question": "Does FastAPI mine cryptocurrency in the background?", "expected_behavior": "deny_or_abstain", "ground_truth_ref": None},
    {"id": 31, "category": "off_topic", "question": "Why does FastAPI require a GPU to run?", "expected_behavior": "deny_or_abstain", "ground_truth_ref": None},
    {"id": 32, "category": "off_topic", "question": "Does FastAPI use quantum computing for routing decisions?", "expected_behavior": "deny_or_abstain", "ground_truth_ref": None},
    {"id": 33, "category": "off_topic", "question": "Why did FastAPI switch its entire backend to Rust?", "expected_behavior": "deny_or_abstain", "ground_truth_ref": None},

    # ---------- MULTI-FACT / COMPOUND: tests threshold calibration (8) ----------
    {"id": 34, "category": "multi_fact", "question": "Why was APIRouter changed to store the entire object, and what two new features does this enable?", "expected_behavior": "answer_and_pass_multi", "ground_truth_ref": "PR #15745"},
    {"id": 35, "category": "multi_fact", "question": "How do per-route middleware and per-router dependency execution relate to each other in FastAPI's design?", "expected_behavior": "answer_and_pass_multi", "ground_truth_ref": "issue #4437, PR #4794"},
    {"id": 36, "category": "multi_fact", "question": "What changed for both route storage and subrouter inclusion order in the APIRouter refactor?", "expected_behavior": "answer_and_pass_multi", "ground_truth_ref": "PR #15745"},
    {"id": 37, "category": "multi_fact", "question": "Summarize both the logging improvements and the Pydantic validation changes from issue #14078.", "expected_behavior": "answer_and_pass_multi", "ground_truth_ref": "issue #14078"},
    {"id": 38, "category": "multi_fact", "question": "What are the risks of iterating over router.routes directly, and why did this change with the new object-preserving design?", "expected_behavior": "answer_and_pass_multi", "ground_truth_ref": "PR #15745"},
    {"id": 39, "category": "multi_fact", "question": "How does response validation in issue #1359 relate to request validation logging in issue #14078?", "expected_behavior": "answer_and_pass_multi", "ground_truth_ref": "issue #1359, issue #14078 -- VERIFY relation exists"},
    {"id": 40, "category": "multi_fact", "question": "What experimental customization options does the APIRouter refactor introduce, and why are they still considered unstable?", "expected_behavior": "answer_and_pass_multi", "ground_truth_ref": "PR #15745"},
    {"id": 41, "category": "multi_fact", "question": "Why does middleware execution without a matching route matter for dependency handling per router?", "expected_behavior": "answer_and_pass_multi", "ground_truth_ref": "PR #4794"},

    # ---------- AMBIGUOUS / UNDERSPECIFIED: tests retrieval precision (5) ----------
    {"id": 42, "category": "ambiguous", "question": "What changed with routing?", "expected_behavior": "answer_and_pass", "ground_truth_ref": "PR #15745 -- VERIFY (very broad, may match multiple)"},
    {"id": 43, "category": "ambiguous", "question": "Why was validation improved?", "expected_behavior": "answer_and_pass", "ground_truth_ref": "issue #14078 or #1359 -- VERIFY"},
    {"id": 44, "category": "ambiguous", "question": "What was fixed in the middleware system?", "expected_behavior": "answer_and_pass", "ground_truth_ref": "issue #4437 or PR #4794 -- VERIFY"},
    {"id": 45, "category": "ambiguous", "question": "Tell me about router changes.", "expected_behavior": "answer_and_pass", "ground_truth_ref": "PR #15745 -- VERIFY"},
    {"id": 46, "category": "ambiguous", "question": "What's new with APIRouter?", "expected_behavior": "answer_and_pass", "ground_truth_ref": "PR #15745 -- VERIFY"},

    # ---------- EDGE CASES: short queries, typos, alt naming (4) ----------
    {"id": 47, "category": "edge_case", "question": "APIRouter middleware?", "expected_behavior": "answer_and_pass", "ground_truth_ref": "issue #4437 -- VERIFY short-query retrieval works"},
    {"id": 48, "category": "edge_case", "question": "Why apirouter store entire object not copy routes", "expected_behavior": "answer_and_pass", "ground_truth_ref": "PR #15745 -- VERIFY typo/casing tolerance"},
    {"id": 49, "category": "edge_case", "question": "What does `API_Router` (with underscore) do differently?", "expected_behavior": "abstain", "ground_truth_ref": None},
    {"id": 50, "category": "edge_case", "question": "middleware", "expected_behavior": "answer_and_pass", "ground_truth_ref": "issue #4437 -- VERIFY single-word query behavior"},
]