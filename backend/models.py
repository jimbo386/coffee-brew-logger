from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime

class Brew(SQLModel, table=True):
    id: Optional[str] = Field(default=None, primary_key=True)
    timestamp: Optional[datetime] = None
    bean_variety: Optional[str] = None
    fermentation: Optional[str] = None
    origin_country: Optional[str] = None
    region: Optional[str] = None
    altitude_m: Optional[int] = None
    roast_level: Optional[str] = None
    grind_size_microns: Optional[int] = None
    coffee_weight_g: Optional[float] = None
    water_weight_g: Optional[float] = None
    brew_method: Optional[str] = None
    water_temp_c: Optional[float] = None
    pours_json: Optional[str] = None
    total_time_s: Optional[float] = None
    aroma_rating: Optional[float] = None
    taste_rating: Optional[float] = None
    descriptors: Optional[str] = None
    notes: Optional[str] = None


class BrewCreate(SQLModel):
    bean_variety: Optional[str] = None
    fermentation: Optional[str] = None
    origin_country: Optional[str] = None
    region: Optional[str] = None
    altitude_m: Optional[int] = None
    roast_level: Optional[str] = None
    grind_size_microns: Optional[int] = None
    coffee_weight_g: float
    water_weight_g: float
    brew_method: str
    water_temp_c: float
    pours_json: Optional[str] = None
    total_time_s: Optional[float] = None
    aroma_rating: Optional[float] = None
    taste_rating: Optional[float] = None
    descriptors: Optional[str] = None
    notes: Optional[str] = None
