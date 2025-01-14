RESTORE FILELISTONLY
FROM DISK = N'/var/opt/mssql/Northwind2016.bak';

RESTORE DATABASE Northwind
FROM DISK = N'/var/opt/mssql/Northwind2016.bak'
WITH MOVE 'Northwind' TO '/var/opt/mssql/Northwind.MDF',
	 MOVE 'Northwind_log' TO '/var/opt/mssql/Northwind_LOG.LDF',
	 REPLACE;

/*1*/	
SELECT * 
FROM Categories;
/*2*/
SELECT CategoryName, Description 
FROM Categories;
/*3*/
SELECT FirstName, LastName, HireDate 
FROM Employees 
WHERE Title = 'Sales Representative';
/*4*/
SELECT FirstName, LastName, HireDate 
FROM Employees 
WHERE Title = 'Sales Representative' AND Country = 'USA';
/*5*/
SELECT OrderID, OrderDate 
FROM Orders 
WHERE EmployeeID = 5;
/*6*/
SELECT SupplierID, ContactName, ContactTitle 
FROM Suppliers 
WHERE ContactTitle != 'Marketing Manager';	
/*7*/
SELECT ProductID, ProductName 
FROM Products 
WHERE ProductName like '%queso%';
/*8*/
SELECT OrderID, CustomerID, ShipCountry 
FROM Orders 
WHERE ShipCountry = 'France' OR ShipCountry = 'Belgium';
/*9*/
SELECT OrderID, CustomerID, ShipCountry 
FROM Orders 
WHERE ShipCountry IN ('Brazil', 'Mexico', 'Argentina', 'Venezuela');
/*10*/
SELECT FirstName, LastName, Title, BirthDate 
FROM Employees 
ORDER BY BirthDate ASC;
/*11*/
SELECT FirstName, LastName, Title, CONVERT (DATE, BirthDate) 
FROM Employees 
ORDER BY BirthDate ASC;
/*12*/
SELECT FirstName, LastName, FirstName + ' ' + LastName as FullName  
FROM Employees;
/*13*/
SELECT OrderID, ProductID, UnitPrice, Quantity, UnitPrice*Quantity as TotalPrice 
FROM OrderDetails 
ORDER BY OrderID, ProductID;
/*14*/
SELECT Count(*) as TotalCustomer 
FROM Customers;
/*15*/
SELECT MIN(OrderDate) as FirstOrder 
FROM Orders;
/*16*/
SELECT DISTINCT Country 
FROM Customers;
/*17*/
SELECT ContactTitle, count(*) as TotalContactTitle 
FROM Customers 
GROUP BY ContactTitle 
ORDER BY TotalContactTitle DESC;
/*18*/
SELECT  p.ProductID, p.ProductName, s.CompanyName 
FROM Products p 
JOIN Suppliers s on p.SupplierID = s.SupplierID 
ORDER BY ProductID;
/*19*/	
SELECT o.OrderID, CONVERT (DATE, o.OrderDate), s.CompanyName 
FROM Orders o
JOIN Shippers s	on o.ShipVia = s.ShipperID  
	WHERE o.OrderID < 10300 
ORDER BY OrderID;

/* Intermedi */

/*20*/
SELECT c.CategoryName, COUNT(*) as TotalProducts 
FROM Categories c 
JOIN Products p on c.CategoryID = p.CategoryID
GROUP BY CategoryName 
ORDER BY COUNT(*) DESC;
/*21*/
SELECT Country, City, COUNT(*) as TotalCustomer 
FROM Customers 
GROUP BY Country, City 
ORDER BY COUNT(*) DESC;
/*22*/
SELECT ProductID, ProductName, UnitsInStock, ReorderLevel
FROM Products
WHERE UnitsInStock < ReorderLevel
ORDER BY ProductID;
/*23*/
SELECT ProductID, ProductName, UnitsInStock, UnitsOnOrder, ReorderLevel, Discontinued
FROM Products
WHERE UnitsInStock + UnitsOnOrder <= ReorderLevel AND  Discontinued = 0;
/*24*/
SELECT CustomerID, CompanyName, Region
FROM Customers
ORDER BY 
    CASE 
        WHEN Region IS NULL THEN 1 
        ELSE 0 
    END, 
    Region ASC, 
    CustomerID;
