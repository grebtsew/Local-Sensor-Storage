from onvif import ONVIFCamera
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)


def main():
    # Camera connection parameters
    ip = "192.168.1.1"  # Replace with your camera's IP address
    port = 2020  # Replace with your camera's port
    username = "admin"  # Replace with your camera's username
    password = "admin"  # Replace with your camera's password

    # Initialize the ONVIF camera
    camera = ONVIFCamera(ip, port, username, password)

    # Get Device Management Service
    device_service = camera.create_devicemgmt_service()
    logging.info("Device Information: %s", device_service.GetDeviceInformation())

    # Get Media Service
    media_service = camera.create_media_service()
    logging.info("Media Service: %s", media_service.GetProfiles())

    # Get PTZ Service
    try:
        ptz_service = camera.create_ptz_service()
        logging.info("PTZ Service: %s", ptz_service.GetConfigurations())
    except Exception as e:
        logging.info("PTZ Service not available: %s", str(e))

    # Get Events Service
    try:
        event_service = camera.create_events_service()
        logging.info("Events Service: %s", event_service.GetEventProperties())
    except Exception as e:
        logging.info("Events Service not available: %s", str(e))

    # Get Analytics Service
    try:
        analytics_service = camera.create_analytics_service()
        logging.info(
            "Analytics Service: %s", analytics_service.GetAnalyticsCapabilities()
        )
    except Exception as e:
        logging.info("Analytics Service not available: %s", str(e))

    # Get Imaging Service
    try:
        imaging_service = camera.create_imaging_service()
        logging.info("Imaging Service: %s", imaging_service.GetImagingSettings())
    except Exception as e:
        logging.info("Imaging Service not available: %s", str(e))


if __name__ == "__main__":
    main()
