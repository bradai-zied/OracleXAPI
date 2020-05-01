# Oracle API
<a href="https://ibb.co/gDYZRY4"><img src="https://i.ibb.co/brt5Ktb/img.jpg" alt="img" border="0"></a>
Generating REST APIs for Oracle Databases

# Motivation
While working on oracle Database, sometimes you need a quick access to your data from rest interface, if you wanna test Inonic , angular or ...., here is the solution, you don't need to write your REST API, Oracle API will prepare it in couple of second.

# Description
Docker base on python:3.7-alpine
Flask for API
CX_oracle  connector for database connection

# Setup
Build the docker image
by default the container will not connect to any database
set Envirement variable as DB_DSN if you have or you must change 
-DB_IP     :IP of database target
-DB_PORT   :Port (by default oracle use 1521)
-DB_SID    :
-DB_USER   :username fo schema
-DB_PASSWORD:
internal Port of API is 5000 (i'm lazy to change it)

# Features
* Generates API for **ANY** Oracle database :stop::fire:





