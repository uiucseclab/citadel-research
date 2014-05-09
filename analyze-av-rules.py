import simplejson
import json
import urllib
import urllib2
import time
url = "https://www.virustotal.com/vtapi/v2/file/report"

inFile = open("./false-positives.txt", "r")
outFile = open("./av-rule-report.txt", "w")
rules = []
occurrences = []
rates = []
directory = "/home/Citadel_Files"

#analyze rules for each false positive
for line in inFile:
	#parse line data
	line.rstrip()
	str1 = line
	loc1 = str1.find(" ") + 1
	nums = str1[loc1:-1]
	rate = float(nums)

	#open json file
	binary = line[:loc1-1]
	jsonFile = directory + binary + "/avresults.json"
	try:
		f = open(jsonFile, "r")
		results = f.read()
		#get each av rule in file
		while results.find(":") >= 0:
			#get rule
			ruleLoc = results.find(":")
			results = results[ruleLoc+2:]
			endLoc = results.find("\"")
			ruleStr = results[:endLoc]

			#check if already in array
			try:
				ind = rules.index(ruleStr)
				rates[ind] = ((rates[ind] * occurrences[ind]) + rate) / (occurrences[ind] + 1)
				occurrences[ind] = occurrences[ind] + 1
			except ValueError:
				rules.append(ruleStr)
				occurrences.append(1)
				rates.append(rate)


			results = results[endLoc:]


		f.close()
	except IOError:
		#download report if needed
		print "NO REPORT FOR" + jsonFile
		print "Downloading report..."
		parameters = {"resource": binary,"apikey": "52aba3f51bb2b1ba8c233209e0dda879d1906f3e3ff4f7ab5b09d19047ed10c6"}
		data = urllib.urlencode(parameters)
		req = urllib2.Request(url, data)
		response = urllib2.urlopen(req)
		json_string = response.read()
		data = json.loads(json_string)
		results = str(data['scans'])

		#get each av rule in report
		while results.find("result': u") >= 0:
			#get rule
			ruleLoc = results.find("result': u")
			results = results[ruleLoc+11:]
			endLoc = results.find("'")
			ruleStr = results[:endLoc]

			#check if already in array
			try:
				ind = rules.index(ruleStr)
				rates[ind] = ((rates[ind] * occurrences[ind]) + rate) / (occurrences[ind] + 1)
				occurrences[ind] = occurrences[ind] + 1
			except ValueError:
				rules.append(ruleStr)
				occurrences.append(1)
				rates.append(rate)

			results = results[endLoc:]
		time.sleep(20)
		print "Report downloaded."

#write report
for x in range(len(rules)):
	repRule = rules[x]
	repOccurrences = str(occurrences[x])
	repRates = str(rates[x])
	outFile.write(repOccurrences)
	outFile.write(" ")
	#if len(repOccurrences) = 1:
	#	outFile.write(" ")
	outFile.write(repRates)
	outFile.write(" ")
	outFile.write(repRule)
	outFile.write("\n")

outFile.close()
inFile.close()