# importing module 
from flask import Flask ,Response ,jsonify ,request ,json
from get_db_data import GetData ,gettablestruct ,getalltables ,insertdata ,deletedata ,updatedata 
import json
import datetime

app = Flask(__name__)

def formatdate(obj):
    if isinstance(obj, (datetime.date, datetime.datetime)):
        return obj.isoformat()

def validateJSON(jsonData):
    try:
        json.loads(jsonData)
    except ValueError as err:
        print(" error")
        return "False"
    return "True"

@app.route('/', methods=['GET'])
def hello():
    return "Hello World misssouli!"

@app.route('/oracleapi/tables', methods=['GET'])
def alltables():
    owner=request.args.get('owner', default = '0', type = str)
    if owner == '':
        owner='0'
    data,status=getalltables(owner)
    return Response(json.dumps(data), mimetype='application/json',status=status)

@app.route('/oracleapi/<string:tablename>/details', methods=['GET'])
def describetable(tablename):
    #print (gettablestruct(tablename))
    data,status=gettablestruct(tablename)
    return Response(json.dumps(data,default=formatdate), mimetype='application/json',status=status)

#fetch data
@app.route('/oracleapi/<string:tablename>/select', methods=['GET'])
def getdata(tablename):
    column=request.args.get('col', default = '*', type = str)
    where = request.args.get('filter', default = '1=1', type = str)
    groupby = request.args.get('groupby', default = '0', type = str)
    orderby = request.args.get('orderby', default = '1', type = str)
    #print ("Table = " + str(tablename) + "column = " + str(column) +" where = " + str(where) + " groupby = " + str(groupby) + " orderby = " + str(orderby)) 
    data,status=GetData(column,tablename,where,groupby,orderby)
    return Response(json.dumps(data,default=formatdate ), mimetype='application/json',status=status)

#Add data
@app.route('/oracleapi/<string:tablename>/add', methods=['POST'])
def adddata(tablename):
    #print (request.get_json(force=True))
    if(request.data):
        data,status=insertdata(tablename,request.get_json(force=True))
    else:
        data={"Error ":[{"Error Message:": " Missing Json in BODY "}]}
        status=400        
    return Response(json.dumps(data,default=formatdate ), mimetype='application/json',status=status)

#update DATA
@app.route('/oracleapi/<string:tablename>/update', methods=['PATCH'])
def uptdata(tablename):
    if request.data and ("NEWROWS" in request.get_json(force=True)) and ("OLDROWS" in request.get_json(force=True)) :
        data,status=updatedata(tablename,request.get_json(force=True))
    else:
        data={"Error ":[{"Error Message:": " Missing Json in BODY or incorect JSONFormat"}]}
        status=400    
    return  Response(json.dumps(data,default=formatdate ), mimetype='application/json',status=status)

#delete data
@app.route('/oracleapi/<string:tablename>/delete', methods=['DELETE'])
def deldata(tablename):
    column = request.args.get('col', default = '*', type = str)
    value = request.args.get('val', default = '', type = str)
    operator = request.args.get('op', default = '=', type = str)
    if (column == '*') or ( value == '') :
        dataout={"Request Error":[{"Missing Argument:":"col ( Mandatory, column of condition ) , op ( Not Mandatory; = < > like != ... default is = ) and val (Mandatory, Value  top match )"}]}
        status=400
    else:
        dataout,status=deletedata(tablename,column,operator,value)
    return Response(json.dumps(dataout,default=formatdate ), mimetype='application/json',status=status)

#def setup_app(app):
#    json.JSONEncoder()

#setup_app(app)

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000, threaded=True , use_reloader=True, use_debugger=True, use_evalex=True)