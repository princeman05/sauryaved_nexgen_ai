from deep_translator import GoogleTranslator
from flask import (
    Blueprint,
    render_template,
    request
)
from flask_login import (
    login_required,
    current_user
)
utility_bp = Blueprint(

    'utility',

    __name__
)

# =========================
# UTILITIES HOME
# =========================

@utility_bp.route(
    '/utilities'
)
@login_required
def utilities():

    return render_template(
        'utilities.html'
    )

# =========================
# SPEECH TO TEXT
# =========================

@utility_bp.route(
    '/speech_to_text'
)
def speech_to_text():

    return render_template(
        'speech_to_text.html'
    )

# =========================
# TEXT TO SPEECH
# =========================

@utility_bp.route(
    '/text_to_speech'
)
def text_to_speech():

    return render_template(
        'text_to_speech.html'
    )
#===========================
# traslator
#===========================
@utility_bp.route(
    '/translator',
    methods=['GET', 'POST']
)
def translator():

    translated_text = ""

    if request.method == 'POST':

        text = request.form['text']

        language = request.form['language']

        translated_text = GoogleTranslator(

            source='auto',

            target=language

        ).translate(text)

    return render_template(

        'translator.html',

        translated_text=translated_text
    )