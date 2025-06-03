"""
Functional tests for the Food Waste Reduction System.
"""

import unittest
import os
import importlib
import sys
import inspect
import warnings
from datetime import datetime, date, timedelta
from test.TestUtils import TestUtils

# Configure warnings
warnings.filterwarnings("ignore")

class TestFunctional(unittest.TestCase):

    def check_file_exists(self, filename):
        """Check if a file exists in the current directory."""
        return os.path.exists(filename)

    def safely_import_module(self, module_name):
        """Safely import a module, returning None if import fails."""
        try:
            return importlib.import_module(module_name)
        except ImportError:
            return None

    def check_function_exists(self, module, function_name):
        """Check if a function exists in a module."""
        return hasattr(module, function_name) and callable(getattr(module, function_name))

    def safely_call_function(self, module, function_name, *args, **kwargs):
        """Safely call a function, returning None if it fails."""
        if not self.check_function_exists(module, function_name):
            return None
        try:
            return getattr(module, function_name)(*args, **kwargs)
        except Exception:
            return None

    def test_validate_food_item_functionality(self):
        """Test validate_food_item functionality"""
        test_obj = TestUtils()
        try:
            # Check if module can be imported
            module_obj = self.safely_import_module("skeleton")
            if module_obj is None:
                module_obj = self.safely_import_module("solution")
            
            if module_obj is None:
                test_obj.yakshaAssert("TestValidateFoodItemFunctionality", False, "functional")
                print("TestValidateFoodItemFunctionality = Failed")
                return
            
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
            
            result = self.safely_call_function(module_obj, "validate_food_item", valid_item)
            if result is None or not isinstance(result, dict) or "is_valid" not in result or not result["is_valid"]:
                test_obj.yakshaAssert("TestValidateFoodItemFunctionality", False, "functional")
                print("TestValidateFoodItemFunctionality = Failed")
                return
            
            # Test with invalid item (missing fields)
            invalid_item = {"id": "F003", "name": "Bread"}
            result = self.safely_call_function(module_obj, "validate_food_item", invalid_item)
            if result is None or not isinstance(result, dict) or "is_valid" not in result or result["is_valid"]:
                test_obj.yakshaAssert("TestValidateFoodItemFunctionality", False, "functional")
                print("TestValidateFoodItemFunctionality = Failed")
                return
            
            test_obj.yakshaAssert("TestValidateFoodItemFunctionality", True, "functional")
            print("TestValidateFoodItemFunctionality = Passed")
        except:
            test_obj.yakshaAssert("TestValidateFoodItemFunctionality", False, "functional")
            print("TestValidateFoodItemFunctionality = Failed")

    def test_calculate_days_functionality(self):
        """Test calculate_days_until_expiration functionality"""
        test_obj = TestUtils()
        try:
            # Check if module can be imported
            module_obj = self.safely_import_module("skeleton")
            if module_obj is None:
                module_obj = self.safely_import_module("solution")
            
            if module_obj is None:
                test_obj.yakshaAssert("TestCalculateDaysFunctionality", False, "functional")
                print("TestCalculateDaysFunctionality = Failed")
                return
            
            future_date = (date.today() + timedelta(days=5)).strftime("%Y-%m-%d")
            days = self.safely_call_function(module_obj, "calculate_days_until_expiration", future_date)
            
            if days is None or not isinstance(days, int) or days != 5:
                test_obj.yakshaAssert("TestCalculateDaysFunctionality", False, "functional")
                print("TestCalculateDaysFunctionality = Failed")
                return
            
            # Test with past date
            past_date = (date.today() - timedelta(days=3)).strftime("%Y-%m-%d")
            days = self.safely_call_function(module_obj, "calculate_days_until_expiration", past_date)
            
            if days is None or days != -3:
                test_obj.yakshaAssert("TestCalculateDaysFunctionality", False, "functional")
                print("TestCalculateDaysFunctionality = Failed")
                return
            
            test_obj.yakshaAssert("TestCalculateDaysFunctionality", True, "functional")
            print("TestCalculateDaysFunctionality = Passed")
        except:
            test_obj.yakshaAssert("TestCalculateDaysFunctionality", False, "functional")
            print("TestCalculateDaysFunctionality = Failed")

    def test_identify_expiring_items_functionality(self):
        """Test identify_expiring_items functionality"""
        test_obj = TestUtils()
        try:
            # Check if module can be imported
            module_obj = self.safely_import_module("skeleton")
            if module_obj is None:
                module_obj = self.safely_import_module("solution")
            
            if module_obj is None:
                test_obj.yakshaAssert("TestIdentifyExpiringItemsFunctionality", False, "functional")
                print("TestIdentifyExpiringItemsFunctionality = Failed")
                return
            
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
            
            expiring = self.safely_call_function(module_obj, "identify_expiring_items", test_inventory, 3)
            if expiring is None or not isinstance(expiring, list) or len(expiring) != 1 or expiring[0]["id"] != "F002":
                test_obj.yakshaAssert("TestIdentifyExpiringItemsFunctionality", False, "functional")
                print("TestIdentifyExpiringItemsFunctionality = Failed")
                return
            
            # Test with larger threshold
            expiring = self.safely_call_function(module_obj, "identify_expiring_items", test_inventory, 7)
            if expiring is None or len(expiring) != 2:
                test_obj.yakshaAssert("TestIdentifyExpiringItemsFunctionality", False, "functional")
                print("TestIdentifyExpiringItemsFunctionality = Failed")
                return
            
            test_obj.yakshaAssert("TestIdentifyExpiringItemsFunctionality", True, "functional")
            print("TestIdentifyExpiringItemsFunctionality = Passed")
        except:
            test_obj.yakshaAssert("TestIdentifyExpiringItemsFunctionality", False, "functional")
            print("TestIdentifyExpiringItemsFunctionality = Failed")

    def test_sort_items_functionality(self):
        """Test sort_items_by_expiration functionality"""
        test_obj = TestUtils()
        try:
            # Check if module can be imported
            module_obj = self.safely_import_module("skeleton")
            if module_obj is None:
                module_obj = self.safely_import_module("solution")
            
            if module_obj is None:
                test_obj.yakshaAssert("TestSortItemsFunctionality", False, "functional")
                print("TestSortItemsFunctionality = Failed")
                return
            
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
            
            sorted_items = self.safely_call_function(module_obj, "sort_items_by_expiration", test_inventory)
            if (sorted_items is None or not isinstance(sorted_items, list) or len(sorted_items) != 3 or 
                sorted_items[0]["id"] != "F003" or sorted_items[1]["id"] != "F002" or sorted_items[2]["id"] != "F001"):
                test_obj.yakshaAssert("TestSortItemsFunctionality", False, "functional")
                print("TestSortItemsFunctionality = Failed")
                return
            
            test_obj.yakshaAssert("TestSortItemsFunctionality", True, "functional")
            print("TestSortItemsFunctionality = Passed")
        except:
            test_obj.yakshaAssert("TestSortItemsFunctionality", False, "functional")
            print("TestSortItemsFunctionality = Failed")

    def test_match_donations_functionality(self):
        """Test match_donations functionality"""
        test_obj = TestUtils()
        try:
            # Check if module can be imported
            module_obj = self.safely_import_module("skeleton")
            if module_obj is None:
                module_obj = self.safely_import_module("solution")
            
            if module_obj is None:
                test_obj.yakshaAssert("TestMatchDonationsFunctionality", False, "functional")
                print("TestMatchDonationsFunctionality = Failed")
                return
            
            test_inventory = [
                {"id": "F001", "name": "Apples", "category": "Produce"},
                {"id": "F002", "name": "Milk", "category": "Dairy"},
                {"id": "F003", "name": "Bread", "category": "Bakery"}
            ]
            
            test_recipients = [
                {"id": "R001", "name": "City Food Bank", "accepts_categories": ["Produce", "Bakery"]},
                {"id": "R002", "name": "Community Shelter", "accepts_categories": ["Dairy", "Prepared"]}
            ]
            
            matches = self.safely_call_function(module_obj, "match_donations", test_inventory, test_recipients)
            if matches is None or not isinstance(matches, list) or len(matches) != 3:
                test_obj.yakshaAssert("TestMatchDonationsFunctionality", False, "functional")
                print("TestMatchDonationsFunctionality = Failed")
                return
            
            # Check specific matches
            found_apple_match = False
            found_milk_match = False
            found_bread_match = False
            
            for match in matches:
                if not isinstance(match, dict) or "item" not in match or "recipient" not in match:
                    test_obj.yakshaAssert("TestMatchDonationsFunctionality", False, "functional")
                    print("TestMatchDonationsFunctionality = Failed")
                    return
                
                item_id = match["item"]["id"] if "id" in match["item"] else None
                recipient_id = match["recipient"]["id"] if "id" in match["recipient"] else None
                
                if item_id == "F001" and recipient_id == "R001":
                    found_apple_match = True
                elif item_id == "F002" and recipient_id == "R002":
                    found_milk_match = True
                elif item_id == "F003" and recipient_id == "R001":
                    found_bread_match = True
            
            if not found_apple_match or not found_milk_match or not found_bread_match:
                test_obj.yakshaAssert("TestMatchDonationsFunctionality", False, "functional")
                print("TestMatchDonationsFunctionality = Failed")
                return
            
            test_obj.yakshaAssert("TestMatchDonationsFunctionality", True, "functional")
            print("TestMatchDonationsFunctionality = Passed")
        except:
            test_obj.yakshaAssert("TestMatchDonationsFunctionality", False, "functional")
            print("TestMatchDonationsFunctionality = Failed")

    def test_format_food_item_functionality(self):
        """Test format_food_item functionality"""
        test_obj = TestUtils()
        try:
            # Check if module can be imported
            module_obj = self.safely_import_module("skeleton")
            if module_obj is None:
                module_obj = self.safely_import_module("solution")
            
            if module_obj is None:
                test_obj.yakshaAssert("TestFormatFoodItemFunctionality", False, "functional")
                print("TestFormatFoodItemFunctionality = Failed")
                return
            
            test_item = {
                "id": "F001",
                "name": "Apples",
                "quantity": 25,
                "unit": "kg",
                "expiration_date": "2023-12-15",
                "category": "Produce"
            }
            
            formatted = self.safely_call_function(module_obj, "format_food_item", test_item)
            if (formatted is None or not isinstance(formatted, str) or 
                "F001" not in formatted or "Apples" not in formatted or 
                "25" not in formatted or "kg" not in formatted or 
                "Produce" not in formatted or "2023-12-15" not in formatted):
                test_obj.yakshaAssert("TestFormatFoodItemFunctionality", False, "functional")
                print("TestFormatFoodItemFunctionality = Failed")
                return
            
            test_obj.yakshaAssert("TestFormatFoodItemFunctionality", True, "functional")
            print("TestFormatFoodItemFunctionality = Passed")
        except:
            test_obj.yakshaAssert("TestFormatFoodItemFunctionality", False, "functional")
            print("TestFormatFoodItemFunctionality = Failed")

    def test_function_signatures_and_docstrings(self):
        """Test that functions have proper signatures and docstrings"""
        test_obj = TestUtils()
        try:
            # Check if module can be imported
            module_obj = self.safely_import_module("skeleton")
            if module_obj is None:
                module_obj = self.safely_import_module("solution")
            
            if module_obj is None:
                test_obj.yakshaAssert("TestFunctionSignaturesAndDocstrings", False, "functional")
                print("TestFunctionSignaturesAndDocstrings = Failed")
                return
            
            required_functions = [
                "validate_food_item",
                "calculate_days_until_expiration",
                "identify_expiring_items",
                "sort_items_by_expiration",
                "match_donations",
                "format_food_item"
            ]
            
            for func_name in required_functions:
                if not self.check_function_exists(module_obj, func_name):
                    test_obj.yakshaAssert("TestFunctionSignaturesAndDocstrings", False, "functional")
                    print("TestFunctionSignaturesAndDocstrings = Failed")
                    return
                
                func = getattr(module_obj, func_name)
                
                # Check if function has docstring
                if not func.__doc__ or len(func.__doc__.strip()) < 20:
                    test_obj.yakshaAssert("TestFunctionSignaturesAndDocstrings", False, "functional")
                    print("TestFunctionSignaturesAndDocstrings = Failed")
                    return
                
                # Check function signature
                sig = inspect.signature(func)
                params = list(sig.parameters.keys())
                
                if func_name == "validate_food_item":
                    if len(params) < 1 or "food_item" not in params[0]:
                        test_obj.yakshaAssert("TestFunctionSignaturesAndDocstrings", False, "functional")
                        print("TestFunctionSignaturesAndDocstrings = Failed")
                        return
                
                elif func_name == "calculate_days_until_expiration":
                    if len(params) < 1 or "expiration_date" not in params[0]:
                        test_obj.yakshaAssert("TestFunctionSignaturesAndDocstrings", False, "functional")
                        print("TestFunctionSignaturesAndDocstrings = Failed")
                        return
                
                elif func_name == "identify_expiring_items":
                    if len(params) < 1 or "food_items" not in params[0]:
                        test_obj.yakshaAssert("TestFunctionSignaturesAndDocstrings", False, "functional")
                        print("TestFunctionSignaturesAndDocstrings = Failed")
                        return
                
                elif func_name == "sort_items_by_expiration":
                    if len(params) < 1 or "food_items" not in params[0]:
                        test_obj.yakshaAssert("TestFunctionSignaturesAndDocstrings", False, "functional")
                        print("TestFunctionSignaturesAndDocstrings = Failed")
                        return
                
                elif func_name == "match_donations":
                    if len(params) < 2 or "food_items" not in params[0] or "recipients" not in params[1]:
                        test_obj.yakshaAssert("TestFunctionSignaturesAndDocstrings", False, "functional")
                        print("TestFunctionSignaturesAndDocstrings = Failed")
                        return
                
                elif func_name == "format_food_item":
                    if len(params) < 1 or "food_item" not in params[0]:
                        test_obj.yakshaAssert("TestFunctionSignaturesAndDocstrings", False, "functional")
                        print("TestFunctionSignaturesAndDocstrings = Failed")
                        return
            
            # Check for main function
            if not self.check_function_exists(module_obj, "main"):
                test_obj.yakshaAssert("TestFunctionSignaturesAndDocstrings", False, "functional")
                print("TestFunctionSignaturesAndDocstrings = Failed")
                return
            
            main_func = getattr(module_obj, "main")
            if not main_func.__doc__:
                test_obj.yakshaAssert("TestFunctionSignaturesAndDocstrings", False, "functional")
                print("TestFunctionSignaturesAndDocstrings = Failed")
                return
            
            test_obj.yakshaAssert("TestFunctionSignaturesAndDocstrings", True, "functional")
            print("TestFunctionSignaturesAndDocstrings = Passed")
        except:
            test_obj.yakshaAssert("TestFunctionSignaturesAndDocstrings", False, "functional")
            print("TestFunctionSignaturesAndDocstrings = Failed")

if __name__ == '__main__':
    unittest.main(verbosity=0, buffer=True)