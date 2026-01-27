#!/usr/bin/env python3
import sys
from main import run_file

def main():
    if len(sys.argv) < 2:
        print("Usage: rayvn <file.rv>")
        return

    run_file(sys.argv[1])

if __name__ == "__main__":
    main()