Project: Citadel Malware Feed Analysis
Team: Mike Patterson & Will Ratner


Python Scrips:
==============

virusTotal.py
-------------
For each binary in the feed, this script will use the hash to download the corresponding report from VirusTotal.com using their public API. It will grab the number of positive detections and the total number of antivirus softwares the sample was run through. If a particular binary has not had a report built for it yet, it is ignored. All of this information is output to a file named "virus-total-report.txt" in the following format:

<hash of the binary> <# of positive detections> <total number of tests>

This script takes a while to run. The virustotal.com public API limits queries to 4 per minute per API key. The script limits use of the API to 3 queries per minute to ensure that the script would continue to run for long periods of time without being refused by the API, which would cause our script to fail.

collect-false-positives.py
--------------------------
This script uses the "virus-total-report.txt" file as an input. For each binary listed in the report, it calculates the detection rate (# positive detections / total # tests). This information is then output to a file named "detection-rates.txt" in the following format:

<hash of the binary> <detection rate>

Next, all of the detection rates are used to calculate the average detection rate, variance, and standard deviation, which are all printed out to the console.

Finally, any binaries that have a detection rate outside two standard deviations from the average detection rate are written to a file called "false-positives.txt" in the same format as above.

collect-non-false-positives.py
------------------------------
This script uses the "detection-rates.txt" report as an input. Any binaries with a detection rate inside of two standard deviations from the average detection rate are written to a file called "non-false-positives.txt" in the following format:

<hash of the binary> <detection rate>

Note: the average detection rate and standard deviation must be set in the script.

analyze-av-rules.py
-------------------
This script uses the "false-positives.txt" report as an input. For each binary in the report, the script will first try to open a local copy of the report it it exists (i.e. if we downloaded it from the malware feed). If a local copy of the report does not exist, the script will download the report from virustotal.com. These reports are used to see which rules detected the Citadel malware. The script will count how many times each rule was used, and calculate the average detection rate among all the binaries that were detected using that rule. The results are output to the "av-rule-report.txt" report in the following format:

<# times rule detected Citadel> <avg. detection rate among binaries detected with this rule> <rule>

analyze-av-rules-local-only.py
------------------------------
This script is identical to the previous script except it will ignore binaries where a local copy of the report cannot be found. The results are output to a file named "av-rule-report-local-only.txt". This script was used to analyze the non-false-positive rules faster, because the reports were divided between two different computers and downloading reports takes much longer due to virustotal.com's public API limits.

rate-av-rules.py
----------------
This script takes two av rule reports as input: "false-positives-av-rule-report.txt" and "non-false-positive-av-rule-report.txt". For each rule in the false positives rule report, the script will determine how many times the rule was used to cause a non-false-positive and what percentage of the time the rule caused false positives. All of this information is output to the "av-rule-ratings.txt" report in the following format:

<rule>,<# times rule caused false positive>,<avg. detection rate among false positives detected with this rule>,<# times rule caused non false positive>,<avg. detection rate among non false positives detected with this rule>,<percentage of time the rule caused a false positive>

