# importing module 
import cx_Oracle 
import os
import platform
import sys
import json
import time

print (" * Python version: " + platform.python_version())
print (" * cx_Oracle version: " + cx_Oracle.version)
print (" * Oracle client: " + str(cx_Oracle.clientversion()).replace(', ','.'))


if "DB_DSN" in os.environ:
    dsn = os.environ['DB_DSN']
else:
    #Setup db Connection 
    ip = os.environ['DB_IP']
    if ip == 'default':
        while True:
            print (" ***** Default ip please setup the database connection en ENV  *****")
            print (" ***** use can setup DB_DSN with your connection string ************")
            print (" ***** or change DB_IP ,DB_PORT ,DB_SID, DB_USER ,DB_PASSWORD ******")
            time.sleep(60)
    port = os.environ['DB_PORT']
    SID = os.environ['DB_SID']
    user = os.environ['DB_USER']
    password = os.environ['DB_PASSWORD']
    dsn = cx_Oracle.makedsn(ip, port, service_name=SID)

print ( "ip = ",ip)
print ("SID = ", SID)
print ("user = ", user)
print ("dns = ", dsn )

os.putenv('NLS_LANG', 'AMERICAN_AMERICA.WE8MSWIN1252')
#os.putenv('NLS_DATE_FORMAT', 'DDMMYYYYHH24MISS')
# os.putenv('NLS_TIMESTAMP_FORMAT', 'DDMMYYYYHH24MISS')

# Set the NLS_DATE_FORMAT for a session
def initSession(connection, requestedTag):
    sql = "ALTER SESSION SET NLS_DATE_FORMAT = 'YYYY-MM-DD HH24:MI:SS'"
    cursor = connection.cursor()
    cursor.execute(sql)
    connection.tag = requestedTag

# Create the pool with session callback defined
#get session from pool
for i in range(0,100):
    while True:
        try:
            pool = cx_Oracle.SessionPool("db", "db", dsn, min=2, max=10, increment=1, 
            threaded=True,sessionCallback=initSession, encoding="UTF-8")
        except cx_Oracle.DatabaseError as e:
            errorObj, = e.args
            print ("Database not reachable :" + errorObj.message)
            print ("******* Fatal error Exit due Database not reachable  ********")
            print ("******* Try number "+i +" from 100 ********")
            print ("******* Next Try in 30 sec ********")
            # Wait for 30 seconds
            time.sleep(30)
            #sys.exit(' ******* Fatal error Exit due Database not reachable ********')
        break

dataX={"DATA":[{
        "ANUMBER": "1",
        "AVARCHAR5": "row16",
        "ADATE": "2020-01-04 00:00:00"
    }, {
        "ANUMBER": 2,
        "AVARCHAR5": "row",
        "ADATE": "1977-01-04 00:00:00"
    }]}

def validateJSON(jsonData):
    try:
        json.loads(jsonData)
    except ValueError as err:
        print(" error")
        return "False"
    return "True"

#Check data constentency
def checkdata(datain):
    zeroarray=[]
    keyiseqaul=0
    valtypeisequal=0
    if "DATA" in datain:
        for value in datain["DATA"][1].values():
            zeroarray.append(type(value))
        #print (zeroarray)
        for i in range(len(datain["DATA"])):
            keyiseqaul=datain["DATA"][0].keys()==datain["DATA"][i].keys()
            #print (keyiseqaul)
            if not keyiseqaul:
                break
            for j in range(len(datain["DATA"][i])):
                #print ("j",j ,"data",type(list(datain["DATA"][i].values())[j]))
                valtypeisequal=type(list(datain["DATA"][0].values())[j])==type(list(datain["DATA"][i].values())[j])
                #print ("j",valtypeisequal)
                if not valtypeisequal :
                    break
    #print (keyiseqaul,valtypeisequal)
    result= keyiseqaul == valtypeisequal == 1
    #print (result)
    return result

