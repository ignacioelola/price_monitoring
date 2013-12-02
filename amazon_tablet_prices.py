import requests
import json
import datetime
import csv
import sys
import time 



#login details
my_username = username
my_password = password



#Login into import.io
endpoint = "api.import.io"
port = "80"
post_body = {'username': my_username, 'password': my_password}

try:
    r = requests.post("http://" + endpoint + ":" + port + "/auth/login", data=post_body)
except:
    print "There appears to be some problem logging in."
    sys.exit()
if r.status_code == 200:
        cookie = r.cookies["AUTH"]
        session = {"cookie":cookie, "endpoint": endpoint, "port": port}
else:
    print "There appears to be some problem logging in."
    sys.exit()





#details for data extraction:
extractor_guid="e8a55ca5-4dd4-4710-8fe4-6a641d2138f3"
urls=["http://www.amazon.com/Google-Nexus-Tablet-7-Inch-Black/dp/B00DVFLJKQ",
	"http://www.amazon.com/Google-Nexus-10-Wi-Fi-only/dp/B00ACVI202",
	"http://www.amazon.com/Apple-MD786LL-Wi-Fi-NEWEST-VERSION/dp/B00G2X1VIY",
	"http://www.amazon.com/Apple-iPad-MD532LL-Wi-Fi-White/dp/B00746WCEA"]





#Function to query an extractor an get the results back
def query_connector(query, connector_guid, session):
    print "\nsearching connector. guid = %s..." % connector_guid
    endpoint = "http://query.import.io/store/connector/"
    rr = requests.post( endpoint + connector_guid + "/_query", data=json.dumps(query), cookies={"AUTH": session["cookie"]})
    if rr.status_code == 200:
    	#print rr.text
        results = rr.json()
        return results
    else:
        print rr.json()
        return False



#read the previous data:
all_rows=[]
with open('black_friday_prices.csv', 'rb') as infile:
    reader=csv.reader(infile)
    for row in reader:
        all_rows.append(row)
infile.close()


current_datetime=datetime.datetime.now()


#Querying extractor
for url in urls:
		row=[]
		query = {"input": {"webpage/url":url}}
		response = query_connector(query, extractor_guid, session)
		try:
			row.append(current_datetime)
		except:
			row.append("")
		try:
			row.append(response["results"][0]["product"])
		except:
			row.append("")
		try:
			row.append(response["results"][0]["latest_price"])
		except:
			row.append("")
		try:
			row.append(response["results"][0]["reviews_5_stars"])
		except:
			row.append("")
		try:
			row.append(response["results"][0]["reviews_4_stars"])
		except:
			row.append("")
		try:
			row.append(response["results"][0]["reviews_3_stars"])
		except:
			row.append("")
		try:
			row.append(response["results"][0]["reviews_2_stars"])
		except:
			row.append("")
		try:
			row.append(response["results"][0]["reviews_1_stars"])
		except:
			row.append("")
		all_rows.append(row)



#saving results:
with open("black_friday_prices.csv","wb") as outfile:
	writer=csv.writer(outfile)	
	for row in all_rows:
		writer.writerow(row)



