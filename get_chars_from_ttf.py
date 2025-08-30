"""
MX-Font
Copyright (c) 2021-present NAVER Corp.
MIT license
"""

import argparse
from tqdm import tqdm
from pathlib import Path
from multiprocessing import Pool

from datasets import get_filtered_chars


def process_ttffile(ttffile):
    filename = ttffile.stem
    dirname = ttffile.parent
    avail_chars = get_filtered_chars(ttffile)
    with open((dirname / (filename+".txt")), "w") as f:
        f.write("".join(avail_chars))

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--root_dir")
    args = parser.parse_args()

    print(args.root_dir)
    ttffiles = list(Path(args.root_dir).rglob("*.ttf"))

    
    for each in tqdm(ttffiles):
        try:
            process_ttffile(each)
        except Exception as e:
            print(f"Error: {each} {e}")
            continue


if __name__ == "__main__":
    main()
