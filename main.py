#!/usr/bin/env python3
"""
main.py - End-to-end alarm.com -> simPRO integration script.
"""

import os
import logging

from dotenv import load_dotenv

import alarmcom_api
import simpro_api

# Configure logging (write to a file named integration.log)
logging.basicConfig(
    filename="integration.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def transform_data(alarm_data):
    """
    Transform the raw data from alarm.com into a structure simPRO expects.
    Modify as needed depending on the real schemas.
    """
    # Example transformation: flatten or rename fields
    # Suppose alarm_data is a dictionary with a 'devices' key containing a list
    devices = alarm_data.get("devices", [])
    transformed = []
    for dev in devices:
        item = {
            "deviceId": dev.get("id"),
            "deviceName": dev.get("name"),
            "status": dev.get("status", "unknown"),
            # ... map or rename additional fields ...
        }
        transformed.append(item)
    return transformed

def main():
    """
    Main workflow:
    1. Load environment variables
    2. Get Alarm.com access token
    3. Fetch data from Alarm.com
    4. Transform data
    5. Send to simPRO
    """
    load_dotenv()  # Load .env if available

    # 1. Gather credentials
    alarm_user = os.getenv("ALARM_COM_API_USERNAME")
    alarm_pass = os.getenv("ALARM_COM_API_PASSWORD")
    alarm_client_id = os.getenv("ALARM_COM_API_CLIENT_ID")
    alarm_client_secret = os.getenv("ALARM_COM_API_CLIENT_SECRET")

    simpro_api_key = os.getenv("SIMPRO_API_KEY")
    simpro_account_id = os.getenv("SIMPRO_ACCOUNT_ID")

    if not all([alarm_user, alarm_pass, alarm_client_id, alarm_client_secret, simpro_api_key, simpro_account_id]):
        logging.error("Missing one or more required environment variables.")
        return

    try:
        # 2. Authenticate
        token = alarmcom_api.get_alarmcom_token(
            username=alarm_user,
            password=alarm_pass,
            client_id=alarm_client_id,
            client_secret=alarm_client_secret
        )
        logging.info("Successfully retrieved Alarm.com token.")

        # 3. Fetch raw data
        alarm_data = alarmcom_api.fetch_alarmcom_data(token)
        logging.info(f"Fetched data from Alarm.com: {alarm_data}")

        # 4. Transform data
        prepared_data = transform_data(alarm_data)
        logging.info(f"Transformed data for simPRO: {prepared_data}")

        # 5. Send to simPRO
        result = simpro_api.send_data_to_simpro(prepared_data, simpro_api_key, simpro_account_id)
        logging.info(f"Data successfully sent to simPRO. Response: {result}")

    except Exception as e:
        logging.error(f"Integration process failed: {e}", exc_info=True)

if __name__ == "__main__":
    main()

