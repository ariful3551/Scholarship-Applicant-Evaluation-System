"""
Scholarship Applicant Evaluation System
========================================
A menu-driven Python application that evaluates scholarship
applicants using a weighted scoring algorithm.

Features:
-Add Applicant
-View All Applicants
-Search Applicant
-Update Applicant
-Delete Applicant
-Ranking System
-Scholarship Recommendation
-Statistics
-JSON Data Persistence

Author: Ariful Islam
Version: 1.0
"""

# ==================== IMPORT MODULES ====================
import json
import sys
from datetime import datetime

# ==================== CONFIGURATION ====================
JSON_FILE = "applicants.json"
SCORE_WEIGHTS = {
    "gpa": 0.30,
    "sat": 0.20,
    "english": 0.10,
    "programming": 0.20,
    "research": 0.15,
    "eca": 0.05
}


# ==================== DATA LOAD/SAVE FUNCTIONS ====================

def load_data():
    """
    Load all applicant data from JSON file
    
    Returns:
        list: List of applicants (empty list if file doesn't exist)
    """
    try:
        with open(JSON_FILE, "r") as file:
            return json.load(file)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def save_all_data(applicant_list):
    """
    Save applicant list to JSON file
    
    Parameters:
        applicant_list (list): List of applicants
    """
    try:
        with open(JSON_FILE, "w") as file:
            json.dump(applicant_list, file, indent=4)

    except Exception as e:
        print(f"Error saving data: {e}")


def save_applicant_json(applicant):
    """
    Add new applicant to JSON file
    
    Parameters:
        applicant (dict): Applicant information
    """
    applicant_list = load_data()
    applicant_list.append(applicant)
    save_all_data(applicant_list)
    print("\nApplicant saved successfully!")


# ==================== VALIDATION FUNCTIONS ====================

def get_valid_float(prompt, min_val, max_val, error_msg):
    """
    Get valid float input from user
    
    Parameters:
        prompt (str): Input prompt
        min_val (float): Minimum allowed value
        max_val (float): Maximum allowed value
        error_msg (str): Error message for invalid input
    
    Returns:
        float: Valid input value
    """
    while True:
        try:
            value = float(input(prompt))
            if min_val <= value <= max_val:
                return value
            print(f"{error_msg} ({min_val} - {max_val})")
        except ValueError:
            print("Please enter a number!")


def get_valid_int(prompt, min_val, max_val, error_msg):
    """
    Get valid integer input from user
    
    Parameters:
        prompt (str): Input prompt
        min_val (int): Minimum allowed value
        max_val (int): Maximum allowed value
        error_msg (str): Error message for invalid input
    
    Returns:
        int: Valid input value
    """
    while True:
        try:
            value = int(input(prompt))
            if min_val <= value <= max_val:
                return value
            print(f"{error_msg} ({min_val} - {max_val})")
        except ValueError:
            print("Please enter an integer!")


# ==================== APPLICANT FUNCTIONS ====================

def add_applicant():
    """
    Collect applicant information from user
    
    Returns:
        dict: Complete applicant information
    """
    print("\n" + "="*50)
    print("Enter New Applicant Information")
    print("="*50)
    
    name = input("Name: ").strip()
    while not name:
        print("Name cannot be empty!")
        name = input("Name: ").strip()
    
    print("\nAcademic Information:")
    gpa = get_valid_float(
        "  GPA (2.00 - 5.00): ",
        2.00, 5.00,
        "GPA must be between 2.00 and 5.00"
    )
    
    sat = get_valid_int(
        "  SAT Score (400 - 1600): ",
        400, 1600,
        "SAT score must be between 400 and 1600"
    )
    
    english = get_valid_float(
        "  English Score (5.00 - 9.00): ",
        5.00, 9.00,
        "English score must be between 5.00 and 9.00"
    )
    
    print("\nSkill Assessment:")
    programming = get_valid_int(
        "  Programming Score (40 - 100): ",
        40, 100,
        "Programming score must be between 40 and 100"
    )
    
    research = get_valid_int(
        "  Research Score (40 - 100): ",
        40, 100,
        "Research score must be between 40 and 100"
    )
    
    eca = get_valid_int(
        "  ECA Score (40 - 100): ",
        40, 100,
        "ECA score must be between 40 and 100"
    )
    
    return {
        "Name": name,
        "GPA": gpa,
        "SAT": sat,
        "English": english,
        "Programming": programming,
        "Research": research,
        "ECA": eca
    }


