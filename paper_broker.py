from dataclasses import dataclass
from datetime import datetime, timezone

@dataclass
class PaperTrade:
    trade_id: int
    side: str
    stake: float
    entry: float
    opened_at: str
    exit: float | None = None
    pnl: float | None = None

class PaperBroker:
    def __init__(self) -> None:
        self._next_id = 1
        self.open_trade: PaperTrade | None = None
        self.history: list[PaperTrade] = []

    def place(self, side: str, stake: float, price: float) -> PaperTrade:
        if self.open_trade is not None:
            raise RuntimeError('A paper trade is already open.')
        trade = PaperTrade(self._next_id, side, stake, float(price), datetime.now(timezone.utc).isoformat())
        self._next_id += 1
        self.open_trade = trade
        return trade

    def close(self, price: float, payout: float = 0.0, won: bool | None = None) -> PaperTrade:
        if self.open_trade is None:
            raise RuntimeError('No open paper trade.')
        trade = self.open_trade
        trade.exit = float(price)
        if won is None:
            won = (trade.side == 'BUY' and trade.exit > trade.entry) or (trade.side == 'SELL' and trade.exit < trade.entry)
        trade.pnl = trade.stake * payout if won else -trade.stake
        self.history.append(trade)
        self.open_trade = None
        return trade
