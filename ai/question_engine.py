
import random

questions = {

    "python": [

        "Explain OOP concepts.",

        "What is Flask?",

        "What is inheritance?",

        "Explain polymorphism."
    ],

    "hr": [

        "Tell me about yourself.",

        "What are your strengths?"
    ]
}

def get_random_question(category):

    return random.choice(
        questions.get(category, [])
    )
