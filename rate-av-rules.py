inFile1 = open("false-positives-av-rule-report.txt", "r")
inFile2 = open("non-false-positives-av-rule-report.txt", "r")
outFile = open("av-rule-ratings.txt", "w")

nfp_rules = []
nfp_occurrences = []
nfp_rates = []
fp_rules = []
fp_occurrences = []
fp_rates = []

#grab false-positive rules
for line in inFile1:
	#parse line data
	str1 = line
	loc1 = str1.find(" ")
	ocur = int(str1[:loc1])
	str1 = str1[loc1+1:]
	loc1 = str1.find(" ")
	rate = float(str1[:loc1])
	str1 = str1[loc1+1:]
	ruleStr = str1[:-1]
	fp_rules.append(ruleStr)
	fp_occurrences.append(ocur)
	fp_rates.append(rate)

#grab non-false-positive rules
for line in inFile2:
	#parse line data
	str1 = line
	loc1 = str1.find(" ")
	ocur = int(str1[:loc1])
	str1 = str1[loc1+1:]
	loc1 = str1.find(" ")
	rate = float(str1[:loc1])
	str1 = str1[loc1+1:]
	ruleStr = str1[:-1]
	nfp_rules.append(ruleStr)
	nfp_occurrences.append(ocur)
	nfp_rates.append(rate)

#write all rules to output file
for x in range(len(fp_rules)):
	#format: fp_ocur fp_rate nfp_ocur nfp_rate fp_percentage rule
	repRule = fp_rules[x]
	repFPOcur = fp_occurrences[x]
	repFPRate = fp_rates[x]
	#see if this rule caused any non-false-positives
	try:
		ind = nfp_rules.index(repRule)
		repNFPOcur = nfp_occurrences[ind]
		repNFPRate = nfp_rates[ind]
		fp_percentage = (float(repFPOcur) / (float(repFPOcur) + float(repNFPOcur))) * 100
	except ValueError:
		repNFPOcur = 0
		repNFPRate = -1
		fp_percentage = float(100)
	outFile.write(repRule)
	outFile.write(",")
	outFile.write(str(repFPOcur))
	outFile.write(",")
	outFile.write(str(repFPRate))
	outFile.write(",")
	outFile.write(str(repNFPOcur))
	outFile.write(",")
	outFile.write(str(repNFPRate))
	outFile.write(",")
	outFile.write(str(fp_percentage))
	outFile.write("\n")

outFile.close()
inFile1.close()
inFile2.close()
