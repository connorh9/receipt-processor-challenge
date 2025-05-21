import requests
import json
from helpers import (
    pts_for_retail_name,
    pts_for_total,
    pts_for_amnt_items,
    pts_for_trimmed_items,
    pts_for_date_time
)
import unittest
from app import app, calculate_points

class ReceiptProcessorTests(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_process_receipt_valid(self):
        #Test a valid receipt and check status code and existence of an id
        receipt = {
            "retailer": "Target",
            "purchaseDate": "2022-01-01",
            "purchaseTime": "13:01",
            "items": [
                {
                    "shortDescription": "Mountain Dew 12PK",
                    "price": "6.49"
                }
            ],
            "total": "6.49"
        }

        response = self.app.post('/receipts/process', json=receipt, content_type='application/json')

        self.assertEqual(response.status_code, 200)
        data= json.loads(response.data)
        self.assertIn('id', data)

    def test_process_receipt_broken(self):
        #Testing a broken receipt to ensure we get a 400 code
        receipt = {
            "retailer": "Target",
            "purchaseDate": "2022-01-01",
            "purchaseTime": "13:01",
            "items": [
                {
                    "shortDescription": "Mountain Dew 12PK",
                    "price": "6.49"
                }
            ],
            #Missing total
        }
        response = self.app.post('/receipts/process', json=receipt, content_type='application/json')
        self.assertEqual(response.status_code, 400)
        data= json.loads(response.data)
        self.assertIn('error', data)

    def test_get_points_valid(self):
        """Test getting points with valid receipt id"""
        receipt = {
            "retailer": "Target",
            "purchaseDate": "2022-01-01",
            "purchaseTime": "13:01",
            "items": [
                {
                    "shortDescription": "Mountain Dew 12PK",
                    "price": "6.49"
                }
            ],
            "total": "6.49"
        }

        process_response = self.app.post('/receipts/process', 
                                         json=receipt,
                                         content_type='application/json')
        receipt_id = json.loads(process_response.data)['id']

        points_response = self.app.get(f'/receipts/{receipt_id}/points')
        self.assertEqual(points_response.status_code, 200)
        data = json.loads(points_response.data)
        self.assertIn('points', data)

    def test_get_points_invalid(self):
        response = self.app.get(f'/receipts/invalid/points')
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertIn('error', data)

    def test_points_calculation(self):
        receipt = {
            "retailer": "Target",
            "purchaseDate": "2022-01-01",
            "purchaseTime": "13:01",
            "items": [
                {
                "shortDescription": "Mountain Dew 12PK",
                "price": "6.49"
                },{
                "shortDescription": "Emils Cheese Pizza",
                "price": "12.25"
                },{
                "shortDescription": "Knorr Creamy Chicken",
                "price": "1.26"
                },{
                "shortDescription": "Doritos Nacho Cheese",
                "price": "3.35"
                },{
                "shortDescription": "   Klarbrunn 12-PK 12 FL OZ  ",
                "price": "12.00"
                }
            ],
            "total": "35.35"
        }
        points = calculate_points(receipt)
        self.assertEqual(points, 28)

        receipt = {
            "retailer": "M&M Corner Market",
            "purchaseDate": "2022-03-20",
            "purchaseTime": "14:33",
            "items": [
                {
                "shortDescription": "Gatorade",
                "price": "2.25"
                },{
                "shortDescription": "Gatorade",
                "price": "2.25"
                },{
                "shortDescription": "Gatorade",
                "price": "2.25"
                },{
                "shortDescription": "Gatorade",
                "price": "2.25"
                }
            ],
            "total": "9.00"
        }
        points = calculate_points(receipt)
        self.assertEqual(points, 109)

    def test_retailer_name(self):
        """Test the function that calculates pts for retailer name"""
        pts = pts_for_retail_name(" T&ar^get ")
        self.assertEqual(pts, 6)
    
    def test_points_for_total(self):
        """Test point calculation for dollar value"""
        pts = pts_for_total(1.25)
        self.assertEqual(pts, 25)

        pts = pts_for_total(2.00)
        self.assertEqual(pts, 75)

    def test_item_count(self):
        """Test cases for point values based on amount of items"""
        items= [
            {"shortDescription": "Item 1", "price": "1.00"},
            {"shortDescription": "Item 2", "price": "1.00"},
            {"shortDescription": "Item 3", "price": "1.00"},
            {"shortDescription": "Item 4", "price": "1.00"}
        ]
        pts = pts_for_amnt_items(items)
        self.assertEqual(pts, 10)

        items.pop()

        pts = pts_for_amnt_items(items)
        self.assertEqual(pts, 5)
    
    def test_description_length(self):
        """Test cases for point values based on description length"""
        items= [
            {"shortDescription": "Item 1", "price": "1.00"},
            {"shortDescription": "Item 2", "price": "1.00"},
            {"shortDescription": "Item 3", "price": "1.00"},
        ]
        pts = pts_for_trimmed_items(items)
        self.assertEqual(pts, 3)

        items= [
            {"shortDescription": "Item 12", "price": "1.00"},
            {"shortDescription": "Item 23", "price": "1.00"},
            {"shortDescription": "Item 34", "price": "1.00"},
        ]

        pts = pts_for_trimmed_items(items)
        self.assertEqual(pts, 0)

    def test_purchase_datetime(self):
        """Test points for date and time of purchase"""
        purchase_date = "2025-05-20"
        purchase_time = "16:00"
        pts = pts_for_date_time(purchase_date, purchase_time)
        self.assertEqual(pts, 0)

        purchase_date = "2025-05-20"
        purchase_time = "14:01"
        pts = pts_for_date_time(purchase_date, purchase_time)
        self.assertEqual(pts, 10)

        purchase_date = "2025-05-21"
        purchase_time = "14:00"
        pts = pts_for_date_time(purchase_date, purchase_time)
        self.assertEqual(pts, 6)

        purchase_date = "2025-05-21"
        purchase_time = "14:01"
        pts = pts_for_date_time(purchase_date, purchase_time)
        self.assertEqual(pts, 16)

if __name__ == '__main__':
    unittest.main()