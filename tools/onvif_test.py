from onvif import ONVIFCamera
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)


def print_service_methods(service):
    """Print all available methods and attributes of the given service."""
    # List all attributes and methods
    attributes = dir(service)
    logging.info("Available attributes and methods in the service:")
    for attr in attributes:
        logging.info("  %s", attr)


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

    # Print all available methods and attributes in the event service
    print_service_methods(event_service)


if __name__ == "__main__":
    main()