/*25*/
SELECT TOP 3 ShipCountry, AVG(Freight) as AverageFreight
FROM Orders
GROUP BY ShipCountry 
ORDER BY AverageFreight DESC;
/*26*/
SELECT TOP 3 ShipCountry, AVG(Freight) as AverageFreight
FROM Orders
WHERE YEAR(OrderDate) = 2015
GROUP BY ShipCountry 
ORDER BY AverageFreight DESC;
/*27*/
SELECT OrderID, ShipCountry
FROM Orders
WHERE OrderDate between '12/31/2015' and '1/1/2016';
/*28*/
SELECT TOP 3 ShipCountry, AVG(Freight) as AverageFreight
FROM Orders
WHERE OrderDate BETWEEN (DATEADD(yy, -1, (SELECT Max(OrderDate) FROM Orders))) AND (SELECT MAX(OrderDate) FROM Orders)
GROUP BY ShipCountry 
ORDER BY AverageFreight DESC;
/*29*/
SELECT e.EmployeeID, e.LastName, o.OrderID, p.ProductName, od.Quantity
FROM Employees e
JOIN Orders o ON e.EmployeeID = o.EmployeeID
JOIN OrderDetails od ON o.OrderID = od.OrderID
JOIN Products p ON od.ProductID = p.ProductID
ORDER BY o.OrderID;
/*30*/
SELECT c.CustomerID as Customers_CustomerID, o.CustomerID as Orders_CustomerID
FROM Customers c
LEFT JOIN Orders o ON o.CustomerID = c.CustomerID
WHERE o.CustomerID IS NULL;
/*31*/
SELECT c.CustomerID, o.CustomerID
FROM Customers c
LEFT JOIN Orders o ON c.CustomerID = o.CustomerID AND o.EmployeeID = 4
WHERE o.CustomerID IS NULL;

/*Avanzati*/

