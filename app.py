from flask import Flask, request
import requests
import json

app = Flask(__name__)

# Default route
@app.route('/')
def index():
    # If the postcode parameter is not supplied, print error message
    if request.args.get('postcodes') is None:
        return "You must supply postcodes in the GET parameter \"postcodes\".\n e.g ?postcodes=1234,5432"

    # Split postcodes from GET parameter into list
    postCodes = request.args.get('postcodes').split(",")

    # If an uneven number of postcodes were supplied, print error message
    if len(postCodes)%2 != 0:
        return "Postcodes are processed in pairs. You must supply an EVEN number of postcodes.\n?postcodes=1234,5678,9876,5432"

    # Get unique postcodes from list of postCodes
    uniqPostCodes = list(set(postCodes))

    # Get geo-coordinates for all unique postcodes
    postCodeGeo = {}
    for postcode in uniqPostCodes:
        # Make api request. Extract JSON
        res = requests.get("http://v0.postcodeapi.com.au/suburbs/"+postcode+".json")
        res = json.loads(res.text)
        # Save to dictionary
        postCodeGeo[postcode] = {"latitude":res[0]['latitude'],"longitude":res[0]['longitude']}

    # Loop through postcode-pairs.
    distanceList=[]
    for i in range(0,len(postCodes),2):
        # Get geo data of postcode1
        postcode1=postCodes[i]
        postcode1_lat = str(postCodeGeo[str(postcode1)]['latitude'])
        postcode1_long = str(postCodeGeo[str(postcode1)]['longitude'])
        # Get geo data of postcode2
        postcode2=postCodes[i+1]
        postcode2_lat = str(postCodeGeo[str(postcode2)]['latitude'])
        postcode2_long = str(postCodeGeo[str(postcode2)]['longitude'])

        # Make mapbox API call to get distance
        url="https://api.mapbox.com/directions/v5/mapbox/driving/"+postcode1_long+","+postcode1_lat+";"+postcode2_long+","+postcode2_lat+"?access_token=pk.eyJ1Ijoid2Vic2ZvcngiLCJhIjoiY2tydWVxcG9uMTJ0eTJvcGZleHhjcGVvYSJ9.pxx2mIVsm5RUqGhZhtO7Gw"
        res = requests.get(url)
        res = json.loads(res.text)
        # Extract JSON to var
        distance = res['routes'][0]['distance']

        # Append (distance or postcode-distance-dict to results list)
        distanceList.append(round(distance/1000,4))
        #distanceList.append({'postcode1':postcode1,'postcode2':postcode2,'distance':round(distance/1000,4)})
    # If multiple pairs were supplied return entire list, else return 1st//only element.
    if len(distanceList) > 1:
        #return str(distanceList)
        xstr = ""
        for x in distanceList:
            xstr+=str(x)+"<br>"
        return xstr
    return str(distanceList[0])

if __name__ == '__main__':
    app.debug = True
    app.run()
