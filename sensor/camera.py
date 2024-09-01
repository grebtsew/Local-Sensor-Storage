import cv2
import subprocess
import time
from datetime import datetime
import os
import multiprocessing
from utils.log import logger


class Camera(multiprocessing.Process):
    def __init__(self, system, ip, config):
        """
        Initializes the Camera class with the provided system credentials, IP address, and configuration.

        :param system: A dictionary containing 'user' and 'password' keys.
        :param ip: The IP address of the camera.
        :param config: A dictionary containing various configuration options.
        """
        super().__init__()
        self.ip = ip
        self.connect_string = f"rtsp://{system['user']}:{system['password']}@{ip}:{system['port']}/{system['path']}"
        self.config = config
        self.running = (
            multiprocessing.Event()
        )  # Event to control the process's execution
        self.running.set()

    def record_stream_with_audio(
        self, connect_string, output_folder, filename, duration_seconds=30
    ):
        """
        Records the RTSP stream with audio using FFmpeg.

        :param connect_string: The RTSP connection string.
        :param output_folder: Folder to save the video files.
        :param filename: The base name for the output file.
        :param duration_seconds: Duration for each video file in seconds.
        """
        output_file = f"{filename}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.avi"
        filepath = os.path.join(output_folder, output_file)

        ffmpeg_command = [
            "ffmpeg",
            "-i",
            connect_string,
            "-t",
            str(duration_seconds),
            "-c:v",
            "mjpeg",  # Use MJPEG codec for video
            "-c:a",
            "pcm_s16le",  # Use PCM 16-bit Little Endian for audio
            "-y",  # Overwrite the output file if it exists
            filepath,
        ]
        subprocess.Popen(ffmpeg_command)

    def run(self):
        """
        Runs the process to capture frames from the camera, display them in a window,
        and save them to video files using FFmpeg.
        """
        try:
            cap = cv2.VideoCapture(self.connect_string)

            if not cap.isOpened():
                raise ValueError(
                    f"Camera at {self.connect_string} could not be opened."
                )

            frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fps = int(cap.get(cv2.CAP_PROP_FPS))

            # Start recording with audio using FFmpeg
            self.record_stream_with_audio(
                self.connect_string,
                self.config["STORAGE_FOLDER"],
                self.ip,
                self.config["RECORDING_TIME"] * 60,
            )

            start_time = time.time()

            while self.running.is_set():
                ret, frame = cap.read()

                if not ret:
                    logger.warning(f"Failed to grab frame from {self.ip}.")
                    break

                resized_frame = cv2.resize(
                    frame, (self.config["VIDEO_WIDTH"], self.config["VIDEO_HEIGHT"])
                )

                # Display the frame
                if self.config["SHOW_STREAM"]:
                    cv2.imshow(f"{self.ip}", resized_frame)

                current_time = time.time()
                elapsed_time = current_time - start_time

                # Check if the recording duration has elapsed
                if elapsed_time >= self.config["RECORDING_TIME"] * 60 + 2:
                    # Restart the recording with a new file
                    self.record_stream_with_audio(
                        self.connect_string,
                        self.config["STORAGE_FOLDER"],
                        self.ip,
                        self.config["RECORDING_TIME"] * 60,
                    )
                    start_time = current_time  # Reset the timer

                if cv2.waitKey(1) & 0xFF == ord(
                    "q"
                ):  # Optional: stop if 'q' is pressed
                    self.running.clear()
                    break

            # Release resources
            cap.release()
            cv2.destroyAllWindows()

        except Exception as e:
            logger.error(f"Error in camera process for {self.ip}: {str(e)}")

    def stop(self):
        """
        Stops the camera process.
        """
        self.running.clear()