/*32*/
SELECT c.CustomerID, c.CompanyName, o.OrderID, SUM(od.UnitPrice * od.Quantity) as TotalOrderAmount
FROM Customers c
JOIN Orders o on c.CustomerID = o.CustomerID
JOIN OrderDetails od on o.OrderID = od.OrderID
WHERE YEAR(o.OrderDate) = 2016
GROUP BY c.customerid, c.companyname, o.orderid
HAVING SUM(od.UnitPrice * od.Quantity) >= 10000
ORDER BY TotalOrderAmount DESC;
/*33*/
SELECT c.CustomerID, c.CompanyName, SUM(od.UnitPrice * od.Quantity) as TotalOrderAmount
FROM Customers c
JOIN Orders o on c.CustomerID = o.CustomerID
JOIN OrderDetails od on o.OrderID = od.OrderID
WHERE YEAR(o.OrderDate) = 2016
GROUP BY c.customerid, c.companyname
HAVING SUM(od.UnitPrice * od.Quantity) >= 15000
ORDER BY TotalOrderAmount DESC;
/*34*/
SELECT c.CustomerID, c.CompanyName, SUM(od.UnitPrice * od.Quantity) as TotalsWithoutDiscount, SUM(od.UnitPrice*od.Quantity*(1-od.Discount)) as TotalsWithDiscount 
FROM Customers c
JOIN Orders o on c.CustomerID = o.CustomerID
JOIN OrderDetails od on o.OrderID = od.OrderID
WHERE YEAR(o.OrderDate) = 2016
GROUP BY c.customerid, c.companyname
HAVING SUM(od.UnitPrice * od.Quantity*(1-od.Discount)) >= 10000
ORDER BY TotalsWithDiscount DESC;
/*35*/
SELECT EmployeeID, OrderID, OrderDate 
FROM Orders
WHERE OrderDate = EOMONTH(OrderDate)
ORDER BY EmployeeID, OrderID;
/*36*/
SELECT TOP 10 o.OrderID, COUNT(*) as TotalOrderDetails
FROM Orders o
JOIN OrderDetails od
ON o.OrderID = od.OrderID
GROUP BY o.OrderID
ORDER BY TotalOrderDetails DESC;
/*37*/
SELECT TOP (SELECT CAST(COUNT(*) * 0.02 AS INT) FROM Orders) OrderID
FROM Orders
ORDER BY NEWID();
/*38*/
SELECT od.OrderID
FROM OrderDetails od
JOIN Orders o 
ON od.OrderID = o.OrderID 
WHERE Quantity >= 60
GROUP BY od.OrderID, od.Quantity
HAVING COUNT(*) > 1 
ORDER BY od.OrderID;
/*39*/
SELECT OrderID, ProductID, UnitPrice, Quantity, Discount
FROM OrderDetails
WHERE OrderID IN (
	SELECT od.OrderID
	FROM OrderDetails od
	JOIN Orders o 
	ON od.OrderID = o.OrderID 
	WHERE Quantity >= 60
	GROUP BY od.OrderID, od.Quantity
	HAVING COUNT(*) > 1
);
/*40*/
SELECT OrderDetails.OrderID,ProductID,UnitPrice,Quantity,Discount
FROM OrderDetails
JOIN (
	SELECT DISTINCT OrderID
    FROM OrderDetails
    WHERE Quantity >= 60
    GROUP BY OrderID, Quantity
    HAVING Count(*) > 1
)  PotentialProblemOrders
ON PotentialProblemOrders.OrderID = OrderDetails.OrderID
ORDER BY OrderID, ProductID;
/*41*/
SELECT OrderID, OrderDate, RequiredDate, ShippedDate
FROM Orders
WHERE ShippedDate >= RequiredDate
ORDER BY OrderID;
/*42*/
SELECT e.EmployeeID, e.LastName, COUNT(*) as TotalLateOrders 
FROM Employees e
JOIN Orders o
ON e.EmployeeID = o.EmployeeID
WHERE ShippedDate >= RequiredDate
GROUP BY e.EmployeeID, e.LastName
ORDER BY TotalLateOrders DESC;
/*43*/
SELECT total.*, late.LateOrders
FROM (
	(SELECT e.EmployeeID, e.LastName, COUNT(*) as AllOrders 
	FROM Employees e
	JOIN Orders o
	ON e.EmployeeID = o.EmployeeID
	GROUP BY e.EmployeeID, e.LastName
	) total
	JOIN (
	SELECT e.EmployeeID, e.LastName, COUNT(*) as LateOrders 
	FROM Employees e
	JOIN Orders o
	ON e.EmployeeID = o.EmployeeID
	WHERE ShippedDate >= RequiredDate
	GROUP BY e.EmployeeID, e.LastName
	) late
	ON total.EmployeeID = late.EmployeeID
)	
ORDER BY total.EmployeeID;
/*44*/
SELECT total.*, late.LateOrders
FROM (
	(SELECT e.EmployeeID, e.LastName, COUNT(*) as AllOrders 
	FROM Employees e
	JOIN Orders o
	ON e.EmployeeID = o.EmployeeID
	GROUP BY e.EmployeeID, e.LastName
	) total
	LEFT JOIN (
	SELECT e.EmployeeID, e.LastName, COUNT(*) as LateOrders 
	FROM Employees e
	JOIN Orders o
	ON e.EmployeeID = o.EmployeeID
	WHERE ShippedDate >= RequiredDate
	GROUP BY e.EmployeeID, e.LastName
	) late
	ON total.EmployeeID = late.EmployeeID
)	
ORDER BY total.EmployeeID;
/*45*/
SELECT total.*, ISNULL(late.LateOrders, 0) AS LateOrders
FROM (
	(SELECT e.EmployeeID, e.LastName, COUNT(*) as AllOrders 
	FROM Employees e
	JOIN Orders o
	ON e.EmployeeID = o.EmployeeID
	GROUP BY e.EmployeeID, e.LastName
	) total
	LEFT JOIN (
	SELECT e.EmployeeID, e.LastName, COUNT(*) as LateOrders 
	FROM Employees e
	JOIN Orders o
	ON e.EmployeeID = o.EmployeeID
	WHERE ShippedDate >= RequiredDate
	GROUP BY e.EmployeeID, e.LastName
	) late
	ON total.EmployeeID = late.EmployeeID
)	
ORDER BY total.EmployeeID;
/*46*/
SELECT total.EmployeeID, total.LastName, total.AllOrders, ISNULL(late.LateOrders, 0) AS LateOrders, CAST(ISNULL(late.LateOrders, 0) AS FLOAT) / total.AllOrders AS PercentLateOrders
FROM (
	(SELECT e.EmployeeID, e.LastName, COUNT(*) as AllOrders 
	FROM Employees e
	JOIN Orders o
	ON e.EmployeeID = o.EmployeeID
	GROUP BY e.EmployeeID, e.LastName
	) total
	LEFT JOIN (
	SELECT e.EmployeeID, COUNT(*) as LateOrders 
	FROM Employees e
	JOIN Orders o
	ON e.EmployeeID = o.EmployeeID
	WHERE ShippedDate >= RequiredDate
	GROUP BY e.EmployeeID
	) late
	ON total.EmployeeID = late.EmployeeID
)	
ORDER BY total.EmployeeID;
/*47*/
SELECT total.EmployeeID, total.LastName, total.AllOrders, ISNULL(late.LateOrders, 0) AS LateOrders, ROUND(CAST(ISNULL(late.LateOrders, 0) AS FLOAT) / total.AllOrders, 2) AS PercentLateOrders
FROM (
	(SELECT e.EmployeeID, e.LastName, COUNT(*) as AllOrders 
	FROM Employees e
	JOIN Orders o
	ON e.EmployeeID = o.EmployeeID
	GROUP BY e.EmployeeID, e.LastName
	) total
	LEFT JOIN (
	SELECT e.EmployeeID, COUNT(*) as LateOrders 
	FROM Employees e
	JOIN Orders o
	ON e.EmployeeID = o.EmployeeID
	WHERE ShippedDate >= RequiredDate
	GROUP BY e.EmployeeID
	) late
	ON total.EmployeeID = late.EmployeeID
)	
ORDER BY total.EmployeeID;
/*48-49*/
SELECT c.CustomerID, c.CompanyName, SUM(od.UnitPrice * od.Quantity) as TotalOrderAmount,
	CASE 
		WHEN SUM(od.UnitPrice * od.Quantity) < 1000 THEN 'Low'
        WHEN SUM(od.UnitPrice * od.Quantity) BETWEEN 1000 AND 5000 THEN 'Medium'
        WHEN SUM(od.UnitPrice * od.Quantity) BETWEEN 5000 AND 10000 THEN 'High'
        ELSE 'Very High'
	END as CustomerGroup	
