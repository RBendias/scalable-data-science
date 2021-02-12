#!/usr/bin/env python
import sys
import datetime


def main():
    customer = {}
    # In Python Inputs are not grouped
    for line in sys.stdin:
        key, values = line.strip().split("\t")
        values = values.split("|")
        # customer
        if len(values) == 3:
            name = values[0]
            if key not in customer:
                counts = 0
            else:
                counts = customer[key][1]
            customer[key] = (name, counts)
        # orders
        else:
            if key not in customer:
                name = ''
                counts = 0
            else:
                counts = customer[key][1]
                customer[key] = (name, (counts + 1))
    for key in customer:
        (name, counts) = customer[key]
        if name != '' and counts == 0:
            print(f'{name}')


if __name__ == "__main__":
    main()
