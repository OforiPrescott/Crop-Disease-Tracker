-- Create Database
CREATE DATABASE AgriDiseaseDB;
GO


USE AgriDiseaseDB;
GO


-- Farms Table
CREATE TABLE Farms (
    farm_id INT PRIMARY KEY IDENTITY(1,1),
    farm_name VARCHAR(100) NOT NULL,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    soil_type VARCHAR(50),
    irrigation_method VARCHAR(50),
    farm_size_ha FLOAT
);


-- Crops Table
CREATE TABLE Crops (
    crop_id INT PRIMARY KEY IDENTITY(1,1),
    farm_id INT FOREIGN KEY REFERENCES Farms(farm_id),
    crop_type VARCHAR(50) NOT NULL,
    planting_date DATE NOT NULL
);


-- DiseaseReports Table
CREATE TABLE DiseaseReports (
    report_id INT PRIMARY KEY IDENTITY(1,1),
    farm_id INT FOREIGN KEY REFERENCES Farms(farm_id),
    crop_id INT FOREIGN KEY REFERENCES Crops(crop_id),
    disease_name VARCHAR(50) NOT NULL,
    report_date DATE NOT NULL,
    severity INT CHECK (severity BETWEEN 1 AND 10),
    description VARCHAR(255)
);


-- WeatherData Table
CREATE TABLE WeatherData (
    weather_id INT PRIMARY KEY IDENTITY(1,1),
    farm_id INT FOREIGN KEY REFERENCES Farms(farm_id),
    record_date DATE NOT NULL,
    temperature_c FLOAT,
    humidity_percent FLOAT,
    rainfall_mm FLOAT,
    wind_speed_kph FLOAT
);


GO

PRINT 'Database and tables created successfully!';