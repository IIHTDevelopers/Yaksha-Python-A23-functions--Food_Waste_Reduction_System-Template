"""
Functional tests for the Food Waste Reduction System.
"""

import pytest
import os
import importlib
import sys
import inspect
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

def test_validate_food_item_functionality(test_obj):
    """Test validate_food_item functionality"""
    errors = []
    
    # Check if module can be imported
    module_obj = safely_import_module("skeleton")
    if module_obj is None:
        module_obj = safely_import_module("solution")
    
    if module_obj is None:
        test_obj.yakshaAssert("TestValidateFoodItemFunctionality", False, "functional")
        pytest.fail("Could not import skeleton or solution module.")
        return
    
    try:
        if not check_function_exists(module_obj, "validate_food_item"):
            errors.append("Function validate_food_item not found")
        else:
            # Test with valid item
            valid_item = {
                "id": "F001",
                "name": "Apples",
                "category": "Produce",
                "quantity": 25,
                "unit": "kg",
                "expiration_date": (date.today() + timedelta(days=5)).strftime("%Y-%m-%d"),
                "storage_location": "Cooler 3"
            }
            
            result = safely_call_function(module_obj, "validate_food_item", valid_item)
            if result is None:
                errors.append("validate_food_item returned None for valid item")
            elif not isinstance(result, dict) or "is_valid" not in result:
                errors.append("validate_food_item should return dict with is_valid key")
            elif not result["is_valid"]:
                errors.append("Valid item should be validated as valid")
            elif "message" not in result:
                errors.append("validate_food_item should return dict with message key")
            elif "valid" not in result["message"].lower():
                errors.append("Message should indicate item is valid")
            
            # Test with invalid item (missing fields)
            invalid_item = {"id": "F003", "name": "Bread"}
            result = safely_call_function(module_obj, "validate_food_item", invalid_item)
            if result is None:
                errors.append("validate_food_item returned None for invalid item")
            elif not isinstance(result, dict) or "is_valid" not in result:
                errors.append("validate_food_item should return dict with is_valid key for invalid item")
            elif result["is_valid"]:
                errors.append("Invalid item should be validated as invalid")
        
        # Final assertion
        if errors:
            test_obj.yakshaAssert("TestValidateFoodItemFunctionality", False, "functional")
            pytest.fail("\n".join(errors))
        else:
            test_obj.yakshaAssert("TestValidateFoodItemFunctionality", True, "functional")
    except Exception as e:
        test_obj.yakshaAssert("TestValidateFoodItemFunctionality", False, "functional")
        pytest.fail(f"Validate food item functionality test failed: {str(e)}")

def test_calculate_days_functionality(test_obj):
    """Test calculate_days_until_expiration functionality"""
    errors = []
    
    # Check if module can be imported
    module_obj = safely_import_module("skeleton")
    if module_obj is None:
        module_obj = safely_import_module("solution")
    
    if module_obj is None:
        test_obj.yakshaAssert("TestCalculateDaysFunctionality", False, "functional")
        pytest.fail("Could not import skeleton or solution module.")
        return
    
    try:
        if not check_function_exists(module_obj, "calculate_days_until_expiration"):
            errors.append("Function calculate_days_until_expiration not found")
        else:
            future_date = (date.today() + timedelta(days=5)).strftime("%Y-%m-%d")
            days = safely_call_function(module_obj, "calculate_days_until_expiration", future_date)
            
            if days is None:
                errors.append("calculate_days_until_expiration returned None")
            elif not isinstance(days, int):
                errors.append("calculate_days_until_expiration should return an integer")
            elif days != 5:
                errors.append(f"Days until {future_date} should be 5, got {days}")
            
            # Test with past date
            past_date = (date.today() - timedelta(days=3)).strftime("%Y-%m-%d")
            days = safely_call_function(module_obj, "calculate_days_until_expiration", past_date)
            
            if days is None:
                errors.append("calculate_days_until_expiration returned None for past date")
            elif days != -3:
                errors.append(f"Days until past date should be -3, got {days}")
        
        # Final assertion
        if errors:
            test_obj.yakshaAssert("TestCalculateDaysFunctionality", False, "functional")
            pytest.fail("\n".join(errors))
        else:
            test_obj.yakshaAssert("TestCalculateDaysFunctionality", True, "functional")
    except Exception as e:
        test_obj.yakshaAssert("TestCalculateDaysFunctionality", False, "functional")
        pytest.fail(f"Calculate days functionality test failed: {str(e)}")

