# -*- coding: utf-8 -*-
# !/usr/bin/python3

import csv


def create_csv(path, csv_head):
    with open(path, 'w', encoding='GBK', newline="") as f:
        csv_write = csv.writer(f)
        csv_write.writerow(csv_head)  # csv_head填写第一行信息


def write_csv(path, list_row):
    with open(path, 'a+', encoding='GBK', newline="") as f:
        csv_write = csv.writer(f)
        csv_write.writerow(list_row)
