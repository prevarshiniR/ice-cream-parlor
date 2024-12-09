import sqlite3
from sqlite3 import Error

def initialize_database(conn, cursor):
    try:
        cursor.execute("CREATE TABLE IF NOT EXISTS ice_cream_flavors (flavor TEXT NOT NULL, price REAL NOT NULL, allergens TEXT, seasonal INTEGER DEFAULT 0, start_date TEXT, end_date TEXT, PRIMARY KEY(flavor))")

        cursor.execute("CREATE TABLE IF NOT EXISTS ice_cream_inventory (ingredient TEXT NOT NULL, quantity INTEGER NOT NULL, PRIMARY KEY(ingredient))")

        cursor.execute("CREATE TABLE IF NOT EXISTS customers (customer_name TEXT NOT NULL, email TEXT NOT NULL, phone TEXT NOT NULL, allergens TEXT, PRIMARY KEY(email))")
        
        cursor.execute("CREATE TABLE IF NOT EXISTS customer_suggestions (email TEXT NOT NULL, flavor TEXT, FOREIGN KEY (email) REFERENCES customers (email))")
        
        cursor.execute("CREATE TABLE IF NOT EXISTS cart (customer_name TEXT NOT NULL, flavor TEXT PRIMARY KEY NOT NULL, quantity INTEGER NOT NULL, price REAL NOT NULL, total REAL NOT NULL, date TEXT NOT NULL, FOREIGN KEY (customer_name) REFERENCES customers (customer_name))")
        default_flavors = [
            ("vanilla", 120.0, "milk", 0),
            ("chocolate", 150.0, "milk", 0),
            ("pistachio", 200.0, "milk, nuts", 0),
            ("almond", 180.0, "milk, nuts", 0)
        ]

        default_ingredients = [
            ("milk", 100),
            ("nuts", 50),
            ("sugar", 200),
            ("flavoring", 100)
        ]

        cursor.executemany("INSERT OR REPLACE INTO ice_cream_flavors (flavor, price, allergens, seasonal) VALUES (?, ?, ?, ?)", default_flavors)
        cursor.executemany("INSERT OR REPLACE INTO ice_cream_inventory (ingredient, quantity) VALUES (?, ?)", default_ingredients)
        conn.commit()
    except Error as e:
        print(e)
    
    return conn

def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    cursor = None
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
    except Error as e:
        print(e)

    return conn, cursor

#function to add a customer flavor suggestion
def add_customer_suggestion(conn, cursor, email, allergens):
    flavors = view_flavors(conn, cursor)
    for flavor in flavors:
        if allergens.lower() not in flavor[2].lower():
            cursor.execute("INSERT INTO customer_suggestions (email, flavor) VALUES (?, ?)", (email.lower(), flavor[0].lower()))
    conn.commit()
    return cursor

#function to view customer flavor suggestions
def show_customer_suggestions(conn, cursor, email = None):
    if email is None:
        cursor.execute("SELECT * FROM customer_suggestions")
    else:
        cursor.execute("SELECT * FROM customer_suggestions WHERE email=?", (email.lower(),))
    rows = cursor.fetchall()
    conn.commit()
    return rows

#function to add a customer
def add_customer(conn, cursor, customer_name, email, phone, allergens):
    cursor.execute("INSERT OR REPLACE INTO customers (customer_name, email, phone, allergens) VALUES (?, ?, ?, ?)", (customer_name.lower(), email.lower(), phone, allergens.lower()))
    add_customer_suggestion(conn, cursor, email, allergens)
    conn.commit()
    return cursor

#function to add a flavor
def add_flavor(conn, cursor, flavor, price, allergens, seasonal=0, start_date=None, end_date=None):
    cursor.execute("INSERT OR REPLACE INTO ice_cream_flavors (flavor, price, allergens, seasonal, start_date, end_date) VALUES (?, ?, ?, ?, ?, ?)", (flavor.lower(), price, allergens.lower(), seasonal, start_date, end_date))
    conn.commit()
    return cursor

#function to view flavors
def view_flavors(conn, cursor, flavor = None):
    if flavor is None:
        cursor.execute("SELECT * FROM ice_cream_flavors")
    else:
        cursor.execute("SELECT * FROM ice_cream_flavors where flavor = ?", (flavor.lower(),))
    rows = cursor.fetchall()
    conn.commit()
    return rows

#function to delete a flavor
def delete_flavor(conn, cursor, flavor):
    cursor.execute("DELETE FROM ice_cream_flavors WHERE flavor=?", (flavor.lower()))
    conn.commit()
    return cursor

