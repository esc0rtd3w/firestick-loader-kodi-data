"""
Exports Issues from a specified repository to a CSV file
Uses basic authentication (Github username + password) to retrieve Issues
from a repository that username has access to. Supports Github API v3.
"""
import csv
import xbmc
import os
import requests
import kodi

def run(REPO, STATE):
    ISSUES_FOR_REPO_URL = 'http://api.github.com/repos/%s/issues?state=%s' % (REPO, STATE)

    def write_issues(response):
        "output a list of issues to csv"
        if not r.status_code == 200:
            raise Exception(r.status_code)
        for issue in r.json():
            username = issue.get("user", {}).get('login', {})
            if issue['labels']:
                labels = issue['labels']
                for label in labels:
                    #if label['name'] == "Client Requested":
                    csvout.writerow(['\n<item>\n<id>'+str(issue['number'])+'</id>\n<username>'+username+'</username>\n<label>'+label['name']+'</label>\n<title>'+issue['title'].encode('utf-8')+'</title>\n<body>'+issue['body'].encode('utf-8')+'</body>\n<created>'+issue['created_at']+'</created>\n</item>\n'])
            else:
                csvout.writerow(['\n<item>\n<id>'+str(issue['number'])+'</id>\n<username>'+username+'</username>\n<label>No Label</label>\n<title>'+issue['title'].encode('utf-8')+'</title>\n<body>'+issue['body'].encode('utf-8')+'</body>\n<created>'+issue['created_at']+'</created>\n</item>\n'])

    r = requests.get(ISSUES_FOR_REPO_URL, verify=False)
    csvfile = xbmc.translatePath(os.path.join(kodi.datafolder, '%s-issues-%s.csv' % (kodi.get_id(),STATE)))
    csvout = csv.writer(open(csvfile, 'wb'))
    write_issues(r)

    #more pages? examine the 'link' header returned
    if 'link' in r.headers:
        pages = dict(
            [(rel[6:-1], url[url.index('<')+1:-1]) for url, rel in
                [link.split(';') for link in
                    r.headers['link'].split(',')]])
        while 'last' in pages and 'next' in pages:
            r = requests.get(pages['next'])
            write_issues(r)
            if pages['next'] == pages['last']:
                break