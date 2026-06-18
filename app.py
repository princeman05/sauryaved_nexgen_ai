from flask import Flask, render_template
from config import Config
from models import db
from flask_migrate import Migrate
from flask_login import LoginManager

# Blueprints
from routes.admin_routes import admin_bp
from routes.utility_routes import utility_bp
from routes.auth_routes import auth_bp
from routes.dashboard_routes import dashboard_bp
from routes.interview_routes import interview_bp

# App init
app = Flask(__name__)
app.config.from_object(Config)

# DB init
db.init_app(app)
migrate = Migrate(app, db)

# Login setup
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

# Models (important for migrations)
from models.user_model import User
from models.interview_model import Interview

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Register Blueprints
app.register_blueprint(utility_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(dashboard_bp)
app.register_blueprint(interview_bp)
app.register_blueprint(admin_bp)

# Home route
@app.route('/')
def home():
    return render_template('index.html')


# IMPORTANT: do NOT use app.run() in production
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)