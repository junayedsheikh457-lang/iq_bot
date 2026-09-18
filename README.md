# IQ Bot

XAUUSD 1-minute breakout strategy engine with paper/demo execution.

## Strategy
- Instrument: XAUUSD
- Timeframe: 1 minute
- Close below previous support -> SELL
- Close above previous resistance -> BUY
- Stake sequence: $1, $2, $4.5, $10, $21.5, $45, $100
- A winning trade stops the current cycle.
- The next fresh signal starts a new cycle at $1.
- Seven consecutive losses stop the cycle for safety.

## Important
This repository is configured for PAPER/DEMO execution. It does not contain an unofficial/private IQ Option order-placement client. Connect a real-money execution adapter only through an officially supported API/integration, after checking the broker's current terms and API availability.

## Run
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py