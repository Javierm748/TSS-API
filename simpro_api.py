
import os
import requests
import logging

SIMPRO_BASE_URL = "https://api.simpro.com"  # Replace with your actual simPRO endpoint

def send_data_to_simpro(data, api_key, account_id):
    """
    Sends data to simPRO. Adjust the URL, headers, and payload
    to match simPRO's actual API specification.
    """
    url = f"{SIMPRO_BASE_URL}/v1/accounts/{account_id}/devices"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    try:
        response = requests.post(url, json=data, headers=headers, timeout=15)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logging.error(f"Failed to send data to simPRO: {e}", exc_info=True)
        raise
