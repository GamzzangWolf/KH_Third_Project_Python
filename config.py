import os
from flask import Flask

app = Flask(__name__)

# Flask 애플리케이션 설정
app.config['DEBUG'] = True  # 디버그 모드 설정
