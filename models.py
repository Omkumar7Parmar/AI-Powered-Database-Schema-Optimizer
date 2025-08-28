from pydantic import BaseModel
from typing import List, Dict, Literal

# --- Core IR (Intermediate Representation) Models ---
class Relationship(BaseModel):
    from_entity: str
    to_entity: str
    cardinality: Literal["1:1", "1:N", "N:M"]

class IR(BaseModel):
    entities: Dict[str, List[str]]
    relationships: List[Relationship]

# --- API Request Models ---
class FullProcessRequest(BaseModel):
    text: str

# --- API Response Models ---
class DDLBundle(BaseModel):
    tables: List[str]
    junctions: List[str]
    foreign_keys: List[str]
    plan_id: str