def test_identify_expiring_items_functionality(test_obj):
    """Test identify_expiring_items functionality"""
    errors = []
    
    # Check if module can be imported
    module_obj = safely_import_module("skeleton")
    if module_obj is None:
        module_obj = safely_import_module("solution")
    
    if module_obj is None:
        test_obj.yakshaAssert("TestIdentifyExpiringItemsFunctionality", False, "functional")
        pytest.fail("Could not import skeleton or solution module.")
        return
    
    try:
        if not check_function_exists(module_obj, "identify_expiring_items"):
            errors.append("Function identify_expiring_items not found")
        else:
            today = date.today()
            test_inventory = [
                {
                    "id": "F001",
                    "name": "Apples",
                    "expiration_date": (today + timedelta(days=5)).strftime("%Y-%m-%d")
                },
                {
                    "id": "F002",
                    "name": "Milk",
                    "expiration_date": (today + timedelta(days=2)).strftime("%Y-%m-%d")
                },
                {
                    "id": "F003",
                    "name": "Bread",
                    "expiration_date": (today + timedelta(days=10)).strftime("%Y-%m-%d")
                }
            ]
            
            expiring = safely_call_function(module_obj, "identify_expiring_items", test_inventory, 3)
            if expiring is None:
                errors.append("identify_expiring_items returned None")
            elif not isinstance(expiring, list):
                errors.append("identify_expiring_items should return a list")
            elif len(expiring) != 1:
                errors.append(f"Should identify 1 item expiring within 3 days, got {len(expiring)}")
            elif len(expiring) > 0 and expiring[0]["id"] != "F002":
                errors.append("Milk (F002) expires soonest and should be identified")
            
            # Test with larger threshold
            expiring = safely_call_function(module_obj, "identify_expiring_items", test_inventory, 7)
            if expiring is None:
                errors.append("identify_expiring_items returned None for larger threshold")
            elif len(expiring) != 2:
                errors.append(f"Should identify 2 items expiring within 7 days, got {len(expiring)}")
        
        # Final assertion
        if errors:
            test_obj.yakshaAssert("TestIdentifyExpiringItemsFunctionality", False, "functional")
            pytest.fail("\n".join(errors))
        else:
            test_obj.yakshaAssert("TestIdentifyExpiringItemsFunctionality", True, "functional")
    except Exception as e:
        test_obj.yakshaAssert("TestIdentifyExpiringItemsFunctionality", False, "functional")
        pytest.fail(f"Identify expiring items functionality test failed: {str(e)}")

def test_sort_items_functionality(test_obj):
    """Test sort_items_by_expiration functionality"""
    errors = []
    
    # Check if module can be imported
    module_obj = safely_import_module("skeleton")
    if module_obj is None:
        module_obj = safely_import_module("solution")
    
    if module_obj is None:
        test_obj.yakshaAssert("TestSortItemsFunctionality", False, "functional")
        pytest.fail("Could not import skeleton or solution module.")
        return
    
    try:
        if not check_function_exists(module_obj, "sort_items_by_expiration"):
            errors.append("Function sort_items_by_expiration not found")
        else:
            today = date.today()
            test_inventory = [
                {
                    "id": "F001",
                    "name": "Apples",
                    "expiration_date": (today + timedelta(days=5)).strftime("%Y-%m-%d")
                },
                {
                    "id": "F002",
                    "name": "Milk",
                    "expiration_date": (today + timedelta(days=2)).strftime("%Y-%m-%d")
                },
                {
                    "id": "F003",
                    "name": "Bread",
                    "expiration_date": (today + timedelta(days=1)).strftime("%Y-%m-%d")
                }
            ]
            
            sorted_items = safely_call_function(module_obj, "sort_items_by_expiration", test_inventory)
            if sorted_items is None:
                errors.append("sort_items_by_expiration returned None")
            elif not isinstance(sorted_items, list):
                errors.append("sort_items_by_expiration should return a list")
            elif len(sorted_items) != 3:
                errors.append(f"Should return all 3 items, got {len(sorted_items)}")
            elif sorted_items[0]["id"] != "F003":
                errors.append("Bread (F003) expires first and should be first in sorted list")
            elif sorted_items[1]["id"] != "F002":
                errors.append("Milk (F002) expires second and should be second in sorted list")
            elif sorted_items[2]["id"] != "F001":
                errors.append("Apples (F001) expire last and should be last in sorted list")
        
        # Final assertion
        if errors:
            test_obj.yakshaAssert("TestSortItemsFunctionality", False, "functional")
            pytest.fail("\n".join(errors))
        else:
            test_obj.yakshaAssert("TestSortItemsFunctionality", True, "functional")
    except Exception as e:
        test_obj.yakshaAssert("TestSortItemsFunctionality", False, "functional")
        pytest.fail(f"Sort items functionality test failed: {str(e)}")

