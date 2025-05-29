"""
Exception handling tests for the Food Waste Reduction System.
"""

import pytest
import os
import importlib
import sys
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

def check_raises(func, args, expected_exception=Exception):
    """Check if a function raises an expected exception."""
    try:
        func(*args)
        return False
    except expected_exception:
        return True
    except Exception:
        return False

def test_input_validation(test_obj):
    """Test input validation and error handling"""
    errors = []
    
    # Check if module can be imported
    module_obj = safely_import_module("skeleton")
    if module_obj is None:
        module_obj = safely_import_module("solution")
    
    if module_obj is None:
        test_obj.yakshaAssert("TestInputValidation", False, "exception")
        pytest.fail("Could not import skeleton or solution module.")
        return
    
    try:
        # Test functions with None inputs
        functions_to_test = [
            ("validate_food_item", [None]),
            ("calculate_days_until_expiration", [None]),
            ("identify_expiring_items", [None, 7]),
            ("identify_expiring_items", [[{"id": "F001"}], None]),
            ("sort_items_by_expiration", [None]),
            ("match_donations", [None, [{"id": "R001"}]]),
            ("match_donations", [[{"id": "F001"}], None]),
            ("format_food_item", [None])
        ]
        
        for func_name, args in functions_to_test:
            if not check_function_exists(module_obj, func_name):
                errors.append(f"Function {func_name} not found")
                continue
            
            try:
                result = safely_call_function(module_obj, func_name, *args)
                
                # Check if the function handles None input appropriately
                if result is not None:
                    if isinstance(result, dict) and "is_valid" in result:
                        if result["is_valid"]:
                            errors.append(f"{func_name} should invalidate None input")
                    elif isinstance(result, list):
                        if result != []:
                            errors.append(f"{func_name} should return empty list for None input")
                    elif isinstance(result, str):
                        if "Invalid" not in result and "invalid" not in result.lower():
                            errors.append(f"{func_name} should indicate invalid input")
                    elif isinstance(result, int):
                        if result >= 0:
                            errors.append(f"{func_name} should return negative value for invalid date")
            except Exception:
                # Exception is acceptable for invalid input
                pass
        
        # Test validate_food_item with various invalid inputs
        if check_function_exists(module_obj, "validate_food_item"):
            # Invalid food item (missing required fields)
            invalid_item = {"id": "F001", "name": "Test Item"}
            result = safely_call_function(module_obj, "validate_food_item", invalid_item)
            
            if result is not None and isinstance(result, dict) and "is_valid" in result:
                if result["is_valid"]:
                    errors.append("validate_food_item should invalidate item missing required fields")
            
            # Invalid category
            invalid_category_item = {
                "id": "F001",
                "name": "Test Item",
                "category": "InvalidCategory",
                "quantity": 10,
                "unit": "kg",
                "expiration_date": "2023-12-15",
                "storage_location": "Test Location"
            }
            result = safely_call_function(module_obj, "validate_food_item", invalid_category_item)
            
            if result is not None and isinstance(result, dict) and "is_valid" in result:
                if result["is_valid"]:
                    errors.append("validate_food_item should invalidate item with invalid category")
            
            # Invalid quantity (negative)
            negative_quantity_item = {
                "id": "F001",
                "name": "Test Item",
                "category": "Produce",
                "quantity": -10,
                "unit": "kg",
                "expiration_date": "2023-12-15",
                "storage_location": "Test Location"
            }
            result = safely_call_function(module_obj, "validate_food_item", negative_quantity_item)
            
            if result is not None and isinstance(result, dict) and "is_valid" in result:
                if result["is_valid"]:
                    errors.append("validate_food_item should invalidate item with negative quantity")
            
            # Test with string instead of dict
            result = safely_call_function(module_obj, "validate_food_item", "not a dict")
            
            if result is not None and isinstance(result, dict) and "is_valid" in result:
                if result["is_valid"]:
                    errors.append("validate_food_item should invalidate non-dict input")
        else:
            errors.append("Function validate_food_item not found")
        
        # Test calculate_days_until_expiration with invalid date format
        if check_function_exists(module_obj, "calculate_days_until_expiration"):
            invalid_date = "12/15/2023"  # MM/DD/YYYY instead of YYYY-MM-DD
            days = safely_call_function(module_obj, "calculate_days_until_expiration", invalid_date)
            
            if days is not None and days >= 0:
                errors.append("calculate_days_until_expiration should return negative value for invalid date format")
            
            # Test with empty string
            days = safely_call_function(module_obj, "calculate_days_until_expiration", "")
            if days is not None and days >= 0:
                errors.append("calculate_days_until_expiration should return negative value for empty string")
        else:
            errors.append("Function calculate_days_until_expiration not found")
        
        # Test identify_expiring_items with invalid inputs
        if check_function_exists(module_obj, "identify_expiring_items"):
            # String instead of list for food_items
            expiring = safely_call_function(module_obj, "identify_expiring_items", "not a list", 7)
            
            if expiring is not None and expiring != []:
                errors.append("identify_expiring_items should return empty list for non-list input")
            
            # Invalid threshold
            valid_items = [{"id": "F001", "expiration_date": "2023-12-15"}]
            expiring = safely_call_function(module_obj, "identify_expiring_items", valid_items, "not a number")
            
            if expiring is None:
                errors.append("identify_expiring_items returned None for invalid threshold")
        else:
            errors.append("Function identify_expiring_items not found")
        
        # Test sort_items_by_expiration with invalid input
        if check_function_exists(module_obj, "sort_items_by_expiration"):
            sorted_items = safely_call_function(module_obj, "sort_items_by_expiration", "not a list")
            
            if sorted_items is not None and sorted_items != []:
                errors.append("sort_items_by_expiration should return empty list for non-list input")
        else:
            errors.append("Function sort_items_by_expiration not found")
        
        # Test match_donations with invalid inputs
        if check_function_exists(module_obj, "match_donations"):
            # Invalid food_items type
            matches = safely_call_function(module_obj, "match_donations", "not a list", [])
            
            if matches is not None and matches != []:
                errors.append("match_donations should return empty list for non-list food_items")
            
            # Invalid recipients type
            matches = safely_call_function(module_obj, "match_donations", [], "not a list")
            
            if matches is not None and matches != []:
                errors.append("match_donations should return empty list for non-list recipients")
        else:
            errors.append("Function match_donations not found")
        
        # Test format_food_item with invalid inputs
        if check_function_exists(module_obj, "format_food_item"):
            # String instead of dict
            formatted = safely_call_function(module_obj, "format_food_item", "not a dict")
            
            if formatted is not None and not isinstance(formatted, str):
                errors.append("format_food_item should return a string even for invalid input")
            
            # Empty dict
            formatted = safely_call_function(module_obj, "format_food_item", {})
            
            if formatted is not None and not isinstance(formatted, str):
                errors.append("format_food_item should return a string for empty dict")
        else:
            errors.append("Function format_food_item not found")
        
        # Final assertion
        if errors:
            test_obj.yakshaAssert("TestInputValidation", False, "exception")
            pytest.fail("\n".join(errors))
        else:
            test_obj.yakshaAssert("TestInputValidation", True, "exception")
    except Exception as e:
        test_obj.yakshaAssert("TestInputValidation", False, "exception")
        pytest.fail(f"Input validation test failed: {str(e)}")

