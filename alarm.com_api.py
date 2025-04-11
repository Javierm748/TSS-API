
import os
import requests
import logging

ALARM_COM_BASE_URL = "https://api.alarm.com"  # Replace with actual base if different

def get_alarmcom_token(username, password, client_id, client_secret):
    """
    Example OAuth or token-based authentication flow with Alarm.com.
    This is purely illustrative; the real method may vary.
    """
    auth_url = f"{ALARM_COM_BASE_URL}/oauth/token"
    # Hypothetical payload based on OAuth2
    payload = {
        "grant_type": "password",
        "username": username,
        "password": password,
        "client_id": client_id,
        "client_secret": client_secret
    }
    try:
        response = requests.post(auth_url, data=payload, timeout=15)
        response.raise_for_status()
        token_data = response.json()
        # Typically an OAuth2 response might have "access_token"
        return token_data["access_token"]
    except requests.RequestException as e:
        logging.error(f"Failed to fetch Alarm.com token: {e}", exc_info=True)
        raise

def fetch_alarmcom_data(token):
    """
    Fetch device data or other info from Alarm.com.
    The exact endpoint and parameters must match your actual usage.
    """
    url = f"{ALARM_COM_BASE_URL}/v1/devices"  # Example endpoint
    headers = {
        "Authorization": f"Bearer {token}"
    }
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        return response.json()  # Or response.text if the API returns non-JSON
    except requests.RequestException as e:
        logging.error(f"Failed to fetch Alarm.com data: {e}", exc_info=True)
        raise
