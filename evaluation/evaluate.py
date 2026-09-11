import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from src.context_extractor import extract_context


TEST_FILE = ROOT / "evaluation" / "test_queries.json"


def evaluate_context_extraction():
    with TEST_FILE.open("r", encoding="utf-8") as f:
        tests = json.load(f)

    correct = 0
    total = 0

    for test in tests:
        context = extract_context(test["query"])

        for field in ["expected_occasion", "expected_style"]:
            expected_key = field
            actual_key = field.replace("expected_", "")

            if expected_key in test:
                total += 1
                if context.get(actual_key) == test[expected_key]:
                    correct += 1

    accuracy = correct / total if total else 0

    print(f"Context extraction accuracy: {accuracy:.2%}")
    print(f"Correct: {correct}/{total}")


if __name__ == "__main__":
    evaluate_context_extraction()
