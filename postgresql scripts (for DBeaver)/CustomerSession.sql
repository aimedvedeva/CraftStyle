CREATE table if not EXISTS CustomerSession(
    CustomerSessionID INT primary key GENERATED ALWAYS AS IDENTITY,
	CustomerID INT REFERENCES Customer(customerID),
	Recommendation text,
	pucturesNumber INT,
	tags varchar,
	sessionDate date
);


INSERT INTO CustomerSession(customerID,Recommendation,pucturesNumber,tags,sessionDate)
VALUES(1,
'Leather pants: You could wear the belt with a pair of black leather pants to create an edgy look. You could wear a graphic t-shirt or a crop top to complete the look.
Denim jacket: You could wear the belt with a denim jacket to create a rock-inspired outfit. You could wear a pair of black skinny jeans and a band t-shirt, and then layer the denim jacket on top. The belt would add some definition to your waistline and complete the look.
Distressed jeans: You could wear the belt with a pair of distressed jeans to add some edge to your outfit. You could wear a black tank top and a leather jacket to complete the look.
Studded boots: You could wear the belt with a pair of studded boots to create a rock-inspired outfit. You could wear a pair of black skinny jeans and a white t-shirt, and then add the boots and belt to complete the look.',
1, 'rock', '2023-05-10');


INSERT into CustomerSession(customerID,Recommendation,pucturesNumber,tags,sessionDate)
VALUES(2,
'Top: Since the trousers are a neutral color, you could pair them with a bright or bold top. A red or yellow top would create a nice contrast, while a pastel pink or blue would create a softer look. You could also wear a classic white or black t-shirt for a more understated look.
Shoes: For a casual look, you could wear a pair of white sneakers or flat sandals. If you prefer a dressier look, you could wear a pair of strappy heeled sandals in a neutral color like beige or black.
Jewelry: You could wear a simple necklace or some small hoop earrings to add some sparkle to the outfit. A delicate bracelet or a thin gold bangle would also look great.
Bag: A crossbody bag in a neutral color like black or brown would work well with this outfit. You could also opt for a small shoulder bag or a clutch in a bright color to add a pop of color to the look.
Hair and makeup: You could wear your hair in a sleek and straight style or opt for loose, tousled waves. For makeup, you could go for a natural and glowing look with a bit of tinted moisturizer, mascara, and lip balm. A touch of blush and bronzer will add some warmth to your complexion.',
1, 'casual, office', '2023-05-10');


INSERT INTO CustomerSession(customerID,Recommendation,pucturesNumber,tags,sessionDate)
VALUES(3,
'Oversized Sweater: You can pair the skirt with an oversized sweater, which will create a cozy yet stylish outfit. You can opt for a neutral color or add some color to your outfit with a bright sweater. You can pair this with ankle boots or knee-high boots.
Denim Jacket: You can pair the skirt with a denim jacket and a white t-shirt for a casual look. This can be paired with white sneakers for a comfortable look or ankle boots for a more stylish look.
White blouse: You can pair the skirt with a white blouse and a blazer for a professional and chic look. You can add some statement jewelry and high heels to complete the look.
Crop Top: You can pair the skirt with a crop top for a more casual look. You can opt for a neutral color or a patterned top. This can be paired with sneakers or sandals.',
1, 'casual', '2023-05-10');


select * from CustomerSession;