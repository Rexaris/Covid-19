import requests
import json

link="https://services7.arcgis.com/mOBPykOjAyBO2ZKk/arcgis/rest/services/RKI_Landkreisdaten/FeatureServer/0/query?where=county%20%3D%20%27LK%20BURGENLANDKREIS%27&outFields=cases,deaths,cases_per_100k,cases_per_population,BL,BL_ID,county,last_update,cases7_per_100k,recovered,OBJECTID&outSR=4326&f=json"
content=requests.get(link)
newData=json.loads(content.text)
newDataSet=newData["features"][0]["attributes"]


fileName="/var/www/html/Covid-19_Burgenlandkreis/rkiData_Burgenlandkreis_aktuell.json"
with open(fileName,"r") as infile:
    oldData=json.load(infile)
print("letzte bekannte Daten:", oldData[-1]["last_update"])
print("aktuellste Daten:", newDataSet["last_update"])
if oldData[-1]["last_update"]!=newDataSet["last_update"]:
    print("Neue Daten vorhanden")
    oldData.append(newDataSet)

    with open(fileName,"w") as outfile:
        json.dump(oldData,outfile)
        print("neue Daten gespeichert")
