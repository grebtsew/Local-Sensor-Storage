def calculate_file_size(days, fps, width, height, format):
    # Define the bitrates for different formats in Mbps (Megabits per second)
    format_bitrates = {
        "mp4": 5,  # Common for 1080p video
        "avi": 8,  # Generally higher bitrate
        "mkv": 10,  # High quality video
        "mov": 8,  # Similar to AVI
        "flv": 2,  # Lower quality streaming format
    }

    # Check if the provided format is supported
    if format not in format_bitrates:
        raise ValueError(
            f"Unsupported format: {format}. Supported formats: {', '.join(format_bitrates.keys())}"
        )

    # Calculate the total number of seconds in the given number of days
    total_seconds = days * 24 * 60 * 60

    # Calculate the total number of frames
    total_frames = total_seconds * fps

    # Calculate the total pixels per frame
    total_pixels_per_frame = width * height

    # Get the bitrate in Mbps (Megabits per second)
    bitrate_mbps = format_bitrates[format]

    # Calculate the total data in Megabits
    total_data_megabits = total_seconds * bitrate_mbps

    # Convert Megabits to Megabytes (1 Megabit = 0.125 Megabytes)
    total_data_megabytes = total_data_megabits * 0.125

    # Convert Megabytes to Gigabytes (1 Gigabyte = 1024 Megabytes)
    total_data_gigabytes = total_data_megabytes / 1024

    return total_data_gigabytes


# Example usage
days = 1
fps = 30
width = 1920
height = 1080
format = "mp4"

file_size = calculate_file_size(days, fps, width, height, format)
print(
    f"The estimated file size for a {days}-day video with {fps} FPS at {width}x{height} resolution in {format} format is approximately {file_size:.2f} GB."
)
