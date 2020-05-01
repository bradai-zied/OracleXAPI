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
* Generates API for any Oracle database :pushpin:
* Description of tables
* Fetch table with filters
* Grouping and counting are possible in fetch
* Sorting
* Column Filtring
* Insert one or multiple row in one request
* Update one or multiple row in one request
* Delete depend on where clause
* ORA errors in respond when something goes wrong
* Management of oracle session.
* Multiple requests handling ( Multithread )

# API Paths and Usage
## Fetch data 

**HTTP Method**   : GET

**PATH**          :/oracleapi/*TableName*/select?col=*column1*,*column2*&filter=*columnx*=0
**DEFAULT**        :If nothing si specified in header, it will fetch teh full table ordered by first column
**Example**
Request:
```
http://127.0.0.1:5000/oracleapi/devinfo/select?col=SROUTINSTANCEID,CDESC&filter=SROUTINSTANCEID < 103&orderby=SROUTINSTANCEID desc
```
Response
```
[
    {
        "SROUTINSTANCEID": 102,
        "CDESC": "Entry 102"
    },
    {
        "SROUTINSTANCEID": 101,
        "CDESC": "Entry 101"
    }
]
```

## insert data 

**HTTP Method**   : POST

**PATH**          :/oracleapi/*TableName*/add
**BODY**        : JSON FORMAT
**DEFAULT**        :Body, data must be nested in json object with name "DATA"
**Example**
Request:
```
http://127.0.0.1:5000/oracleapi/devinfo/add
```
Body
```
{
	"DATA":[{
        "SROUTINSTANCEID": 102,
        "CDESC": "Entry 102"
    },
    {
        "SROUTINSTANCEID": 101,
        "CDESC": "Entry 101"
    }]
}
```
Response
```
{
    "Status ": [
        {
            " Number of row inserted :": 2
        }
    ]
}
```
## Delete data 

**HTTP Method**   : DELETE
**PATH**          :/oracleapi/*TableName*/delete?col=*column1*&val=*valueor experssion*
**DEFAULT**        :Body, data must be nested in json object with name "DATA"
**Example**
Request:
```
http://127.0.0.1:5000/oracleapi/devinfo/delete?col=SROUTINSTANCEID&val=101
```
Response
```
{
    "Status ": [
        {
            " Number of row deleted :": 1
        }
    ]
}
```
## Update data 

**HTTP Method**   : PATCH
**PATH**          :/oracleapi/*TableName*/update
**DEFAULT**        :Body, must contain 2 object, NEWROWS & OLDROWS, number of element in each group must be the same, first element in OLDROWS will be updated by the first element of NEWROWS
**Example**
Request:
```
http://127.0.0.1:5000/oracleapi/devinfo/update
```
Body
```
{
	"NEWROWS":[{
        "SROUTINSTANCEID": 102,
        "CDESC": "Entry 102",
        "ADATE": "2020-01-04 00:00:00"
    },{
        "SROUTINSTANCEID": 101,
        "CDESC": "entry 101",
        "ADATE": "2020-01-04 00:00:00"
    }], 
    "OLDROWS":[{
        "SROUTINSTANCEID": 101,
        "CDESC": "Entry 101",
        "ADATE": "2019-01-04 00:00:00"
    },{
        "SROUTINSTANCEID": 101,
        "CDESC": "entry 100",
        "ADATE": "2019-02-04 00:00:00"                        
    }]
}
```
Response
```
{
    "Status ": [
        {
            " Number of row updated :": 2
        }
    ]
}
```
## Get Table structure 

**HTTP Method**   : GET

**PATH**          :/oracleapi/*TableName*/details
**DEFAULT**        :
**Example**
Request:
```
http://127.0.0.1:5000/oracleapi/devinfo/details
```
Response
```
[
    {
        "COLUMN_NAME": "SROUTINSTANCEID",
        "DATA_TYPE": "NUMBER",
        "DATA_LENGTH": 22,
        "NULLABLE": "N",
        "PK": "YES"
    },
    {
        "COLUMN_NAME": "CDESC",
        "DATA_TYPE": "VARCHAR2",
        "DATA_LENGTH": 168,
        "NULLABLE": "Y",
        "PK": "NO"
    },
    {
        "COLUMN_NAME": "CNODEADDR",
        "DATA_TYPE": "VARCHAR2",
        "DATA_LENGTH": 136,
        "NULLABLE": "Y",
        "PK": "NO"
    }
    ....
]
```




