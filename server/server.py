from flask import Flask, request, abort
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# ============================================================
# ===== LEVEL ROUTING ========================================
# ============================================================

@app.route('/levels')
def fetch_levels():
    raise NotImplementedError

@app.route('/level/<int:level>')
def fetch_level(level: int):
    raise NotImplementedError

@app.route('/random_level')
def fetch_random_level():
    raise NotImplementedError

# ============================================================
# ===== HIGHSCORE ROUTING ====================================
# ============================================================

@app.route('/highscore/<int:level>', methods = ['POST'])
def update_highscore(level: int):
    raise NotImplementedError

if __name__ == '__main__':
    app.run(port=3000)
