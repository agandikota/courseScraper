from lxml import html as ht
import urllib2
import requests


def checkCourse(term, program, courseNo):
	url = "http://www.adm.uwaterloo.ca/cgi-bin/cgiwrap/infocour/salook.pl?sess={term}&level=under&subject={program}&cournum={courseNo}".format(term = term, program = program,courseNo = courseNo)

	page = requests.get(url)
	tree = ht.fromstring(page.text)

	tablePos = 4

	if (tree.xpath("//b")[0].text_content() == "Sorry, but your query had no matches."):
		return

	else:
		if (not tree.xpath('//table[1]/tr[4]/td[2]/table[1]/tr')):
			tablePos = 3

		rowCount = 0

		for row in tree.xpath('//table[1]/tr[{tablePos}]/td[2]/table[1]/tr'.format(tablePos = tablePos)):
			# try:
			# 	if (len(row.xpath('./td')) == 13):
			# except ValueError as v:
			# 	print "Value Error: {0}".format(row[0].text_content())
			
			if (len(row.xpath('./td')) == 13 and
			 int(row.xpath('./td[4]')[0].text_content()) != 99):
				rowCount += 1
				enrolCap = int(row.xpath('./td[7]')[0].text_content())
				enrolTotal = int(row.xpath('./td[8]')[0].text_content())
				print "{program} {course} LEC {lecture}: ".format(program = program, course = courseNo,lecture = rowCount),
				if (enrolTotal == enrolCap):
					print "Class is full"
				elif(enrolTotal > enrolCap):
					print "Class is overflowing"
				else:
					print "{0} slots available".format(enrolCap - enrolTotal)
				
	# return "Last updated: {0}".format(tree.xpath("//b")[0].text_content())


def listOfCSPrograms():
	for courseNo in range(100,500):
		term = 1155
		program = "STAT"
		checkCourse(term,program,courseNo)
		# if (val != "N/A"):
		# 	print "{program} {course} : {value}".format(program = program, course = courseNo, value = val)

listOfCSPrograms()



