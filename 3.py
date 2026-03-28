import urllib.request
import sys
from pathlib import Path
from typing import List, Dict, Tuple, Any
import argparse


def download_with_progress(url: str, output_filename: str):
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

        response = urllib.request.urlopen(url)
        total_size = int(response.headers.get('Content-Length', 0))
        block_size = 8192
        downloaded = 0

        with open(filepath, 'wb') as f:
            while True:
                buffer = response.read(block_size)
                if not buffer:
                    break
                f.write(buffer)
                downloaded += len(buffer)

                if total_size > 0:
                    progress = (downloaded / total_size) * 100
                    bar = '*' * int(progress // 2) + '-' * \
                        (50 - int(progress // 2))
                    print(
                        f"\r[{bar}] {progress:.1f}% ({downloaded}/{total_size} bytes)")
        print("\nDownload completed successfully!")
        print(f"File saved to: {filepath.absolute()}")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A simple wget-like CLI tool")
    parser.add_argument("url", help="URL to download")
    parser.add_argument("-o", "--output", help="Output filename")
    args = parser.parse_args()
    print(args)
    download_with_progress(args.url, args.output)
