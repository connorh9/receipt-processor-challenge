import math
from datetime import datetime
import re


def calculate_points(receipt):


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

def checked_trimmed_items(items):
    points = 0
    for item in items:
        if len(item.shortDescription.strip()) // 3 == 0:
            points += math.ceil(item.price * 0.2)
    return points

