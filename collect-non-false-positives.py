inFile = open("detection-rates.txt", "r")
outFile = open("non-false-positives.txt", "w")
mean = 68.0324795695
stdDev = 2 * 17.556042963

for line in inFile:
	line.rstrip()
	str1 = line
	loc1 = str1.find(" ") + 1
	nums = str1[loc1:-1]
	rate = float(nums)
	
	#compare and write to outFile
	if rate >= (mean-stdDev):
		if rate <= (mean+stdDev):
			outFile.write(line)

outFile.close()
inFile.close()