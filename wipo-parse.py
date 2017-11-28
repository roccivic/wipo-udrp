import os
import re
from bs4 import BeautifulSoup

list = []

for filename in os.listdir("WIPO"):
    with open("WIPO/" + filename, "rb") as file:
        contents = file.read()
        soup = BeautifulSoup(contents, "html.parser")
        contents = soup.get_text()
        list_item = {
            "filename": filename,
            "decision": 'UNKNOWN',
            "type": 'UNKNOWN',
            "responded": 'UNKNOWN'
        }
        contents = contents.replace("\n", " ").lower()

        m = re.findall('7\.\s*decision.*?dated?:', contents, re.M)
        if len(m):
            decision_text = m[0]
            if "cancelled" in decision_text:
                list_item["decision"] = 'CANCELLED'
            elif "denied" in decision_text:
                list_item["decision"] = 'DENIED'
            elif "decline" in decision_text:
                list_item["decision"] = 'DENIED'
            elif "transferred" in decision_text:
                list_item["decision"] = 'TRANSFERRED'

            if "presiding panelist" in decision_text:
                list_item["type"] = 'MULTIPLE'
            elif "sole panelist" in decision_text:
                list_item["type"] = 'SINGLE'

        m = re.findall('b\.\s*respondent.*?6\.\s*discussion', contents, re.M)
        if len(m):
            respondent_text = m[0]
            print(respondent_text)
            if "did not reply" in respondent_text:
                list_item["responded"] = False
            elif "did not respond" in respondent_text:
                list_item["responded"] = False
            elif "not submitted a response" in respondent_text:
                list_item["responded"] = False
            else:
                list_item["responded"] = True

        list.append(list_item)

        print(list_item)

with open("results.csv", 'w') as file:
    file.write("filename")
    file.write(",")
    file.write("decision")
    file.write(",")
    file.write("type")
    file.write(",")
    file.write("responded")
    file.write("\n")
    for item in list:
        file.write(item["filename"])
        file.write(",")
        file.write(item["decision"])
        file.write(",")
        file.write(item["type"])
        file.write(",")
        file.write(str(item["responded"]))
        file.write("\n")
