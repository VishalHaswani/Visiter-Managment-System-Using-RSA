# Visiter-Managment-System-Using-RSA


#Python Packages Used:
  tkinter(In-built)
  smtplib(In-built)
  mysql.connector
  twilio.rest


#Working:
A file Info.txt is created which stores the credentials for accessing the database.
The MySQL database alredy has information stored about the people living in the appartment complex.

The INFO file: contains same data encrypted in 2 different forms:
  1st. Using the DES algorith
  2nd. Using the RSA Algorithm with the secretarie's public key.
So in case the User forgets the login password, he can go to secretary and ask for his private key to unlock the system.

Visitor Authentication part:
  1. Visiter comes to the system user and tells him about the "person he wants to visit and his appartmen number"
  2. The system user sends a x = RSAEncrypted(6-digit-number, owner's public key) to the owner of the house to be visited.
  3. The owner takes 'x' and decrypts it using his private key and gets y = RSADecryption(6-digit-number, owner's private key).
  4. Now the owner sends this 'y' to the visitor and the visitor tells 'y' to the system user.
  5. The system user enters 'y' in the system, and the system matches it with the initial plaintext(i.e. the orignal 6-digit-number).
  6. If the 2 match then the visitor is verified.

Monthly Routine:
  1. For everyone in the database a new key is generated, the private key is sent to them via e-mail and the public key is stored in the database.
  2. The 2nd part of the Info.txt file is changed in accordance with the new public key of the appartment secretary.


#Database Setup:
1. The "DATABASE.sql" file contanes all the necessary codes for database creation.
2. Create the database, then create the 2 tables- Details and Variable.
Note: The deatils table stores the details about the people and the Variable table stores the details about the secretary.


#Info.txt setup:
1. Open "Info File Generator.py".
2. Enter the details asked, but make sure database is setup properly and you have a twilio account setup.
3. Now the Info.txt file is created.
4. Run the "Application.pyw" file and run a "Mounthly Routine".
5. Once the mothly routine is complete the "Forgot Password" feature is active.(IMPORTANT without this step the FP feature doesn't work.
