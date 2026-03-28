import urllib.request
import sys
from pathlib import Path
from typing import List, Dict, Tuple, Any
import argparse


def download_file(url: str, output_filename: str):
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
        filepath = Path(filename)
        print(f"Downloading {url} to {filepath}...")
        urllib.request.urlretrieve(url, filepath)
        print("Download completed successfully!")
        print(f"File saved to: {filepath.absolute()}")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A simple wget-like CLI tool")
    parser.add_argument("url", help="URL of the file to download")
    parser.add_argument("-o", "--output", help="Output filename")
    args = parser.parse_args()
    print(args)
    download_file(args.url, args.output)
