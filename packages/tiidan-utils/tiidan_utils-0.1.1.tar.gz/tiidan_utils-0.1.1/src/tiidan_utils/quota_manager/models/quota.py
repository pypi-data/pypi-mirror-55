from sqlalchemy import TIMESTAMP, Column, BigInteger, text, Integer
from tiidan_utils.quota_manager.models import Base


class Quota(Base):
    __tablename__ = "api_quota"

    COMPANY_ID = Column(BigInteger, primary_key=True)
    QUOTA = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    updated_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