def calculate_score(applicant):
    """
    Calculate final scholarship evaluation score
    
    Calculation Method:
    - GPA: 30% (on 5.00 scale)
    - SAT: 20% (on 1600 scale)
    - English: 10% (on 9.00 scale)
    - Programming: 20% (on 100 scale)
    - Research: 15% (on 100 scale)
    - ECA: 5% (on 100 scale)
    
    Parameters:
        applicant (dict): Applicant information
    
    Returns:
        dict: Updated applicant with Final Score
    """
    # Normalize all scores to 100 scale
    normalized_gpa = (applicant["GPA"] / 5.00) * 100
    normalized_sat = (applicant["SAT"] / 1600) * 100
    normalized_english = (applicant["English"] / 9.00) * 100
    normalized_programming = applicant["Programming"]
    normalized_research = applicant["Research"]
    normalized_eca = applicant["ECA"]
    
    # Calculate weighted score
    final_score = (
        normalized_gpa * SCORE_WEIGHTS["gpa"] +
        normalized_sat * SCORE_WEIGHTS["sat"] +
        normalized_english * SCORE_WEIGHTS["english"] +
        normalized_programming * SCORE_WEIGHTS["programming"] +
        normalized_research * SCORE_WEIGHTS["research"] +
        normalized_eca * SCORE_WEIGHTS["eca"]
    )
    
    applicant["Final Score"] = round(final_score, 2)
    return applicant


def show_applicant(applicant, show_header=True):
    """
    Display applicant information in a formatted way
    
    Parameters:
        applicant (dict): Applicant information
        show_header (bool): Whether to show header
    """
    if show_header:
        print("\n" + "="*50)
        print("Applicant Information")
        print("="*50)
    
    print(f"  Name             : {applicant['Name']}")
    print("-" * 40)
    print("  Academic Profile:")
    print(f"  GPA              : {applicant['GPA']:.2f}")
    print(f"  SAT Score        : {applicant['SAT']}")
    print(f"  English Score    : {applicant['English']:.2f}")
    print("-" * 40)
    print("  Skill Profile:")
    print(f"  Programming      : {applicant['Programming']}")
    print(f"  Research         : {applicant['Research']}")
    print(f"  ECA              : {applicant['ECA']}")
    print("-" * 40)
    print(f"  Final Score      : {applicant['Final Score']:.2f}%")
    
    # Show rating based on score
    score = applicant['Final Score']
    if score >= 90:
        rating = "Excellent"
    elif score >= 80:
        rating = "Very Good"
    elif score >= 70:
        rating = "Good"
    elif score >= 60:
        rating = "Average"
    else:
        rating = "Needs Improvement"
    
    print(f"  Rating           : {rating}")
    print("="*50)


# ==================== CRUD OPERATIONS ====================

def view_applicants():
    """
    Display all applicants
    """
    applicant_list = load_data()
    
    if not applicant_list:
        print("\n No applicants found!")
        return
    
    print(f"\n  Total {len(applicant_list)} applicants found")
    print("-" * 40)
    for applicant in applicant_list:
        show_applicant(applicant, show_header=False)
        print()


def search_applicant():
    """
    Search applicant by name
    """
    applicant_list = load_data()
    search_name = input("\n Enter name to search: ").strip().lower()
    
    found_applicants = [
        app for app in applicant_list 
        if search_name in app["Name"].strip().lower()
    ]
    
    if found_applicants:
        print(f"\n {len(found_applicants)} applicant(s) found:")
        for applicant in found_applicants:
            show_applicant(applicant, show_header=False)
            print()
    else:
        print(f"\n No applicant found with name '{search_name}'!")


