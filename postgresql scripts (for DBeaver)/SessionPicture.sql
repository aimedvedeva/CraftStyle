CREATE table if not EXISTS SessionPicture(
	SessionID INT REFERENCES CustomerSession(customerSessionID),
	PictureID INT REFERENCES Picture(pictureID)
);


insert into SessionPicture
select t2.pictureID, t1.customersessionid ID from CustomerSession t1 join Picture t2 on t1.customerSessionID=t2.pictureID;


select * from sessionPicture;