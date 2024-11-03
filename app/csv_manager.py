####################################################
### Handles generation and creation of CSV files ###
### for simple persistance. A DB can be used if  ###
### preffered.                                   ###
####################################################

import csv

# File paths
FAMILIES_CSV = "data/families.csv"
ASSIGNMENTS_CSV = "data/assignments.csv"

# Save registered familes to a CSV File
def save_families_to_csv(registered_families):
    with open(FAMILIES_CSV, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["email", "name", "spouse_name", "spouse_email", "children"])
        for email, data in registered_families.items():
            children_str = ",".join(data["children"]) if isinstance(data["children"], list) else data["children"]
            writer.writerow([email, data["name"], data["spouse_name"], data["spouse_email"], children_str])

# Load familes from a csv file
def load_families_from_csv():
    families = {}
    try:
        with open(FAMILIES_CSV, mode="r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                children_list = row["children"].split(",") if row["children"] else []
                families[row["email"]] = {
                    "name" : row["name"],
                    "spouse_name": row["spouse_name"],
                    "spouse_email": row["spouse_email"],
                    "children": children_list
                }
    except FileNotFoundError:
        print("families.csv could not be found. Creating empty dictionary.")
        families = {}
    return families

def save_assignments_to_csv(assigned_adults, assigned_children):
    with open(ASSIGNMENTS_CSV, mode="w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["group", "secret_santa", "recipient"])
        for secret_santa, recipient in assigned_adults.items():
            writer.writerow(["adult",secret_santa, recipient])
        for secret_santa, recipient in assigned_children.items():
            writer.writerow(["child", secret_santa, recipient])

def load_assignments_from_csv():
    assigned_adults = {}
    assigned_children = {}

    try:
        with open(ASSIGNMENTS_CSV, mode="r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row ["group"] == "adult":
                    assigned_adults[row["secret_santa"]] = row["recipient"]
                elif row ["group"] == "child":
                    assigned_children[row["secret_santa"]] = row["recipient"]
    except FileNotFoundError:
        print("assignments.csv could not be found. Creating empty dictionary.")
    return assigned_adults, assigned_children