# -*- coding: utf-8 -*-
import json
import codecs

'''
for i in range(1,23,1):
    # just open the file...
    input_file  = open("C://json_files/"+str(i)+".json", "r")
    # need to use codecs for output to avoid error in json.dump
    output_file = codecs.open("C://json_files/conv_"+str(i)+".json", "w", encoding="utf-8")

    # read the file and decode possible UTF-8 signature at the beginning
    # which can be the case in some files.
    j = json.loads(input_file.read())

    new_dict = {}
    for item in j["artists"]:
        name = item.pop('artist')
        new_dict[name] = item

    # then output it, indenting, sorting keys and ensuring representation as it was originally
    json.dump(new_dict, output_file, indent=4, sort_keys=True, ensure_ascii=False)
'''

final_dict = {}

for i in range(1,23,1):
    print (i)
    input_file = open("C://json_files/conv_"+str(i)+".json", "r")
    temp_dict = json.loads(input_file.read())
    final_dict.update(temp_dict)

final_file = codecs.open("C://json_files/art_db.json", "w", encoding="utf-8")
json.dump(final_dict, final_file,ensure_ascii=False)

final_file.close()
