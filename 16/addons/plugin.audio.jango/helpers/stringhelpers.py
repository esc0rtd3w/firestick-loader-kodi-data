'''
Created on 22 jan 2012

@author: Batch
'''

import os

def batch_replace(s, replace_info):
    for r in replace_info:
        s = str(s).replace(r[0], r[1])
    return s

def get_items_in_dir(path):
    items = []
    for dirpath, dirnames, filenames in os.walk(path): 
        for subdirname in dirnames: 
            items.append(subdirname) 
        for filename in filenames:
            items.append(filename)
            #if filename.endswith(".strm"): 
            #    items.append(filename[:-5])
        
    return items


def string_to_list(s):
    r = []
    s = 'r = ' + s
    exec(s)
    return r

def clean_file_name(s, use_encoding=False, use_blanks=True):
    hex_entities = [['&#x26;', '&'], ['&#x27;', '\''], ['&#xC6;', 'AE'], ['&#xC7;', 'C'],
                ['&#xF4;', 'o'], ['&#xE9;', 'e'], ['&#xEB;', 'e'], ['&#xED;', 'i'],
                ['&#xEE;', 'i'], ['&#xA2;', 'c'], ['&#xE2;', 'a'], ['&#xEF;', 'i'],
                ['&#xE1;', 'a'], ['&#xE8;', 'e'], ['%2E', '.'], ['&frac12;', '%BD'],
                ['&#xBD;', '%BD'], ['&#xB3;', '%B3'], ['&#xB0;', '%B0'], ['&amp;', '&'], ['&#xB7;', '.'], ['&#xE4;', 'A']]
    
    special_encoded = [['"', '%22'], ['*', '%2A'], ['/', '%2F'], [':', ','], ['<', '%3C'],
                        ['>', '%3E'], ['?', '%3F'], ['\\', '%5C'], ['|', '%7C']]
    
    special_blanks = [['"', ' '], ['*', ' '], ['/', ' '], [':', ' '], ['<', ' '],
                        ['>', ' '], ['?', ' '], ['\\', ' '], ['|', ' '], ['%BD;', ' '],
                        ['%B3;', ' '], ['%B0;', ' ']]
    
    s = batch_replace(s, hex_entities)
    if use_encoding:
        s = batch_replace(s, special_encoded)
    if use_blanks:
        s = batch_replace(s, special_blanks)
    s = s.strip()
    
    return s
