import pytest
from house_painting_quote import painting_quote, paint_litres, crew_days


def test_unknown_paint():
    with pytest.raises(ValueError, match="unknown paint"):
        painting_quote("primer", 100, 1, False)


def test_zero_area():
    with pytest.raises(ValueError, match="invalid job"):
        painting_quote("emulsion", 0, 1, False)


def test_invalid_coats():
    with pytest.raises(ValueError, match="invalid job"):
        painting_quote("emulsion", 100, 0, False)


def test_exterior_distemper():
    with pytest.raises(ValueError, match="distemper is for interiors only"):
        painting_quote("distemper", 100, 1, True)


def test_low_cost_minimum_quote():
    assert painting_quote("distemper", 100, 1, False) == 5000


def test_regular_interior_quote():
    assert painting_quote("emulsion", 300, 1, False) == 6000


def test_exterior_extra_cost():
    assert painting_quote("enamel", 500, 2, True) == 32500


def test_large_area_discount():
    assert painting_quote("emulsion", 2500, 1, False) == 45000


def test_smooth_exact_coverage():
    assert paint_litres(200, 1, "smooth") == 2


def test_smooth_rounds_up():
    assert paint_litres(201, 1, "smooth") == 3


def test_rough_exact_coverage():
    assert paint_litres(60, 1, "rough") == 1


def test_rough_rounds_up():
    assert paint_litres(61, 1, "rough") == 2


def test_unknown_surface():
    with pytest.raises(ValueError, match="unknown surface"):
        paint_litres(100, 1, "uneven")


def test_zero_painters():
    with pytest.raises(ValueError, match="need at least one painter"):
        crew_days(500, 0, False)


def test_crew_exact_workload():
    assert crew_days(800, 2, False) == 1


def test_crew_rounds_up_days():
    assert crew_days(801, 2, False) == 2


def test_wallpaper_removal_adds_days():
    assert crew_days(800, 2, True) == 3