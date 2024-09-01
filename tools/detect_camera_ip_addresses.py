import subprocess
import platform
import socket
from concurrent.futures import ThreadPoolExecutor, as_completed


# Function to ping a given IP address
def ping_ip(ip):
    param = "-n" if platform.system().lower() == "windows" else "-c"
    command = ["ping", param, "1", ip]
    try:
        result = subprocess.run(
            command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=2
        )
        if result.returncode == 0:
            return ip
    except subprocess.TimeoutExpired:
        pass
    return None


# Function to check if a device is a camera by attempting to connect to common camera ports
def check_camera(ip):
    common_ports = [80, 554, 8080, 443]
    for port in common_ports:
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(1)
            result = sock.connect_ex((ip, port))
            if result == 0:
                sock.close()
                return True
            sock.close()
        except Exception as e:
            pass
    return False


# Function to scan the subnet
def scan_subnet(subnet):
    live_hosts = []
    print("Pinging IP addresses in the subnet...")
    with ThreadPoolExecutor(max_workers=100) as executor:
        futures = {
            executor.submit(ping_ip, f"{subnet}.{i}"): f"{subnet}.{i}"
            for i in range(1, 255)
        }
        for future in as_completed(futures):
            result = future.result()
            if result:
                live_hosts.append(result)
            # Progress update
            print(
                f"Pinging progress: {len(live_hosts)}/254 live hosts detected", end="\r"
            )
    print("\nPinging complete.")

    cameras = []
    print("Checking live hosts for camera ports...")
    with ThreadPoolExecutor(max_workers=100) as executor:
        futures = {executor.submit(check_camera, ip): ip for ip in live_hosts}
        for future in as_completed(futures):
            ip = futures[future]
            if future.result():
                cameras.append(ip)
            # Progress update
            print(
                f"Checking progress: {len(cameras)}/{len(live_hosts)} potential cameras detected",
                end="\r",
            )
    print("\nChecking complete.")

    return cameras


if __name__ == "__main__":
    subnet = "192.168.1"
    cameras = scan_subnet(subnet)
    if cameras:
        print("\nCameras found in the network:")
        for camera in cameras:
            print(camera)
    else:
        print("\nNo cameras found in the network.")
