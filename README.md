# Python REST API CRUD Example using Flask and MySQL

### Step 1. 
Create the below *app.py script(py is the extension to indicate Python script) where we import the flask module. This file should be created under user_crud directory. Notice how we create flask instance. 

### Step 2. 
We create the below *db_config.py Python script under user_crud to setup the MySQL database configurations for connecting to database. We need to configure database connection with flask module and that’s why we have imported app module and setup the MySQL configuration with flask module.

### Step 3. 
Next we need *main.py script under *user_crud directory. This script is the perfect instance of Python REST API CRUD Example using Flask and MySQL. It defines all REST URIs for performing CRUD operations. It will also connect to *MySQL database server and query the database to read, insert, update and delete.
Here you can use http PUT method and http DELETE method for updating and deleting users respectively. I have defined only 404 method to handle not found error. You should basically handle required errors, such as, server errors for http responses 500, occurred during the REST API calls.

### Step 4. 
Create MySQL database table — tbl_user with the following structure.

  CREATE TABLE `tbl_user` (
  `user_id` bigint(20) NOT NULL AUTO_INCREMENT,
  `user_name` varchar(45) COLLATE utf8_unicode_ci DEFAULT NULL,
  `user_email` varchar(45) COLLATE utf8_unicode_ci DEFAULT NULL,
  `user_password` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`user_id`)
  ) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

## Testing the Application (Use Postman For Testing)
* Display all users
  GET http://localhost:5000/users
* Add new user
  POST http://localhost:5000/add
  
  {
	"name":"Soumitra",
	"email":"contact@roytuts.com",
	"pwd":"pwd"
  }
  
 * Response : “User added successfully!”
 * Cmd Command : python main.py
