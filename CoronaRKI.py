import requests
import json

LKNames=["Burgenlandkreis","Halle","Leipzig","Landkreis-Leipzig","Spree-Neiße-Kreis"]
LKIDs=["LK BURGENLANDKREIS","SK Halle","SK Leipzig","LK Leipzig","LK Spree-Neiße"]

def safeFile(fileName,data):
    with open(fileName,"w") as outfile:
            json.dump(data,outfile)
            print("neue Daten gespeichert")


for i in range(len(LKNames)):
    link="https://services7.arcgis.com/mOBPykOjAyBO2ZKk/arcgis/rest/services/RKI_Landkreisdaten/FeatureServer/0/query?where=county%20%3D%20%27"+LKIDs[i]+"%27&outFields=cases,deaths,cases_per_100k,cases_per_population,BL,BL_ID,county,last_update,cases7_per_100k,recovered,OBJECTID&outSR=4326&f=json"
    content=requests.get(link)
    newData=json.loads(content.text)
    newDataSet=newData["features"][0]["attributes"]
    
    
    fileName="/var/www/html/Covid-19/rkiData_"+LKNames[i]+"_aktuell.json"
    try:
        with open(fileName,"a+") as infile:
                infile.seek(0)
                oldData=json.load(infile)
    except json.JSONDecodeError:
        oldData=[]
        safeFile(fileName,oldData)
    if len(oldData)>0:
        print("letzte bekannte Daten:", oldData[-1]["last_update"])
        print("aktuellste Daten:", newDataSet["last_update"])
        if oldData[-1]["last_update"]!=newDataSet["last_update"]:
            print("Neue Daten vorhanden")
            oldData.append(newDataSet)
    
            safeFile(fileName,oldData)
    else:
        print("aktuellste Daten:", newDataSet["last_update"])
        print("Neue Daten vorhanden")
        oldData.append(newDataSet)
        safeFile(fileName,oldData)
    
    

