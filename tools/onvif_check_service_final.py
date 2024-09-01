from onvif import ONVIFCamera
import logging
import time
import requests
from requests.exceptions import RequestException

# Setup logging
logging.basicConfig(level=logging.INFO)


def create_subscription(event_service):
    """Create a subscription to the event service."""
    try:
        response = event_service.CreatePullPointSubscription()
        logging.info("Subscription created: %s", response)
        return response.SubscriptionReference.Address._value_1
    except Exception as e:
        logging.error("Failed to create subscription: %s", e)
        return None


def pull_messages(event_service, subscription_reference):
    """Pull messages from the event service subscription."""
    try:
        response = event_service.PullMessages(0, 0)
        logging.info("Pulled messages: %s", response)
        return response
    except Exception as e:
        logging.error("Failed to pull messages: %s", e)
        return None


def main():
    # Camera connection parameters
    ip = "192.168.1.1"  # Replace with your camera's IP address
    port = 2020  # Replace with your camera's port
    username = "admin"  # Replace with your camera's username
    password = "admin"  # Replace with your camera's password

    # Initialize the ONVIF camera

    mycam = ONVIFCamera(ip, port, username, password)
    event_service = mycam.create_events_service()
    print(event_service.GetEventProperties())

    pullpoint = mycam.create_pullpoint_service()
    req = pullpoint.create_type("PullMessages")
    req.MessageLimit = 100
    print(pullpoint.PullMessages(req))


if __name__ == "__main__":
    main()
