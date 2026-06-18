from flask import (
    Blueprint,
    render_template
)

from flask_login import (
    login_required
)

from models.interview_model import Interview
from models.user_model import User
from models import db
admin_bp = Blueprint(
    'admin',
    __name__
)

@admin_bp.route('/admin')

@login_required
def admin_dashboard():

    from flask import request

    # =========================
    # GET FILTER VALUES
    # =========================

    search = request.args.get(
        'search',
        ''
    )

    category = request.args.get(
        'category',
        ''
    )

    # =========================
    # BASE QUERY
    # =========================

    interviews_query = Interview.query

    # =========================
    # SEARCH USERNAME
    # =========================

    if search:

        users = User.query.filter(

            User.username.ilike(
                f'%{search}%'
            )

        ).all()

        user_ids = [

            user.id

            for user in users
        ]

        interviews_query = interviews_query.filter(

            Interview.user_id.in_(
                user_ids
            )
        )

    # =========================
    # CATEGORY FILTER
    # =========================

    if category:

        interviews_query = interviews_query.filter_by(

            category=category
        )

    # =========================
    # SORT BY SCORE
    # =========================

    interviews = interviews_query.order_by(

        Interview.score.desc()

    ).all()

    # =========================
    # PREPARE DATA
    # =========================

    data = []

    for interview in interviews:

        user = User.query.get(
            interview.user_id
        )

        if user:

            username = user.username

        else:

            username = "Unknown"

        data.append({

            'username': username,

            'category': interview.category,

            'score': interview.score

        })

    return render_template(

        'admin_dashboard.html',

        data=data,

        search=search,

        category=category
    )
@admin_bp.route('/leaderboard')

@login_required
def leaderboard():

    top_candidates = db.session.query(

        Interview,
        User

    ).join(

        User,
        Interview.user_id == User.id

    ).order_by(

        Interview.score.desc()

    ).limit(10).all()

    return render_template(

        'leaderboard.html',

        candidates=top_candidates
    )