def test_error_handling(test_obj):
    """Test specific error handling scenarios"""
    errors = []
    
    # Check if module can be imported
    module_obj = safely_import_module("skeleton")
    if module_obj is None:
        module_obj = safely_import_module("solution")
    
    if module_obj is None:
        test_obj.yakshaAssert("TestErrorHandling", False, "exception")
        pytest.fail("Could not import skeleton or solution module.")
        return
    
    try:
        # Test with valid inputs to confirm proper functionality
        valid_items = [
            {"id": "F001", "name": "Test", "expiration_date": "2023-12-15", "category": "Produce"},
            {"id": "F002", "name": "Test2", "expiration_date": "2023-12-10", "category": "Dairy"}
        ]
        
        if check_function_exists(module_obj, "sort_items_by_expiration"):
            sorted_items = safely_call_function(module_obj, "sort_items_by_expiration", valid_items)
            
            if sorted_items is not None:
                if len(sorted_items) != 2:
                    errors.append("sort_items_by_expiration should sort valid items correctly")
                elif sorted_items[0]["id"] != "F002":
                    errors.append("sort_items_by_expiration should sort by expiration date (earliest first)")
        else:
            errors.append("Function sort_items_by_expiration not found")
        
        valid_recipients = [
            {"id": "R001", "name": "Food Bank", "accepts_categories": ["Produce"]}
        ]
        
        if check_function_exists(module_obj, "match_donations"):
            matches = safely_call_function(module_obj, "match_donations", valid_items, valid_recipients)
            
            if matches is not None:
                if len(matches) != 1:
                    errors.append("match_donations should match only valid categories")
                elif len(matches) > 0 and matches[0]["item"]["id"] != "F001":
                    errors.append("match_donations should match the Produce item (F001)")
        else:
            errors.append("Function match_donations not found")
        
        # Test edge cases that should work
        if check_function_exists(module_obj, "identify_expiring_items"):
            # Test with items that have no expiration_date field
            items_no_date = [
                {"id": "F001", "name": "Test"},
                {"id": "F002", "name": "Test2", "expiration_date": "2023-12-15"}
            ]
            
            expiring = safely_call_function(module_obj, "identify_expiring_items", items_no_date, 7)
            if expiring is None:
                errors.append("identify_expiring_items returned None for items with missing expiration_date")
            else:
                # Should only include items that have expiration_date
                for item in expiring:
                    if "expiration_date" not in item:
                        errors.append("identify_expiring_items should skip items without expiration_date")
        else:
            errors.append("Function identify_expiring_items not found")
        
        # Test format_food_item with partial data
        if check_function_exists(module_obj, "format_food_item"):
            partial_item = {"id": "F001", "name": "Test"}
            formatted = safely_call_function(module_obj, "format_food_item", partial_item)
            
            if formatted is None:
                errors.append("format_food_item returned None for partial item")
            elif not isinstance(formatted, str):
                errors.append("format_food_item should return string for partial item")
        else:
            errors.append("Function format_food_item not found")
        
        # Test validate_food_item with edge cases
        if check_function_exists(module_obj, "validate_food_item"):
            # Test with zero quantity (should be valid)
            zero_quantity_item = {
                "id": "F001",
                "name": "Test Item",
                "category": "Produce",
                "quantity": 0,
                "unit": "kg",
                "expiration_date": "2023-12-15",
                "storage_location": "Test Location"
            }
            result = safely_call_function(module_obj, "validate_food_item", zero_quantity_item)
            
            if result is not None and isinstance(result, dict) and "is_valid" in result:
                if not result["is_valid"]:
                    errors.append("validate_food_item should accept zero quantity as valid")
        else:
            errors.append("Function validate_food_item not found")
        
        # Test calculate_days_until_expiration with edge cases
        if check_function_exists(module_obj, "calculate_days_until_expiration"):
            # Test with malformed date
            malformed_dates = ["2023-13-45", "abcd-ef-gh", "2023/12/15"]
            for bad_date in malformed_dates:
                days = safely_call_function(module_obj, "calculate_days_until_expiration", bad_date)
                if days is not None and days >= 0:
                    errors.append(f"calculate_days_until_expiration should return negative value for malformed date: {bad_date}")
        else:
            errors.append("Function calculate_days_until_expiration not found")
        
        # Test match_donations with malformed data
        if check_function_exists(module_obj, "match_donations"):
            # Items without category
            items_no_category = [{"id": "F001", "name": "Test"}]
            recipients_with_categories = [{"id": "R001", "accepts_categories": ["Produce"]}]
            
            matches = safely_call_function(module_obj, "match_donations", items_no_category, recipients_with_categories)
            if matches is None:
                errors.append("match_donations returned None for items without category")
            elif matches != []:
                errors.append("match_donations should return empty list when items have no category")
            
            # Recipients without accepts_categories
            items_with_category = [{"id": "F001", "category": "Produce"}]
            recipients_no_categories = [{"id": "R001", "name": "Test"}]
            
            matches = safely_call_function(module_obj, "match_donations", items_with_category, recipients_no_categories)
            if matches is None:
                errors.append("match_donations returned None for recipients without accepts_categories")
            elif matches != []:
                errors.append("match_donations should return empty list when recipients have no accepts_categories")
        else:
            errors.append("Function match_donations not found")
        
        # Final assertion
        if errors:
            test_obj.yakshaAssert("TestErrorHandling", False, "exception")
            pytest.fail("\n".join(errors))
        else:
            test_obj.yakshaAssert("TestErrorHandling", True, "exception")
    except Exception as e:
        test_obj.yakshaAssert("TestErrorHandling", False, "exception")
        pytest.fail(f"Error handling test failed: {str(e)}")

if __name__ == '__main__':
    pytest.main(['-v'])