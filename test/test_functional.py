"""
Functional tests for the Food Waste Reduction System.
"""

import pytest
from datetime import datetime, timedelta
from test.TestUtils import TestUtils
from food_waste_reduction_system import (
    validate_food_item,
    calculate_days_until_expiration,
    identify_expiring_items,
    sort_items_by_expiration,
    match_donations,
    format_food_item
)


class TestFunctional:
    """Test class for functional tests of the Food Waste Reduction System."""
    
    def setup_method(self):
        """Setup test data before each test method."""
        # Create test dates relative to today
        self.today = datetime.today().date()
        self.future_date = (self.today + timedelta(days=5)).strftime("%Y-%m-%d")
        self.near_future_date = (self.today + timedelta(days=2)).strftime("%Y-%m-%d")
        
        # Test inventory
        self.test_inventory = [
            {
                "id": "F001",
                "name": "Apples",
                "category": "Produce",
                "quantity": 25,
                "unit": "kg",
                "expiration_date": self.future_date,
                "storage_location": "Cooler 3"
            },
            {
                "id": "F002",
                "name": "Milk",
                "category": "Dairy",
                "quantity": 15,
                "unit": "liter",
                "expiration_date": self.near_future_date,
                "storage_location": "Refrigerator 1"
            }
        ]
        
        # Test recipients
        self.test_recipients = [
            {
                "id": "R001",
                "name": "City Food Bank",
                "accepts_categories": ["Produce", "Canned", "Bakery"]
            },
            {
                "id": "R002",
                "name": "Community Shelter",
                "accepts_categories": ["Dairy", "Bakery", "Prepared"]
            }
        ]
        
        # Test object for assertions
        self.test_obj = TestUtils()
    
    def test_validate_food_item_valid(self):
        """Test validate_food_item with valid input."""
        result = validate_food_item(self.test_inventory[0])
        assert result["is_valid"] == True
        assert "valid" in result["message"].lower()
        
        self.test_obj.yakshaAssert("test_validate_food_item_valid", True, "functional")
    
    def test_validate_food_item_invalid(self):
        """Test validate_food_item with invalid input."""
        invalid_item = {"id": "F003", "name": "Bread"}  # Missing required fields
        result = validate_food_item(invalid_item)
        assert result["is_valid"] == False
        
        self.test_obj.yakshaAssert("test_validate_food_item_invalid", True, "functional")
    
    def test_calculate_days_until_expiration(self):
        """Test calculate_days_until_expiration."""
        days = calculate_days_until_expiration(self.future_date)
        assert days == 5
        
        self.test_obj.yakshaAssert("test_calculate_days_until_expiration", True, "functional")
    
    def test_identify_expiring_items(self):
        """Test identify_expiring_items."""
        expiring = identify_expiring_items(self.test_inventory, 3)
        assert len(expiring) == 1
        assert expiring[0]["id"] == "F002"  # Milk expires sooner
        
        self.test_obj.yakshaAssert("test_identify_expiring_items", True, "functional")
    
    def test_sort_items_by_expiration(self):
        """Test sort_items_by_expiration."""
        sorted_items = sort_items_by_expiration(self.test_inventory)
        assert sorted_items[0]["id"] == "F002"  # Milk expires sooner
        assert sorted_items[1]["id"] == "F001"  # Apples expire later
        
        self.test_obj.yakshaAssert("test_sort_items_by_expiration", True, "functional")
    
    def test_match_donations(self):
        """Test match_donations."""
        matches = match_donations(self.test_inventory, self.test_recipients)
        assert len(matches) == 2
        
        # Check if apples match with City Food Bank
        found_apple_match = False
        for match in matches:
            if match["item"]["id"] == "F001" and match["recipient"]["id"] == "R001":
                found_apple_match = True
                
        assert found_apple_match == True
        
        # Check if milk matches with Community Shelter
        found_milk_match = False
        for match in matches:
            if match["item"]["id"] == "F002" and match["recipient"]["id"] == "R002":
                found_milk_match = True
                
        assert found_milk_match == True
        
        self.test_obj.yakshaAssert("test_match_donations", True, "functional")
    
    def test_format_food_item(self):
        """Test format_food_item."""
        formatted = format_food_item(self.test_inventory[0])
        assert "F001" in formatted
        assert "Apples" in formatted
        assert "25 kg" in formatted
        assert "Produce" in formatted
        assert self.future_date in formatted
        
        self.test_obj.yakshaAssert("test_format_food_item", True, "functional")


if __name__ == '__main__':
    pytest.main(['-v'])