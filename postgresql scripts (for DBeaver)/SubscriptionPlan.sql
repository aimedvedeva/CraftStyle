CREATE table if not EXISTS SubscriptionPlan(
	PlanID INT primary key GENERATED ALWAYS AS IDENTITY,
	Type varchar,
	price money not null,
	AllowedSessions float
);

INSERT INTO SubscriptionPlan(Type,price,AllowedSessions)
VALUES('Basic', 0, 0);

INSERT into SubscriptionPlan(Type,price,AllowedSessions)
VALUES('Advanced', 0.99, 'Infinity');

select * from subscriptionPlan;

