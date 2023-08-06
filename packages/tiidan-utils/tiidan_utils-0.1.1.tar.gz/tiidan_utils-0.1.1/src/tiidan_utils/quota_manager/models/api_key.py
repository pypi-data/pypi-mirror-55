from sqlalchemy import TIMESTAMP, Column, BigInteger, String, text

from tiidan_utils.quota_manager.models import Base


class ApiKey(Base):
    __tablename__ = "api_key"

    API_HASH = Column(String(44), primary_key=True)
    COMPANY_ID = Column(BigInteger, nullable=False)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
