from onvif import ONVIFCamera
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)


def print_zeep_methods(zeep_client):
    """Print all available methods in the Zeep client service."""
    # Access the service object from the Zeep client
    service = zeep_client.service
    # List methods of the service
    methods = dir(service)
    logging.info("Available methods in the Zeep client service:")
    for method in methods:
        logging.info("  %s", method)


def main():
    # Camera connection parameters
    ip = "192.168.1.1"  # Replace with your camera's IP address
    port = 2020  # Replace with your camera's port
    username = "admin"  # Replace with your camera's username
    password = "admin"  # Replace with your camera's password

    # Initialize the ONVIF camera
    camera = ONVIFCamera(ip, port, username, password)

    # Get the event service
    event_service = camera.create_events_service()

    # Print available methods from Zeep client
    print_zeep_methods(event_service.zeep_client)


if __name__ == "__main__":
    main()
