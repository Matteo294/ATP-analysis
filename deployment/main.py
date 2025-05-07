from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import sqlite3
import pickle
import pandas as pd
import numpy as np
app = FastAPI()

DB_PATH = "../data.db"

def get_stats(player_name: str, year: int):
    try:
        conn = sqlite3.connect(DB_PATH)
        cur = conn.cursor()
        cmd = f"SELECT COUNT(*) FROM {player_name} WHERE win='yes' and tourney_date LIKE '" + str(year) + "%';" # count wins
        cur.execute(cmd)
        w = cur.fetchone()[0]
        cmd = f"SELECT COUNT(*) FROM {player_name} WHERE win='no' and tourney_date LIKE '" + str(year) + "%';" # count losses
        cur.execute(cmd)
        l = cur.fetchone()[0]
        wr = w/(w+l) * 100
        return {"matches": w + l, "wins": w, "win_rate": wr}
    except sqlite3.OperationalError:
        raise HTTPException(status_code=404, detail="Tennista non trovato nel database.")
    finally:
        conn.close()

@app.get("/stats")
def read_player_stats(player: str, year: int):
    stats = get_stats(player, year)
    return {"player": player, "year": year, "stats": stats}

@app.get("/predict")
def predict_match(opponent: str, tournament: str):
    # load
    with open('../MLmodel/model.pkl', 'rb') as f:
        pipeline = pickle.load(f)
    X = pd.DataFrame(columns=['opponent', 'tournament'])
    X.loc[0] = [opponent, tournament]
    for feature in pipeline.feature_names_in_:
        if feature not in X.columns:
            X[feature] = np.nan

    # predict
    try:
        y_pred = pipeline.predict(X)[0]
        y_proba = pipeline.predict_proba(X)[0][1]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")
    # return
    if y_pred == 1:
        return {"prediction": "yes", "probability": y_proba}
    else:
        return {"prediction": "no", "probability": 1 - y_proba}