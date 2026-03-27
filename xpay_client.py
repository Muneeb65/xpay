"""Simple XPay Fusion Python client utilities.

This module provides small helper functions to generate HMAC signatures and
call common XPay endpoints showcased in the provided documentation:
- Create Payment Intent
- Capture Payment Intent
- Retrieve Payment Intent
- Delete Payment Intent

Usage: import the functions and pass your base_url, api_key, account_id and
signature_key (HMAC secret).
"""

import json
import hmac
import hashlib
from typing import Optional, Dict, Any
import requests


def generate_signature(secret_key: str, payload: Optional[Dict[str, Any]]) -> str:
    """Generate HMAC SHA256 signature for the JSON payload.

    The API documentation specifies signing JSON.stringify(payload) using
    separators (',', ':') (no spaces). If payload is None, an empty string is
    signed.
    """
    if payload is None:
        message = ""
    else:
        # compact separators to match other SDK examples
        message = json.dumps(payload, separators=(",", ":"), ensure_ascii=False)
    signature = hmac.new(secret_key.encode("utf-8"), message.encode("utf-8"), hashlib.sha256).hexdigest()
    return signature


def _build_headers(api_key: str, account_id: str, signature: str) -> Dict[str, str]:
    return {
        "x-api-key": api_key,
        "x-account-id": account_id,
        "x-signature": signature,
        "Content-Type": "application/json",
    }


def create_payment_intent(base_url: str, api_key: str, account_id: str, signature_key: str, payload: Dict[str, Any], timeout: int = 15) -> Dict[str, Any]:
    """Create a payment intent.

    Returns parsed JSON response on success, otherwise raises requests.HTTPError
    with more details.
    """
    url = base_url.rstrip("/") + "/public/v1/payment/intent"
    signature = generate_signature(signature_key, payload)
    headers = _build_headers(api_key, account_id, signature)
    resp = requests.post(url, headers=headers, json=payload, timeout=timeout)
    resp.raise_for_status()
    return resp.json()


def capture_payment_intent(base_url: str, api_key: str, account_id: str, signature_key: str, pi_client_secret: str, amount: Optional[int] = None, timeout: int = 15) -> Dict[str, Any]:
    """Capture an authorized payment (full or partial).

    If amount is None the API will capture the full authorized amount.
    """
    params = {"pi_client_secret": pi_client_secret}
    url = base_url.rstrip("/") + "/public/v1/payment/intent/capture"
    body = {"amount": amount} if amount is not None else None
    signature = generate_signature(signature_key, body)
    headers = _build_headers(api_key, account_id, signature)
    resp = requests.post(url, headers=headers, params=params, json=body, timeout=timeout)
    resp.raise_for_status()
    return resp.json()


def retrieve_payment_intent(base_url: str, api_key: str, account_id: str, signature_key: str, pi_id: str, timeout: int = 15) -> Dict[str, Any]:
    """Retrieve payment intent details by PI id."""
    url = base_url.rstrip("/") + f"/public/v1/payment/intent/details/{pi_id}"
    # GET usually has no body; sign empty string to match docs
    signature = generate_signature(signature_key, None)
    headers = _build_headers(api_key, account_id, signature)
    resp = requests.get(url, headers=headers, timeout=timeout)
    resp.raise_for_status()
    return resp.json()


def delete_payment_intent(base_url: str, api_key: str, account_id: str, signature_key: str, pi_id: str, timeout: int = 15) -> requests.Response:
    """Delete a payment intent by ID. The API may return no body (204/200).

    Returns the raw Response object so the caller can inspect status_code.
    """
    # NOTE: docs show capitalized Intent in path; preserve that path exactly
    url = base_url.rstrip("/") + f"/public/v1/payment/Intent/{pi_id}"
    signature = generate_signature(signature_key, None)
    headers = _build_headers(api_key, account_id, signature)
    resp = requests.delete(url, headers=headers, timeout=timeout)
    resp.raise_for_status()
    return resp


if __name__ == "__main__":
    # Quick smoke-run if the module is executed directly. Replace the placeholders
    # below with your environment values to exercise the client.
    import os

    BASE_URL = "https://xstak-pay-stg.xstak.com"
    API_KEY = "xpay_sk_test_d547f99a6bc317a32bd95fc18e1591a946f8cf44dcba409c81b48fdd16c22c6d"
    ACCOUNT_ID = "09984c32f2f924e2"
    # Use the API Signature Secret (HMAC key) from dashboard; this value in the
    # repo may be a publishable key — replace with the hex signature secret.
    SIGNATURE_KEY = "6d61204b9741ba6076d51e061cfb63355dc49a35774b7061bbbc9ff45d35632b"

    sample_payload = {
        "amount": 500,
        "currency": "PKR",
        "payment_method_types": "card",
        "customer": {
            "name": "Test User",
            "email": "test@example.com",
            "phone": "1234567890"
        }
    }

    print("This module provides helper functions. Import it from your code to use the XPay APIs.")
    print("Example signature for sample payload:", generate_signature(SIGNATURE_KEY, sample_payload))
