# app/__init__.py

from flask import Flask
from .config import Config
from flask_sqlalchemy import SQLAlchemy

# 데이터베이스 객체 생성
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # 애플리케이션 설정
    app.config.from_object(Config)

    # 데이터베이스 초기화
    db.init_app(app)

    # 라우트 설정
    from .routes import main_bp
    app.register_blueprint(main_bp)

    return app
