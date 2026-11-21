"""MN-TSM-CRY-002: Donchian breakout 55/20 on BTC, long only (classic Turtle rules). Reference implementation.

Licence: MIT (this file). Research example, not investment advice: a call to test a verification pipeline,
not a call to trade or a promise of profit. Simulated results do not predict future returns.

Two interfaces, the same rule:
* ``signal(df)`` for ``monte-neo verify``: one position per bar (0 or 1) from daily OHLCV.
* ``target_weights(closes_by_symbol)`` for ``monte-neo deploy``: the share of capital to hold now.
"""

import numpy as np
import pandas as pd

SYMBOL = "BTCUSDT"
ENTRY, EXIT = 55, 20


def _state(close: pd.Series, entry: int = ENTRY, exit: int = EXIT) -> pd.Series:
    up = close > close.shift(1).rolling(entry).max()
    down = close < close.shift(1).rolling(exit).min()
    state = pd.Series(np.nan, index=close.index)
    state[up] = 1.0
    state[down & ~up] = 0.0
    return state.ffill().fillna(0.0)


def signal(df: pd.DataFrame, entry: int = ENTRY, exit: int = EXIT) -> np.ndarray:
    """Long after a close above the prior ``entry``-bar high; flat after a close below the prior ``exit``-bar low."""
    return _state(df["close"], entry, exit).to_numpy()


def target_weights(closes_by_symbol: dict) -> dict:
    """All capital in BTC while the breakout state is long, else cash."""
    closes = pd.Series(closes_by_symbol[SYMBOL], dtype=float)
    return {SYMBOL: float(_state(closes).iloc[-1])}
