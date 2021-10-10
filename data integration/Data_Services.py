from bottle import route, run, request, response
import petl as etl
import json as js

# create service to respond to "getoffices" request
@route('/getregions')
def get_region():
    print("Received a request for getregion")

    #open farmers.csv
    t1 = etl.fromcsv("Queensland_Regions.csv")
    print(t1)

    #prepare response
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Content-type'] = 'application/json'

    #return farmers data in JSON format
    return js.JSONEncoder().encode(list(etl.dicts(t1)))

@route('/getstations')
def get_station():
    regionid=request.query.regionid
    print("Receive request for region:"+regionid)
    t2 = etl.fromcsv("Fire_Station_Locations (Solution).csv")
    if regionid == '0':
       result_two=etl.cut(t2,"Station Number","Station Name","Street Address","State","Postcode","Phone Number","E-Mail","Latitude","Longitude")
       print(result_two)
    else:
       result_one=etl.select(t2,"{RegionID}=='"+str(regionid)+"'")
       result_two=etl.cut(result_one,"Station Number","Station Name","Street Address","State","Postcode","Phone Number","E-Mail","Latitude","Longitude")
       print(result_two)
    
    #prepare response
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Content-type'] = 'application/json'

    #return farmers data in JSON format
    return js.JSONEncoder().encode(list(etl.dicts(result_two)))
run(host='localhost', port=8080, debug=True)
