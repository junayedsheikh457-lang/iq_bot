from dataclasses import dataclass
from typing import Optional, Sequence

@dataclass(frozen=True)
class Signal:
    side: str
    support: float
    resistance: float
    price: float

def breakout_signal(closes: Sequence[float], lookback: int = 20) -> Optional[Signal]:
    if len(closes) < lookback + 1:
        return None
    previous = closes[-lookback - 1:-1]
    price = float(closes[-1])
    support = min(previous)
    resistance = max(previous)
    if price < support:
        return Signal('SELL', support, resistance, price)
    if price > resistance:
        return Signal('BUY', support, resistance, price)
    return None
