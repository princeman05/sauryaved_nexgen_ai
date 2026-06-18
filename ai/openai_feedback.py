def generate_feedback(
    question,
    answer,
    score=75
):

    feedback = f"""

INTERVIEW ANALYSIS

Score: {score}/100


Strengths:

- Good technical understanding
- Attempted detailed explanation


Weaknesses:

- Could include more practical examples
- Improve confidence in explanation


Recommendation:

Keep practicing technical interviews.
You have strong potential.

"""

    return feedback