import json
from pathlib import Path

from money_manager import MoneyManager
from paper_broker import PaperBroker
from strategy import breakout_signal

def load_config() -> dict:
    return json.loads(Path('config.json').read_text(encoding='utf-8'))

def demo() -> None:
    cfg = load_config()
    manager = MoneyManager([float(x) for x in cfg['stakes']], int(cfg['max_consecutive_losses']))
    broker = PaperBroker()
    closes = [2350.0,2351.0,2349.5,2352.0,2351.5,2353.0,2352.2,2354.0,2353.6,2355.0,2354.2,2356.0,2355.4,2357.0,2356.3,2358.0,2357.2,2359.0,2358.1,2360.0,2359.0,2361.0]
    signal = breakout_signal(closes, int(cfg['lookback']))
    if signal is None:
        print('No breakout signal.')
        return
    if not manager.active:
        manager.new_signal_cycle()
    trade = broker.place(signal.side, manager.current_stake, signal.price)
    print(f'Signal: {signal.side}')
    print(f'Entry: {signal.price}')
    print(f'Support: {signal.support}')
    print(f'Resistance: {signal.resistance}')
    print(f'Paper stake: ${trade.stake:g}')
    print('Trade is PAPER/DEMO only.')

if __name__ == '__main__':
    demo()
