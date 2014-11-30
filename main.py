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

remixsid_cookie = sys.argv[1]
RequestData = {
    "act": "show",
    "al": 1,
    "loc":"im",
    "w": "history" + sys.argv[2] + "_photo",
    "offset" : 0,
    "part" : 1
}

# remixssid_cookie = "8cb32fac0d58f6d70d9cb9263feee8bf8d4ccd6b864ac6ccafcc7"
# RequestData = {
#     "act": "show",
#     "al": 1,
#     "loc": "im",
#     "w": "history" + "9816053" + "_photo",
#     "offset" : 0,
#     "part" : 1
# }

href = "http://vk.com/wkview.php"
bound = {"count" : 10000, "offset" : 0}

try:
    os.mkdir("drop_" + sys.argv[3])
except OSError:
    print "Проблемы с созданием папки 'drop_" + sys.argv[3] + "'"
os.chdir("drop_" + sys.argv[3])

test = open("links", "w")
while( bound['offset'] < bound['count'] ):
    RequestData['offset'] = bound['offset']
    content = requests.post(href, cookies={"remixsid": remixsid_cookie}, params=RequestData).text
    json_data_offset = re.compile('\{"count":.+?,"offset":.+?\}').search(content)

    links = re.compile('src="http://.+?"').findall(content)
    bound = json.loads(content[json_data_offset.span()[0]:json_data_offset.span()[1]])
    bound['count'] = int(bound['count'])
    bound['offset'] = int(bound['offset'])

    for st in links:
        test.write(st[5:len(st)-1] + '\n')
test.close()

test = open("links", "r")
file_num = 0
for href in test:
    urllib.urlretrieve(href, str(file_num))
    file_num += 1
    print "Скачано " + str(file_num) + " файлов\n"
test.close()