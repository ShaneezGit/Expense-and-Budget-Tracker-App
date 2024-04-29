# =========== Compulsory Task (Option 1).py ===========

# ************ BEGIN ************ #


# Import sqlite3 library
import sqlite3

# Connect to the sqlite database called "expense_tracker.db"
# Get a cursor object
conn = sqlite3.connect("expense_tracker.db")
cursor = conn.cursor()


# Create tables if they don't exist
cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS expenses (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category_id INTEGER,
        amount REAL NOT NULL,
        date DATE NOT NULL,
        FOREIGN KEY (category_id) REFERENCES categories (id)
    )
    """
)

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS income (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category TEXT NOT NULL,
        amount REAL NOT NULL,
        date DATE NOT NULL
    )
    """
)

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE
    )
    """
)

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS budgets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        category_id INTEGER,
        budget_amount REAL NOT NULL,
        FOREIGN KEY (category_id) REFERENCES categories (id)
    )
    """
)

cursor.execute(
    """
    CREATE TABLE IF NOT EXISTS financial_goals (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        goal_name TEXT NOT NULL,
        target_amount REAL NOT NULL,
        progress_amount REAL,
        date DATE NOT NULL
    )
    """
)

conn.commit()



# Function to add a new expense category
# Check if the category already exists
# Insert a new category into the 'categories' table
def add_category(name):
    try:
        cursor.execute("SELECT id FROM categories WHERE name = ?", (name.lower(),))
        existing_category = cursor.fetchone()

        if existing_category is None:
            cursor.execute("INSERT INTO categories (name) VALUES (?)", (name.lower(),))
            conn.commit()
            print(f"Category '{name}' added successfully.")
        else:
            raise ValueError(f"Category '{name}' already exists.")
    except ValueError as ve:
        print(f"Error: {ve}")
    except sqlite3.Error as se:
        print(f"SQLite Error: {se}")


# Function to add a new expense
# Insert a new expense into the 'expenses' table
def add_expense(category_name, amount, date):
    try:
        cursor.execute("SELECT id, name FROM categories")
        categories = cursor.fetchall()

        category_names = [category[1].lower() for category in categories]

        if category_name.lower() in category_names:
            existing_category_id = next(
                (category[0] for category in categories if category[1].lower() == category_name.lower()),
                None
            )
            cursor.execute(
                "INSERT INTO expenses (category_id, amount, date) VALUES (?, ?, ?)",
                (existing_category_id, amount, date),
            )
            conn.commit()
            print("Expense added successfully.")
        else:
            print(f"Category '{category_name}' does not exist. Existing categories: {', '.join(category_names)}")

            print("Existing Categories:")
            for category in categories:
                print(category[1])

            add_category_choice = input("Enter 'yes' (case-sensitive) to add or any other key to cancel: ")
            if add_category_choice.lower() == 'yes':
                add_category(category_name)
                add_expense(category_name, amount, date)
            else:
                print("Expense not added. Please add the category first.")
    except ValueError as ve:
        print(f"Error: {ve}")           
    except sqlite3.Error as se:
        print(f"SQLite Error: {se}")


# Function to update an expense amount
def update_expense_amount():
    try:
        cursor.execute("SELECT id, amount FROM expenses")
        expenses = cursor.fetchall()

        if not expenses:
            print("No expenses found.")
            return
        print("\nValid Expenses:")
        print("{:5} {:10}".format("ID", "Amount"))
        print("=" *25)
        for expense in expenses:
            print("{:5} {:10}".format(expense[0], expense[1]))

        expense_id = input("Enter the ID of the expense to update: ")

        try:
            expense_id = int(expense_id)
            new_amount = float(input("Enter the new expense amount: "))
            cursor. execute(
                "UPDATE expenses SET amount = ? WHERE id = ?", (new_amount, expense_id)
            )
            conn.commit()
            print("Expense amount updated successfully.")
        except ValueError as ve:
            print(f"Error: Invalid input for ID or new amount.")
    
    except sqlite3.Error as se:
        print(f"SQLite Error: {se}")


