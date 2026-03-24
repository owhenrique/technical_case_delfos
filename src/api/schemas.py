from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class DataFonteResponse(BaseModel):
    timestamp: datetime
    wind_speed: Optional[float] = None
    power: Optional[float] = None
    ambient_temperature: Optional[float] = None

    model_config = ConfigDict(from_attributes=True)
