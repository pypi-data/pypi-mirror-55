import json
import logging
import re
from contextlib import contextmanager
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from werkzeug.exceptions import Forbidden
from ..crypto import sha256_base64
from .models import *

log = logging.getLogger(__name__)


class QuotaReachedException(Exception):
    def __init__(self, user):
        super().__init__(f"reached maximum quota for user: {user}")


def session_scope_factory(Session):
    def session_scope():
        """Provide a transactional scope around a series of operations."""
        session = Session()
        try:
            yield session
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

    return contextmanager(session_scope)


class QuotaManager:
    def __init__(self, db_url=None):
        self.config = []
        self.Session = sessionmaker(create_engine(db_url))
        self.session_scope = session_scope_factory(self.Session)
        self.remaining_quota = None
        self.company_id = None

    @property
    def remaining(self):
        if self.remaining_quota is None:
            with self.session_scope() as session:
                usage = (
                    session.query(Usage).filter_by(COMPANY_ID=self.company_id).count()
                )
                quota = session.query(Quota).get(self.company_id)
                self.remaining_quota = quota.QUOTA - usage
        return self.remaining_quota

    def add(self, path, methods):
        self.config.append({"path": path, "methods": methods})

    def manage_quota(self, request):
        api_key = request.headers.get("X-Api-Key")
        if api_key is None:
            raise Forbidden("Missing api key")
        request_path = request.path
        hash_res = sha256_base64(api_key)
        with self.session_scope() as session:
            api_key = session.query(ApiKey).get(hash_res)
            if api_key is None:
                raise Forbidden("The API key provided does not exist")
            self.company_id = api_key.COMPANY_ID
            for conf in self.config:
                path, methods = conf["path"], conf["methods"]
                if re.match(path, request_path) and request.method in methods:
                    usage = (
                        session.query(Usage)
                        .filter_by(COMPANY_ID=api_key.COMPANY_ID)
                        .count()
                    )
                    quota = session.query(Quota).get(api_key.COMPANY_ID)
                    if usage >= quota.QUOTA:
                        raise Forbidden(
                            "You have reached your quota maximum. Please renew."
                        )
                    body = request.json
                    session.add(
                        Usage(
                            COMPANY_ID=api_key.COMPANY_ID,
                            PATH=request_path,
                            BODY=json.dumps(body),
                        )
                    )
                    self.remaining_quota = quota.QUOTA - usage
            return api_key.COMPANY_ID
