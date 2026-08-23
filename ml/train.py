#!/usr/bin/env python3
"""
Train a LightGBM regressor on synthetic brews CSV and produce suggestions.

Usage:
 python ml/train.py --input data/brews.csv --output data/suggestions.json --n_suggestions 6
"""
import argparse
import json
from pathlib import Path
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
import lightgbm as lgb
from skopt import gp_minimize
from skopt.space import Real
import joblib


def load_data(path):
    df = pd.read_csv(path)
    # basic preprocessing
    df = df.dropna(subset=["taste_rating"])
    # parse descriptors into list (semi-colon separated)
    df["descriptor_count"] = df["descriptors"].fillna("").apply(lambda s: 0 if s=="" else len(str(s).split(";")))
    return df

def featurize(df):
    # pick a small set of simple features for demo
    X = df[["coffee_weight_g","water_weight_g","water_temp_c","grind_size_microns","altitude_m","brew_method","roast_level"]].copy()
    # categorical one-hot for brew_method + roast_level
    cat_cols = ["brew_method","roast_level"]
    X_cat = pd.get_dummies(X[cat_cols].fillna("NA"))
    X = pd.concat([X.drop(columns=cat_cols).astype(float).fillna(0), X_cat.astype(float)], axis=1)
    return X

def train_model(X, y):
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    lgb_train = lgb.Dataset(X_train, y_train)
    params = {"objective":"regression", "metric":"l2", "verbosity":-1}
    model = lgb.train(params, lgb_train, num_boost_round=200)
    preds = model.predict(X_test)
    mse = np.mean((preds - y_test)**2)
    print("Test MSE:", mse)
    return model, X

def optimize(model, X, n_calls=25):
    # For demo optimize coffee_weight_g (12..24) and water_temp_c (85..98)
    def objective(vals):
        coffee_w, temp = vals
        # construct median feature vector and replace these values
        base = X.median().to_dict()
        base["coffee_weight_g"] = coffee_w
        base["water_temp_c"] = temp
        # if model expects grind_size or water_weight, keep median
        row = pd.DataFrame([base])[X.columns]
        pred = model.predict(row)[0]
        return -pred  # maximize predicted taste

    space = [Real(12.0, 24.0, name="coffee_weight_g"), Real(85.0, 98.0, name="water_temp_c")]
    res = gp_minimize(objective, space, n_calls=n_calls, random_state=0)
    suggestions = []
    for rank, (cw, t) in enumerate([res.x_iters[i] for i in np.argsort(res.func_vals)[:6]]):
        suggestions.append({
            "coffee_weight_g": round(cw,2),
            "water_temp_c": round(t,2),
            "predicted_score": float(-res.func_vals[np.argsort(res.func_vals)[rank]])
        })
    return suggestions

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=str, default="data/brews.csv")
    parser.add_argument("--output", type=str, default="data/suggestions.json")
    parser.add_argument("--model-out", type=str, default="data/model.joblib")
    parser.add_argument("--n_suggestions", type=int, default=6)
    args = parser.parse_args()

    Path("data").mkdir(exist_ok=True)
    df = load_data(args.input)
    y = df["taste_rating"].astype(float)
    X = featurize(df)

    model, X_full = train_model(X, y)

    print("Top feature importances:")
    imps = model.feature_importance()
    features = X_full.columns.tolist()
    impdf = pd.Series(imps, index=features).sort_values(ascending=False)
    print(impdf.head(20).to_string())

    # save model
    joblib.dump(model, args.model_out)
    print("Model saved to", args.model_out)

    # optimize
    suggestions = optimize(model, X_full, n_calls=30)
    out = {"suggestions": suggestions, "meta": {"n_train": len(df)}}
    with open(args.output, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)
    print("Wrote suggestions to", args.output)

if __name__ == "__main__":
    main()
