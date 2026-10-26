"""El cargador de Yelp debe encontrar el CSV incluido en data/raw."""
from src.data.loaders import YelpDataLoader


def test_yelp_loader_reads_bundled_raw_file():
    df = YelpDataLoader().load_from_external()
    assert len(df) > 0
    assert {"name", "rating", "city"}.issubset(df.columns)
