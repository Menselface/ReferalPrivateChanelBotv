from pydantic import BaseModel
from typing import Optional

class InvoiceCreateDTO(BaseModel):
    user_id: int
    order_id: str
    status: Optional[str]
    amount: float
    currency: Optional[str]
    payer_email: Optional[str]
