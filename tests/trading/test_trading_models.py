from alpaca.trading.enums import OrderSide, OrderType, TimeInForce
from alpaca.trading.requests import (
    MarketOrderRequest,
    TrailingStopOrderRequest,
    LimitOrderRequest,
)
import pytest


def test_has_qty_or_notional_but_not_both():
    with pytest.raises(ValueError) as e:
        MarketOrderRequest(
            symbol="SPY",
            side=OrderSide.BUY,
            time_in_force=TimeInForce.DAY,
        )

    assert "At least one of qty or notional must be provided" in str(e.value)

    with pytest.raises(ValueError) as e:
        MarketOrderRequest(
            symbol="SPY",
            side=OrderSide.BUY,
            time_in_force=TimeInForce.DAY,
            qty=5,
            notional=5,
        )

    assert "Both qty and notional can not be set." in str(e.value)


def test_notional_works():
    mo = MarketOrderRequest(
        symbol="SPY",
        side=OrderSide.BUY,
        time_in_force=TimeInForce.DAY,
        notional=5,
    )

    lo = LimitOrderRequest(
        symbol="BTC/USD",
        side=OrderSide.BUY,
        limit_price=5,
        time_in_force=TimeInForce.DAY,
        notional=50,
    )

    assert mo.type == OrderType.MARKET

    assert lo.type == OrderType.LIMIT


def test_trailing_stop_order_type():
    with pytest.raises(ValueError) as e:
        TrailingStopOrderRequest(
            symbol="SPY",
            side=OrderSide.BUY,
            time_in_force=TimeInForce.DAY,
            qty=1,
        )

    assert (
        "Either trail_percent or trail_price must be set for a trailing stop order."
        in str(e.value)
    )

    with pytest.raises(ValueError) as e:
        TrailingStopOrderRequest(
            symbol="SPY",
            side=OrderSide.BUY,
            time_in_force=TimeInForce.DAY,
            qty=1,
            trail_percent=2,
            trail_price=5,
        )

    assert "Both trail_percent and trail_price cannot be set." in str(e.value)
