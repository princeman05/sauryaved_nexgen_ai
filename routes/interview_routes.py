import os
import cv2

from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    session,
    Response
)

from flask_login import (
    login_required,
    current_user
)
from models.question_model import Question

import random

from utils.resume_parser import (
    extract_resume_text
)

from utils.pdf_generator import (
    generate_pdf_report
)

from ai.evaluator import (
    evaluate_answer
)

from ai.openai_feedback import (
    generate_feedback
)


from models.interview_model import Interview

from models import db
from models.user_model import User
from flask_login import current_user

# ==========================================
# BLUEPRINT
# ==========================================

interview_bp = Blueprint(
    'interview',
    __name__
)


# ==========================================
# HAAR CASCADES
# ==========================================

face_cascade = cv2.CascadeClassifier(

    cv2.data.haarcascades +

    'haarcascade_frontalface_default.xml'
)

eye_cascade = cv2.CascadeClassifier(

    cv2.data.haarcascades +

    'haarcascade_eye.xml'
)

smile_cascade = cv2.CascadeClassifier(

    cv2.data.haarcascades +

    'haarcascade_smile.xml'
)


# ==========================================
# LIVE ANALYTICS
# ==========================================

eye_contact_frames = 0

total_frames = 0

smile_count = 0

distraction_count = 0


# ==========================================
# ATS SCORE
# ==========================================

def calculate_ats_score(
    extracted_text
):

    score = 0

    text = extracted_text.lower()

    skills = [

        "python",
        "flask",
        "sql",
        "html",
        "css",
        "javascript",
        "bootstrap"
    ]

    detected_skills = []

    for skill in skills:

        if skill in text:

            score += 15

            detected_skills.append(skill)

    if score > 100:

        score = 100

    return score, detected_skills


# ==========================================
# QUESTION GENERATOR
# ==========================================

def generate_questions_from_resume(
    resume_text
):

    questions = []

    text = resume_text.lower()

    if "python" in text:

        questions.append(
            "Explain Python OOP concepts."
        )

        questions.append(
            "What are Python decorators?"
        )

    if "flask" in text:

        questions.append(
            "Why did you use Flask?"
        )

        questions.append(
            "Explain Flask routing."
        )

    if "sql" in text:

        questions.append(
            "Explain SQL joins."
        )

    if "html" in text or "css" in text:

        questions.append(
            "Difference between HTML and CSS?"
        )

    if "javascript" in text:

        questions.append(
            "Explain JavaScript event handling."
        )

    if not questions:

        questions = [

            "Tell me about yourself.",

            "Why should we hire you?"
        ]

    return questions


# ==========================================
# INTERVIEW ROUTE
# ==========================================

@interview_bp.route(
    '/interview',
    methods=['GET', 'POST']
)

@login_required
def interview():

    resume_text = session.get(
        'resume_text',
        ''
    )

    QUESTIONS = generate_questions_from_resume(
        resume_text
    )

    if 'question_index' not in session:

        session['question_index'] = 0

        session['total_score'] = 0

    index = session['question_index']

    # ======================================
    # INTERVIEW FINISHED
    # ======================================

    if index >= len(QUESTIONS):

        feedback = generate_feedback(

            "Final Interview",

            "Interview Completed Successfully"
        )

        final_score = int(

            session['total_score'] / len(QUESTIONS)
        )

        _, detected_skills = calculate_ats_score(
            resume_text
        )

        # GENERATE PDF REPORT
        pdf_file = generate_pdf_report(

            current_user.username,

            final_score,

            feedback,

            detected_skills
        )

        # SAVE INTERVIEW
        interview = Interview(

            user_id=current_user.id,

            category="Python",

            score=final_score,

            feedback=feedback
        )

        db.session.add(interview)

        db.session.commit()

        # CLEAR SESSION
        session.pop('question_index')

        session.pop('total_score')

        return render_template(

            'feedback.html',

            feedback=feedback,

            score=final_score,

            pdf_file=pdf_file,

            detected_skills=detected_skills
        )

    # ======================================
    # CURRENT QUESTION
    # ======================================

    question = QUESTIONS[index]

    if request.method == 'POST':

        answer = request.form['answer']

        keywords = [

            "class",
            "object",
            "inheritance",
            "polymorphism",
            "framework",
            "database",
            "api",
            "routing"
        ]

        score = evaluate_answer(
            answer,
            keywords
        )

        session['total_score'] += score

        session['question_index'] += 1

        return redirect('/interview')

    return render_template(

        'interview.html',

        question=question,

        current=index + 1,

        total=len(QUESTIONS)
    )


# ==========================================
# RESUME UPLOAD
# ==========================================

