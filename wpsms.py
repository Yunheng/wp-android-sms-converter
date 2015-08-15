import sys
import string, datetime, codecs, copy
from lxml import etree
from io import StringIO, BytesIO

def ldap_to_unix_timestamp(ldap_timestamp):
	x = int(ldap_timestamp / 10000)
	unix_timestamp = x - 11644473600000
	return unix_timestamp

def unix_to_ldap_timestamp(unix_timestamp):
	x = int(unix_timestamp * 10000)
	ldap_timestamp = x + 11644473600000
	return ldap_timestamp
	
input_file = sys.argv[1]
output_file = sys.argv[2]

input_tree = etree.parse(input_file)
output_tree = etree.Element("smses")
count = 0

for msg in input_tree.xpath('//Message'):
	attachments = msg.xpath('Attachments/node()')
	incoming = msg.xpath('IsIncoming/text()')[0] == 'true' if True else False
	read = msg.xpath('IsRead/text()')[0] == 'true' if True else False
	body = msg.xpath('Body/text()')
	if body:
		body = body[0]
	else:
		body = ""
	timestamp = int(msg.xpath('LocalTimestamp/text()')[0])
	timestamp = ldap_to_unix_timestamp(timestamp)
	
	if attachments:
		sms = etree.SubElement(output_tree, "mms")
		print("MMS -"),
	else:
		sms = etree.SubElement(output_tree, "sms")
		print("SMS -"),

	sms.attrib['protocol'] = "0"
	sms.attrib['subject'] = "null"
	sms.attrib['toa'] = "null"
	sms.attrib['sc_toa'] = "null"
	if read:
		sms.attrib['read'] = "1"
	else:
		sms.attrib['read'] = "0"
	sms.attrib['status'] = "-1"
	sms.attrib['locked'] = "0"
	sms.attrib['body'] = body
	sms.attrib['date'] = str(timestamp)
	
	timestamp = datetime.datetime.fromtimestamp(timestamp / 1000)
	if incoming:
		print("In  :"),
		sender = msg.xpath('Sender/text()')[0]
		sms.attrib['address'] = sender
		sms.attrib['type'] = "1"

		print "Received from " + sender + " at " + timestamp.strftime('%Y-%m-%d %H:%M:%S')
		count = count + 1
	else:
		print("Out :"),
		recepients = msg.xpath('Recepients/node()/text()')
		sms.attrib['type'] = "2"
		remaining = len(recepients)
			
		for recepient in recepients:
			sms.attrib['address'] = recepient

			print "Sent to " + recepient + " at " + timestamp.strftime('%Y-%m-%d %H:%M:%S')
			remaining = remaining - 1
			
			if remaining > 0:
				print("Out :"),
				sms = copy.deepcopy(sms)
				output_tree.append(sms)

		count = count + len(recepients)

output_tree.attrib['count'] = str(count)
output = etree.tostring(output_tree, pretty_print=True)

with codecs.open(output_file,'w',encoding='utf8') as f:
    f.write(output)
	
print "Done Converting " + str(count) + " SMS/MMS"