# coding=utf-8
##########################################################################
#
#  Copyright 2013 Lee Smith
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
# 
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
# 
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##########################################################################

import urllib2
import urlparse
import re
from datetime import date
import time

from xbmcswift2 import Plugin
from bs4 import BeautifulSoup

BASE_URL = "http://visibleearth.nasa.gov"

SCHEME_RE = re.compile("view_cat.php\?scheme=([A-Z]+)")
THUMB_RE = re.compile("view.php\?id=([0-9]+)")
CAT_RE = re.compile("view_cat.php\?categoryID=([0-9]+)")
IMG_RE = re.compile("\.(jpg|tiff?|png)$", re.IGNORECASE)

plugin = Plugin()

def get_soup(url):
    html = urllib2.urlopen(url).read()
    # script.module.html5lib is a requirement
    # so html5lib will automatically be used instead of HTMLParser.
    return BeautifulSoup(html)


def get_schemes():
    soup = get_soup(BASE_URL)

    for scheme_link in soup.find('div', id='nav').find_all('a', href=SCHEME_RE):
        scheme = SCHEME_RE.search(scheme_link['href']).group(1)
        item = {'label': scheme_link.string,
                'path': plugin.url_for('browse_by',
                                       scheme=scheme)
                }
        yield item

def get_subcategories(scheme):
    url = urlparse.urljoin(BASE_URL, "view_cat.php?scheme={}".format(scheme))
    soup = get_soup(url)

    for sub_link in soup.find('div', id='subs').find_all('a'):
        label = sub_link.string + sub_link.next_sibling
        m = CAT_RE.match(sub_link['href'])
        if m:
            item = {'label': label,
                    'path': plugin.url_for('select_item',
                                           cat_id=m.group(1),
                                           page='1')
                    }
            yield item

def get_items(cat_id, page=1):
    page = int(page)
    url = urlparse.urljoin(BASE_URL, "view_cat.php?categoryID={}&p={}".format(cat_id, page))
    soup = get_soup(url)
    
    if page > 1:
        previous_page = str(page - 1)
        item = {'label': "<< Page {} <<".format(previous_page),
                'path': plugin.url_for('select_item', cat_id=cat_id, page=previous_page)
        }
        yield item  
    
    if soup.find('a', text='»'):
        next_page = str(page + 1)
        item = {'label': ">> Page {} >>".format(next_page),
                'path': plugin.url_for('select_item', cat_id=cat_id, page=next_page)
        }
        yield item

    for link in soup('a', href=THUMB_RE):
        if link.img is not None:
            item = {'label': link.img['alt'],
                    'path': plugin.url_for('select_image_file',
                                           img_id=THUMB_RE.match(link['href']).group(1)),
                    'thumbnail':link.img['src']
                    }
            yield item

def get_image_files(img_id):
    url = urlparse.urljoin(BASE_URL, "view.php?id={}".format(img_id))
    soup = get_soup(url)

    title = soup.find('div', id='title').h2.string 
    
    vis_date_str = soup.find('h4', text="Visualization Date:").string.next.strip()
    vis_date = date(*(time.strptime(vis_date_str, "%B %d, %Y")[0:3]))
    
    div = soup.find('div', id='visuals')
    
    for col0, col1 in zip(div.find_all('div', id='col00'), div.find_all('div', id='col01')):
        link = col0.find('a')
        if link:
            href = link['href']
            if IMG_RE.search(href):
                ul = link.parent.ul
                if ul:
                    desc = ul.string.strip()
                    label_info = " ".join(line.string for line in col1('li')
                                      if line.string is not None)
                    label = "{} ({})".format(desc, label_info)
                else:
                    label = link.string
                
                resp = urllib2.urlopen(href)
                size = int(resp.headers.getheader('Content-Length'))
                
                item = {'label': label,
                        'path': href,
                        'info':{'title': title,
                                'date': vis_date.strftime("%d.%m.%Y"),
                                'size': size
                                },
                        'is_playable': True}
                yield item

def get_search_results(query):
    url = urlparse.urljoin(BASE_URL, "search.php?q={}".format(query))
    soup = get_soup(url)
    for result in soup('table', 'gsc-table-result'):
        href = result.find('div', 'gs-visibleUrl').string
        item = {'label': result,
                'path': href
                }
        yield item


@plugin.route('/')
def index():
    return [{'label': 'Search', 'path': plugin.url_for('search')},
            {'label': 'Browse', 'path': plugin.url_for('browse')}
            ]

@plugin.route('/search')
def search():
    query = plugin.keyboard(heading="Search")
    if query:
        url = plugin.url_for('do_search', query=query)
        plugin.redirect(url)

@plugin.route('/search/query/<query>')
def do_search(query):
    return list(get_search_results(query))

@plugin.route('/browse')
def browse():
    return list(get_schemes())

@plugin.route('/scheme/<scheme>')
def browse_by(scheme):
    return list(get_subcategories(scheme))

@plugin.route('/img_id/<img_id>')
def select_image_file(img_id):
    items = list(get_image_files(img_id))

    return plugin.finish(items, sort_methods=['unsorted', 'size'])

@plugin.route('/cat_id/<cat_id>/page/<page>')
def select_item(cat_id, page):
    items = list(get_items(cat_id, page))

    return plugin.finish(items, update_listing=True)

if __name__ == '__main__':
    plugin.run()
