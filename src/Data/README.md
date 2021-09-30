The Visually Grounded Memory Assistant Dataset was collected using Amazon Mechinical Turk. See the set up [here](https://www.youtube.com/watch?v=T97r2leqFyQ). 
The data from this AMT study has been filtered and stored in an MySQL database which we provide in this folder [here](https://github.com/meera1hahn/Visual-Assistant/blob/main/src/Data/VisualAssistantDataset/assistDB_filtered.sql)
(https://github.com/meera1hahn/Visual-Assistant/blob/main/src/Data/VisualAssistantDataset/assistDB_filtered.sql)

 
## Setup and Install

First you need to install MySQL: https://www.digitalocean.com/community/tutorials/how-to-install-mysql-on-ubuntu-18-04

Install MySQLdb for python: `pip 

### Read Dataset Dump

Once mysql is set up you can read the database from the provided file 

1. Open/run mysql: `mysql -u root -p`
2. Show the existing databases: `SHOW DATABASES;`
3. If no database exists for your db create the database:  `CREATE DATABASE [dbname];`
4. Exit mysql: `exit; `
5. Read the dump file into the database you just created: `mysql -u root -p [dbname] < [dumpfilename]`
	 
   ex. `mysql -u root -p assistDB < assistDB_filtered.sql`
   
### If you ever need to write the database to a new file
1. `mysqldump -u root -p [database_name] > [dumpfilename]`

### How to use with python

Please see the file [questionFeatureCreation.py](https://github.com/meera1hahn/Visual-Assistant/blob/main/src/Modeling/TaskA/questionFeatureCreation.py) 
to see how we used the database using MySQLdb to create the features for task A. 
