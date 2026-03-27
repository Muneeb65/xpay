# XPay Fusion Python snippets

This small helper contains simple, runnable Python snippets to call common XPay Fusion APIs (Create Payment Intent, Capture, Retrieve, Delete).

Files:
- `xpay_client.py` - helper functions to generate HMAC signatures and call the API endpoints.
- `main.py` - small runnable main that demonstrates creating a PI, retrieving it, capturing, and deleting.
- `requirements.txt` - Python dependency (requests).

Quickstart

1. Install dependencies:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

2. Set environment variables (or edit `main.py` to hardcode values):

```bash
export XPAY_BASE_URL="https://xpay-app-stage.postexglobal.com/"
export XPAY_API_KEY="6d61204b9741ba6076d51e061cfb63355dc49a35774b7061bbbc9ff45d35632b"
export XPAY_ACCOUNT_ID="09984c32f2f924e2"
export XPAY_SIGNATURE_KEY="your_signature_key"
```

3. Run the main:

```bash
python3 main.py
```

Notes

- The HMAC signature uses SHA256 and signs the compact JSON string (no spaces) of the request body. For requests without a body we sign an empty string.
- Update the base URL and credentials from your XPay account before running against the real API.
- The main performs actions that may affect real data; prefer running against a staging environment.
