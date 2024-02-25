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

ALTER TABLE Tasks
MODIFY COLUMN status INT;

CREATE TABLE Task_Employee_Mapping (
    mapping_id INT AUTO_INCREMENT PRIMARY KEY,
    task_id INT,
    employee_id INT,
    FOREIGN KEY (task_id) REFERENCES Tasks(task_id),
    FOREIGN KEY (employee_id) REFERENCES Employee_Info(employee_id)
);


-- Populate the tables with sample data
INSERT INTO Employee_Info (name, email, address, phone_number) VALUES 
    ('John Doe', 'john@example.com', '123 Main St', '123-456-7890'),
    ('Jane Smith', 'jane@example.com', '456 Elm St', '987-654-3210');

INSERT INTO Tasks (name, description, status, estimated_completion_time) VALUES 
    ('Task 1', 'Description for Task 1', 0, 8),
    ('Task 2', 'Description for Task 2', 1, 6);

INSERT INTO Skills (skill_name) VALUES 
    ('Python'),
    ('JavaScript'),
    ('HTML/CSS'),
    ('React'),
    ('Node.js'),
    ('SQL');

-- Mapping developer skills to employees
INSERT INTO Skill_to_Employee_Mapping (employee_id, skill_id) VALUES 
    (1, 1), -- John Doe knows Python
    (1, 2), -- John Doe knows JavaScript
    (2, 2), -- Jane Smith knows JavaScript
    (2, 4), -- Jane Smith knows React
    (2, 5); -- Jane Smith knows Node.js

-- Mapping developer skills to tasks
INSERT INTO Skill_to_Task_Mapping (task_id, skill_id) VALUES 
    (1, 1), -- Task 1 requires Python
    (1, 2), -- Task 1 requires JavaScript
    (2, 2), -- Task 2 requires JavaScript
    (2, 4), -- Task 2 requires React
    (2, 5); -- Task 2 requires Node.js

-- Inserting availability for employees
INSERT INTO Availability (employee_id, hours_available) VALUES 
    (1, 40), -- John Doe is available for 40 hours
    (2, 30); -- Jane Smith is available for 30 hours
    
CREATE USER 'aanyasd'@'%' IDENTIFIED BY 'hackillinois';
GRANT ALL PRIVILEGES ON *.* TO 'aanyasd'@'%' WITH GRANT OPTION;
<<<<<<< HEAD
FLUSH PRIVILEGES;
=======
FLUSH PRIVILEGES;
>>>>>>> 44339cee75ab18bc4a03132de361814b6835e138
