import json as simplejson
import json
import urllib
import urllib2
import time
url = "https://www.virustotal.com/vtapi/v2/file/report"

inFile = open("./non-false-positives.txt", "r")
outFile = open("./av-rule-report-local-only.txt", "w")
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