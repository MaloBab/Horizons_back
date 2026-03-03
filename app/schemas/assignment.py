from pydantic import BaseModel, ConfigDict
from uuid import UUID
from .job import JobResponse
from .volunteer import VolunteerShortResponse 

class AssignmentBase(BaseModel):
    pass

class AssignmentCreate(AssignmentBase):
    volunteer_id: UUID
    job_id: int

class AssignmentResponse(AssignmentBase):
    id: int
    job_id: int
    volunteer: VolunteerShortResponse
    job: JobResponse

    model_config = ConfigDict(from_attributes=True)