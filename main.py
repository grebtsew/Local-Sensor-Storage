import json
from utils.network import scan_subnet
from sensor.camera import Camera

from utils.log import logger
import os
import time
from datetime import datetime, timedelta


def manage_video_folder(folder_path, max_size_gb=20, max_age_days=14):
    """
    Monitors the /video folder, ensuring it doesn't exceed the max size and removes files older than max age.

    :param folder_path: The path to the video folder.
    :param max_size_gb: Maximum allowed folder size in GB.
    :param max_age_days: Maximum file age in days.
    """

    max_size_bytes = max_size_gb * 1024 * 1024 * 1024  # Convert GB to bytes
    max_age = timedelta(days=max_age_days)

    while True:
        # Get all files in the folder
        files = [
            os.path.join(folder_path, f)
            for f in os.listdir(folder_path)
            if os.path.isfile(os.path.join(folder_path, f))
        ]

        # Sort files by modification time (oldest first)
        files.sort(key=lambda x: os.path.getmtime(x))

        # Check total folder size
        total_size = sum(os.path.getsize(f) for f in files)

        # Check for files older than max_age
        now = datetime.now()

        for file in files:
            file_age = now - datetime.fromtimestamp(os.path.getmtime(file))

            # If the file is too old or the total size exceeds the limit, delete the file
            if file_age > max_age or total_size > max_size_bytes:
                try:
                    os.remove(file)
                    total_size -= os.path.getsize(file)
                    logger.info(
                        f"Deleted: {file} (Size: {os.path.getsize(file)} bytes, Age: {file_age})"
                    )
                except Exception as e:
                    logger.error(f"Error deleting file {file}: {str(e)}")

        # Sleep for 60 seconds before checking again
        time.sleep(60)


def read_json(path):
    jsonObj = None
    with open(path, "r") as file:
        jsonObj = json.loads(file.read())
    return jsonObj


if __name__ == "__main__":
    logger.info("Local Sensor Data Storage started!")

    config = read_json("./config/camera_config.json")
    system = read_json("./config/camera_secret_example.json")
    logger.info("Loaded configs successfully!")

    cameras = scan_subnet(config["subnet"])

    # TODO: We make this smart so that we detect and find ips and try the combos first.

    if cameras:
        logger.info(f"\nCameras found in the network: {cameras}")
        for camera in cameras:
            if camera not in config["ignore-ips"]:
                for s in system:
                    logger.info(f"Starting Camera combo: {s} {camera}")

                    camera_process = Camera(system=s, ip=camera, config=config)
                    camera_process.start()
        if len(cameras) == 0:
            logger.info("\n No Cameras Detected!")

    else:
        logger.info("\nNo cameras found in the network.")

    manage_video_folder(
        config["STORAGE_FOLDER"], config["RECORD_MAX_SIZE"], config["RECORD_MAX_TIME"]
    )
