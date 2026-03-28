from typing import Any
import urllib.request
import base64
import sys
from pathlib import Path
import argparse
import time
import threading


class DownloadState:
    def __init__(self, total_size):
        self.total_size = total_size
        self.downloaded = 0
        self.lock = threading.Lock()
        self.done = False


def progress_worker(state: DownloadState):
    last_time = time.time()
    last_downloaded = 0

    while not state.done:
        time.sleep(0.5)

        with state.lock:
            downloaded = state.downloaded
            total = state.total_size

        now = time.time()
        speed = (downloaded - last_downloaded) / (now - last_time + 1e-6)

        last_time = now
        last_downloaded = downloaded

        if total > 0:
            progress = downloaded / total * 100
        else:
            progress = 0

        if speed >= 1024 * 1024:
            speed_str = f"{speed / (1024 * 1024):.2f} MB/s"
        elif speed >= 1024:
            speed_str = f"{speed / 1024:.2f} KB/s"
        else:
            speed_str = f"{speed:.2f} B/s"

        if speed > 0 and total > 0:
            eta = (total - downloaded) / speed
            eta_str = f"{int(eta//60)}m{int(eta % 60)}s"
        else:
            eta_str = "N/A"

        bar_len = 50
        filled = int(progress / 100 * bar_len)
        bar = "#" * filled + "-" * (bar_len - filled)

        sys.stdout.write(
            f"\r[{threading.current_thread().name}] [{bar}] {progress:.1f}% | {speed_str} | ETA: {eta_str}")
        sys.stdout.flush()

    print("\nDownload completed successfully!")


def download_with_progress(url: str, output_filename: str, retries: int, timeout: float = 0.5,
                           user=None, password=None, headers: dict[str, Any] = {}):
    attempt = 0
    while attempt < retries:
        try:
            if output_filename:
                filename = output_filename
            else:
                url_path = url.split('?')[0]
                last_part = url_path.split('/')[-1]
                if '.' in last_part:
                    filename = last_part
                else:
                    filename = "downloaded_file"
            print(filename)
            filepath = Path(filename)

            req = urllib.request.Request(url)
            if headers:
                for key, value in headers.items():
                    req.add_header(key, value)

            if user and password:
                auth = base64.b64encode(f"{user}:{password}".encode()).decode()
                req.add_header("Authorization", f"Basic {auth}")

            opener = urllib.request.build_opener(
                urllib.request.HTTPRedirectHandler())
            urllib.request.install_opener(opener)

            response = urllib.request.urlopen(req, timeout=timeout)
            status = response.getcode()
            print(f"Attempt {attempt+1}/{retries} | HTTP Status: {status}")

            total_size = int(response.headers.get('Content-Length', 0))
            block_size = 1024 * 256

            state = DownloadState(total_size)

            progress_thread = threading.Thread(
                target=progress_worker, args=(state,))
            progress_thread.start()

            with open(filepath, 'wb') as f:
                while True:
                    buffer = response.read(block_size)
                    if not buffer:
                        break
                    f.write(buffer)

                    with state.lock:
                        state.downloaded += len(buffer)
            state.done = True
            progress_thread.join()

            print(f"File saved to: {filepath.absolute()}")
            return
        except Exception as e:
            print(f"\nError: {e}")
            attempt += 1
            print(f"\nAttempt {attempt} failed: {e}")
            if attempt < retries:
                print(
                    f"Retrying in 2 seconds... ({retries - attempt} attempts left)")
                time.sleep(2)
    print(f"\nAll {retries} attempts failed. Download aborted.")
    sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A simple wget-like CLI tool")
    parser.add_argument("url", help="URL to download")
    parser.add_argument("-o", "--output", help="Output filename")
    parser.add_argument("-r", "--retry", type=int, default=3,
                        help="Number of retries (default: 3)")
    parser.add_argument("--user", help="Username")
    parser.add_argument("--password", help="Password")
    parser.add_argument("--header", action="append",
                        help="Custom header")
    args = parser.parse_args()

    headers = {}
    if args.header:
        for h in args.header:
            h: str
            key, value = h.split(':', 1)
            headers[key.strip()] = value.strip()
    download_with_progress(args.url, args.output, args.retry, 1,
                           args.user, args.password, headers)
