from sqlalchemy import Column, BigInteger, String, JSON, TIMESTAMP, text, Integer

from tiidan_utils.quota_manager.models import Base


class Usage(Base):
    __tablename__ = "api_usage"

    ID = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    COMPANY_ID = Column(BigInteger, nullable=False)
    PATH = Column(String(256), nullable=False)
    BODY = Column(JSON)
    created_at = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
