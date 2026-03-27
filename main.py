"""Example script demonstrating common XPay calls using xpay_client.py.

Set the environment variables or edit the values below:
- XPAY_BASE_URL
- XPAY_API_KEY
- XPAY_ACCOUNT_ID
- XPAY_SIGNATURE_KEY

Run: python3 example.py
"""

import os
import pprint
from xpay_client import (
    create_payment_intent,
    retrieve_payment_intent,
    capture_payment_intent,
    delete_payment_intent,
)

pp = pprint.PrettyPrinter(indent=2)
BASE_URL = "https://xstak-pay-stg.xstak.com"
API_KEY = "xpay_sk_test_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
ACCOUNT_ID = "XXXXXXXXXXXXXXXXXX"
# Use the API Signature Secret (HMAC key) from dashboard; this value in the
# repo may be a publishable key — replace with the hex signature secret.
SIGNATURE_KEY = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"


def main():
    # 1) Create a payment intent
    payload = {
        "amount": 500,
        "currency": "PKR",
        "payment_method_types": "card",
        "customer": {
            "name": "Jane Doe",
            "email": "jane.doe@example.com",
            "phone": "09123456789",
        }
    }

    print("Creating Payment Intent...")
    try:
        create_resp = create_payment_intent(BASE_URL, API_KEY, ACCOUNT_ID, SIGNATURE_KEY, payload)
        pp.pprint(create_resp)
    except Exception as e:
        print("Create Payment Intent failed:", e)
        return

    # Extract ids for the next steps
    data = create_resp.get("data") if isinstance(create_resp, dict) else None
    if not data:
        print("No 'data' in create response; aborting example.")
        return

    pi_id = data.get("_id")
    pi_client_secret = data.get("pi_client_secret")

    if not pi_id or not pi_client_secret:
        print("Missing pi_id or pi_client_secret in response; aborting.")
        return

    # 2) Retrieve the payment intent
    print("\nRetrieving Payment Intent...", pi_id)
    try:
        ret = retrieve_payment_intent(BASE_URL, API_KEY, ACCOUNT_ID, SIGNATURE_KEY, pi_id)
        pp.pprint(ret)
    except Exception as e:
        print("Retrieve failed:", e)

    # 3) (Optional) Capture the authorized amount - here we'll attempt a partial capture of 10
    print("\nCapturing Payment Intent (partial amount = 10)...")
    try:
        cap = capture_payment_intent(BASE_URL, API_KEY, ACCOUNT_ID, SIGNATURE_KEY, pi_client_secret, amount=10)
        pp.pprint(cap)
    except Exception as e:
        print("Capture failed:", e)

    # 4) (Optional) Delete the PI (if supported by your account)
    print("\nDeleting Payment Intent...")
    # try:
    #     resp = delete_payment_intent(BASE_URL, API_KEY, ACCOUNT_ID, SIGNATURE_KEY, pi_id)
    #     print("Delete status:", resp.status_code)
    # except Exception as e:
    #     print("Delete failed:", e)


if __name__ == "__main__":
    main()
