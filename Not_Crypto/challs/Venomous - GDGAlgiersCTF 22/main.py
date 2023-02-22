#!/usr/bin/env python3

from sys import argv, stderr, exit
from echo import echo

if __name__ == "__main__":
    if len(argv) < 2:
        print(f"Usage: {argv[0]} STRING", file=stderr)
        exit(1)

    echo(argv[1])
