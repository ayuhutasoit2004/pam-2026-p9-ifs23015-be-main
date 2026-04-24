from sqlalchemy import Column, Integer, Text, String, DateTime
from datetime import datetime, timezone
from app.extensions import Base

class Tree(Base):
    __tablename__ = "trees"

    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    description = Column(Text)
    facts = Column(Text)
    benefits = Column(Text)
    type = Column(String(50))  # 'generate' or 'identify'
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