# Function to delete an expense category
def delete_expense_category_from_database(expense_name):
    cursor.execute("SELECT * FROM expenses")
    expenses = cursor.fetchall()

    if not expenses:
        print("No expenses found.")
        return

    print("Current Expense Categories:")
    print("{:<5} {:<15}".format("ID", "Expense Name"))
    print("=" * 25)
    for expense in expenses:
        print("{:<5} {:<15}".format(expense[0], expense[1]))

    try:
        cursor.execute(
            "DELETE FROM expenses WHERE category_id IN (SELECT id FROM categories WHERE name = ?)",
            (expense_name,),
        )
        cursor.execute("DELETE FROM categories WHERE name = ?", (expense_name,))
        conn.commit()
        print(f"Expense '{expense_name}' deleted successfully.")
    except ValueError as ve:
        print(f"Error: {ve}")
    except sqlite3.Error as se:
        print(f"SQLite Error: {se}")


# Function to track pending expenses
def track_pending_expenses():
    cursor.execute("SELECT * FROM expenses WHERE amount > 0")
    pending_expenses = cursor.fetchall()

    if not pending_expenses:
        print("No pending expenses found.")
        return

    print("\nPending Expenses:")
    print("{:<5} {:<15} {:<10} {:<10}".format("ID", "Category", "Amount", "Date"))
    print("=" * 40)

    for expense in pending_expenses:
        expense_id, category_id, amount, date = expense
        cursor.execute("SELECT name FROM categories WHERE id = ?", (category_id,))
        category_name = cursor.fetchone()[0]
        print(
            "{:<5} {:<15} {:<10} {:<10}".format(expense_id, category_name, amount, date)
        )


# Function to handle additional expense functionalities
def additional_expense_options():
    print("\nAdditional Expense Options:")
    print("\na. Update Expense Amount")
    print("b. Delete Expense Category from Database")
    print("c. Track Pending Expenses")
    print("d. Go Back to Main Menu")
    choice = input("\nEnter your choice (a, b, c, d): ")

    if choice == "a":
        try:
            expense_name = input("Enter expense name to update: ")
            new_amount = float(input("Enter new expense amount: "))
            update_expense_amount(expense_name, new_amount)
        except ValueError:
            print("Invalid input. Please enter valid values.")

    elif choice == "b":
        try:
            expense_name = input("Enter expense name to delete: ")
            delete_expense_category_from_database(expense_name)
        except ValueError:
            print("Invalid input. Please enter a valid expense name.")

    elif choice == "c":
        track_pending_expenses()
    
    elif choice == "d":
        return

    else:
        print("Invalid choice. Returning to main menu.")


# Function to view all expenses
def view_expenses():
    print("View Expenses Function Called")
    cursor.execute("SELECT * FROM expenses")
    expenses = cursor.fetchall()

    if expenses:
        print("{:<5} {:<15} {:<10} {:<10}".format("ID", "Category", "Amount", "Date"))
        print("=" * 40)
        for expense in expenses:
            expense_id, category_id, amount, date = expense
            cursor.execute("SELECT name FROM categories WHERE id = ?", (category_id,))
            category_name = cursor.fetchone()[0]
            print(
                "{:<5} {:<15} {:<10} {:<10}".format(
                    expense_id, category_name, amount, date
                )
            )
    else:
        print("No expenses found.")
    print("View Expenses Function Completed")


# Function to view expenses by category
# Display available categories
# Get user input for the category name
# Fetch category_id for the given category_name
# Fetch expenses for the specified category_id
def view_expenses_by_category():
    cursor.execute("SELECT name FROM categories")
    categories = cursor.fetchall()

    print("Available Categories:")
    for category in categories:
        print(category[0])

    category_name = input("Enter the name of the category: ")

    cursor.execute("SELECT id FROM categories WHERE name = ?", (category_name,))
    category_id = cursor.fetchone()

    if category_id is not None:
        cursor.execute(
            "SELECT * FROM expenses WHERE LOWER(category_id) = LOWER(?)", (category_id[0],)
        )
        expenses = cursor.fetchall()

        if expenses:
            print(f"\nExpenses for category '{category_name}':")
            for expense in expenses:
                expense_id, _, amount, date = expense
                print(f"ID: {expense_id}, Amount: {amount}, Date: {date}")
        else:
            print(f"No expenses found for category '{category_name}'.")
    else:
        print(f"Category '{category_name}' not found.")


# Function to add income
def add_income(category_name, amount, date):
    try:
        category_name = category_name.lower()
        cursor.execute(
            "INSERT INTO income (category, amount, date) VALUES (?, ?, ?)",
            (category_name, amount, date),
        )
        conn.commit()
        print(
            f"Income entry of {amount} added successfully for category '{category_name}' on {date}."
        )
    except sqlite3.IntegrityError as ie:
        print(ie)


