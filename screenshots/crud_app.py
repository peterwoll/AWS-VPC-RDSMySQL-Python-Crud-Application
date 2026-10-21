import mysql.connector
import getpass

DB_HOST = "mysql-lab-db.c47ywe28idfx.us-east-1.rds.amazonaws.com"
DB_USER = "admin"
DB_NAME = "labdb"
DB_PORT = 3306


def connect_database():
    password = getpass.getpass("Enter MySQL password: ")

    return mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=password,
        database=DB_NAME,
        port=DB_PORT,
        connection_timeout=10
    )


def display_customers(connection):
    cursor = connection.cursor()

    try:
        cursor.execute("""
            SELECT customer_id, first_name, last_name,
                   email, city, state, signup_date
            FROM customers
            ORDER BY customer_id
        """)

        customers = cursor.fetchall()

        print("\nCUSTOMER LIST")
        print("-" * 70)

        for customer in customers:
            print(customer)

        print("-" * 70)
        print(f"Total customers: {len(customers)}")

    finally:
        cursor.close()

def add_customer(connection):
    print("\nADD NEW CUSTOMER")
    print("-" * 40)

    first_name = input("First name: ").strip()
    last_name = input("Last name: ").strip()
    email = input("Email: ").strip()
    city = input("City: ").strip()
    state = input("State (2 letters): ").strip().upper()
    signup_date = input("Signup date (YYYY-MM-DD): ").strip()

    if not first_name or not last_name:
        print("First and last name are required.")
        return

    if len(state) != 2 or not state.isalpha():
        print("State must contain two letters.")
        return

    cursor = connection.cursor()

    try:
        sql = """
            INSERT INTO customers
                (first_name, last_name, email,
                 city, state, signup_date)
            VALUES (%s, %s, %s, %s, %s, %s)
        """

        values = (
            first_name,
            last_name,
            email,
            city,
            state,
            signup_date
        )

        cursor.execute(sql, values)
        connection.commit()

        print("\nCustomer added successfully!")
        print(f"New customer ID: {cursor.lastrowid}")

    except mysql.connector.Error as error:
        connection.rollback()
        print(f"Insert failed: {error}")

    finally:
        cursor.close()

def update_customer(connection):
    print("\nUPDATE CUSTOMER")
    print("-" * 40)

    try:
        customer_id = int(input("Enter customer ID: "))
    except ValueError:
        print("Invalid customer ID.")
        return

    cursor = connection.cursor()

    try:
        # Check whether the customer exists
        cursor.execute(
            """
            SELECT first_name, last_name, city, state
            FROM customers
            WHERE customer_id = %s
            """,
            (customer_id,)
        )

        customer = cursor.fetchone()

        if customer is None:
            print("Customer not found.")
            return

        print(f"\nCustomer: {customer[0]} {customer[1]}")
        print(f"Current city: {customer[2]}")
        print(f"Current state: {customer[3]}")

        new_city = input("Enter new city: ").strip()
        new_state = input("Enter new state (2 letters): ").strip().upper()

        if not new_city:
            print("City cannot be empty.")
            return

        if len(new_state) != 2 or not new_state.isalpha():
            print("State must contain two letters.")
            return

        sql = """
            UPDATE customers
            SET city = %s,
                state = %s
            WHERE customer_id = %s
        """

        cursor.execute(sql, (new_city, new_state, customer_id))
        connection.commit()

        print("\nCustomer updated successfully!")

    except mysql.connector.Error as error:
        connection.rollback()
        print(f"Update failed: {error}")

    finally:
        cursor.close()



def delete_customer(connection):
    print("\nDELETE CUSTOMER")
    print("-" * 40)

    try:
        customer_id = int(input("Enter customer ID to delete: "))
    except ValueError:
        print("Invalid customer ID.")
        return

    cursor = connection.cursor()

    try:
        cursor.execute(
            """
            SELECT first_name, last_name
            FROM customers
            WHERE customer_id = %s
            """,
            (customer_id,)
        )

        customer = cursor.fetchone()

        if customer is None:
            print("Customer not found.")
            return

        print(f"\nCustomer: {customer[0]} {customer[1]}")

        confirmation = input(
            "Delete this customer? (yes/no): "
        ).strip().lower()

        if confirmation != "yes":
            print("Deletion cancelled.")
            return

        cursor.execute(
            "DELETE FROM customers WHERE customer_id = %s",
            (customer_id,)
        )

        deleted_count = cursor.rowcount
        connection.commit()

        if deleted_count == 1:
            print("Customer deleted successfully!")
        else:
            print("No customer was deleted.")

    except mysql.connector.Error as error:
        connection.rollback()
        print(f"Delete failed: {error}")

    finally:
        cursor.close()

def main():
    connection = None

    try:
        connection = connect_database()
        print("\nConnected to Amazon RDS MySQL!")
        while True:
            print("\n===== CUSTOMER MANAGEMENT =====")
            print("1. Display all customers")
            print("2. Add a new customer")
            print("3. Update a customer")
            print("4. Delete a customer")
            print("5. Exit")

            choice = input("\nEnter your choice: ").strip()

            if choice == "1":
                display_customers(connection)

            elif choice == "2":
                add_customer(connection)

            elif choice == "3":
                update_customer(connection)

            elif choice == "4":
                delete_customer(connection)

            elif choice == "5":
                print("Exiting application.")
                break

            else:
                print("Invalid choice. Please try again.")

    except mysql.connector.Error as error:
        print(f"Database error: {error}")

    finally:
        if connection is not None and connection.is_connected():
            connection.close()
            print("Database connection closed.")


if __name__ == "__main__":
    main()
(venv) (venv) [ec2-user@ip-10-0-1-174 mysql-python-app]$ 
