-- Creates a trigger that decreases the quantity of an item after adding a new order
CREATE TRIGGER IF NOT EXISTS decreaseItemQuantity
AFTER INSERT ON orders
FOR EACH ROW
	UPDATE items
	SET quantity = quantity - NEW.quantity
	WHERE name = NEW.name;
