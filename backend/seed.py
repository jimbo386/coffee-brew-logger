"""Seed the Postgres DB from data/brews.csv

Usage:
  python backend/seed.py --input data/brews.csv
"""
import argparse
import csv
from sqlmodel import Session
from .db import engine
from .models import Brew
import datetime


def seed(path):
    with Session(engine) as session:
        with open(path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # convert types
                b = Brew(
                    id=row.get('id') or None,
                    timestamp=row.get('timestamp') or datetime.datetime.utcnow(),
                    bean_variety=row.get('bean_variety'),
                    fermentation=row.get('fermentation'),
                    origin_country=row.get('origin_country'),
                    region=row.get('region'),
                    altitude_m=int(row['altitude_m']) if row.get('altitude_m') else None,
                    roast_level=row.get('roast_level'),
                    grind_size_microns=int(row['grind_size_microns']) if row.get('grind_size_microns') else None,
                    coffee_weight_g=float(row['coffee_weight_g']) if row.get('coffee_weight_g') else None,
                    water_weight_g=float(row['water_weight_g']) if row.get('water_weight_g') else None,
                    brew_method=row.get('brew_method'),
                    water_temp_c=float(row['water_temp_c']) if row.get('water_temp_c') else None,
                    pours_json=row.get('pours_json'),
                    total_time_s=float(row['total_time_s']) if row.get('total_time_s') else None,
                    aroma_rating=float(row['aroma_rating']) if row.get('aroma_rating') else None,
                    taste_rating=float(row['taste_rating']) if row.get('taste_rating') else None,
                    descriptors=row.get('descriptors'),
                    notes=row.get('notes')
                )
                session.add(b)
        session.commit()
    print("Seeding complete.")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', default='data/brews.csv')
    args = parser.parse_args()
    seed(args.input)
