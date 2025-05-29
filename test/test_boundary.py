"""
Boundary tests for the Food Waste Reduction System.
"""

import pytest
import os
import importlib
import sys
from datetime import datetime, date, timedelta
from test.TestUtils import TestUtils

@pytest.fixture
def test_obj():
    return TestUtils()

def check_file_exists(filename):
    """Check if a file exists in the current directory."""
    return os.path.exists(filename)

def safely_import_module(module_name):
    """Safely import a module, returning None if import fails."""
    try:
        return importlib.import_module(module_name)
    except ImportError:
        return None

def check_function_exists(module, function_name):
    """Check if a function exists in a module."""
    return hasattr(module, function_name) and callable(getattr(module, function_name))

def safely_call_function(module, function_name, *args, **kwargs):
    """Safely call a function, returning None if it fails."""
    if not check_function_exists(module, function_name):
        return None
    try:
        return getattr(module, function_name)(*args, **kwargs)
    except Exception:
        return None

def test_boundary_scenarios(test_obj):
    """Test boundary scenarios for food waste reduction system"""
    errors = []
    
    # Check if module can be imported
    module_obj = safely_import_module("skeleton")
    if module_obj is None:
        module_obj = safely_import_module("solution")
    
    if module_obj is None:
        test_obj.yakshaAssert("TestBoundaryScenarios", False, "boundary")
        pytest.fail("Could not import skeleton or solution module.")
        return
    
    try:
        # Check required functions exist
        required_functions = [
            "validate_food_item",
            "calculate_days_until_expiration", 
            "identify_expiring_items",
            "sort_items_by_expiration",
            "match_donations",
            "format_food_item"
        ]
        
        for func_name in required_functions:
            if not check_function_exists(module_obj, func_name):
                errors.append(f"Function {func_name} not found")
        
        # Test with empty food items list
        empty_food_items = []
        
        # Test identify_expiring_items with empty list
        if check_function_exists(module_obj, "identify_expiring_items"):
            expiring = safely_call_function(module_obj, "identify_expiring_items", empty_food_items, 7)
            if expiring is None:
                errors.append("identify_expiring_items returned None for empty list")
            elif expiring != []:
                errors.append("identify_expiring_items should return empty list for empty input")
        else:
            errors.append("Function identify_expiring_items not found")
        
        # Test sort_items_by_expiration with empty list
        if check_function_exists(module_obj, "sort_items_by_expiration"):
            sorted_items = safely_call_function(module_obj, "sort_items_by_expiration", empty_food_items)
            if sorted_items is None:
                errors.append("sort_items_by_expiration returned None for empty list")
            elif sorted_items != []:
                errors.append("sort_items_by_expiration should return empty list for empty input")
        else:
            errors.append("Function sort_items_by_expiration not found")
        
        # Test match_donations with empty food items list
        if check_function_exists(module_obj, "match_donations"):
            empty_recipients = [{"id": "R001", "name": "Food Bank", "accepts_categories": ["Produce"]}]
            matches = safely_call_function(module_obj, "match_donations", empty_food_items, empty_recipients)
            if matches is None:
                errors.append("match_donations returned None for empty food items list")
            elif matches != []:
                errors.append("match_donations should return empty list for empty food items")
            
            # Test with empty recipients list
            test_items = [{"id": "F001", "category": "Produce", "name": "Apples"}]
            matches = safely_call_function(module_obj, "match_donations", test_items, [])
            if matches is None:
                errors.append("match_donations returned None for empty recipients list")
            elif matches != []:
                errors.append("match_donations should return empty list for empty recipients")
        else:
            errors.append("Function match_donations not found")
        
        # Test calculate_days_until_expiration with various dates
        if check_function_exists(module_obj, "calculate_days_until_expiration"):
            today = date.today()
            today_str = today.strftime("%Y-%m-%d")
            tomorrow_str = (today + timedelta(days=1)).strftime("%Y-%m-%d")
            yesterday_str = (today - timedelta(days=1)).strftime("%Y-%m-%d")
            
            days_today = safely_call_function(module_obj, "calculate_days_until_expiration", today_str)
            if days_today is None:
                errors.append("calculate_days_until_expiration returned None for today's date")
            elif days_today != 0:
                errors.append(f"Days until today should be 0, got {days_today}")
            
            days_tomorrow = safely_call_function(module_obj, "calculate_days_until_expiration", tomorrow_str)
            if days_tomorrow is None:
                errors.append("calculate_days_until_expiration returned None for tomorrow's date")
            elif days_tomorrow != 1:
                errors.append(f"Days until tomorrow should be 1, got {days_tomorrow}")
            
            days_yesterday = safely_call_function(module_obj, "calculate_days_until_expiration", yesterday_str)
            if days_yesterday is None:
                errors.append("calculate_days_until_expiration returned None for yesterday's date")
            elif days_yesterday >= 0:
                errors.append(f"Days until yesterday should be negative, got {days_yesterday}")
        else:
            errors.append("Function calculate_days_until_expiration not found")
        
        # Test expiring items with exact threshold boundaries
        if check_function_exists(module_obj, "identify_expiring_items"):
            today = date.today()
            items = [
                {"id": "F001", "name": "Item1", "expiration_date": today.strftime("%Y-%m-%d")},
                {"id": "F002", "name": "Item2", "expiration_date": (today + timedelta(days=1)).strftime("%Y-%m-%d")},
                {"id": "F003", "name": "Item3", "expiration_date": (today + timedelta(days=7)).strftime("%Y-%m-%d")},
                {"id": "F004", "name": "Item4", "expiration_date": (today + timedelta(days=8)).strftime("%Y-%m-%d")}
            ]
            
            expiring = safely_call_function(module_obj, "identify_expiring_items", items, 7)
            if expiring is None:
                errors.append("identify_expiring_items returned None for valid items list")
            else:
                if len(expiring) != 3:
                    errors.append(f"Should identify 3 items expiring within 7 days, got {len(expiring)}")
                
                item_ids = [item["id"] for item in expiring] if expiring else []
                if "F004" in item_ids:
                    errors.append("Should not include item beyond threshold (F004)")
        
        # Test validate_food_item with minimal valid item
        if check_function_exists(module_obj, "validate_food_item"):
            minimal_item = {
                "id": "F001",
                "name": "Test",
                "category": "Produce",
                "quantity": 0,
                "unit": "kg",
                "expiration_date": (date.today() + timedelta(days=1)).strftime("%Y-%m-%d"),
                "storage_location": "Test"
            }
            result = safely_call_function(module_obj, "validate_food_item", minimal_item)
            if result is None:
                errors.append("validate_food_item returned None for minimal valid item")
            elif not isinstance(result, dict) or "is_valid" not in result:
                errors.append("validate_food_item should return dict with is_valid key")
            elif not result["is_valid"]:
                errors.append("Minimal valid item with zero quantity should be valid")
            
            # Test all valid categories
            valid_categories = ["Produce", "Dairy", "Bakery", "Meat", "Frozen", "Canned", "Dry Goods", "Prepared"]
            for category in valid_categories:
                item = minimal_item.copy()
                item["category"] = category
                result = safely_call_function(module_obj, "validate_food_item", item)
                if result is None:
                    errors.append(f"validate_food_item returned None for category: {category}")
                    continue
                
                if not isinstance(result, dict) or "is_valid" not in result:
                    errors.append(f"validate_food_item should return dict with is_valid key for category: {category}")
                    continue
                
                if not result["is_valid"]:
                    errors.append(f"Should accept valid category: {category}")
        else:
            errors.append("Function validate_food_item not found")
        
        # Final assertion
        if errors:
            test_obj.yakshaAssert("TestBoundaryScenarios", False, "boundary")
            pytest.fail("\n".join(errors))
        else:
            test_obj.yakshaAssert("TestBoundaryScenarios", True, "boundary")
            
    except Exception as e:
        test_obj.yakshaAssert("TestBoundaryScenarios", False, "boundary")
        pytest.fail(f"Boundary scenarios test failed: {str(e)}")

