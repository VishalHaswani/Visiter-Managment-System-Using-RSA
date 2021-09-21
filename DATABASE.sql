create database alpha;

use alpha;

create table Details
(
flatNo int primary key,
ownerName varchar(30),
email varchar(50),
phoneNo char(10),
publicKey_e bigint,
publicKey_n bigint
);

insert into Details values
(101, 'Vishal Haswani', 'vishal.haswani2019@vitstudent.ac.in', '8756943216', 92294493, 92313721),
(102, 'Sarthak Sharma', 'sarthak.sharma2019a@vitstudent.ac.in', '8510182460', 91423433, 91442569),
(103, 'Rahul Gupta', 'rahul.gupta2019@vitstudent.ac.in', '8217751191', 94595033, 94614493),
(104, 'Harshith Suraag', 'harshith.suraag2019@vitstudent.ac.in', '9618168245', 93569887, 93589241);

select * from Details;
UPDATE Details SET publicKey_e=92294493,publicKey_n=92313721 WHERE flatNo=101;

SET @sec:=101;
SELECT @sec;
SELECT publicKey_e,publicKey_n FROM Details WHERE flatNo= @sec;

CREATE TABLE Variable (sec int);

INSERT INTO Variable VALUES(101);

SELECT * FROM Variable;
SELECT publickey_e,publickey_n FROM Details WHERE flatNo= (SELECT * FROM Variable);