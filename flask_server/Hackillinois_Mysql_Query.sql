CREATE DATABASE organization_db;

USE organization_db;

-- Table for storing employee information
CREATE TABLE Employee_Info (
    employee_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    email VARCHAR(255),
    address VARCHAR(255),
    phone_number VARCHAR(20)
);

-- Table for storing tasks
CREATE TABLE Tasks (
    task_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255),
    description TEXT,
    status VARCHAR(50),
    estimated_completion_time INT -- You may want to adjust data type according to your requirements
);

-- Table for storing skills
CREATE TABLE Skills (
    skill_id INT AUTO_INCREMENT PRIMARY KEY,
    skill_name VARCHAR(255)
);

-- Table for mapping skills to employees
CREATE TABLE Skill_to_Employee_Mapping (
    row_id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id INT,
    skill_id INT,
    FOREIGN KEY (employee_id) REFERENCES Employee_Info(employee_id),
    FOREIGN KEY (skill_id) REFERENCES Skills(skill_id)
);

-- Table for mapping skills required for tasks
CREATE TABLE Skill_to_Task_Mapping (
    task_to_skill_id INT AUTO_INCREMENT PRIMARY KEY,
    task_id INT,
    skill_id INT,
    FOREIGN KEY (task_id) REFERENCES Tasks(task_id),
    FOREIGN KEY (skill_id) REFERENCES Skills(skill_id)
);

-- Table for storing employee availability
CREATE TABLE Availability (
    availability_id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id INT,
    hours_available INT,
    FOREIGN KEY (employee_id) REFERENCES Employee_Info(employee_id)
);
