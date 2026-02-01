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

## Session Management

The client supports full session lifecycle management.

### Reading Session Details

```python
details = client.session.read()
print(f"Client ID: {details.get('clientId')}")
```

### Switching Accounts

You can switch to another account (e.g., from a spread betting to a CFD account):

```python
client.session.switch_account("NEW_ACCOUNT_ID")
```

## Accounts Service

Retrieve a list of all accounts belonging to the client:

```python
accounts_data = client.accounts.get_accounts()
for account in accounts_data['accounts']:
    print(account['accountId'])
```

### Logging Out

Always logout when finished to invalidate your tokens:

```python
client.logout()
```
