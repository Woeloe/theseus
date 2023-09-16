import os
import json
import random
from pathlib import Path

from flask import Flask, request, abort
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# ============================================================
# ===== LEVEL ROUTING ========================================
# ============================================================

@app.route('/levels')
def fetch_levels():
    if request.method == 'GET':
        count = 0
        for path in os.listdir("levels"):

            if os.path.isfile(os.path.join("levels", path)):
                count += 1
        data = {
            "aantal_levels": count
        }
        return data

@app.route('/level/<int:level>')
def fetch_level(level: int):
    if request.method == 'GET':
        path = Path('levels/level' + str(level) + '.json')

        if path.is_file():
            with open(path) as f:
                data = json.load(f)
        else:
            data = {
                "foutboodschap": "Puzzel " + str(level) + " bestaat niet."
            }
        return data


@app.route('/random_level')
def fetch_random_level():
    level = random.randint(1, fetch_levels().get("aantal_levels"))


    path = Path('levels/level' + str(level) + '.json')
    if path.is_file():
        with open(path) as f:
            data = json.load(f)

    if "highscore" in data:
        highscore = data.get("highscore")
    else:
        highscore = -1



    data = {
        "level": level,
        "game": {},
        "highscore": highscore
    }

    return data

# ============================================================
# ===== HIGHSCORE ROUTING ====================================
# ============================================================

@app.route('/highscore/<int:level>', methods = ['POST'])
def update_highscore(level: int):
    raise NotImplementedError

if __name__ == '__main__':
    app.run(port=3000, debug=True)