def test_edge_case_filtering(test_obj):
    """Test filtering with edge case inputs"""
    errors = []
    
    # Check if module can be imported
    module_obj = safely_import_module("skeleton")
    if module_obj is None:
        module_obj = safely_import_module("solution")
    
    if module_obj is None:
        test_obj.yakshaAssert("TestEdgeCaseFiltering", False, "boundary")
        pytest.fail("Could not import skeleton or solution module.")
        return
    
    try:
        # Test sorting with identical dates
        if check_function_exists(module_obj, "sort_items_by_expiration"):
            same_date_items = [
                {"id": "F001", "name": "Item1", "expiration_date": "2023-12-15"},
                {"id": "F002", "name": "Item2", "expiration_date": "2023-12-15"}
            ]
            sorted_items = safely_call_function(module_obj, "sort_items_by_expiration", same_date_items)
            if sorted_items is None:
                errors.append("sort_items_by_expiration returned None for items with identical dates")
            elif len(sorted_items) != 2:
                errors.append("Should maintain all items when sorting with identical dates")
        else:
            errors.append("Function sort_items_by_expiration not found")
        
        # Test matching with exact category matches
        if check_function_exists(module_obj, "match_donations"):
            food_items = [
                {"id": "F001", "category": "Produce", "name": "Apples"},
                {"id": "F002", "category": "Dairy", "name": "Milk"},
                {"id": "F003", "category": "Bakery", "name": "Bread"}
            ]
            
            recipients = [
                {"id": "R001", "name": "Food Bank", "accepts_categories": ["Produce"]},
                {"id": "R002", "name": "Shelter", "accepts_categories": ["Dairy", "Bakery"]}
            ]
            
            matches = safely_call_function(module_obj, "match_donations", food_items, recipients)
            if matches is None:
                errors.append("match_donations returned None for valid items and recipients")
            elif len(matches) != 3:
                errors.append(f"All items should find a match, got {len(matches)} matches")
            
            # Test with item missing category field
            items_missing_category = [
                {"id": "F001", "name": "Apples"},
                {"id": "F002", "category": "Dairy", "name": "Milk"}
            ]
            
            matches = safely_call_function(module_obj, "match_donations", items_missing_category, recipients)
            if matches is None:
                errors.append("match_donations returned None for items with missing category")
            else:
                if len(matches) > 1:
                    errors.append("Only items with category field should be matched")
            
            # Test with recipient missing accepts_categories field
            recipients_missing_fields = [
                {"id": "R001", "name": "Food Bank"},
                {"id": "R002", "name": "Shelter", "accepts_categories": ["Dairy"]}
            ]
            
            matches = safely_call_function(module_obj, "match_donations", food_items, recipients_missing_fields)
            if matches is None:
                errors.append("match_donations returned None for recipients with missing accepts_categories")
            else:
                if len(matches) > 1:
                    errors.append("Only items matching recipients with accepts_categories should be matched")
        else:
            errors.append("Function match_donations not found")
        
        # Test format_food_item with missing fields
        if check_function_exists(module_obj, "format_food_item"):
            valid_item = {
                "id": "F001",
                "name": "Apples",
                "quantity": 25,
                "unit": "kg",
                "expiration_date": "2023-12-15",
                "category": "Produce"
            }
            
            formatted = safely_call_function(module_obj, "format_food_item", valid_item)
            if formatted is None:
                errors.append("format_food_item returned None for valid item")
            elif not isinstance(formatted, str):
                errors.append("format_food_item should return a string")
            elif "F001" not in formatted or "Apples" not in formatted:
                errors.append("Formatting should include item ID and name")
            
            invalid_item = {"id": "F001"}
            formatted = safely_call_function(module_obj, "format_food_item", invalid_item)
            if formatted is None:
                errors.append("format_food_item returned None for invalid item")
            elif not isinstance(formatted, str):
                errors.append("format_food_item should return a string even for invalid items")
            elif "Invalid" not in formatted and "invalid" not in formatted.lower():
                errors.append("Should handle missing fields gracefully")
        else:
            errors.append("Function format_food_item not found")
        
        # Final assertion
        if errors:
            test_obj.yakshaAssert("TestEdgeCaseFiltering", False, "boundary")
            pytest.fail("\n".join(errors))
        else:
            test_obj.yakshaAssert("TestEdgeCaseFiltering", True, "boundary")
            
    except Exception as e:
        test_obj.yakshaAssert("TestEdgeCaseFiltering", False, "boundary")
        pytest.fail(f"Edge case filtering test failed: {str(e)}")

if __name__ == '__main__':
    pytest.main(['-v'])