def update_applicant():
    """
    Update applicant information
    """
    applicant_list = load_data()
    search_name = input("\nEnter applicant name to update: ").strip().lower()
    
    for applicant in applicant_list:
        if applicant["Name"].strip().lower() == search_name:
            print("\nApplicant found!")
            show_applicant(applicant, show_header=False)
            
            print("\nWhat do you want to update?")
            print("1. GPA")
            print("2. SAT Score")
            print("3. English Score")
            print("4. Programming Score")
            print("5. Research Score")
            print("6. ECA Score")
            print("7. Update All Information")
            print("8. Cancel")
            
            choice = input("Your choice (1-8): ")
            
            if choice == "1":
                applicant["GPA"] = get_valid_float("New GPA: ", 2.00, 5.00, "GPA must be 2.00-5.00")
            elif choice == "2":
                applicant["SAT"] = get_valid_int("New SAT Score: ", 400, 1600, "SAT must be 400-1600")
            elif choice == "3":
                applicant["English"] = get_valid_float("New English Score: ", 5.00, 9.00, "English must be 5.00-9.00")
            elif choice == "4":
                applicant["Programming"] = get_valid_int("New Programming Score: ", 40, 100, "Programming must be 40-100")
            elif choice == "5":
                applicant["Research"] = get_valid_int("New Research Score: ", 40, 100, "Research must be 40-100")
            elif choice == "6":
                applicant["ECA"] = get_valid_int("New ECA Score: ", 40, 100, "ECA must be 40-100")
            elif choice == "7":
                applicant["GPA"] = get_valid_float("New GPA: ", 2.00, 5.00, "GPA must be 2.00-5.00")
                applicant["SAT"] = get_valid_int("New SAT Score: ", 400, 1600, "SAT must be 400-1600")
                applicant["English"] = get_valid_float("New English Score: ", 5.00, 9.00, "English must be 5.00-9.00")
                applicant["Programming"] = get_valid_int("New Programming Score: ", 40, 100, "Programming must be 40-100")
                applicant["Research"] = get_valid_int("New Research Score: ", 40, 100, "Research must be 40-100")
                applicant["ECA"] = get_valid_int("New ECA Score: ", 40, 100, "ECA must be 40-100")
            elif choice == "8":
                print("Update cancelled!")
                return
            else:
                print("Invalid choice!")
                return
            
            # Recalculate score
            calculate_score(applicant)
            save_all_data(applicant_list)
            print("Applicant updated successfully!")
            return
    
    print(f" No applicant found with name '{search_name}'!")


def delete_applicant():
    """
    Delete applicant from list
    """
    applicant_list = load_data()
    search_name = input("\nEnter applicant name to delete: ").strip().lower()
    
    for i, applicant in enumerate(applicant_list):
        if applicant["Name"].strip().lower() == search_name:
            show_applicant(applicant, show_header=False)
            confirm = input(f"\n Are you sure you want to delete '{applicant['Name']}'? (y/n): ").lower()
            
            if confirm == 'y':
                del applicant_list[i]
                save_all_data(applicant_list)
                print("Applicant deleted successfully!")
            else:
                print("Deletion cancelled!")
            return
    
    print(f" No applicant found with name '{search_name}'!")


# ==================== RANKING AND RECOMMENDATION ====================

def rank_applicants():
    """
    Rank all applicants based on final score
    """
    applicant_list = load_data()
    
    if not applicant_list:
        print("\n📭 No applicants found!")
        return
    
    # Sort by score (highest to lowest)
    ranked_list = sorted(
        applicant_list,
        key=lambda x: x["Final Score"],
        reverse=True
    )
    
    print("\n" + "="*60)
    print("Top Scholarship Candidates Ranking")
    print("="*60)
    
    # Show all applicants with rank
    for rank, applicant in enumerate(ranked_list, start=1):
        # Format rank with proper spacing
        rank_str = f"{rank}." if rank > 3 else f"{rank}"
        
        # Fixed width formatting
        print(f"{rank_str:<4} {applicant['Name']:20} | Score: {applicant['Final Score']:6.2f}%")
    
    print("="*60)
    print(f"Total {len(ranked_list)} applicants evaluated")