# Function to view all income entries
def view_income(category_name=None):
    if category_name:
        cursor.execute("SELECT * FROM income WHERE LOWER(category) = LOWER(?)", (category_name,))
    else:
        cursor.execute("SELECT * FROM income")

    income_entries = cursor.fetchall()

    if income_entries:
        print("{:<5} {:<15} {:<10} {:<10}".format("ID", "Category", "Amount", "Date"))
        print("=" * 40)
        for entry in income_entries:
            income_id, category, amount, date = entry
            print(
                "{:<5} {:<15} {:<10} {:<10}".format(income_id, category, amount, date)
            )
    else:
        print("No income entries found.")


# Function to view income by category
def view_income_by_category(category_name):
    cursor.execute("SELECT * FROM income WHERE LOWER(category) = LOWER(?)", (category_name,))
    income_entries = cursor.fetchall()

    if income_entries:
        print("{:<5} {:<15} {:<10} {:<10}".format("ID", "Category", "Amount", "Date"))
        print("=" * 40)
        for entry in income_entries:
            income_id, category, amount, date = entry
            print("{:<5} {:<15} {:<10} {:<10}".format(income_id, category, amount, date))
    else:
        print("No income entries found for category '{}'.".fomat(category_name))
        

# Function to set budget for a catagory
def set_budget(category_name, budget_amount):
    try:
        category_name = category_name.lower()
        cursor.execute(
            "INSERT OR REPLACE INTO budgets (category_id, budget_amount) VALUES ((SELECT id FROM categories WHERE LOWER(name) = LOWER(?)), ?)",
            (category_name, budget_amount),
        )
        conn.commit()
        print(
            f"Budget of {budget_amount} set successfully for category '{category_name}'."
        )
    except sqlite3.Error as se:
        print(f"SQLite Error: {se}")


# Function to view budget for a category
def view_budget(category_name):
    category_name = category_name.lower()
    cursor.execute(
        "SELECT budget_amount FROM budgets WHERE category_id = (SELECT id FROM categories WHERE name = ?)",
        (category_name,),
    )
    budget_amount = cursor.fetchone()

    if budget_amount is not None:
        print(f"The budget for category '{category_name}' is: {budget_amount[0]}")
    else:
        print(
            f"Budget not set for category '{category_name}'. Please consider setting a budget for better financial management."
        )


# Function to set financial goals
def set_financial_goals(goal_name, target_amount, date):
    progress_amount = 0
    cursor.execute(
        "INSERT INTO financial_goals (goal_name, target_amount, progress_amount, date) VALUES (?, ?, ?, ?)",
        (goal_name, target_amount, progress_amount, date),
    )
    conn.commit()
    print(
        f"Financial goal '{goal_name}' of {target_amount} set successfully. Target date: {date}."
    )


# Function to view progress towards financial goals
def view_progress_towards_goals():
    cursor.execute("SELECT DISTINCT * FROM financial_goals")
    goals = cursor.fetchall()

    if not goals:
        print("No goals in progress.")
        return

    for goal in goals:
        print(
            f"Goal Name: {goal[1]}, Target Amount: {goal[2]}, Progress Amount: {goal[3]}, Date: {goal[4]}"
        )


# Add sample data
def add_sample_data():
    cursor.execute("SELECT COUNT(*) FROM categories WHERE name IN ('utilities', 'salary')")
    existing_category_count = cursor.fetchone()[0]

    if existing_category_count < 2:
        cursor.execute("INSERT OR IGNORE INTO categories (name) VALUES ('utilities')")
        cursor.execute("INSERT OR IGNORE INTO categories (name) VALUES ('salary')")
        conn.commit() 

    def insert_category(name):
        cursor.execute("INSERT OR IGNORE INTO categories (name) VALUES (?)", (name.lower(),))
    
    def insert_expense(category_name, amount, date):
        category_name = category_name.lower()
        cursor.execute("SELECT id FROM categories WHERE name = ?", (category_name,))
        category_id = cursor.fetchone()

        if category_id is not None:
            cursor.execute(
                "INSERT OR IGNORE INTO expenses (category_id, amount, date) VALUES (?, ?, ?)",
                (category_id[0], amount, date),
            )
    
    def insert_income(category_name, amount, date):
        category_name = category_name.lower()
        cursor.execute(
            "INSERT OR IGNORE INTO income (category, amount, date) VALUES (?, ?, ?)",
            (category_name, amount, date),
        )

    def insert_budget(category_name, budget_amount):
        category_name = category_name.lower()
        cursor.execute(
            "INSERT OR IGNORE INTO budgets (category_id, budget_amount) VALUES ((SELECT id FROM categories WHERE name = ?), ?)",
            (category_name, budget_amount),
        )
    
    def insert_goal(goal_name, target_amount, date):
        goal_name_lower = goal_name.lower()

        cursor.execute(
            "SELECT COUNT(*) FROM financial_goals WHERE goal_name = ?", (goal_name_lower,)
        )
        goal_exists = cursor.fetchone()[0] > 0

        if not goal_exists:
            cursor.execute(
                "INSERT INTO financial_goals (goal_name, target_amount, progress_amount, date) VALUES (?, ?, 0, ?)",
                (goal_name, target_amount, date),
            )
    insert_goal("vacation", 15000.0, "2024-06-30")

    insert_expense("utilities", 1200.0, "2024-01-19")
    insert_income("salary", 45000.0, "2024-01-25")

    insert_category("groceries")
    insert_category("entertainment")

    insert_budget("groceries", 3000.00)
    insert_budget("entertainment", 1500.0)

    conn.commit()



