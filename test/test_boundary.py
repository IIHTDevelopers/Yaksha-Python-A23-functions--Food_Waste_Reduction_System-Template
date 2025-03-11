import pytest
from datetime import datetime, date, timedelta
from test.TestUtils import TestUtils
from food_waste_reduction_system import *


class TestBoundary:
    """Test class for boundary tests of the Food Waste Reduction System."""
    
    def setup_method(self):
        """Setup test data before each test method."""
        self.test_obj = TestUtils()
    
    def test_boundary_scenarios(self):
        """Consolidated test for boundary scenarios"""
        try:
            # Test with empty food items list
            empty_food_items = []
            
            # Test functions with empty food items list
            expiring = identify_expiring_items(empty_food_items, 7)
            assert expiring == [], "Identifying expiring items in empty list should return empty list"
            
            sorted_items = sort_items_by_expiration(empty_food_items)
            assert sorted_items == [], "Sorting empty food items list should return empty list"
            
            matches = match_donations(empty_food_items, [{"id": "R001", "name": "Food Bank", "accepts_categories": ["Produce"]}])
            assert matches == [], "Matching empty food items list should return empty list"
            
            # Test with empty recipients list
            matches = match_donations([{"id": "F001", "category": "Produce", "name": "Apples"}], [])
            assert matches == [], "Matching with empty recipients list should return empty list"
            
            # Test with various expiration dates
            today = date.today()
            today_str = today.strftime("%Y-%m-%d")
            tomorrow_str = (today + timedelta(days=1)).strftime("%Y-%m-%d")
            yesterday_str = (today - timedelta(days=1)).strftime("%Y-%m-%d")
            
            days = calculate_days_until_expiration(today_str)
            assert days == 0, "Days until today's date should be 0"
            
            days = calculate_days_until_expiration(tomorrow_str)
            assert days == 1, "Days until tomorrow should be 1"
            
            days = calculate_days_until_expiration(yesterday_str)
            assert days < 0, "Days until yesterday should be negative (invalid date)"
            
            # Test expiring items with exact threshold boundaries
            items = [
                {"id": "F001", "name": "Item1", "expiration_date": today_str},
                {"id": "F002", "name": "Item2", "expiration_date": tomorrow_str},
                {"id": "F003", "name": "Item3", "expiration_date": (today + timedelta(days=7)).strftime("%Y-%m-%d")},
                {"id": "F004", "name": "Item4", "expiration_date": (today + timedelta(days=8)).strftime("%Y-%m-%d")}
            ]
            
            expiring = identify_expiring_items(items, 7)
            assert len(expiring) == 3, "Should include items expiring today, tomorrow, and exactly at threshold (7 days)"
            assert "F004" not in [item["id"] for item in expiring], "Should not include item beyond threshold"
            
            # Test validate_food_item with minimal valid item
            minimal_item = {
                "id": "F001",
                "name": "Test",
                "category": "Produce",
                "quantity": 0,  # Test with zero quantity
                "unit": "kg",
                "expiration_date": tomorrow_str,
                "storage_location": "Test"
            }
            result = validate_food_item(minimal_item)
            assert result["is_valid"] == True, "Minimal valid item with zero quantity should be valid"
            
            # Test category validation with all valid categories
            valid_categories = ["Produce", "Dairy", "Bakery", "Meat", "Frozen", "Canned", "Dry Goods", "Prepared"]
            for category in valid_categories:
                item = minimal_item.copy()
                item["category"] = category
                result = validate_food_item(item)
                assert result["is_valid"] == True, f"Should accept valid category: {category}"
            
            self.test_obj.yakshaAssert("TestBoundaryScenarios", True, "boundary")
        except Exception as e:
            self.test_obj.yakshaAssert("TestBoundaryScenarios", False, "boundary")
            pytest.fail(f"Boundary scenarios test failed: {str(e)}")

    def test_edge_case_filtering(self):
        """Test filtering with edge case inputs"""
        try:
            today = date.today()
            
            # Test sorting with identical dates
            same_date_items = [
                {"id": "F001", "name": "Item1", "expiration_date": "2023-12-15"},
                {"id": "F002", "name": "Item2", "expiration_date": "2023-12-15"}
            ]
            sorted_items = sort_items_by_expiration(same_date_items)
            assert len(sorted_items) == 2, "Should maintain all items when sorting with identical dates"
            
            # Test matching with exact category matches
            food_items = [
                {"id": "F001", "category": "Produce", "name": "Apples"},
                {"id": "F002", "category": "Dairy", "name": "Milk"},
                {"id": "F003", "category": "Bakery", "name": "Bread"}
            ]
            
            recipients = [
                {"id": "R001", "name": "Food Bank", "accepts_categories": ["Produce"]},
                {"id": "R002", "name": "Shelter", "accepts_categories": ["Dairy", "Bakery"]}
            ]
            
            matches = match_donations(food_items, recipients)
            assert len(matches) == 3, "All items should find a match"
            
            # Test with item missing category field
            items_missing_category = [
                {"id": "F001", "name": "Apples"},  # Missing category
                {"id": "F002", "category": "Dairy", "name": "Milk"}
            ]
            
            matches = match_donations(items_missing_category, recipients)
            assert len(matches) == 1, "Only items with category field should be matched"
            assert matches[0]["item"]["id"] == "F002", "Only item with category should be matched"
            
            # Test with recipient missing accepts_categories field
            recipients_missing_fields = [
                {"id": "R001", "name": "Food Bank"},  # Missing accepts_categories
                {"id": "R002", "name": "Shelter", "accepts_categories": ["Dairy"]}
            ]
            
            matches = match_donations(food_items, recipients_missing_fields)
            assert len(matches) == 1, "Only items matching recipients with accepts_categories should be matched"
            assert matches[0]["item"]["category"] == "Dairy", "Only Dairy should match"
            
            # Test format_food_item with missing fields
            valid_item = {
                "id": "F001",
                "name": "Apples",
                "quantity": 25,
                "unit": "kg",
                "expiration_date": "2023-12-15",
                "category": "Produce"
            }
            
            formatted = format_food_item(valid_item)
            assert "F001" in formatted and "Apples" in formatted, "Formatting should include item ID and name"
            
            invalid_item = {"id": "F001"}  # Missing most fields
            formatted = format_food_item(invalid_item)
            assert "Invalid" in formatted, "Should handle missing fields gracefully"
            
            self.test_obj.yakshaAssert("TestEdgeCaseFiltering", True, "boundary")
        except Exception as e:
            self.test_obj.yakshaAssert("TestEdgeCaseFiltering", False, "boundary")
            pytest.fail(f"Edge case filtering test failed: {str(e)}")

if __name__ == '__main__':
    pytest.main(['-v'])