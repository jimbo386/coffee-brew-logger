#!/usr/bin/env python3
"""
Generate synthetic brews CSV for demo.

Fields:
- id,timestamp,bean_variety,fermentation,origin_country,region,altitude_m,roast_level,
  grind_size_microns,coffee_weight_g,water_weight_g,brew_method,water_temp_c,
  pours_json,total_time_s,aroma_rating,taste_rating,descriptors,notes
"""
import csv
import uuid
import random
import datetime
import json
import argparse
from pathlib import Path

BEAN_VARIETIES = [
    "Ethiopian Yirgacheffe", "Colombian Huila", "Kenyan AA",
    "Guatemalan Antigua", "Brazil Santos", "Costa Rica Tarrazu"
]
FERMENTATIONS = ["washed", "natural", "honey", "anaerobic"]
REGIONS = ["Yirgacheffe", "Huila", "Nyeri", "Antigua", "Mogiana", "Tarrazu"]
ROAST_LEVELS = ["light", "light-medium", "medium", "city", "dark"]
BREW_METHODS = ["v60", "chemex", "aeropress", "french_press", "espresso", "kalita"]
DESCRIPTORS = ["floral", "citrus", "chocolate", "nutty", "caramel", "tea-like", "berry"]

def random_pours(method, coffee_w, water_w):
    if method in ("espresso",):
        return [{"time_s": 25, "grams": water_w}]
    if method == "french_press":
        return [{"time_s": int(random.uniform(240,300)), "grams": water_w}]
    # pour-over style
    steps = random.choice([2,3,4])
    pours = []
    remaining = water_w
    for i in range(steps):
        if i == steps-1:
            grams = remaining
        else:
            grams = int(round(water_w / steps * (0.8 + random.uniform(-0.2,0.2))))
            remaining -= grams
        pours.append({"time_s": 30*(i+1), "grams": grams})
    return pours

def flavor_score(bean, roast, grind, coffee_w, water_w, temp, altitude):
    # synthetic score mixing parameters; used to derive aroma/taste ratings
    base = {
        "Ethiopian Yirgacheffe": 0.9,
        "Colombian Huila": 0.75,
        "Kenyan AA": 0.85,
        "Guatemalan Antigua": 0.78,
        "Brazil Santos": 0.7,
        "Costa Rica Tarrazu": 0.77
    }.get(bean, 0.75)
    roast_mod = {"light": 0.05, "light-medium": 0.02, "medium": 0.0, "city": -0.03, "dark": -0.08}[roast]
    ratio = coffee_w / water_w
    ratio_pref = -abs(ratio - 0.06) * 15  # prefer ~1:16.6 = 0.06
    temp_pref = -abs(temp - 93) * 0.02
    grind_pref = -abs(grind - 600) * 0.0005  # prefer ~600 microns (medium)
    altitude_pref = (altitude - 1000)/2000
    rnd = random.uniform(-0.1, 0.1)
    score = 6.5 + base + roast_mod + ratio_pref + temp_pref + grind_pref + altitude_pref + rnd
    return max(1.0, min(10.0, score))

def generate(n=200, out="data/brews.csv"):
    Path("data").mkdir(exist_ok=True)
    with open(out, "w", newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        header = ["id","timestamp","bean_variety","fermentation","origin_country","region","altitude_m","roast_level","grind_size_microns","coffee_weight_g","water_weight_g","brew_method","water_temp_c","pours_json","total_time_s","aroma_rating","taste_rating","descriptors","notes"]
        writer.writerow(header)
        for i in range(n):
            bean = random.choice(BEAN_VARIETIES)
            fermentation = random.choice(FERMENTATIONS)
            origin = bean.split()[0]
            region = random.choice(REGIONS)
            altitude = int(random.gauss(1500, 400))
            roast = random.choice(ROAST_LEVELS)
            grind = int(random.choice([400, 500, 600, 700, 850]))  # microns
            brew_method = random.choice(BREW_METHODS)
            coffee_w = round(random.uniform(12,24),1)
            # ratio ~ 1:15 - 1:18
            ratio = random.choice([15,16,17,18])
            water_w = round(coffee_w * ratio,1)
            temp = round(random.gauss(93,2),1)
            pours = random_pours(brew_method, coffee_w, water_w)
            total_time = sum(p["time_s"] for p in pours) if pours else random.randint(120,240)
            taste = round(flavor_score(bean, roast, grind, coffee_w, water_w, temp, altitude),2)
            aroma = max(1.0, min(10.0, round(taste + random.uniform(-0.8,0.8),2)))
            descriptors = random.sample(DESCRIPTORS, k=random.choice([1,2,3]))
            notes = ""
            writer.writerow([
                str(uuid.uuid4()),
                (datetime.datetime.utcnow() - datetime.timedelta(days=random.randint(0,90))).isoformat()+"Z",
                bean, fermentation, origin, region, altitude, roast, grind, coffee_w, water_w,
                brew_method, temp, json.dumps(pours), total_time, aroma, taste, ";".join(descriptors), notes
            ])

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--n", type=int, default=300)
    parser.add_argument("--out", type=str, default="data/brews.csv")
    args = parser.parse_args()
    generate(args.n, args.out)
    print(f"Generated {args.n} synthetic brews at {args.out}")
