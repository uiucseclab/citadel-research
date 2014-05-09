import json as simplejson
import json
import urllib
import urllib2
import os, sys, time, pickle
i = 1;
url = "https://www.virustotal.com/vtapi/v2/file/report"
dirs = os.listdir("/home/Citadel_Files")
f = open("D:\\temp_CS460\\virus-total-report.txt", "w")
for file in dirs:
    f.write(file)
    f.write(" ")
    parameters = {"resource": file,"apikey": "b00adc54d1e6eb126c9ecc703120672978b3e19b722b018287e82d481dfbae17"}
    data = urllib.urlencode(parameters)
    req = urllib2.Request(url, data)
    response = urllib2.urlopen(req)
    json_string = response.read()
    data = json.loads(json_string)

    try:
        f.write(str(data['positives']))
        f.write(" ")
        f.write(str(data['total']))
        f.write('\n')
        print "%d %s" % (i, file)
        i = i + 1
    except KeyError:
        f.write("xx xx\n")
        print "%d %s NO REPORT" % (i, file)
        i = i + 1
    time.sleep(20)
f.close()