@interview_bp.route(
    '/upload_resume',
    methods=['GET', 'POST']
)

@login_required
def upload_resume():

    extracted_text = ""

    ats_score = 0

    detected_skills = []

    if request.method == 'POST':

        file = request.files['resume']

        os.makedirs(
            'uploads',
            exist_ok=True
        )

        filepath = os.path.join(
            'uploads',
            file.filename
        )

        file.save(filepath)

        extracted_text = extract_resume_text(
            filepath
        )

        session['resume_text'] = extracted_text

        ats_score, detected_skills = calculate_ats_score(
            extracted_text
        )

    return render_template(

        'resume_upload.html',

        extracted_text=extracted_text,

        ats_score=ats_score,

        detected_skills=detected_skills
    )


# ==========================================
# CAMERA PAGE
# ==========================================

@interview_bp.route('/camera_ai')

@login_required
def camera_ai():

    return render_template(
        'camera_ai.html'
    )


# ==========================================
# VIDEO FEED
# ==========================================

@interview_bp.route('/video_feed')

def video_feed():

    return Response(

        generate_frames(),

        mimetype='multipart/x-mixed-replace; boundary=frame'
    )


# ==========================================
# CAMERA FRAME GENERATOR
# ==========================================

def generate_frames():

    global eye_contact_frames
    global total_frames
    global smile_count
    global distraction_count

    # CAMERA INIT
    camera = cv2.VideoCapture(
        0,
        cv2.CAP_DSHOW
    )

    # CAMERA SIZE
    camera.set(
        cv2.CAP_PROP_FRAME_WIDTH,
        640
    )

    camera.set(
        cv2.CAP_PROP_FRAME_HEIGHT,
        480
    )

    # CHECK CAMERA
    if not camera.isOpened():

        print("❌ Camera failed")

        return

    # VIDEO RECORDING
    os.makedirs(
        'static/recordings',
        exist_ok=True
    )

    fourcc = cv2.VideoWriter_fourcc(
        *'mp4v'
    )

    out = cv2.VideoWriter(

        'static/recordings/interview.mp4',

        fourcc,

        20.0,

        (640,480)
    )

    while True:

        success, frame = camera.read()

        if not success:

            print("❌ Frame failed")

            break

        total_frames += 1

        # SAVE RECORDING
        out.write(frame)

        # GRAYSCALE
        gray = cv2.cvtColor(

            frame,

            cv2.COLOR_BGR2GRAY
        )

        emotion_text = "Focused 🚀"

        # ======================================
        # FACE DETECTION
        # ======================================

        faces = face_cascade.detectMultiScale(

            gray,

            1.1,

            5
        )

        status = "No Face"

        if len(faces) > 0:

            status = "Face Detected"

        # NO FACE
        if len(faces) == 0:

            cv2.putText(

                frame,

                "⚠ Candidate Missing",

                (20,210),

                cv2.FONT_HERSHEY_SIMPLEX,

                1,

                (0,0,255),

                2
            )

        # MULTIPLE PERSONS
        if len(faces) > 1:

            cv2.putText(

                frame,

                "⚠ Multiple Persons",

                (20,170),

                cv2.FONT_HERSHEY_SIMPLEX,

                1,

                (0,0,255),

                2
            )

        # ======================================
        # FACE LOOP
        # ======================================

        for (x, y, w, h) in faces:

            cv2.rectangle(

                frame,

                (x,y),

                (x+w,y+h),

                (0,255,255),

                3
            )

            roi_gray = gray[
                y:y+h,
                x:x+w
            ]

            roi_color = frame[
                y:y+h,
                x:x+w
            ]

            # ==================================
            # EYE DETECTION
            # ==================================

            eyes = eye_cascade.detectMultiScale(
                roi_gray
            )

            eye_status = "Eyes Detected"

            if len(eyes) == 0:

                eye_status = "Looking Away"

                distraction_count += 1

                emotion_text = "Distracted 😐"

            if len(eyes) > 0:

                eye_contact_frames += 1

            # DRAW EYES
            for (ex, ey, ew, eh) in eyes:

                cv2.rectangle(

                    roi_color,

                    (ex, ey),

                    (ex+ew, ey+eh),

                    (0,255,0),

                    2
                )

            cv2.putText(

                frame,

                eye_status,

                (20,90),

                cv2.FONT_HERSHEY_SIMPLEX,

                1,

                (0,255,0),

                2
            )

            # ==================================
            # SMILE DETECTION
            # ==================================

            smiles = smile_cascade.detectMultiScale(

                roi_gray,

                1.8,

                20
            )

            if len(smiles) > 0:

                smile_count += 1

                emotion_text = "Confident 😊"

                cv2.putText(

                    frame,

                    "😊 Confident Smile",

                    (20,130),

                    cv2.FONT_HERSHEY_SIMPLEX,

                    1,

                    (255,255,0),

                    2
                )

            # DRAW SMILES
            for (sx, sy, sw, sh) in smiles:

                cv2.rectangle(

                    roi_color,

                    (sx, sy),

                    (sx+sw, sy+sh),

                    (255,0,255),

                    2
                )

        # ======================================
        # ANALYTICS
        # ======================================

        if total_frames > 0:

            eye_contact_percent = int(

                (eye_contact_frames / total_frames) * 100
            )

        else:

            eye_contact_percent = 0

        # ======================================
        # DISPLAY STATUS
        # ======================================

        cv2.putText(

            frame,

            status,

            (20,50),

            cv2.FONT_HERSHEY_SIMPLEX,

            1,

            (255,255,0),

            2
        )

        cv2.putText(

            frame,

            f"AI Status: {emotion_text}",

            (20,290),

            cv2.FONT_HERSHEY_SIMPLEX,

            1,

            (255,0,0),

            2
        )

        cv2.putText(

            frame,

            "🔴 Recording",

            (20,250),

            cv2.FONT_HERSHEY_SIMPLEX,

            1,

            (0,0,255),

            3
        )

        # LIVE ANALYTICS
        cv2.putText(

            frame,

            f"Eye Contact: {eye_contact_percent}%",

            (20,330),

            cv2.FONT_HERSHEY_SIMPLEX,

            0.8,

            (0,255,255),

            2
        )

        cv2.putText(

            frame,

            f"Smiles: {smile_count}",

            (20,370),

            cv2.FONT_HERSHEY_SIMPLEX,

            0.8,

            (255,255,0),

            2
        )

        cv2.putText(

            frame,

            f"Distractions: {distraction_count}",

            (20,410),

            cv2.FONT_HERSHEY_SIMPLEX,

            0.8,

            (0,0,255),

            2
        )

        # ENCODE FRAME
        ret, buffer = cv2.imencode(

            '.jpg',

            frame
        )

        frame = buffer.tobytes()

        yield (

            b'--frame\r\n'

            b'Content-Type: image/jpeg\r\n\r\n'

            + frame +

            b'\r\n'
        )

    # RELEASE
    camera.release()

    out.release()

