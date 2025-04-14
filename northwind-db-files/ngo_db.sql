DROP DATABASE IF EXISTS ngo_database;
CREATE DATABASE IF NOT EXISTS ngo_database;

USE ngo_database;


CREATE TABLE IF NOT EXISTS WorldNGOs (
    NGO_ID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(255) NOT NULL,
    Country VARCHAR(100) NOT NULL,
    Founding_Year INTEGER,
    Focus_Area VARCHAR(100),
    Website VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS Projects (
    Project_ID INT AUTO_INCREMENT PRIMARY KEY,
    Project_Name VARCHAR(255) NOT NULL,
    Focus_Area VARCHAR(100),
    Budget DECIMAL(15, 2),
    NGO_ID INT,
    Start_Date DATE,
    End_Date DATE,
    FOREIGN KEY (NGO_ID) REFERENCES WorldNGOs(NGO_ID)
);

CREATE TABLE IF NOT EXISTS Donors (
    Donor_ID INT AUTO_INCREMENT PRIMARY KEY,
    Donor_Name VARCHAR(255) NOT NULL,
    Donor_Type ENUM('Individual', 'Organization') NOT NULL,
    Donation_Amount DECIMAL(15, 2),
    NGO_ID INT,
    FOREIGN KEY (NGO_ID) REFERENCES WorldNGOs(NGO_ID)
);

INSERT INTO WorldNGOs (Name, Country, Founding_Year, Focus_Area, Website)
VALUES
('World Wildlife Fund', 'United States', 1961, 'Environmental Conservation', 'https://www.worldwildlife.org'),
('Doctors Without Borders', 'France', 1971, 'Medical Relief', 'https://www.msf.org'),
('Oxfam International', 'United Kingdom', 1995, 'Poverty and Inequality', 'https://www.oxfam.org'),
('Amnesty International', 'United Kingdom', 1961, 'Human Rights', 'https://www.amnesty.org'),
('Save the Children', 'United States', 1919, 'Child Welfare', 'https://www.savethechildren.org'),
('Greenpeace', 'Netherlands', 1971, 'Environmental Protection', 'https://www.greenpeace.org'),
('International Red Cross', 'Switzerland', 1863, 'Humanitarian Aid', 'https://www.icrc.org'),
('CARE International', 'Switzerland', 1945, 'Global Poverty', 'https://www.care-international.org'),
('Habitat for Humanity', 'United States', 1976, 'Affordable Housing', 'https://www.habitat.org'),
('Plan International', 'United Kingdom', 1937, 'Child Rights', 'https://plan-international.org');

INSERT INTO Projects (Project_Name, Focus_Area, Budget, NGO_ID, Start_Date, End_Date)
VALUES
('Save the Amazon', 'Environmental Conservation', 5000000.00, 1, '2022-01-01', '2024-12-31'),
('Emergency Medical Aid in Syria', 'Medical Relief', 3000000.00, 2, '2023-03-01', '2023-12-31'),
('Education for All', 'Poverty and Inequality', 2000000.00, 3, '2021-06-01', '2025-05-31'),
('Human Rights Advocacy in Asia', 'Human Rights', 1500000.00, 4, '2022-09-01', '2023-08-31'),
('Child Nutrition Program', 'Child Welfare', 2500000.00, 5, '2022-01-01', '2024-01-01');

INSERT INTO Donors (Donor_Name, Donor_Type, Donation_Amount, NGO_ID)
VALUES
('Bill & Melinda Gates Foundation', 'Organization', 10000000.00, 1),
('Elon Musk', 'Individual', 5000000.00, 2),
('Google.org', 'Organization', 2000000.00, 3),
('Open Society Foundations', 'Organization', 3000000.00, 4),
('Anonymous Philanthropist', 'Individual', 1000000.00, 5);