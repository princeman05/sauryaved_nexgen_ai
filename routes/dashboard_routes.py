from flask import (
    Blueprint,
    render_template
)

from flask_login import (
    login_required,
    current_user
)

from models.interview_model import Interview

dashboard_bp = Blueprint(
    'dashboard',
    __name__
)

@dashboard_bp.route('/dashboard')

@login_required
def dashboard():

    interviews = Interview.query.filter_by(
        user_id=current_user.id
    ).all()

    total_interviews = len(interviews)

    # TOTAL SCORE
    total_score = sum(
        interview.score
        for interview in interviews
    )

    # AVERAGE SCORE
    average_score = 0

    if total_interviews > 0:

        average_score = int(
            total_score / total_interviews
        )

    # BEST SCORE
    best_score = 0

    if interviews:

        best_score = max(
            interview.score
            for interview in interviews
        )

    # LAST 5 INTERVIEWS
    recent_interviews = interviews[-5:]

    # CHART DATA
    chart_scores = [
        interview.score
        for interview in interviews
    ]

    chart_labels = [

        f"Interview {i+1}"

        for i in range(
            len(chart_scores)
        )
    ]

    return render_template(

        'dashboard.html',

        interviews=recent_interviews,

        total_interviews=total_interviews,

        average_score=average_score,

        best_score=best_score,

        chart_scores=chart_scores,

        chart_labels=chart_labels
    )