def test_match_donations_functionality(test_obj):
    """Test match_donations functionality"""
    errors = []
    
    # Check if module can be imported
    module_obj = safely_import_module("skeleton")
    if module_obj is None:
        module_obj = safely_import_module("solution")
    
    if module_obj is None:
        test_obj.yakshaAssert("TestMatchDonationsFunctionality", False, "functional")
        pytest.fail("Could not import skeleton or solution module.")
        return
    
    try:
        if not check_function_exists(module_obj, "match_donations"):
            errors.append("Function match_donations not found")
        else:
            test_inventory = [
                {"id": "F001", "name": "Apples", "category": "Produce"},
                {"id": "F002", "name": "Milk", "category": "Dairy"},
                {"id": "F003", "name": "Bread", "category": "Bakery"}
            ]
            
            test_recipients = [
                {"id": "R001", "name": "City Food Bank", "accepts_categories": ["Produce", "Bakery"]},
                {"id": "R002", "name": "Community Shelter", "accepts_categories": ["Dairy", "Prepared"]}
            ]
            
            matches = safely_call_function(module_obj, "match_donations", test_inventory, test_recipients)
            if matches is None:
                errors.append("match_donations returned None")
            elif not isinstance(matches, list):
                errors.append("match_donations should return a list")
            elif len(matches) != 3:
                errors.append(f"Should match all 3 items, got {len(matches)} matches")
            else:
                # Check specific matches
                found_apple_match = False
                found_milk_match = False
                found_bread_match = False
                
                for match in matches:
                    if not isinstance(match, dict) or "item" not in match or "recipient" not in match:
                        errors.append("Each match should be a dict with 'item' and 'recipient' keys")
                        continue
                    
                    item_id = match["item"]["id"] if "id" in match["item"] else None
                    recipient_id = match["recipient"]["id"] if "id" in match["recipient"] else None
                    
                    if item_id == "F001" and recipient_id == "R001":
                        found_apple_match = True
                    elif item_id == "F002" and recipient_id == "R002":
                        found_milk_match = True
                    elif item_id == "F003" and recipient_id == "R001":
                        found_bread_match = True
                
                if not found_apple_match:
                    errors.append("Apples (Produce) should match with City Food Bank")
                if not found_milk_match:
                    errors.append("Milk (Dairy) should match with Community Shelter")
                if not found_bread_match:
                    errors.append("Bread (Bakery) should match with City Food Bank")
        
        # Final assertion
        if errors:
            test_obj.yakshaAssert("TestMatchDonationsFunctionality", False, "functional")
            pytest.fail("\n".join(errors))
        else:
            test_obj.yakshaAssert("TestMatchDonationsFunctionality", True, "functional")
    except Exception as e:
        test_obj.yakshaAssert("TestMatchDonationsFunctionality", False, "functional")
        pytest.fail(f"Match donations functionality test failed: {str(e)}")

def test_format_food_item_functionality(test_obj):
    """Test format_food_item functionality"""
    errors = []
    
    # Check if module can be imported
    module_obj = safely_import_module("skeleton")
    if module_obj is None:
        module_obj = safely_import_module("solution")
    
    if module_obj is None:
        test_obj.yakshaAssert("TestFormatFoodItemFunctionality", False, "functional")
        pytest.fail("Could not import skeleton or solution module.")
        return
    
    try:
        if not check_function_exists(module_obj, "format_food_item"):
            errors.append("Function format_food_item not found")
        else:
            test_item = {
                "id": "F001",
                "name": "Apples",
                "quantity": 25,
                "unit": "kg",
                "expiration_date": "2023-12-15",
                "category": "Produce"
            }
            
            formatted = safely_call_function(module_obj, "format_food_item", test_item)
            if formatted is None:
                errors.append("format_food_item returned None")
            elif not isinstance(formatted, str):
                errors.append("format_food_item should return a string")
            else:
                # Check if formatted string contains key information
                if "F001" not in formatted:
                    errors.append("Formatted string should include item ID (F001)")
                if "Apples" not in formatted:
                    errors.append("Formatted string should include item name (Apples)")
                if "25" not in formatted or "kg" not in formatted:
                    errors.append("Formatted string should include quantity and unit (25 kg)")
                if "Produce" not in formatted:
                    errors.append("Formatted string should include category (Produce)")
                if "2023-12-15" not in formatted:
                    errors.append("Formatted string should include expiration date (2023-12-15)")
        
        # Final assertion
        if errors:
            test_obj.yakshaAssert("TestFormatFoodItemFunctionality", False, "functional")
            pytest.fail("\n".join(errors))
        else:
            test_obj.yakshaAssert("TestFormatFoodItemFunctionality", True, "functional")
    except Exception as e:
        test_obj.yakshaAssert("TestFormatFoodItemFunctionality", False, "functional")
        pytest.fail(f"Format food item functionality test failed: {str(e)}")

