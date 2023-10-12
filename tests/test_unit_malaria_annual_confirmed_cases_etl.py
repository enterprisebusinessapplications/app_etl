from unittest.mock import Mock


def test_correctly_transforms_empty_data():
    """
    malariaannualconfirmedcasesrepository = Mock()
    etl = MalariaAnnualConfirmedCasesETL(malariaannualconfirmedcasesrepository)

    etl_id = 67
    source_data = []

    assert source_data == etl.transform(source_data, etl_id)
    """
