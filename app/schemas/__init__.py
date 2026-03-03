# app/schemas/__init__.py

from .user import UserCreate, UserResponse, UserRole, UserBase, UserShortResponse
from .activity import ActivityCreate, ActivityResponse, ActivityBase
from .category import CategoryCreate, CategoryResponse, CategoryBase
from .slot import SlotCreate, SlotResponse, SlotBase
from .preference import PreferenceCreate, PreferenceResponse, PreferenceBase
from .job import JobCreate, JobResponse, JobBase

# Liaison - On les met ici car ils dépendent des schémas ci-dessus
from .volunteer_mate import VolunteerMateCreate, VolunteerMateResponse, VolunteerMateBase
from .volunteer_preference import VolunteerPreferenceCreate, VolunteerPreferenceResponse, VolunteerPreferenceBase
from .volunteer_slot import VolunteerSlotCreate, VolunteerSlotResponse, VolunteerSlotBase

# Le schéma Volunteer (qui utilise les liaisons)
from .volunteer import VolunteerCreate, VolunteerResponse, VolunteerBase, VolunteerShortResponse

# L'affectation finale
from .assignment import AssignmentCreate, AssignmentResponse, AssignmentBase

__all__ = [
    "UserCreate", "UserResponse", "UserRole", "UserBase", "UserShortResponse",
    "ActivityCreate", "ActivityResponse", "ActivityBase",
    "VolunteerCreate", "VolunteerResponse", "VolunteerBase", "VolunteerShortResponse",
    "CategoryCreate", "CategoryResponse", "CategoryBase",
    "JobCreate", "JobResponse", "JobBase",
    "SlotCreate", "SlotResponse", "SlotBase",
    "PreferenceCreate", "PreferenceResponse", "PreferenceBase",
    "VolunteerMateCreate", "VolunteerMateResponse", "VolunteerMateBase",
    "VolunteerPreferenceCreate", "VolunteerPreferenceResponse", "VolunteerPreferenceBase",
    "VolunteerSlotCreate", "VolunteerSlotResponse", "VolunteerSlotBase",
    "AssignmentCreate", "AssignmentResponse", "AssignmentBase",
]