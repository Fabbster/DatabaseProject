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
('Milk','2024-1-31','200', 'ml', 'hassank1'),
('Chicken','2024-1-31','500', 'g', 'hassank1'),
('Butter','2024-1-31','200', 'g', 'hassank1'),
('Tomato','2024-1-31','200', 'g', 'Fabian');
INSERT INTO Recipes (DishName, Ingredient, Quantity, RecipeQuantity) VALUES
('Chicken Alfredo','Chicken','500', 'g'),
('Chicken Alfredo','Milk','200', 'ml'),
('Pancakes','Milk','200', 'ml');

select * from Users;
select * from Produce;
select * from Recipes;

SELECT * FROM Users WHERE Users.UserName = '%s' AND Users.Password = '%s';

INSERT INTO Produce (ingredients, expirationdate, quantity, username)
VALUES ('%s', '%s', '%i', '%s');

INSERT INTO Users (username, password) VALUES ('Fabian', '12345');

DELETE FROM Users
WHERE Username = 'Fabian';


drop procedure GetAvailableDishNames if exists
DELIMITER //
# Queri 1: Get the names of dishes that can be made with the ingredients available to a specific user.
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
# Query 2: Remove the produce of a deleted user.
CREATE TRIGGER RemoveProduceTrigger
AFTER DELETE ON Users
FOR EACH ROW
BEGIN
    DELETE FROM Produce
    WHERE UserName = OLD.UserName;
END; //

DELIMITER ;


DELIMITER //
-- Query 3: Function to get the expiration date of a particular ingredient for a specific user.
CREATE FUNCTION GETEXPIRATIONDATE(P_USERNAME VARCHAR(255), P_INGREDIENT VARCHAR(255)) 
RETURNS DATE 
READS SQL DATA
BEGIN 
    DECLARE expDate DATE;

    SELECT ExpirationDate INTO expDate
    FROM Produce
    WHERE UserName = P_USERNAME AND Ingredient = P_INGREDIENT;

    RETURN expDate;
END //
DELIMITER ;
SELECT GetExpirationDate('hassank1', 'Milk') as ExpirationDate;

-- Query 4: Get the details of users along with their respective produce details.
SELECT u.UserName, p.Ingredient, p.ExpirationDate, p.Quantity
FROM Users u
JOIN Produce p ON u.UserName = p.UserName;

-- Query 5: Delete the expired ingredients of a specific user.
DELIMITER //
CREATE PROCEDURE DeleteExpiredIngredients(IN p_UserName VARCHAR(255))
BEGIN
    DELETE FROM Produce
    WHERE UserName = p_UserName AND ExpirationDate < CURDATE();
END //
DELIMITER ;
CALL DeleteExpiredIngredients('hassank1');


-- Query 6 : Get the details of a specific recipe along with the available quantity of each ingredient.
SELECT 
    r.DishName, 
    r.Ingredient, 
    CONCAT(r.Quantity, ' ', r.RecipeQuantity) as RequiredQuantity, CONCAT(p.Quantity, ' ', p.RecipeQuantity) as AvailableQuantity
FROM 
    Recipes r
LEFT JOIN 
    Produce p ON r.Ingredient = p.Ingredient AND p.UserName = 'hassank1'
WHERE 
    r.DishName = 'Chicken Alfredo';
