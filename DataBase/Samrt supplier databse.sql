CREATE DATABASE supply_chain_db;

USE supply_chain_db;


SHOW TABLES;

#suppliers
CREATE TABLE Suppliers (
    Supplier_ID VARCHAR(10) PRIMARY KEY,
    Supplier_Name VARCHAR(255),
    Supplier_Rating DECIMAL(3,1),
    Supplier_Location VARCHAR(100)
);

DESCRIBE suppliers;
SELECT * FROM Suppliers;
SELECT * FROM Suppliers LIMIT 10;
SELECT COUNT(*) AS Total_Rows
FROM Suppliers;
SELECT COUNT(*) FROM Shipments;


#Warehouses

CREATE TABLE Warehouses (
    Warehouse_ID VARCHAR(10) PRIMARY KEY,
    Warehouse_Name VARCHAR(100),
    Warehouse_Location VARCHAR(100),
    Capacity INT
);

SELECT * FROM Warehouses;
DESCRIBE warehouses;

# Shipments 

CREATE TABLE Shipments (
    Shipment_ID VARCHAR(20) PRIMARY KEY,
    Order_ID VARCHAR(20),
    Shipment_Date DATE,
    Delivery_Date DATE,
    Delivery_Time INT
);


DESC Shipments;
SELECT * FROM Shipments;


SELECT * FROM Suppliers;

SELECT * FROM Warehouses;

SELECT * FROM Shipments;

CREATE TABLE orders (
    Order_ID VARCHAR(20) NOT NULL,
    Supplier_ID VARCHAR(20),
    Warehouse_ID VARCHAR(20),
    Customer_Priority VARCHAR(45),
    PRIMARY KEY (Order_ID)
);

SELECT * FROM orders;




#Create Predictions Table


CREATE TABLE Predictions (
    Prediction_ID INT AUTO_INCREMENT PRIMARY KEY,
    Order_ID VARCHAR(20),
    Predicted_Status VARCHAR(20),
    Prediction_Date DATETIME DEFAULT CURRENT_TIMESTAMP
);

DESCRIBE Predictions;


#Create Prediction_logs
CREATE TABLE Prediction_Logs (
    Log_ID INT AUTO_INCREMENT PRIMARY KEY,
    Prediction_ID INT,
    Log_Message VARCHAR(255),
    Log_Time DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (Prediction_ID)
        REFERENCES Predictions(Prediction_ID)
);

DESCRIBE Prediction_Logs;

INSERT INTO Predictions
(Order_ID,Predicted_Status)

VALUES

('ORD001','Delayed');


#JOIN Query
#Retrieve supplier and warehouse information.

SELECT
    s.Supplier_ID,
    s.Supplier_Name,
    COUNT(sh.Shipment_ID) AS Total_Shipments
FROM Suppliers s
JOIN Orders o
    ON s.Supplier_ID = o.Supplier_ID
JOIN Shipments sh
    ON o.Order_ID = sh.Order_ID
GROUP BY s.Supplier_ID, s.Supplier_Name
ORDER BY Total_Shipments DESC;


# Retrieve Warehouse Performance (Route Performance)

SELECT
    w.Warehouse_ID,
    w.Warehouse_City,
    COUNT(sh.Shipment_ID) AS Total_Shipments
FROM Warehouses w
JOIN Orders o
    ON w.Warehouse_ID = o.Warehouse_ID
JOIN Shipments sh
    ON o.Order_ID = sh.Order_ID
GROUP BY
    w.Warehouse_ID,
    w.Warehouse_City
ORDER BY Total_Shipments DESC;


    
    




SELECT * FROM Suppliers;
SELECT * FROM Warehouses;
SELECT * FROM Shipments;

#CTE
#Average delivery time per warehouse.
WITH WarehouseDelivery AS
(SELECT o.Warehouse_ID,
AVG(sh.Delivery_Time) AS AvgDelivery
FROM Orders o
JOIN Shipments sh
ON o.Order_ID=sh.Order_ID
GROUP BY o.Warehouse_ID)
SELECT * FROM WarehouseDelivery
ORDER BY AvgDelivery DESC;



#Window Function
#Ranking warehouses based on shipment count.
SELECT
Warehouse_ID,
COUNT(*) AS TotalShipments,
RANK() OVER
(
ORDER BY COUNT(*) DESC
)
AS WarehouseRank
FROM Orders
GROUP BY Warehouse_ID;



#View
CREATE VIEW Supplier_Performance AS
SELECT
s.Supplier_Name,
COUNT(sh.Shipment_ID) AS TotalShipments
FROM Suppliers s
JOIN Orders o
ON s.Supplier_ID=o.Supplier_ID
JOIN Shipments sh
ON o.Order_ID=sh.Order_ID
GROUP BY s.Supplier_Name;

SELECT * FROM Supplier_Performance;


#Stored Proceduresupplier_performance
DELIMITER $$
CREATE PROCEDURE GetSupplierPerformance()
BEGIN
SELECT
s.Supplier_Name,
COUNT(sh.Shipment_ID) AS TotalShipments
FROM Suppliers s
JOIN Orders o
ON s.Supplier_ID=o.Supplier_ID
JOIN Shipments sh
ON o.Order_ID=sh.Order_ID
GROUP BY s.Supplier_Name;
END $$
DELIMITER ;

CALL GetSupplierPerformance();

SELECT *
FROM Predictions;