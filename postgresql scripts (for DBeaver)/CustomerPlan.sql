CREATE table if not EXISTS CustomerPlan(
	CustomerID INT REFERENCES Customer(customerID),
	subscriptionPlanID INT REFERENCES SubscriptionPlan(planID),
	purchaseDate date
);

INSERT INTO CustomerPlan(customerID,subscriptionPlanID,purchaseDate)
VALUES(4, 1, Current_date);

INSERT into CustomerPlan(customerID,subscriptionPlanID, purchaseDate)
VALUES(2, 1, Current_date);

INSERT INTO CustomerPlan(customerID,subscriptionPlanID, purchaseDate)
VALUES(3, 1, Current_date);


select * from CustomerPlan;