#126665
#checkdata(dataX)
#Get all tables func
def getalltables(owner):
    dataout=[]
    status=500
    if owner == '0':
        owner=user
    #get session from pool
    try:
        con = pool.acquire()
    except cx_Oracle.DatabaseError as e:
        errorObj, = e.args
        dataout={"Database not reachable":[{"Error Message:":errorObj.message}]}
        status=500
    else:
        #prepare staement
        cur = con.cursor() 
        Collist=[]
        rowlist=()
        urllist=()
        sqlquery="SELECT TABLE_NAME FROM ALL_TABLES where OWNER= UPPER('"+ owner +"') and TABLESPACE_NAME is not null order by 1"
        print('getalltables sqlquery =  ' ,sqlquery )
        try:
            cur.execute(sqlquery)
        except cx_Oracle.Error as e:
            errorObj, = e.args
            #print("Error Code:", errorObj.code)
            #print("Error Message:", errorObj.message)
            dataout={"Statement Error ":[{"Error Message:":errorObj.message}]}
            status=400
        else:
            for index,row in enumerate(cur):
                rowlist=rowlist + row
                dataout=rowlist
                status=200
        con.close()
        #print (row)
    return dataout,status

# get table columns
def gettablestruct(tablename):
    dataout=[]
    status=500
    #Prepare connection to db
    try:
        con = pool.acquire()
    except cx_Oracle.DatabaseError as e:
        errorObj, = e.args
        dataout={"Database not reachable":[{"Error Message:":errorObj.message}]}
        status=500
    else:
        #prepare staement
        cur = con.cursor() 
        Collist=[]
        rowlist=[]
        sqlquery="SELECT T1.COLUMN_NAME, T1.DATA_TYPE,T1.DATA_LENGTH,T1.NULLABLE,(case when T2.COLUMN_NAME = T2.COLUMN_NAME then 'YES' else 'NO' end) as PK FROM ALL_TAB_COLUMNS T1 left join all_cons_columns t2 on T1.COLUMN_NAME=T2.COLUMN_NAME and T1.TABLE_NAME=T2.TABLE_NAME WHERE T1.TABLE_NAME= upper('" + tablename +"' ) and T1.TABLE_NAME= upper( '" + tablename +"') order by PK desc,T1.COLUMN_NAME"
        print('gettablestruct sqlquery = ' , sqlquery)
        try:
            cur.execute(sqlquery)
        except cx_Oracle.Error as e:
            errorObj, = e.args
            #print("Error Code:", errorObj.code)
            #print("Error Message:", errorObj.message)
            dataout={"Statement Error ":[{"Error Message:":errorObj.message}]}
            status=400
        else:
            for column in cur.description:
                Collist.append(column[0])
            for index,row in enumerate(cur):
                rowlist.append(row)
                dataout.append(dict(zip(Collist,row)))
                status=200
        con.close()
        #print (rowlist)
    return dataout,status

#function to get data as JSON
def GetData(column,tablename,where,groupby,orderby):
    DICTX=[]
    status=500
    #Prepare connection to db
    try:
        con = pool.acquire()
    except cx_Oracle.DatabaseError as e:
        errorObj, = e.args
        DICTX={"Database not reachable":[{"Error Message:":errorObj.message}]}
        status=500
    else:
        #prepare staement
        cur = con.cursor() 
        Collist=[]
        rowlist=[]
        if groupby =='0':
            groupby =''
        else:
            groupby = 'group by '+ groupby
        sqlquery="select "+ column + " from " + tablename + " where ( " + where + " ) " + groupby + " order by " + orderby
        print('GetData sqlquery = ' ,sqlquery)
        try:
            cur.execute(sqlquery)
        except cx_Oracle.Error as e:
            errorObj, = e.args
            DICTX={"Statement Error ":[{"Error Message:":errorObj.message}]}
            status=400
        else:
            for column in cur.description:
                Collist.append(column[0])
            for index,row in enumerate(cur):
                rowlist.append(row)
                #print(row)
                DICTX.append(dict(zip(Collist,row)))
                status=200
                #print (DICTX)
        con.close()
    return DICTX,status

#function to insert data
def prepareinsert(tablename,din):
    dout=[]
    columns=str(list(din['DATA'][0].keys())).replace("'","").replace("[","(").replace("]",")")
    binds=str(list(din['DATA'][0].keys())).replace("'","").replace("[","( :").replace("]",")").replace(", ",", :")
    #print (columns)
    #print (binds)
    #print (din['DATA'][0].values())
    for d in din['DATA']:
        dout.append(tuple(d.values()))
    SQL="INSERT INTO " + tablename  + " " + columns + " VALUES " + binds +" "
    print('prepareinsert SQL = ' ,SQL)
    return SQL,dout