FROM Customers c
JOIN Orders o on c.CustomerID = o.CustomerID
JOIN OrderDetails od on o.OrderID = od.OrderID
WHERE YEAR(o.OrderDate) = 2016
GROUP BY c.customerid, c.companyname
ORDER BY c.CustomerID;
/*50*/
WITH CustomerTotals AS (
    SELECT c.CustomerID, c.CompanyName, SUM(od.UnitPrice * od.Quantity) as TotalOrderAmount,
		CASE 
			WHEN SUM(od.UnitPrice * od.Quantity) < 1000 THEN 'Low'
       		WHEN SUM(od.UnitPrice * od.Quantity) BETWEEN 1000 AND 5000 THEN 'Medium'
        	WHEN SUM(od.UnitPrice * od.Quantity) BETWEEN 5000 AND 10000 THEN 'High'
        	ELSE 'Very High'
		END as CustomerGroup	
	FROM Customers c
	JOIN Orders o on c.CustomerID = o.CustomerID
	JOIN OrderDetails od on o.OrderID = od.OrderID
	WHERE YEAR(o.OrderDate) = 2016
	GROUP BY c.customerid, c.companyname
),
GroupCounts AS (
    SELECT CustomerGroup, COUNT(*) AS TotalInGroup
    FROM CustomerTotals
    GROUP BY CustomerGroup
)
SELECT CustomerGroup, TotalInGroup, CAST(TotalInGroup AS FLOAT) / (SELECT SUM(TotalInGroup) FROM GroupCounts) AS PercentageInGroup
FROM GroupCounts
ORDER BY PercentageInGroup DESC;
/*51*/
WITH tot as (
	SELECT c.CustomerID, c.CompanyName, SUM(od.UnitPrice * od.Quantity) as TotalOrderAmount
	FROM Customers c
	JOIN Orders o on c.CustomerID = o.CustomerID
	JOIN OrderDetails od on o.OrderID = od.OrderID
	WHERE YEAR(o.OrderDate) = 2016
	GROUP BY c.customerid, c.companyname
)
SELECT tot.*, cgt.CustomerGroupName 
FROM tot
JOIN CustomerGroupThresholds cgt on TotalOrderAmount <= cgt.RangeTop AND TotalOrderAmount >= cgt.RangeBottom;
/*52*/
(SELECT Distinct Country 
FROM Customers)
UNION
(SELECT Distinct Country 
FROM Suppliers)
ORDER BY Country;
/*53*/
WITH c AS (
    SELECT Country AS SupplierCountry, NULL AS CustomerCountry
    FROM Suppliers
    UNION
    SELECT NULL AS SupplierCountry, Country AS CustomerCountry
    FROM Customers
)
SELECT SupplierCountry, CustomerCountry
FROM c
ORDER BY 
    COALESCE(SupplierCountry, CustomerCountry), SupplierCountry;
