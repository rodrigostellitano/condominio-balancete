from dataclasses import dataclass
from typing import Dict, List
import pandas as pd





@dataclass
class EntranceResult:
    previous_value: float
    current_month: str
    total: float
    details: Dict


@dataclass
class ExitResult:
    total: float
    details: Dict


@dataclass
class DebitResult:
    houses_debit: List[str]
    total_houses_debit: int


@dataclass
class Balancete:
    date_info: Dict
    previous_value: float
    total_entrance: float
    total_exit: float
    total_final: float
    people: Dict
    houses_debit: List[str]
