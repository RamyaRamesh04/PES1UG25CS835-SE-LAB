import pytest
from house_painting_quote import painting_quote, paint_litres, crew_days


# painting_quote: paint validation and job validation

def test_unknown_paint_branch():
    with pytest.raises(ValueError, match="unknown paint"):
        painting_quote("primer", 100, 1, False)


def test_valid_paint_branch():
    assert painting_quote("emulsion", 300, 1, False) == 6000


def test_invalid_area_branch():
    with pytest.raises(ValueError, match="invalid job"):
        painting_quote("emulsion", -1, 1, False)


def test_invalid_coats_branch():
    with pytest.raises(ValueError, match="invalid job"):
        painting_quote("emulsion", 100, 0, False)


def test_interior_distemper_allowed():
    assert painting_quote("distemper", 100, 1, False) == 5000


def test_exterior_distemper_rejected():
    with pytest.raises(ValueError, match="distemper is for interiors only"):
        painting_quote("distemper", 100, 1, True)


def test_exterior_other_paint_allowed():
    assert painting_quote("enamel", 500, 2, True) == 32500


def test_interior_has_no_exterior_charge():
    assert painting_quote("emulsion", 300, 1, False) == 6000


def test_large_area_discount_applied():
    assert painting_quote("emulsion", 2500, 1, False) == 45000


def test_no_large_area_discount():
    assert painting_quote("emulsion", 300, 1, False) == 6000


def test_minimum_quote_applied():
    assert painting_quote("distemper", 100, 1, False) == 5000


def test_calculated_quote_returned():
    assert painting_quote("emulsion", 300, 1, False) == 6000


# paint_litres: surface selection and rounding branches

def test_smooth_surface():
    assert paint_litres(200, 1, "smooth") == 2


def test_rough_surface():
    assert paint_litres(60, 1, "rough") == 1


def test_unknown_surface_rejected():
    with pytest.raises(ValueError, match="unknown surface"):
        paint_litres(100, 1, "uneven")


def test_exact_litre_coverage():
    assert paint_litres(200, 1, "smooth") == 2


def test_remaining_area_rounds_up():
    assert paint_litres(201, 1, "smooth") == 3


# crew_days: painter validation, rounding and wallpaper branches

def test_invalid_painter_count():
    with pytest.raises(ValueError, match="need at least one painter"):
        crew_days(500, 0, False)


def test_exact_daily_workload():
    assert crew_days(800, 2, False) == 1


def test_remaining_work_needs_another_day():
    assert crew_days(801, 2, False) == 2


def test_wallpaper_removal_adds_two_days():
    assert crew_days(800, 2, True) == 3


def test_no_wallpaper_removal():
    assert crew_days(800, 2, False) == 1