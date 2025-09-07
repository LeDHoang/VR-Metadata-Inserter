#!/usr/bin/env python3
"""
Test Manager for VR Metadata Inserter
Helps track test numbers and descriptions for development testing.
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional

TEST_TRACKER_FILE = "test_tracker.json"


def load_test_tracker() -> Dict:
    """Load the test tracker data from JSON file."""
    if not os.path.exists(TEST_TRACKER_FILE):
        return {
            "current_test_number": 1,
            "tests": [],
            "last_updated": datetime.now().strftime("%Y-%m-%d")
        }
    
    with open(TEST_TRACKER_FILE, 'r') as f:
        return json.load(f)


def save_test_tracker(data: Dict) -> None:
    """Save the test tracker data to JSON file."""
    data["last_updated"] = datetime.now().strftime("%Y-%m-%d")
    with open(TEST_TRACKER_FILE, 'w') as f:
        json.dump(data, f, indent=2)


def add_test(description: str, status: str = "pending", notes: str = "", folder: str = "") -> int:
    """Add a new test to the tracker."""
    data = load_test_tracker()
    
    # Ensure test number is always the next available number
    if data["tests"]:
        # Find the highest test number and add 1
        max_test_number = max(test["test_number"] for test in data["tests"])
        test_number = max_test_number + 1
    else:
        test_number = 1
    
    new_test = {
        "test_number": test_number,
        "description": description,
        "date": datetime.now().strftime("%Y-%m-%d"),
        "status": status,
        "notes": notes,
        "folder": folder
    }
    
    data["tests"].append(new_test)
    data["current_test_number"] = test_number + 1
    
    save_test_tracker(data)
    return test_number


def update_test_status(test_number: int, status: str, notes: str = "", folder: str = "") -> bool:
    """Update the status of an existing test."""
    data = load_test_tracker()
    
    for test in data["tests"]:
        if test["test_number"] == test_number:
            test["status"] = status
            if notes:
                test["notes"] = notes
            if folder:
                test["folder"] = folder
            save_test_tracker(data)
            return True
    
    return False


def list_tests() -> None:
    """Display all tests in the tracker."""
    data = load_test_tracker()
    
    print(f"\n=== Test Tracker (Last Updated: {data['last_updated']}) ===")
    print(f"Next Test Number: {data['current_test_number']}")
    print()
    
    if not data["tests"]:
        print("No tests recorded yet.")
        return
    
    for test in data["tests"]:
        status_emoji = {
            "pending": "⏳",
            "in_progress": "🔄", 
            "completed": "✅",
            "failed": "❌",
            "cancelled": "🚫"
        }.get(test["status"], "❓")
        
        print(f"Test #{test['test_number']} {status_emoji} {test['status'].upper()}")
        print(f"  Description: {test['description']}")
        print(f"  Date: {test['date']}")
        if test.get("folder"):
            print(f"  Folder: {test['folder']}")
        if test.get("notes"):
            print(f"  Notes: {test['notes']}")
        print()


def get_next_test_number() -> int:
    """Get the next test number without creating a test."""
    data = load_test_tracker()
    
    # Ensure we return the correct next number based on existing tests
    if data["tests"]:
        max_test_number = max(test["test_number"] for test in data["tests"])
        return max_test_number + 1
    else:
        return 1


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python test_manager.py add 'Test description' [status] [notes] [folder]")
        print("  python test_manager.py update <test_number> <status> [notes] [folder]")
        print("  python test_manager.py list")
        print("  python test_manager.py next")
        print()
        print("Status options: pending, in_progress, completed, failed, cancelled")
        print("Folder: Optional folder path where test files are located (e.g., 'test_1', 'raw/subfolder')")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command == "add":
        if len(sys.argv) < 3:
            print("Error: Test description is required")
            sys.exit(1)
        
        description = sys.argv[2]
        status = sys.argv[3] if len(sys.argv) > 3 else "pending"
        notes = sys.argv[4] if len(sys.argv) > 4 else ""
        folder = sys.argv[5] if len(sys.argv) > 5 else ""
        
        test_num = add_test(description, status, notes, folder)
        print(f"Added Test #{test_num}: {description}")
    
    elif command == "update":
        if len(sys.argv) < 4:
            print("Error: Test number and status are required")
            sys.exit(1)
        
        try:
            test_number = int(sys.argv[2])
            status = sys.argv[3]
            notes = sys.argv[4] if len(sys.argv) > 4 else ""
            folder = sys.argv[5] if len(sys.argv) > 5 else ""
            
            if update_test_status(test_number, status, notes, folder):
                print(f"Updated Test #{test_number} to {status}")
            else:
                print(f"Error: Test #{test_number} not found")
        except ValueError:
            print("Error: Test number must be an integer")
    
    elif command == "list":
        list_tests()
    
    elif command == "next":
        next_num = get_next_test_number()
        print(f"Next test number: {next_num}")
    
    else:
        print(f"Error: Unknown command '{command}'")
        sys.exit(1)
