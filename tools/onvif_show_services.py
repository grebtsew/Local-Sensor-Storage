from onvif import ONVIFCamera
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)


def list_services(camera):
    """List all available services from the ONVIF camera."""
    # Get the device service from the camera
    device_service = camera.create_devicemgmt_service()

    # Retrieve the device information
    device_info = device_service.GetDeviceInformation()
    logging.info("Device Information: %s", device_info)

    # Get the available services
    services = device_service.GetServices(False, True)
    logging.info("Available services:")

    for service in services:
        logging.info("  %s", service)
        logging.info("    xaddr: %s", service.XAddr)
        logging.info("    Type: %s", service.Namespace)
        logging.info("    Version: %s", service.Version)


def main():
    # Camera connection parameters
    ip = "192.168.1.1"  # Replace with your camera's IP address
    port = 2020  # Replace with your camera's port (usually 8080)
    username = "admin"  # Replace with your camera's username
    password = "admin"  # Replace with your camera's password

    # Initialize the ONVIF camera
    camera = ONVIFCamera(ip, port, username, password)

    # List all available services
    list_services(camera)


if __name__ == "__main__":
    main()
