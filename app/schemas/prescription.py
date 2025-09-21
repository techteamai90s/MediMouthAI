from pydantic import BaseModel
from typing import List, Optional

class MedicineDetails(BaseModel):
    name: str
    usage: Optional[str] = None
    side_effects: Optional[str] = None

class PrescriptionResponse(BaseModel):
    medicines: List[MedicineDetails]