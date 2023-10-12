from app_etl.gateway.global_health_data import retrieve_indicator_data


def test_correctly_retrieves_data():
    source_data = retrieve_indicator_data("MALARIA_CONF_CASES")
    assert len(source_data) > 0