@interview_bp.route('/analytics')

@login_required
def analytics():

    interviews = Interview.query.all()

    # =========================
    # BASIC STATS
    # =========================

    total = len(interviews)

    scores = [i.score for i in interviews]

    highest = max(scores) if scores else 0

    lowest = min(scores) if scores else 0

    average = round(
        sum(scores) / len(scores),
        2
    ) if scores else 0

    # =========================
    # BAR CHART DATA
    # =========================

    usernames = []

    score_data = []

    for interview in interviews:

        user = User.query.get(
            interview.user_id
        )

        if user:

            usernames.append(
                user.username
            )

        else:

            usernames.append(
                "Unknown"
            )

        score_data.append(
            interview.score
        )

    # =========================
    # CATEGORY PIE CHART
    # =========================

    category_map = {}

    for interview in interviews:

        category = interview.category

        if category in category_map:

            category_map[category] += 1

        else:

            category_map[category] = 1

    categories = list(
        category_map.keys()
    )

    category_counts = list(
        category_map.values()
    )

    # =========================
    # TREND LINE CHART
    # =========================

    trend_labels = []

    trend_scores = []

    for index, interview in enumerate(interviews):

        trend_labels.append(
            f"Interview {index + 1}"
        )

        trend_scores.append(
            interview.score
        )

    # =========================
    # TOP CANDIDATES
    # =========================

    top_interviews = sorted(

        interviews,

        key=lambda x: x.score,

        reverse=True

    )[:5]

    top_names = []

    top_scores = []

    for interview in top_interviews:

        user = User.query.get(
            interview.user_id
        )

        if user:

            top_names.append(
                user.username
            )

        else:

            top_names.append(
                "Unknown"
            )

        top_scores.append(
            interview.score
        )

    return render_template(

        'analytics.html',

        total=total,

        highest=highest,

        lowest=lowest,

        average=average,

        usernames=usernames,

        scores=score_data,

        categories=categories,

        category_counts=category_counts,

        trend_labels=trend_labels,

        trend_scores=trend_scores,

        top_names=top_names,

        top_scores=top_scores
    )
@interview_bp.route('/history')

@login_required
def history():

    interviews = Interview.query.filter_by(

        user_id=current_user.id

    ).order_by(

        Interview.id.desc()

    ).all()

    return render_template(

        'history.html',

        interviews=interviews
    )