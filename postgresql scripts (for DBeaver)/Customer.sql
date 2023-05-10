CREATE table if not EXISTS Customer(
	CustomerID INT primary key GENERATED ALWAYS AS IDENTITY,
	Name varchar not null,
	sessionsNumber INT,
	subscriptionPlanID INT REFERENCES SubscriptionPlan(planID)
);

INSERT into Customer(Name,sessionsNumber,subscriptionPlanID)
VALUES('Far', 0, NUll);


INSERT INTO Customer(Name,sessionsNumber,subscriptionPlanID)
VALUES('Bob', 0, 1);


select * from customer;