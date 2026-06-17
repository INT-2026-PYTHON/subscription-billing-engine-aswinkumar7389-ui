"""Customer dataclass. ✅ COMPLETE."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from enum import Enum

class CustomerStatus(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


@dataclass(frozen=True)
class Customer:
    id: Optional[int]
    name: str
    email: str
    country_code: str
    state_code: str = ""
    status: CustomerStatus = CustomerStatus.ACTIVE
    created_at: Optional[date] = None
