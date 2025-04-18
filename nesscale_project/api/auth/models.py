from pydantic import BaseModel, Field
from typing import Optional, List

class CreateUser(BaseModel):
    email: str 
    first_name: str 
    mobile_no: str