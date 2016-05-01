# coding=utf-8

import requests
import re
import sys
import os
import urllib
import json

# argv[1] = remixsid_cookie
# argv[2] = dialog_id
# argv[3] = person_name

def printHelp():
    print """
    Usage: python main.py <remixsid_cookie> <dialog_id> <name_of_folder>
    <dialog_id> is a string parameter "sel" in address line which you see when open a dialog
    """

try:
    sys.argv[1]
except IndexError:
    printHelp()
    exit()

if( sys.argv[1] == '--help' ):
    printHelp()
    exit()
else:
    if( len(sys.argv) < 4 ):
        print """
        Invalid number of arguments. Use parameter --help to know more
        """
        exit()

remixsid_cookie = sys.argv[1]

RequestData = {
    "act": "show",
    "al": 1,
    "loc":"im",
    "w": "history" + sys.argv[2] + "_photo",
    "offset" : 0,
    "part" : 1
}

request_href = "http://vk.com/wkview.php"
bound = {"count" : 10000, "offset" : 0}

try:
    os.mkdir("drop_" + sys.argv[3])
except OSError:
    print "Проблемы с созданием папки 'drop_" + sys.argv[3] + "'"
if( os.path.exists("drop_" + sys.argv[3]) ):
    os.chdir("drop_" + sys.argv[3])
else:
    print "Не удалось создать папку\n"
    exit()

test = open("links", "w")
while( bound['offset'] < bound['count'] ):
    RequestData['offset'] = bound['offset']
    content = requests.post(request_href, cookies={"remixsid": remixsid_cookie}, params=RequestData).text
    json_data_offset = re.compile('\{"count":.+?,"offset":.+?\}').search(content)
    bound = json.loads(content[json_data_offset.span()[0]:json_data_offset.span()[1]])
    bound['count'] = int(bound['count'])
    bound['offset'] = int(bound['offset'])

    links = re.compile('&quot;http://cs.+?"').findall(content)

    for st in links:
        st = st.replace("&quot;,&quot;x_&quot;:[&quot;", "")
        test.write(st[6:st.find("&quot;", 6)] + '.jpg\n')

test.close()

test = open("links", "r")
file_num = 0
for href in test:
    urllib.urlretrieve(href, str(file_num) + ".jpg")
    file_num += 1
    print "Скачано " + str(file_num) + " файлов\n"
test.close()