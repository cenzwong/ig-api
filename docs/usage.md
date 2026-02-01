# Usage

## Installation

Make sure you have `uv` installed.

```bash
uv sync
```

## Basic Connection

To connect to the IG API, use the `IGClient`:

```python
from ig_api import IGClient

client = IGClient()
session = client.connect()
print(f"Connected to account: {session['account_id']}")
```

## Environment Variables

The client looks for the following in a `.env` file:

- `IG_API_KEY`
- `IG_USERNAME`
- `IG_PASSWORD`
- `IG_ENV` (defaults to `demo`)
