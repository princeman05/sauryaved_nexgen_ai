def evaluate_answer(
    answer,
    keywords
):

    score = 0

    answer = answer.lower()

    for word in keywords:

        if word.lower() in answer:

            score += 25

    return score