# Display menu options to user
# Proceed based on user input
# Close database connection when exiting program
print("\n*** Welcome to the Budget Tracker! ***")
try:
    add_sample_data()
    while True:
        print("\nExpense Tracker Menu:")
        print("\n1.  Add Expense")
        print("2.  View Expenses")
        print("3.  View Expenses by Category")
        print("4.  Add Income")
        print("5.  View Income")
        print("6.  View Income by Category")
        print("7.  Set Budget for a Category")
        print("8.  View Budget for a Category")
        print("9.  Set Financial Goals")
        print("10. View Progress towards Financial Goals")
        print("11. Add New Category")
        print("12. Quit")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            category_name = input("Enter category name: ")
            amount = float(input("Enter expense amount: "))
            date = input("Enter expense date (YYYY-MM-DD): ")

            try:
                amount = float(amount)
                add_expense(category_name, amount, date)
                additional_expense_options()
            except ValueError:
                print("Error: Please enter a valid numeric amount.")

        elif choice == "2":
            try:
                view_expenses()
            except sqlite3.Error as se:
                print(f"SQLite Error: {se}")
            additional_expense_options()

        elif choice == "3":
            view_expenses_by_category()

        elif choice == "4":
            category_name = input("Enter category name: ")
            amount = float(input("Enter income amount: "))
            date = input("Enter income date (YYYY-MM-DD): ")

            try:
                add_expense(category_name, amount, date)
                additional_expense_options()
            except ValueError:
                print("Error: Please enter a valid numeric amount.")

        elif choice == "5":
            print("\nView Income Options:")
            print("a. View all income")
            print("b. View income by category")
            view_income_choice = input("\nEnter your choice (a, b): ")

            if view_income_choice == "a":
                view_income()
            elif view_income_choice == "b":
                cursor.execute("SELECT name FROM categories")
                categories = cursor.fetchall()

                print("\nAvailable Categories:")
                for category in categories:
                    print(category[0])

                category_name = input("Enter the name of the category: ")
                view_income(category_name)
            else:
                print("Invalid choice. Returning to main menu.")

        elif choice == "6":
            category_name = input("Enter category name: ")
            view_income_by_category(category_name)

        elif choice == "7":
            category_name = input("Enter category name: ")
            budget_amount = float(input("Enter budget amount: "))
            set_budget(category_name, budget_amount)

        elif choice == "8":
            category_name = input("Enter category name: ")
            view_budget(category_name)

        elif choice == "9":
            goal_name = input("Enter financial goal name: ")
            target_amount = float(input("Enter target amount for the goal: "))
            date = input("Enter goal date (YYYY-MM-DD): ")
            set_financial_goals(goal_name, target_amount, date)
            print(
                f"Financial goal '{goal_name}' successfully added with a target amount of {target_amount} on {date}."
            )

        elif choice == "10":
            view_progress_towards_goals()
        
        elif choice == "11":
            new_category_name = input("Enter new category name: ")
            add_category(new_category_name)
            print(f"Category '{new_category_name}' added successfully.")

        elif choice == "12":
            print("Goodbye, remember to budget!")
            break

        else:
            print("Invalid choice. Please try again.")


except Exception as e:
    print(f"An error occured: {e}")

finally:
    conn.close()
    print("Database connection closed.")

# ****************** END OF CODE ********************* #
