from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class Mamberlist(BaseModel):
    user : str
    role : str

class CreateProjectDetails(BaseModel):
    project_name: str
    project_manager: str
    description: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    members: List[Mamberlist]

class GetProjectList(BaseModel):
    filters: Optional[List] = []
    start: Optional[int] = 0
    page_length: Optional[int] = 20 
    
class GetProjectByID(BaseModel):
    name : str

class UpdateProjectDetails(BaseModel):
    name: str
    project_name: str
    project_manager: str
    description: Optional[str] = None
    start_date: Optional[str] = None
    end_date: Optional[str] = None
    members: List[Mamberlist]
    