#function to view ingredients
def view_ingredients(conn, cursor):
    cursor.execute("SELECT * FROM ice_cream_inventory")
    rows = cursor.fetchall()
    conn.commit()
    return rows

#function to view all customers
def view_customers(conn, cursor, email = None):
    if email is None: 
        cursor.execute("SELECT * FROM customers")
    else:
        print(email)
        cursor.execute("SELECT * FROM customers WHERE email=?", (email.lower(),))  
    rows = cursor.fetchall()
    conn.commit()
    return rows



def main():
    database = "ice_cream_parlor.db"

    # create a database connection
    conn, cursor = create_connection(database)
    conn = initialize_database(conn, cursor)
    if conn is not None:
        print("Database connection established")
    else:
        print("Error! cannot create the database connection.")

    while True:
        print("\nIce Cream Parlor Café Management")
        print("1. Admin")
        print("2. Customers")
        print("3. Exit")
        role = input("Enter your role: ")

        if role == "1":
            while True:
                print("1. Add Flavors")
                print("2. View Flavors")
                print("3. Delete Flavor")
                print("4. View Ingredients")
                print("5. View Customers")
                print("6. View Customer Suggestions")
                print("7. Exit")
                choice = input("Enter your choice: ")

                if choice == "1":
                    flavor = input("Enter flavor: ")
                    price = float(input("Enter price: "))
                    allergons = input("Enter allergons: ")
                    seasonal = input("Is this a seasonal flavor? (y/n): ")
                    if seasonal == "y":
                        start_date = input("Enter start date (yyyy-mm-dd): ")
                        end_date = input("Enter end date (yyyy-mm-dd): ")
                        add_flavor(conn, cursor, flavor, price, allergons, seasonal=1, start_date=start_date, end_date=end_date)
                    else:
                        add_flavor(conn, cursor, flavor, price, allergons, seasonal=0)
                    print("Flavor added successfully!")

                elif choice == "2":
                    rows = view_flavors(conn, cursor)
                    for row in rows:
                        print(row)

                elif choice == "3":
                    flavor = input("Enter flavor to delete: ")
                    delete_flavor(conn, cursor, flavor)
                    print("Flavor deleted successfully!")

                elif choice == "4":
                    ingredients = view_ingredients(conn, cursor)
                    for ingredient in ingredients:
                        print(ingredient)

                elif choice == "5":
                    rows = view_customers(conn, cursor, None)
                    for row in rows:
                        print(row)

                elif choice == "6":
                    rows = show_customer_suggestions(conn, cursor, None)
                    for row in rows:
                        print(row)

                elif choice == "7":
                    break

                else:
                    print("Invalid option. Please try again.")

        elif role == "2":
            email = input("Enter your email: ")
            customer_name = input("Enter your name: ")
            phone = input("Enter your phone: ")
            allergens = input("Enter allergens: ")
            add_customer(conn, cursor, customer_name, email, phone, allergens)

            while True:
                print("1. Get suggestions")
                print("2. Search Flavors")
                print("3. View cart")
                print("4. Exit")
                choice = input("Enter your choice: ")

                if choice == '1':
                    rows = show_customer_suggestions(conn, cursor, email)
                    for row in rows:
                        print(row)

                elif choice == '2':
                    fav_flavor = input("Enter your favourite flavor: ")
                    flavors = view_flavors(conn, cursor, fav_flavor)
                    for flavor in flavors:
                        while True:
                            print("1. Add to cart")
                            print("2. Exit")
                            choice = input("Enter your choice: ")

                            if choice == '1':
                                quantity = int(input("Enter quantity: "))
                                total = quantity * flavor[1]
                                date = input("Enter date (yyyy-mm-dd): ")
                                cursor.execute("INSERT or REPLACE INTO cart (customer_name, flavor, quantity, price, total, date) VALUES (?, ?, ?, ?, ?, ?)", (customer_name, flavor[0], quantity, flavor[1], total, date))
                                conn.commit()
                                print("Flavor added to cart successfully!")
                                break

                            elif choice == '2':
                                break

                            else:
                                print("Invalid option. Please try again.")
                        print(flavor)
                
                elif choice == '3':
                    rows = cursor.execute("SELECT * FROM cart WHERE customer_name=?", (customer_name,))
                    for row in rows:
                        print(row)
                        
                elif choice == '4':
                    break

        elif role == "3":
            break

        else:
            print("Invalid option. Please try again.")

    conn.close()
if __name__ == "__main__":
    main()

