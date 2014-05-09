import math

inFile = open("./virus-total-report.txt", "r")
outFile = open("./detection-rates.txt", "w")
array = []
varArray = []

for line in inFile:
	#ignore lines with no report
	if line.find(" xx xx") < 0:
		line.rstrip()
		str1 = line
		loc1 = str1.find(" ") + 1
		nums = str1[loc1:]
		loc2 = nums.find(" ")
		pos = nums[:loc2]
		tot = nums[loc2+1:len(nums)-1]
		res = float(pos)/float(tot)
		res = res * 100
		array.append( res )
		outFile.write(line[:loc1])
		outFile.write(str(res))
		outFile.write('\n')

outFile.close()
inFile.close()

#calculate mean
mean = sum(array) / float(len(array))

#calculate variance
for x in range(len(array)):
	varArray.append(array[x] - mean)
	varArray[x] = varArray[x] * varArray[x]
variance = sum(varArray) / float(len(varArray))

#calculate standard deviation
stdDev = math.sqrt(variance)

#print stats
print "Mean: " + str(mean)
print "Variance: " + str(variance)
print "Std Deviation: " + str(stdDev)

inFile = open("./detection-rates.txt", "r")
outFile = open("./false-positives.txt", "w")

for line in inFile:
	line.rstrip()
	str1 = line
	loc1 = str1.find(" ") + 1
	nums = str1[loc1:-1]
	rate = float(nums)
	
	#compare and write to outFile
	if rate > (mean + (stdDev*2)):
		outFile.write(line)
	if rate < (mean - (stdDev*2)):
		outFile.write(line)
outFile.close()
inFile.close()