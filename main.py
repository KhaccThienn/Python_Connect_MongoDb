import pymongo as pm
from bson.objectid import ObjectId
from typing import Final
import re

# MongoDB URL
URL_MONGODB: Final = "mongodb://localhost:27017/"

def main_menus():
    """
    Display main menu options.
    """
    print("\n1. Read All . ")
    print("2. Find by name . ")
    print("3. Insert one. ")
    print("4. Update. ")
    print("5. Delete. ")
    print("0. Quit. ")
    choose = int(input("Your choice: "))
    return choose

def show_tables_data(data):
    """
    Display category data in a formatted table.
    """
    print(f"{'-' * 72}")
    print(f"ObjectId \t\t\t| Category Name \t\t| Status \t")
    print(f"{'-' * 72}")
    for x in data:
        print(f"{x['_id']} \t| {x['name']} \t\t\t| {x['status']}")
        print(f"{'-' * 72}")

def read_all_category(category_col):
    """
    Read all categories from the collection.
    """
    show_tables_data(category_col.find())

def find_one(collection, finding_id):
    """
    Find a document in the collection by ID.
    """
    query = {"_id": ObjectId(finding_id)}
    filter = {"_id": 0}
    result = collection.find_one(query, filter)
    if result is None:
        return False
    else:
        return True

def read_all_category_by_name(category_col, name_search):
    """
    Read all categories from the collection by name.
    """
    rgx = re.compile(f'.*{name_search}.*', re.IGNORECASE)
    query = {"name": rgx}
    data = category_col.find(query)
    show_tables_data(data)

def insert_category(category_col):
    """
    Insert a category into the collection.
    """
    name = input("Enter category's name: ")
    status = bool(input("Enter status: "))
    
    dict_data = {"name": name, "status": status}
    if category_col.insert_one(dict_data) is not None:
        print("Category inserted successfully")
    else:
        print("Failed to insert category")

def update_category(category_col, _id):
    """
    Update a category in the collection.
    """
    query = {"_id": ObjectId(_id)}
    
    name = input("Enter new category's name: ")
    status = bool(input("Enter new status: "))
    
    new_values = { "$set": {"name": name, "status": status} }
    
    if category_col.update_one(query, new_values) is not None:
        print("Category updated successfully")
    else:
        print("Failed to update category")

def delete_category(category_col, _id):
    """
    Delete a category from the collection.
    """
    query = {"_id": ObjectId(_id)}
    if category_col.delete_one(query) is not None:
        print("Category deleted successfully")
    else:
        print("Failed to delete category")

def main():
    # Connect to MongoDB
    my_client = pm.MongoClient(URL_MONGODB)
    my_db = my_client['PyMongoDB']
    
    # Check if database and collection exist
    db_list = my_client.list_database_names()
    if "PyMongoDB" in db_list:
        print("The database exists.")
    else:
        print("The database does not exist.")
    
    collections_list = my_db.list_collection_names()
    if "categories" in collections_list:
        print("The collection exists.")
    
    category_col = my_db['categories']
    
    # Main program loop
    while True:
        choice = main_menus()
        
        if choice == 1:
            print("\nList Categories: ")
            read_all_category(category_col)
        elif choice == 2:
            name_search = input("Enter name to search: ")
            if len(name_search) == 0:
                print("Please enter a name !")
            else:
                read_all_category_by_name(category_col, name_search)
        elif choice == 3:
            print("\nInsert one category: ")
            insert_category(category_col)
        elif choice == 4:
            print("\n")
            read_all_category(category_col)
            _id = input("Enter one category to Update: ")
            if find_one(category_col, _id):
                update_category(category_col, _id)
            else:
                print("Invalid category: " + _id)
        elif choice == 5:
            print("\n")
            read_all_category(category_col)
            _id = input("Enter one category to Delete: ")
            if find_one(category_col, _id):
                check = input("You wanna delete this category (%s) ? (y / n): " % (_id))
                if check == "y":
                    delete_category(category_col, _id)
            else:
                print("Invalid category: " + _id)
        elif choice == 0:
            # Close MongoDB connection and exit program
            my_client.close()
            break

if __name__ == "__main__":
    main()