def scholarship_recommendation():
    """
    Generate scholarship recommendation based on final score
    """
    applicant_list = load_data()
    
    if not applicant_list:
        print("\nNo applicants found!")
        return
    
    print("\n" + "="*60)
    print(" Scholarship Recommendation Report")
    print("="*60)
    
    # Sort by score
    ranked_list = sorted(
        applicant_list,
        key=lambda x: x["Final Score"],
        reverse=True
    )
    
    for applicant in ranked_list:
        score = applicant["Final Score"]
        
        # Recommendation based on score
        if score >= 90:
            recommendation = " Full Scholarship"
            color = "🟢"
        elif score >= 80:
            recommendation = " Partial Scholarship"
            color = "🔵"
        elif score >= 70:
            recommendation = " Consider"
            color = "🟡"
        elif score >= 60:
            recommendation = " Needs Improvement"
            color = "🟠"
        else:
            recommendation = " Not Recommended"
            color = "🔴"
        
        print(f"\n{color} {applicant['Name']}")
        print(f"    Final Score: {score:.2f}%")
        print(f"    Recommendation: {recommendation}")
    
    print("\n" + "="*60)
    print("   Guidelines:")
    print("   • 90%+  : Full Scholarship")
    print("   • 80-89%: Partial Scholarship")
    print("   • 70-79%: Consider")
    print("   • 60-69%: Needs Improvement")
    print("   • <60%  : Not Recommended")
    print("="*60)


def get_statistics():
    """
    Display system statistics
    """
    applicant_list = load_data()
    
    if not applicant_list:
        print("\n No applicants found!")
        return
    
    total = len(applicant_list)
    scores = [app["Final Score"] for app in applicant_list]
    avg_score = sum(scores) / total if total > 0 else 0
    
    print("\n" + "="*50)
    print(" System Statistics")
    print("="*50)
    print(f"Total Applicants      : {total}")
    print(f"Average Final Score   : {avg_score:.2f}%")
    print(f"Highest Score         : {max(scores):.2f}%")
    print(f"Lowest Score          : {min(scores):.2f}%")
    print("="*50)


# ==================== MAIN MENU ====================

def main_menu():
    """
    Display main menu and process user input
    """
    print("\n" + "="*60)
    print(" Scholarship Applicant Evaluation System")
    print("="*60)
    print(f" {datetime.now().strftime('%B %d, %Y')}")
    print("="*60)
    
    while True:
        print("\n Main Menu:")
        print("  1.  Add Applicant")
        print("  2.  View All Applicants")
        print("  3.  Search Applicant")
        print("  4.  Update Applicant")
        print("  5.  Delete Applicant")
        print("  6.  View Ranking")
        print("  7.  Scholarship Recommendation")
        print("  8.  Statistics")
        print("  9.  Exit")
        print("-" * 60)
        
        choice = input("Your choice (1-9): ").strip()
        
        if choice == "1":
            applicant = add_applicant()
            calculate_score(applicant)
            save_applicant_json(applicant)
            show_applicant(applicant)
            
        elif choice == "2":
            view_applicants()
            
        elif choice == "3":
            search_applicant()
            
        elif choice == "4":
            update_applicant()
            
        elif choice == "5":
            delete_applicant()
            
        elif choice == "6":
            rank_applicants()
            
        elif choice == "7":
            scholarship_recommendation()
            
        elif choice == "8":
            get_statistics()
            
        elif choice == "9":
            print("\n Thank you! Exiting the system...")
            print(" Your data has been saved in JSON file!")
            sys.exit()
            
        else:
            print(" Invalid choice! Please enter a number between 1 and 9.")
        
        # Pause before returning to menu
        input("\n⏎ Press Enter to return to menu...")


# ==================== PROGRAM ENTRY POINT ====================

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print("\n\n Program terminated by user...")
        sys.exit()
    except Exception as e:
        print(f"\n An unexpected error occurred: {e}")
        print(" Please restart the program.")
        sys.exit()