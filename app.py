from flask import Flask, request
import requests
import json

app = Flask(__name__)

@app.route('/')
def index():
    if request.args.get('postcodes') is None:
        return "supply postcodes in GETparm \"postcodes\".\n e.g ?postcodes=1234,5432"

    postCodes = request.args.get('postcodes').split(",")
    uniqPostCodes = list(set(postCodes))

    postCodeGeo = {}
    for postcode in uniqPostCodes:
        res = requests.get("http://v0.postcodeapi.com.au/suburbs/"+postcode+".json")
        res = json.loads(res.text)
        #postCodeGeo.append({"postcode":postcode,"latitude":res[0]['latitude'],"longitude":res[0]['longitude']})
        postCodeGeo[postcode] = {"latitude":res[0]['latitude'],"longitude":res[0]['longitude']}

    distanceList=[]
    for i in range(0,len(postCodes),2):
        postcode1=postCodes[i]
        postcode1_lat = str(postCodeGeo[str(postcode1)]['latitude'])
        postcode1_long = str(postCodeGeo[str(postcode1)]['longitude'])

        postcode2=postCodes[i+1]
        postcode2_lat = str(postCodeGeo[str(postcode2)]['latitude'])
        postcode2_long = str(postCodeGeo[str(postcode2)]['longitude'])

        url="https://api.mapbox.com/directions/v5/mapbox/driving/"+postcode1_long+","+postcode1_lat+";"+postcode2_long+","+postcode2_lat+"?access_token=pk.eyJ1Ijoid2Vic2ZvcngiLCJhIjoiY2tydWVxcG9uMTJ0eTJvcGZleHhjcGVvYSJ9.pxx2mIVsm5RUqGhZhtO7Gw"
        res = requests.get(url)
        res = json.loads(res.text)

        distance = res['routes'][0]['distance']

        distanceList.append(round(distance/1000,4))
        #distanceList.append({'postcode1':postcode1,'postcode2':postcode2,'distance':round(distance/1000,4)})
    if len(distanceList > 1):
        return str(distanceList)
    return str(distanceList[0])

if __name__ == '__main__':
    app.debug = True
    app.run()