/*54*/    
SELECT COALESCE(s.Country, c.Country) AS Country,
       COALESCE(s.TotalSupplier, 0) AS TotalSupplier,
       COALESCE(c.TotalCustomer, 0) AS TotalCustomer
FROM (
    SELECT Country, COUNT(*) AS TotalSupplier
    FROM Suppliers
    GROUP BY Country
) s
FULL OUTER JOIN (
    SELECT Country, COUNT(*) AS TotalCustomer
    FROM Customers
    GROUP BY Country
) c
ON s.Country = c.Country
ORDER BY Country;
/*55*/
WITH ranked as (
	SELECT ShipCountry, CustomerID, OrderID, convert(DATE, OrderDate) as OrderDate, rank() OVER (PARTITION BY shipcountry ORDER BY orderdate) as ranking
	FROM orders
)
SELECT ShipCountry, CustomerID, OrderID, OrderDate
FROM ranked
WHERE ranking = 1
ORDER BY ShipCountry ,OrderID;
/*56*/
SELECT InitialOrder.CustomerID,
	   InitialOrder.OrderID as InitialOrderID,
 	   CONVERT(DATE, InitialOrder.OrderDate) as InitialOrderDate,
	   NextOrder.OrderID as NextOrderID,
 	   CONVERT(DATE, NextOrder.OrderDate) as NextOrderDate,
 	   DATEDIFF(DAY, InitialOrder.OrderDate, NextOrder.OrderDate) as DaysBetween
FROM Orders InitialOrder
JOIN Orders NextOrder
ON InitialOrder.CustomerID = NextOrder.CustomerID 
	AND InitialOrder.OrderID < NextOrder.OrderID 
	AND DATEDIFF(DAY, InitialOrder.OrderDate, NextOrder.OrderDate) <= 5
ORDER BY InitialOrder.CustomerID, InitialOrder.OrderID;
/*57*/
WITH nxt AS (
    SELECT CustomerID, 
    	   CONVERT(DATE, OrderDate) AS OrderDate,
           LEAD(CONVERT(DATE, OrderDate), 1) OVER (PARTITION BY CustomerID ORDER BY OrderDate) AS NextOrderDate
    FROM Orders
)
SELECT
    CustomerID, OrderDate, NextOrderDate, DATEDIFF(DAY, OrderDate, NextOrderDate) AS DaysBetweenOrders
FROM nxt
WHERE DATEDIFF(DAY, OrderDate, NextOrderDate) <= 5;
