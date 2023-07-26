from typing import List

from pydantic import BaseModel


class ActionIgnore(BaseModel):
    reason: str


class ActionHighRisk(BaseModel):
    reason: str
    affected_networks: List[str]


class ActionLowRisk(BaseModel):
    reason: str
    affected_networks: List[str]


class ActionOpportunity(BaseModel):
    reason: str
    affected_networks: List[str]


class ActionAddToWatchList(BaseModel):
    reason: str
    affected_networks: List[str]
    recheck_in_hours: int


class ActionMoreInfo(BaseModel):
    pass
