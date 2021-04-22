from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import CSRFProtect

db = SQLAlchemy()
scratch = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()
csrf._exempt_views.add('dash.dash.dispatch')  # Flask bug, included this so that the dash callbacks are working


def create_app(config_classname):
    app = Flask(__name__)
    app.config.from_object(config_classname)

# SECURITY STUFF, FLASK LOGIN PREVENTS DASH APP CALLBACKS AND TEMPLATES FROM LOADING (Will get back to this later)
    db.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    csrf.init_app(app)

    with app.app_context():
        # Import Dash application
        from dash_app.dash import init_dashboard
        app = init_dashboard(app)

        # CREATING FIRST INSTANCE OF DATABASE, COMMENTED SINCE DATABASE EXISTS
        # from my_app.models import Profile
        # db.create_all()

        db.Model.metadata.reflect(bind=db.engine)

    # Loading blueprints for all pages
    from my_app.home.home import home_bp
    app.register_blueprint(home_bp)

    from my_app.snp500.snp500 import snp500_bp
    app.register_blueprint(snp500_bp)

    from my_app.watchlist.watchlist import watchlist_bp
    app.register_blueprint(watchlist_bp)

    from my_app.community.community import community_bp
    app.register_blueprint(community_bp)

    from my_app.auth.auth import signup_bp
    app.register_blueprint(signup_bp)

    from my_app.auth.auth import login_bp
    app.register_blueprint(login_bp)

    from my_app.auth.auth import logout_bp
    app.register_blueprint(logout_bp)

    from my_app.profile.profile import profile_bp
    app.register_blueprint(profile_bp)

    return app
