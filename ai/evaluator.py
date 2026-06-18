def evaluate_answer(
    answer,
    keywords
):

    answer = answer.lower()

    score = 40

    matched_keywords = 0

    # KEYWORD MATCHING
    for keyword in keywords:

        if keyword.lower() in answer:

            matched_keywords += 1

            score += 8

    # ANSWER LENGTH BONUS
    word_count = len(answer.split())

    if word_count > 20:

        score += 10

    if word_count > 40:

        score += 10

    # PRACTICAL EXAMPLE BONUS
    practical_words = [

        "project",
        "example",
        "real-time",
        "practical",
        "experience",
        "application"
    ]

    for word in practical_words:

        if word in answer:

            score += 5

            break

    # CONFIDENCE BONUS
    strong_words = [

        "implemented",
        "developed",
        "built",
        "optimized",
        "designed"
    ]

    for word in strong_words:

        if word in answer:

            score += 5

            break

    # LIMIT SCORE
    if score > 100:

        score = 100

    return score