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
            acctbal = float(values[2])
            address = values[1]
            name = values[0]
            if acctbal < 1000:
                name = address = ''
                pass
            if key not in customer:
                price = 0.0
                counts = 0
            else:
                price = customer[key][2]
                counts = customer[key][3]
            customer[key] = (name, address, price, counts)
        # orders
        else:
            orderdate = datetime.datetime.strptime(values[1], '%Y-%m-%d')
            if orderdate >= datetime.datetime(1995, 1, 1):
                if key not in customer:
                    price = 0.0
                    name = address = ''
                    counts = 0
                else:
                    price = customer[key][2]
                    counts = customer[key][3]
                customer[key] = (name, address, price + float(values[0]), (counts + 1))
    for key in customer:
        (name, address, price, counts) = customer[key]
        if name != '' and price > 0:
            avg_price = price / counts
            print(f'{name}, {address}, {avg_price}')


if __name__ == "__main__":
    main()
