from typing import Any

from check_private_ci_is_blocked import is_private_ci_blocked

_SEPTEMBER = "2026-09-01T00:00:00Z"
_OCTOBER = "2026-10-01T00:00:00Z"


def _usage(*items: dict[str, Any]) -> dict[str, Any]:
    return {"usageItems": list(items)}


def _item(*, sku: str, quantity: float, date: str, net_amount: float = 0, unit: str = "Minutes") -> dict[str, Any]:
    return {"date": date, "product": "actions", "unitType": unit, "sku": sku, "quantity": quantity, "netAmount": net_amount}


def test_october_2026_was_blocked_by_septembers_unpaid_storage_with_minutes_to_spare() -> None:
    # The org's billing on 2026-10-20, as the API returned it: October at 1,354 Linux + 63 macOS x10 = 1,984 of 2,000 minutes and nothing charged, September owing $0.018 for storage; GitHub refused every job, "recent account payments have failed".
    usage = _usage(
        _item(sku="Actions Linux", quantity=1053, date=_SEPTEMBER),
        _item(sku="Actions macOS 3-core", quantity=64, date=_SEPTEMBER),
        _item(sku="Actions storage", quantity=54.87, net_amount=0.018437098, unit="GigabyteHours", date=_SEPTEMBER),
        _item(sku="Actions Linux", quantity=1354, date=_OCTOBER),
        _item(sku="Actions macOS 3-core", quantity=63, date=_OCTOBER),
        _item(sku="Actions storage", quantity=59.75, unit="GigabyteHours", date=_OCTOBER),
    )
    assert is_private_ci_blocked(usage=usage) is True


def test_minutes_past_the_allowance_block_with_nothing_charged() -> None:
    # macOS is weighted x10: 150 macOS = 1500, plus 600 Linux = 2100 >= 2000.
    usage = _usage(
        _item(sku="Actions macOS 3-core", quantity=150, date=_OCTOBER),
        _item(sku="Actions Linux", quantity=600, date=_OCTOBER),
    )
    assert is_private_ci_blocked(usage=usage) is True


def test_minutes_left_and_nothing_charged_runs_private() -> None:
    usage = _usage(
        _item(sku="Actions Linux", quantity=900, date=_SEPTEMBER),
        _item(sku="Actions Linux", quantity=500, date=_OCTOBER),
        _item(sku="Actions macOS 3-core", quantity=100, date=_OCTOBER),
    )
    assert is_private_ci_blocked(usage=usage) is False


def test_last_months_minutes_do_not_count_against_this_month() -> None:
    usage = _usage(
        _item(sku="Actions macOS 3-core", quantity=500, date=_SEPTEMBER),
        _item(sku="Actions Linux", quantity=100, date=_OCTOBER),
    )
    assert is_private_ci_blocked(usage=usage) is False
