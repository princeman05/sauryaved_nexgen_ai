from ai.evaluator import evaluate_answer

def test_evaluate():
    score = evaluate_answer(
        "class object inheritance",
        ["class", "object", "inheritance"]
    )

    assert score == 100