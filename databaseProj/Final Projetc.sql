
drop table if exists Produce;
drop table if exists Users;
drop table if exists Recipes;

create table Users (
UserName varchar(255) PRIMARY KEY,
Password varchar(255)
);

create table Produce (
Ingredient varchar(255),
ExpirationDate Date,
Quantity int,
RecipeQuantity varchar(255),
UserName varchar(255)

);

create table Recipes (
DishName varchar(255),
Ingredient varchar(255),
Quantity int,
RecipeQuantity varchar(255),
primary key (DishName, Ingredient)
);

INSERT INTO Users (Username, Password) VALUES
('hassank1', '123456'),
('Fabian', '123456');
INSERT INTO Produce (Ingredient, ExpirationDate, Quantity, RecipeQuantity, UserName) VALUES
('Milk','2023-05-17','200', 'ml', 'hassank1'),
('Chicken','2023-05-17','500', 'g', 'hassank1'),
('Butter','2023-05-17','200', 'g', 'hassank1'),
('Tomato','2023-05-23','200', 'g', 'Fabian');
INSERT INTO Recipes (DishName, Ingredient, Quantity, RecipeQuantity) VALUES
('Chicken Alfredo','Chicken','500', 'g'),
('Chicken Alfredo','Milk','200', 'ml'),
('Pancakes','Milk','200', 'ml');

select * from Users;
select * from Produce;
#select * from Recipes;

SELECT * FROM Users WHERE Users.UserName = '%s' AND Users.Password = '%s';

INSERT INTO Produce (ingredients, expirationdate, quantity, username)
VALUES ('%s', '%s', '%i', '%s');

drop procedure GetAvailableDishNames if exists

DELIMITER //

CREATE PROCEDURE GetAvailableDishNames (
  IN p_UserName VARCHAR(50)
)

BEGIN
  SELECT r.DishName
  FROM Recipes r
  LEFT JOIN Produce p ON r.Ingredient = p.Ingredient AND p.UserName = p_UserName and
  p.ExpirationDate >= curdate() and r.quantity = p.quantity and
  r.recipequantity = p.recipequantity
  GROUP BY r.DishName
  HAVING COUNT(DISTINCT r.Ingredient) = COUNT(DISTINCT p.Ingredient);
END //
DELIMITER ;


CALL GetAvailableDishNames('hassank1');

DELIMITER //


INSERT INTO Users (username, password) VALUES ('Fabian2', '12345');

DELETE FROM Users
WHERE Username = 'Fabian';


DELIMITER //

CREATE TRIGGER RemoveProduceTrigger
AFTER DELETE ON Users
FOR EACH ROW
BEGIN
    DELETE FROM Produce
    WHERE UserName = OLD.UserName;
END; //

DELIMITER ;

-- Queryis to be intergrated into the database and wihtin the app.py

-- Query 1: Get total quantity of each ingredient available across all users.
SELECT Ingredient, SUM(Quantity) as TotalQuantity
FROM Produce
GROUP BY Ingredient;

DELIMITER //
-- Query 2: Function to get the expiration date of a particular ingredient for a specific user.
CREATE FUNCTION GetExpirationDate (p_UserName VARCHAR(255), p_Ingredient VARCHAR(255)) 
RETURNS DATE 
BEGIN 
    DECLARE expDate DATE; 
    SELECT ExpirationDate INTO expDate 
    FROM Produce 
    WHERE UserName = p_UserName AND Ingredient = p_Ingredient; 
    RETURN expDate; 
END // 
DELIMITER ;

-- You can use this function like this: 
SELECT GetExpirationDate('hassank1', 'Milk') as ExpirationDate;

DELIMITER //
-- Query 3: Trigger to update the Quantity in Produce table when a new recipe is added.
CREATE TRIGGER UpdateProduceQuantity
AFTER INSERT ON Recipes
FOR EACH ROW 
BEGIN
    UPDATE Produce
    SET Quantity = Quantity - NEW.Quantity
    WHERE Ingredient = NEW.Ingredient;
END; //
DELIMITER ;

-- Query 4: Get the details of users along with their respective produce details.
SELECT u.UserName, p.Ingredient, p.ExpirationDate, p.Quantity
FROM Users u
JOIN Produce p ON u.UserName = p.UserName;