# insert rows
def insertdata(tablename,datain):
    dataout=[]
    status=400
    #Prepare connection to db
    #if checkdata(datain)
    if checkdata(datain):
        try:
            con = pool.acquire()
        except cx_Oracle.DatabaseError as e:
            errorObj, = e.args
            dataout={"Database not reachable":[{"Error Message:":errorObj.message}]}
            status=500
        else:
            #prepare staement
            cur = con.cursor() 
            Collist=[]
            rowlist=[]
            sqlquery,data=prepareinsert(tablename,datain)
            print('insertdata sqlquery = ' ,sqlquery)
            print('insertdata data = ' , str(data))
            try:
                #print(type(data[0][0]))
                cur.executemany(sqlquery,data,batcherrors=False)
            except cx_Oracle.Error as e:
                errorObj, = e.args
                dataout={"Statement Error ":[{"Error Message:":errorObj.message}]}
                status=400
            else:
                status=200
                dataout={"Status ":[{" Number of row inserted :":cur.rowcount}]}
                #print(cur.rowcount)
                con.commit()
    else:
        status=400
        dataout={"BodyError column number and value type must be the same in all object example":[{"DATA":[{"COLUMNNAME1": 1,"COLUMNNAME2": "string","COLUMNNAME3": "2020-01-04 00:00:00"}, {"COLUMNNAME1": 2,"COLUMNNAME2": "string","COLUMNNAME3": "1977-01-04 00:00:00"}]}]}
    return dataout,status

# delte rows
def deletedata(tablename,col,op,val):
    dataout=[]
    status=500
    #Prepare connection to db
    try:
        con = pool.acquire()
    except cx_Oracle.DatabaseError as e:
        errorObj, = e.args
        dataout={"Database not reachable":[{"Error Message:":errorObj.message}]}
        status=500
    else:
        #prepare staement
        cur = con.cursor() 
        Collist=[]
        rowlist=[]
        bind=":"+col
        sqlquery="delete from " + tablename  + " where " + col + " " + op  + " " + val
        print('insertdata deletedata = ' , sqlquery)
        try:
            #print (sqlquery)
            #print (val)
            #resultsql = cur.var(str,arraysize=len(data))
            cur.execute(sqlquery)
        except cx_Oracle.Error as e:
            errorObj, = e.args
            dataout={"Statement Error ":[{"Error Message:":errorObj.message}]}
            status=400
        else:
            status=200
            dataout={"Status ":[{" Number of row deleted :":cur.rowcount}]}
            #print(cur.rowcount)
            con.commit()
    return dataout,status

def updatedata(tablename,datain):
    #print (len(datain['NEWROWS']))
    #print (len(datain['OLDROWS']))
    if len(datain['NEWROWS'])==len(datain['OLDROWS']):
        for i in range(len(datain['NEWROWS'])):
            #print(datain['NEWROWS'][i])
            try:
                con = pool.acquire()
            except cx_Oracle.DatabaseError as e:
                errorObj, = e.args
                dataout={"Database not reachable":[{"Error Message:":errorObj.message}]}
                status=500
            else:
                #print("do job")
                setstring=" "
                wherestring=" "
                #prepare Tuple New rows            
                for j,val in enumerate(datain['NEWROWS'][i].keys()):
                    setstring=setstring+val+" = :"+ str(j+1) +" , "
                #prepare Tuple old rows      
                for k,val in enumerate(datain['OLDROWS'][i].keys()):
                    wherestring=wherestring+val+" = :"+ str(k+j+1+1) +" and "
            #combine both tuple
            Finaltuple=tuple(datain['NEWROWS'][i].values())+tuple(datain['OLDROWS'][i].values())
            sqlquery="UPDATE " + tablename  + " SET "+ setstring[0:-2] + " WHERE " + wherestring[0:-4] + " "
            print('updatedata deletedata = ' ,sqlquery)
            cur = con.cursor()
            try:
                cur.execute(sqlquery,Finaltuple)
            except cx_Oracle.Error as e:
                errorObj, = e.args
                dataout={"Statement Error ":[{"Error Message:":errorObj.message}]}
                status=400
            else:
                status=200
                dataout={"Status ":[{" Number of row updated :":cur.rowcount}]}
            con.commit()

    else:
        dataout={"Error ":[{"Error Message:": " differance between NEWROWS and  OLDROWS  element number "}]}
        status=400     
    return dataout,status
#print (str(GetData('alpja','geometry_l')))
#print (str(gettablestruct('devcam')))
