import math
from datetime import datetime
import re


def calculate_points(receipt):
    points = 0
    points += count_retailer_name(receipt["retailer"])
    points += check_total(receipt["total"])
    points += check_items(receipt["items"])
    points += check_trimmed_items(receipt["items"])
    points += check_date_and_time(receipt["purchaseDate"], receipt["purchaseTime"])


def count_retailer_name(retailer):
    count = sum(1 for char in retailer if char.isalnum())
    return count

def check_total(total):
    total = float(total)
    points = 0
    if total.is_integer():
        points += 50
    if total % .25 == 0:
        points += 25
    return points

def check_items(items):
    return (len(items) // 2) * 5

def check_trimmed_items(items):
    points = 0
    for item in items:
        if len(item["shortDescription"].strip()) % 3 == 0:
            points += math.ceil(float(item["price"]) * 0.2)
    return points

def check_date_and_time(purchase_date, purchase_time):
    points = 0
    purchase_date = datetime.strptime(purchase_date, "%Y-%m-%d")
    if purchase_date.day % 2 == 1:
        points += 6

    purchase_time = datetime.strptime(purchase_time, "%H:%M")
    beginning = datetime.strptime("14:00", "%H:%M")
    end = datetime.strptime("16:00", "%H:%M")

    if beginning < purchase_time < end:
        points += 10

    return points
