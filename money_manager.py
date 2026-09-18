from dataclasses import dataclass

@dataclass
class MoneyManager:
    stakes: list[float]
    max_consecutive_losses: int = 7
    index: int = 0
    consecutive_losses: int = 0
    active: bool = True

    @property
    def current_stake(self) -> float:
        return self.stakes[self.index]

    def on_win(self) -> None:
        self.active = False

    def on_loss(self) -> None:
        self.consecutive_losses += 1
        if self.consecutive_losses >= self.max_consecutive_losses:
            self.active = False
            return
        if self.index < len(self.stakes) - 1:
            self.index += 1
        else:
            self.active = False

    def new_signal_cycle(self) -> None:
        if not self.active:
            self.index = 0
            self.consecutive_losses = 0
            self.active = True
