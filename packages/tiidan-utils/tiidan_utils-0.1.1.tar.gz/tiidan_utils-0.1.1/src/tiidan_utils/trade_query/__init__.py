import logging
from .data import _Data
from .trade_search import get_supplier_query

log = logging.getLogger(__name__)



def lambda_handler(event, context=None):
    name = (
        event.get("name")
        or event.get("supplier")
        or event.get("englishName")
        or event.get("english")
        or event.get("english_name")
    )
    if name is None:
        raise ValueError("Please specify name")
    log.info(f"received: {name}")
    res = get_supplier_query(name)
    log.info(f"returning: {res}")
    return res
