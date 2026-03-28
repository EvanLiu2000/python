import urllib.request
import sys
from pathlib import Path
from typing import List, Dict, Tuple, Any


def downlaod_file(url: str):
    try:
        url_path = url.split('?')[0]
        last_part = url_path.split('/')[-1]
        if '.' in last_part:
            filename = last_part
        else:
            filename = "downloaded_file"
        filepath = Path(filename)
        print(f"Downloading {url} to {filepath}...")
        urllib.request.urlretrieve(url, filepath)
        print("Download completed successfully!")
        print(f"File saved to: {filepath.absolute()}")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python 1.py <URL>")
        sys.exit(1)
    url = sys.argv[1]
    downlaod_file(url)