def test_function_signatures_and_docstrings(test_obj):
    """Test that functions have proper signatures and docstrings"""
    errors = []
    
    # Check if module can be imported
    module_obj = safely_import_module("skeleton")
    if module_obj is None:
        module_obj = safely_import_module("solution")
    
    if module_obj is None:
        test_obj.yakshaAssert("TestFunctionSignaturesAndDocstrings", False, "functional")
        pytest.fail("Could not import skeleton or solution module.")
        return
    
    try:
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
                continue
            
            try:
                func = getattr(module_obj, func_name)
                
                # Check if function has docstring
                if not func.__doc__:
                    errors.append(f"Function {func_name} should have a docstring")
                else:
                    docstring = func.__doc__.strip()
                    if len(docstring) < 20:
                        errors.append(f"Function {func_name} should have a meaningful docstring")
                    
                    # Check for basic docstring components
                    if "Parameters:" not in docstring and "Args:" not in docstring:
                        errors.append(f"Function {func_name} docstring should document parameters")
                    
                    if "Returns:" not in docstring and "Return:" not in docstring:
                        errors.append(f"Function {func_name} docstring should document return value")
                
                # Check function signature
                try:
                    sig = inspect.signature(func)
                    params = list(sig.parameters.keys())
                    
                    if func_name == "validate_food_item":
                        if len(params) < 1 or "food_item" not in params[0]:
                            errors.append(f"Function {func_name} should have food_item parameter")
                    
                    elif func_name == "calculate_days_until_expiration":
                        if len(params) < 1 or "expiration_date" not in params[0]:
                            errors.append(f"Function {func_name} should have expiration_date parameter")
                    
                    elif func_name == "identify_expiring_items":
                        if len(params) < 1 or "food_items" not in params[0]:
                            errors.append(f"Function {func_name} should have food_items parameter")
                    
                    elif func_name == "sort_items_by_expiration":
                        if len(params) < 1 or "food_items" not in params[0]:
                            errors.append(f"Function {func_name} should have food_items parameter")
                    
                    elif func_name == "match_donations":
                        if len(params) < 2:
                            errors.append(f"Function {func_name} should have at least 2 parameters")
                        elif "food_items" not in params[0] or "recipients" not in params[1]:
                            errors.append(f"Function {func_name} should have food_items and recipients parameters")
                    
                    elif func_name == "format_food_item":
                        if len(params) < 1 or "food_item" not in params[0]:
                            errors.append(f"Function {func_name} should have food_item parameter")
                            
                except Exception as e:
                    errors.append(f"Error checking signature for {func_name}: {str(e)}")
                    
            except Exception as e:
                errors.append(f"Error checking function {func_name}: {str(e)}")
        
        # Check for main function
        if check_function_exists(module_obj, "main"):
            main_func = getattr(module_obj, "main")
            if not main_func.__doc__:
                errors.append("Main function should have a docstring")
        else:
            errors.append("Function main not found")
        
        # Final assertion
        if errors:
            test_obj.yakshaAssert("TestFunctionSignaturesAndDocstrings", False, "functional")
            pytest.fail("\n".join(errors))
        else:
            test_obj.yakshaAssert("TestFunctionSignaturesAndDocstrings", True, "functional")
    except Exception as e:
        test_obj.yakshaAssert("TestFunctionSignaturesAndDocstrings", False, "functional")
        pytest.fail(f"Function signatures and docstrings test failed: {str(e)}")

if __name__ == '__main__':
    pytest.main(['-v'])