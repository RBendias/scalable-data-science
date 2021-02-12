#!/usr/bin/env python
"""mapper.py"""

import sys


def main():
    for line in sys.stdin:
        line = line.strip()
        key_value = line.split("|")
        # customer table
        if len(key_value) == 8:
            key = key_value[0]  # custkey
            values = key_value[1] + '|' + key_value[2] + '|' + key_value[5]  # name | addres | acctbal
        # order table
        else:
            key = key_value[1]  # custkey
            values = key_value[3] + '|' + key_value[4]  # price | orderdate
        print( f'{key}\t{values}') # try yield, maybe formatting


if __name__ == "__main__":
    main()
