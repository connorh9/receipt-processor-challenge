import math
from datetime import datetime
import re


def calculate_points(receipt):
    """
    Function will go through and total up all points for the receipt
    and return the points total back to server.py.
    """
    points = 0
    points += pts_for_retail_name(receipt["retailer"])
    points += pts_for_total(receipt["total"])
    points += pts_for_amnt_items(receipt["items"])
    points += pts_for_trimmed_items(receipt["items"])
    points += pts_for_date_time(receipt["purchaseDate"], receipt["purchaseTime"])
    return points


def pts_for_retail_name(retailer):
    """
    Awards a point to the total for every alphanumeric character 
    in the retailer name

    Returns: int: point total for retailer name
    """
    count = sum(1 for char in retailer if char.isalnum())
    return count

def pts_for_total(total):
    """
    Checks if receipt total is a round dollar, and if
    the total is a multiple of .25

    Returns: int: points accrued for the two conditions
    """
    total = float(total) #typecast to prevent errors
    points = 0
    if total.is_integer(): #check if the total is a round dollar
        points += 50
    if total % .25 == 0: #check if total is multiple of .25
        points += 25
    return points

def pts_for_amnt_items(items):
    """
    Adds 5 points for every 2 items in the receipt

    Returns: int: points gained for item count
    """
    return (len(items) // 2) * 5

def pts_for_trimmed_items(items):
    """
    Goes through each item's short description, removes leading
    and trailing whitespace, and checks if the character count
    is a multiple of 3. If so, adds the item price * .2 to the 
    point total.

    Returns: int: points earned based on item description and price
    """
    points = 0
    for item in items:
        if len(item["shortDescription"].strip()) % 3 == 0: #strips item description and checks if multiple of 3
            points += math.ceil(float(item["price"]) * 0.2) #converted to float to prevent errors
    return points

def pts_for_date_time(purchase_date, purchase_time):
    """
    Checks both the date and time conditions for the receipt.
    If purchase date is odd, 6 points are given. 
    If the time of the purchase is between 2pm and 4pm exclusive, 
    10 points are given

    Returns: int: points awarded for purchaseDate and purchaseTime
    """
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
