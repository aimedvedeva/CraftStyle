CREATE table if not EXISTS Picture(
	pictureID INT primary key GENERATED ALWAYS AS IDENTITY,
	customerID INT REFERENCES Customer(customerID),
	pictureUrl varchar,
	tags varchar
);


INSERT INTO Picture(customerID,pictureUrl,tags)
VALUES(1, 'https://drive.google.com/file/d/1UytPqBiPHJE4ES5jTToOr8BRRvLi2nT1/view?usp=sharing', 'rock');


INSERT into Picture(customerID,pictureUrl,tags)
VALUES(2, 'https://drive.google.com/file/d/1dT8WV288nerOT8PdG2HlYJCGND-ibCeZ/view?usp=sharing', 'casual, office');


INSERT INTO Picture(customerID,pictureUrl,tags)
VALUES(3, 'https://drive.google.com/file/d/1f6pIr-1ab7T9-Rc8j37zpJ0QiRwA0nA2/view?usp=share_link', 'casual');


select * from Picture;