import petl as etl
import re
t2=etl.fromcsv("Stations.csv")

t2=etl.capture(t2,'Address','(\d{4}$)',['Postcode'],include_original=True)

def substitute(table, field, pattern, repl, count=0,flags=0):
	 prog = re.compile(pattern, flags)
	 conv = lambda v: prog.sub(repl, v, count=count)
	 return etl.convert(table, field, conv)

t2=substitute(t2,"Address",'\d{4}\Z',"")

t2=etl.addfield(t2,"State","Qld")

t2=etl.addfield(t2,'email', lambda rec:rec['Station Name'].lower())
t2=substitute(t2,'email','[\s]','')
t2=substitute(t2,'email','firestation','')
t2=etl.addfield(t2,'E-mail', lambda rec: 'enquire@{}.qfes.gov.au'.format(rec['email']))
t2=etl.cutout(t2,"email")

t2 = etl.rename(t2, 'Phone', 'Phone Number')
t2 = etl.rename(t2, 'Fax', 'Fax Number')
t2 = etl.rename(t2, 'Address', 'Street Address')
t2 = etl.rename(t2, 'Stn Number', 'Station Number')
t2 = etl.rename(t2, 'Stn Type', 'Station Type')
t2=etl.cutout(t2,'Alternate Address')
t2 = etl.rename(t2, 'Region', 'Region Code')
print(t2)

t3=etl.fromcsv("Queensland_Regions.csv")
print(t3)

t4=etl.fromxml("Station_Locations.xml","STATION",{"NAME":"NAME","LONG":"LONG","LAT":"LAT"})
t4 = etl.rename(t4, 'LAT', 'Latitude')
t4 = etl.rename(t4, 'LONG', 'Longitutde')
t4=etl.convert(t4,"NAME",'title')
t4=etl.addfield(t4,'Station Name', lambda rec: '{} Fire Station'.format(rec['NAME']))
t4=etl.cutout(t4,'NAME')
print(t4)

mer_1=etl.join(t3,t2,key='Region Code')
print(mer_1)
mer_2=etl.join(mer_1,t4,key='Station Name')
mer_2=etl.cutout(mer_2,'Region Name')
mer_2=etl.cutout(mer_2,'Region Code')
mer_2=etl.movefield(mer_2,'Station Number',1)
mer_2 = etl.sort(mer_2, key=['RegionID','Station Number'])
print(mer_2)

etl.tocsv(mer_2,"Fire_Station_Locations.csv")
