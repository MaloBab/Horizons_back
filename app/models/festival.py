from sqlalchemy import Column, String, Integer, Date
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import text

from .base import Base

class Festival(Base):
    __tablename__ = "festival"

    id = Column(UUID(as_uuid=True), primary_key=True, server_default=text("gen_random_uuid()"))
    
    name = Column(String, nullable=False)                    
    edition = Column(Integer, nullable=False)                 

    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)


    # Lieu
    location_name = Column(String, nullable=False)            
    location_city = Column(String, nullable=False)