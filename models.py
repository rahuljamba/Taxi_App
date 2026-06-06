from sqlalchemy import Column, Integer, String, Boolean
from database import Base

class DBUser(Base):
    __tablename__ = "rapido_users"  # Database table ka naam clean rakho

    id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, nullable=False)
    country_code = Column(String)  # Unique hata diya kyunki country code sabka same ho sakta hai (+91)
    mobile_number = Column(String, unique=True, index=True)  # Mobile number unique hona chahiye
    email = Column(String, unique=True, index=True)          # Email unique hona chahiye
    password = Column(String, nullable=False)
    isClassMonitor = Column(Boolean, default=False)