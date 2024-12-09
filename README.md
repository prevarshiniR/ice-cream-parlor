Ice Cream Parlor Café Management
This project is a simple Ice Cream Parlor Café Management system implemented in Python using SQLite for database management. The system allows administrators to manage ice cream flavors, ingredients, and customer information, while customers can view flavors, add flavors to their cart, and get flavor suggestions based on their allergens.

Features
Admin Functions:

Add new ice cream flavors
View all ice cream flavors
Delete an ice cream flavor
View all ingredients
View all customers
View customer flavor suggestions
Customer Functions:

Add customer information
Get flavor suggestions based on allergens
Search for specific ice cream flavors
View and manage cart
Database Schema
The database consists of the following tables:

ice_cream_flavors: Stores information about ice cream flavors.
ice_cream_inventory: Stores information about ingredients.
customers: Stores customer information.
customer_suggestions: Stores flavor suggestions for customers.
cart: Stores items added to the customer's cart.
Functions
initialize_database(conn, cursor)
Initializes the database with the required tables and default data.

create_connection(db_file)
Creates a database connection to a SQLite database.

add_customer_suggestion(conn, cursor, email, allergens)
Adds flavor suggestions for a customer based on their allergens.

show_customer_suggestions(conn, cursor, email=None)
Shows flavor suggestions for a customer. If no email is provided, shows all suggestions.

add_customer(conn, cursor, customer_name, email, phone, allergens)
Adds a new customer to the database.

add_flavor(conn, cursor, flavor, price, allergens, seasonal=0, start_date=None, end_date=None)
Adds a new ice cream flavor to the database.

view_flavors(conn, cursor, flavor=None)
Views all ice cream flavors or a specific flavor if provided.

delete_flavor(conn, cursor, flavor)
Deletes an ice cream flavor from the database.

view_ingredients(conn, cursor)
Views all ingredients in the inventory.

view_customers(conn, cursor, email=None)
Views all customers or a specific customer if an email is provided.

main()
Main function to run the application.

Usage
Ensure you have Python and SQLite installed on your system.
Clone the repository.
Run the ice-cream-parlor.py file using Python: python ice-cream-parlor.py

Follow the on-screen prompts to interact with the system.
License
This project is licensed under the MIT License. See the LICENSE file for details.

Acknowledgements
This project was inspired by the need for a simple management system for an ice cream parlor café. Special thanks to all contributors and the open-source community.
