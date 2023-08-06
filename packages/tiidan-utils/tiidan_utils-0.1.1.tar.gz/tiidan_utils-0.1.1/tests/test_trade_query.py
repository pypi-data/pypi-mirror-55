import json

import pytest
from elasticsearch_dsl import Search

from tiidan_utils.trade_query.trade_search import (
    get_supplier_query,
    parse_structure,
    DomesticChineseCompany,
    UncategorizedChineseCompany,
)


@pytest.mark.parametrize(
    "supplier,expected_class",
    (
        ("ANHUI LTECH INFORMATION TECHNOLOGY CO., LTD.", DomesticChineseCompany),
        ("HARBIN TENGZHAN WOOD PRODUCTS CO.,LTD", DomesticChineseCompany),
        ("Anhui technology import export", DomesticChineseCompany),
        ("China Guoxin Holdings Co., Ltd.", UncategorizedChineseCompany),
        ("China Guoxin Holdings Co., Ltd.", UncategorizedChineseCompany),
        ("DaLian YiLian Trade Co.Ltd", DomesticChineseCompany),
        ("Nanjing Co Energy Optical Crystal Co Ltd ", DomesticChineseCompany),
        ("Zhejiang Ziguang Materials Trading Co ", DomesticChineseCompany),
        ("SHENZHEN COREPIN MOULD CO LTD", DomesticChineseCompany),
    ),
)
def test_parse_structure(supplier, expected_class):
    print("supplier: ", supplier)
    res = parse_structure(supplier)
    assert res is not None
    assert isinstance(res, expected_class)
    if expected_class == DomesticChineseCompany:
        print(res.location)
        print(res.rest)
        print(res.type)


@pytest.mark.parametrize(
    "supplier, field",
    (
        ("HARBIN TENGZHAN WOOD PRODUCTS CO.,LTD", "Exporter"),
        ("Anhui technology import export", "Exporter"),
        ("China Guoxin Holdings Co., Ltd.", "Exporter"),
        ("China Guoxin Holdings Co., Ltd.", "CUSTOM_FIELD"),
        ("DaLian YiLian Trade Co.Ltd", "Exporter"),
        ("Nanjing Co Energy Optical Crystal Co Ltd ", "Exporter"),
    ),
)
def test_trade_query(supplier, field):
    print("supplier: ", supplier)
    res = get_supplier_query(supplier, field)
    assert res is not None
    print(f"result: {res}")
    print("-----------------------------")


def parse_supplier(supplier):
    print("supplier: ", supplier)
    q = parse_structure(supplier)
    print(q)
    print("-----------------------------")


@pytest.mark.skip
def test_parse_co_ltd():
    q = parse_structure("HARBIN TENGZHAN WOOD PRODUCTS CO.,LTD")
    print(q.to_dict())


@pytest.mark.skip
def test_parse_conbest():
    q = parse_structure("Gansu Conbest Biotech Co., Ltd.")
    print(q.to_dict())


@pytest.mark.skip
def test_parse_lideer():
    q = parse_structure(" Jiangsu Lideer Pneumatic Tools Company Limited")
    print(q.to_dict())


@pytest.fixture
def elasticsearch_conn():
    from elasticsearch import Elasticsearch
    from elasticsearch_dsl import connections

    with open("secrets/elasticsearch_prod.json") as f:
        elasticsearch_config = json.load(f)
    client = Elasticsearch(
        **elasticsearch_config, verify_certs=False, use_ssl=True, timeout=120
    )
    connections.add_connection("default", client)


@pytest.mark.parametrize(
    "supplier,shipments",
    (
        ("HARBIN TENGZHAN WOOD PRODUCTS CO.,LTD", 1),
        ("Anhui technology import export", 1),
        ("China Guoxin Holdings Co., Ltd.", 0),
        ("DaLian YiLian Trade Co.Ltd", 0),
        ("Nanjing Co Energy Optical Crystal Co Ltd", 1),
    ),
)
def test_real_search(supplier, shipments, elasticsearch_conn):
    res = (
        Search(index="consolidated_trade")
        .from_dict(get_supplier_query(supplier))
        .execute()
    )
    assert res.hits.total >= shipments
