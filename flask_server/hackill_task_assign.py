import mysql.connector

def match_employees_to_tasks():
    # Connect to the database
    db_connection = mysql.connector.connect(
        host="10.191.157.62",
        user="aanyasd",
        password="hackillinois",
        database="organization_db"
    )

    # Create a cursor object to execute queries
    cursor = db_connection.cursor()

    # Query to get tasks and their required skills
    cursor.execute("SELECT task_id, name, estimated_completion_time FROM Tasks")
    tasks = cursor.fetchall()

    # Match employees to tasks
    for task in tasks:
        task_id, task_name, estimated_completion_time = task
        print(f"\nTask: {task_id}, Name: {task_name}, Estimated Completion Time: {estimated_completion_time}")

        # Query to get required skills for the task
        cursor.execute("SELECT skill_id FROM Skill_to_Task_Mapping WHERE task_id = %s", (task_id,))
        required_skills = [row[0] for row in cursor.fetchall()]
        print("Required Skills:", required_skills)

        # Query to get employees with their skills and availability
        cursor.execute("""
    SELECT e.employee_id, e.name, COUNT(DISTINCT s.skill_id) AS num_skills, a.hours_available
    FROM Employee_Info e
    INNER JOIN Skill_to_Employee_Mapping se ON e.employee_id = se.employee_id
    INNER JOIN Skills s ON se.skill_id = s.skill_id
    INNER JOIN Availability a ON e.employee_id = a.employee_id
    WHERE s.skill_id IN {} 
    GROUP BY e.employee_id, e.name, a.hours_available
    HAVING COUNT(DISTINCT s.skill_id) = {} AND a.hours_available >= {}
""".format(tuple(required_skills), len(required_skills), estimated_completion_time))

        suitable_employees = cursor.fetchall()

        if suitable_employees:
            # Sort employees by the number of matching skills (descending) and hours available (ascending)
            suitable_employees.sort(key=lambda x: (x[2], -x[3]))
            assigned_employee = suitable_employees[0]  # Assign to the employee with the most relevant skills and enough time
            print(f"Assigning task '{task_name}' to employee '{assigned_employee[1]}'")

            # Update employee's available hours
            update_hours_query = "UPDATE Availability SET hours_available = hours_available - %s WHERE employee_id = %s"
            cursor.execute(update_hours_query, (estimated_completion_time, assigned_employee[0]))
            db_connection.commit()  # Commit the update

            # Insert record into Task to Employee mapping table
            insert_mapping_query = "INSERT INTO Task_Employee_Mapping (task_id, employee_id) VALUES (%s, %s)"
            cursor.execute(insert_mapping_query, (task_id, assigned_employee[0]))
            db_connection.commit()  # Commit the insertion
        else:
            print(f"No suitable employee found for task '{task_name}'")

    # Close cursor and database connection
    cursor.close()
    db_connection.close()


def add_employee(name, email, address, phone_number, skills):
    # Connect to the database
    db_connection = mysql.connector.connect(
        host="10.191.157.62",
        user="aanyasd",
        password="hackillinois",
        database="organization_db"
    )

    # Create a cursor object to execute queries
    cursor = db_connection.cursor()

    try:
        # Insert employee information into Employee_Info table
        insert_employee_query = "INSERT INTO Employee_Info (name, email, address, phone_number) VALUES (%s, %s, %s, %s)"
        cursor.execute(insert_employee_query, (name, email, address, phone_number))
        employee_id = cursor.lastrowid

        # Map employee skills to Employee_Info table
        for skill_id in skills:
            insert_skill_mapping_query = "INSERT INTO Skill_to_Employee_Mapping (employee_id, skill_id) VALUES (%s, %s)"
            cursor.execute(insert_skill_mapping_query, (employee_id, skill_id))

        # Commit the transaction
        db_connection.commit()
        print("Employee added successfully.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        # Rollback the transaction in case of error
        db_connection.rollback()

    # Close cursor and database connection
    cursor.close()
    db_connection.close()

def add_task(task_name, description, status, estimated_completion_time, skills):
    # Connect to the database
    db_connection = mysql.connector.connect(
        host="10.191.157.62",
        user="aanyasd",
        password="hackillinois",
        database="organization_db"
    )

    # Create a cursor object to execute queries
    cursor = db_connection.cursor()

    try:
        # Insert task information into Tasks table
        insert_task_query = "INSERT INTO Tasks (name, description, status, estimated_completion_time) VALUES (%s, %s, %s, %s)"
        cursor.execute(insert_task_query, (task_name, description, status, estimated_completion_time))
        task_id = cursor.lastrowid

        # Map required skills to Skill_to_Task_Mapping table
        for skill_id in skills:
            insert_skill_mapping_query = "INSERT INTO Skill_to_Task_Mapping (task_id, skill_id) VALUES (%s, %s)"
            cursor.execute(insert_skill_mapping_query, (task_id, skill_id))

        # Commit the transaction
        db_connection.commit()
        print("Task added successfully.")

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        # Rollback the transaction in case of error
        db_connection.rollback()

    # Close cursor and database connection
    cursor.close()
    db_connection.close()

def generate_task_report():
    # Connect to the database
    db_connection = mysql.connector.connect(
        host="10.191.157.62",
        user="aanyasd",
        password="hackillinois",
        database="organization_db"
    )

    # Create a cursor object to execute queries
    cursor = db_connection.cursor()

    # Query to get tasks and their assigned employees
    cursor.execute("""
        SELECT t.task_id, t.name AS task_name, t.description, e.name AS assigned_employee, e.email AS employee_email
        FROM Task_Employee_Mapping tem
        INNER JOIN Tasks t ON tem.task_id = t.task_id
        INNER JOIN Employee_Info e ON tem.employee_id = e.employee_id
    """)
    assigned_tasks = cursor.fetchall()

    # Close cursor and database connection
    cursor.close()
    db_connection.close()

    # Generate report
    if assigned_tasks:
        with open("task_report.txt", "w") as file:
            file.write("Assigned Tasks Report:\n\n")
            for task in assigned_tasks:
                task_id, task_name, description, assigned_employee, employee_email = task
                file.write(f"Task ID: {task_id}\n")
                file.write(f"Task Name: {task_name}\n")
                file.write(f"Description: {description}\n")
                file.write(f"Assigned Employee: {assigned_employee}\n")
                file.write(f"Employee Email: {employee_email}\n")
                file.write("--------------------------\n")
        print("Task report generated successfully.")
    else:
        print("No tasks assigned.")

# Call the function to generate the report
generate_task_report()

# Example usage:
skills_1 = [3]  # Example skills (Python and JavaScript)
add_employee("New Employee", "new@example.com", "789 Oak St", "123-789-4560", skills_1)

skills_2 = [2, 4, 5]
add_task("New Task", "deploy new features", 0, 12, skills_2)


if __name__ == "__main__":
    match_employees_to_tasks()
