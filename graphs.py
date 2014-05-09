import xlwt

"""modified to fit data multiple times"""

inFile = open("./false-positives-av-rule-report.txt", "r")
list = []
list2 = []

book = xlwt.Workbook(encoding="utf-8")
sheet1 = book.add_sheet("Sheet 1")

sheet1.write(0, 0, "Occurrences")
sheet1.write(0, 1, "Detection Rate")
sheet1.write(0, 2, "Rule")
i = 1
j = 0
k = 0
for line in inFile:
    list = line.split()
    list2.append(list)
    sheet1.write(i, 0, int(list2[j][0]))
    sheet1.write(i, 1, float(list2[j][1]))
    sheet1.write(i, 2, list2[j][2])
    i = i + 1
    j = j + 1

book.save("./report.xls")
print "Done!"

