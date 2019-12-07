# -*- coding: utf-8 -*-

'''
#:::'##::::'#######:::'######::'##::::::::'#######::'##:::::'##:'##::: ##::'######::
#:'####:::'##.... ##:'##... ##: ##:::::::'##.... ##: ##:'##: ##: ###:: ##:'##... ##:
#:.. ##:::..::::: ##: ##:::..:: ##::::::: ##:::: ##: ##: ##: ##: ####: ##: ##:::..::
#::: ##::::'#######:: ##::::::: ##::::::: ##:::: ##: ##: ##: ##: ## ## ##:. ######::
#::: ##::::...... ##: ##::::::: ##::::::: ##:::: ##: ##: ##: ##: ##. ####::..... ##:
#::: ##:::'##:::: ##: ##::: ##: ##::::::: ##:::: ##: ##: ##: ##: ##:. ###:'##::: ##:
#:'######:. #######::. ######:: ########:. #######::. ###. ###:: ##::. ##:. ######::
#:......:::.......::::......:::........:::.......::::...::...:::..::::..:::......:::

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

from resources.lib.modules import trakt
from resources.lib.modules import cleangenre
from resources.lib.modules import cleantitle
from resources.lib.modules import control
from resources.lib.modules import client
from resources.lib.modules import cache
from resources.lib.modules import metacache
from resources.lib.modules import playcount
from resources.lib.modules import workers
from resources.lib.modules import views
from resources.lib.modules import utils
from resources.lib.indexers import navigator

import os,sys,re,json,urllib,urlparse,datetime,base64

params = dict(urlparse.parse_qsl(sys.argv[2].replace('?',''))) if len(sys.argv) > 1 else dict()

action = params.get('action')

#control.moderator()


class collections:
    def __init__(self):
        self.list = []

        self.tmdb_link = 'https://api.themoviedb.org'
        self.trakt_link = 'https://api.trakt.tv'
        self.imdb_link = 'https://www.imdb.com'
        self.tmdb_key = control.setting('tm.user')
        if self.tmdb_key == '' or self.tmdb_key == None:
            self.tmdb_key = base64.b64decode('MDA0OTc5NWVkYjU3NTY4Yjk1MjQwYmM5ZTYxYTlkZmM=')
        self.datetime = (datetime.datetime.utcnow() - datetime.timedelta(hours = 5))
        self.systime = (self.datetime).strftime('%Y%m%d%H%M%S%f')
        self.trakt_user = control.setting('trakt.user').strip()
        self.lang = control.apiLanguage()['trakt']
        self.imdb_user = control.setting('imdb.user').replace('ur', '')
        self.tmdb_lang = 'en'
        self.today_date = (self.datetime).strftime('%Y-%m-%d')
        self.month_date = (self.datetime - datetime.timedelta(days = 30)).strftime('%Y-%m-%d')
        self.year_date = (self.datetime - datetime.timedelta(days = 365)).strftime('%Y-%m-%d')
        self.tmdb_info_link = 'https://api.themoviedb.org/3/movie/%s?api_key=%s&language=%s&append_to_response=credits,releases,external_ids' % ('%s', self.tmdb_key, self.tmdb_lang)
        self.imdb_by_query = 'https://www.omdbapi.com/?t=%s&y=%s'
        self.imdbinfo = 'https://www.omdbapi.com/?i=%s&plot=short&r=json'
        self.tmdb_image = 'https://image.tmdb.org/t/p/original'
        self.tmdb_poster = 'https://image.tmdb.org/t/p/w500'
        self.tm_user = control.setting('tm.user')
        self.fanart_tv_user = control.setting('fanart.tv.user')
        self.user = str(control.setting('fanart.tv.user')) + str(control.setting('tm.user'))
        self.lang = control.apiLanguage()['trakt']

        self.search_link = 'https://api.trakt.tv/search/movie?limit=20&page=1&query='
        self.fanart_tv_art_link = 'https://webservice.fanart.tv/v3/movies/%s'
        self.fanart_tv_level_link = 'https://webservice.fanart.tv/v3/level'
        self.tm_art_link = 'https://api.themoviedb.org/3/movie/%s/images?api_key=%s&language=en-US&include_image_language=en,%s,null' % ('%s', self.tm_user, self.lang)
        self.tm_img_link = 'https://image.tmdb.org/t/p/w%s%s'

        self.traktlists_link = 'https://api.trakt.tv/users/me/lists'
        self.traktlikedlists_link = 'https://api.trakt.tv/users/likes/lists?limit=1000000'
        self.traktlist_link = 'https://api.trakt.tv/users/%s/lists/%s/items'
        self.traktcollection_link = 'https://api.trakt.tv/users/me/collection/movies'
        self.traktwatchlist_link = 'https://api.trakt.tv/users/me/watchlist/movies'
        self.traktfeatured_link = 'https://api.trakt.tv/recommendations/movies?limit=40'
        self.trakthistory_link = 'https://api.trakt.tv/users/me/history/movies?limit=40&page=1'
        self.imdblists_link = 'https://www.imdb.com/user/ur%s/lists?tab=all&sort=modified:desc&filter=titles' % self.imdb_user
        self.imdblist_link = 'https://www.imdb.com/list/%s/?view=detail&sort=title:asc&title_type=feature,short,tv_movie,tv_special,video,documentary,game&start=1'
        self.imdblist2_link = 'https://www.imdb.com/list/%s/?view=detail&sort=created:desc&title_type=feature,short,tv_movie,tv_special,video,documentary,game&start=1'
        self.imdbwatchlist_link = 'https://www.imdb.com/user/ur%s/watchlist?sort=alpha,asc' % self.imdb_user
        self.imdbwatchlist2_link = 'https://www.imdb.com/user/ur%s/watchlist?sort=date_added,desc' % self.imdb_user

# Car Movies
        self.carmovies_link = 'https://api.themoviedb.org/3/list/32790?api_key=%s' % (self.tmdb_key)

# Christmas Movies
        self.xmasmovies_link = 'https://api.themoviedb.org/3/list/32770?api_key=%s' % (self.tmdb_key)

# DC Comics Movies
        self.dcmovies_link = 'https://api.themoviedb.org/3/list/32799?api_key=%s' % (self.tmdb_key)

# Disney Movies
        self.disneymovies_link = 'https://api.themoviedb.org/3/list/32800?api_key=%s' % (self.tmdb_key)

# Kids Movies
        self.kidsmovies_link = 'https://api.themoviedb.org/3/list/32802?api_key=%s' % (self.tmdb_key)

# Marvel Movies
        self.marvelmovies_link = 'https://api.themoviedb.org/3/list/32793?api_key=%s' % (self.tmdb_key)

# Actor Collection
        self.adamsandler_link = 'https://api.themoviedb.org/3/list/32777?api_key=%s' % (self.tmdb_key)
        self.alpacino_link = 'https://api.themoviedb.org/3/list/32815?api_key=%s' % (self.tmdb_key)
        self.alanrickman_link = 'https://api.themoviedb.org/3/list/32819?api_key=%s' % (self.tmdb_key)
        self.anthonyhopkins_link = 'https://api.themoviedb.org/3/list/32820?api_key=%s' % (self.tmdb_key)
        self.angelinajolie_link = 'https://api.themoviedb.org/3/list/32821?api_key=%s' % (self.tmdb_key)
        self.arnoldschwarzenegger_link = 'https://api.themoviedb.org/3/list/32825?api_key=%s' % (self.tmdb_key)
        self.charlizetheron_link = 'https://api.themoviedb.org/3/list/32826?api_key=%s' % (self.tmdb_key)
        self.clinteastwood_link = 'https://api.themoviedb.org/3/list/32827?api_key=%s' % (self.tmdb_key)
        self.demimoore_link = 'https://api.themoviedb.org/3/list/32828?api_key=%s' % (self.tmdb_key)
        self.denzelwashington_link = 'https://api.themoviedb.org/3/list/32829?api_key=%s' % (self.tmdb_key)
        self.eddiemurphy_link = 'https://api.themoviedb.org/3/list/32830?api_key=%s' % (self.tmdb_key)
        self.elvispresley_link = 'https://api.themoviedb.org/3/list/32831?api_key=%s' % (self.tmdb_key)
        self.genewilder_link = 'https://api.themoviedb.org/3/list/32999?api_key=%s' % (self.tmdb_key)
        self.gerardbutler_link = 'https://api.themoviedb.org/3/list/33000?api_key=%s' % (self.tmdb_key)
        self.goldiehawn_link = 'https://api.themoviedb.org/3/list/33023?api_key=%s' % (self.tmdb_key)
        self.jasonstatham_link = 'https://api.themoviedb.org/3/list/33001?api_key=%s' % (self.tmdb_key)
        self.jeanclaudevandamme_link = 'https://api.themoviedb.org/3/list/33002?api_key=%s' % (self.tmdb_key)
        self.jeffreydeanmorgan_link = 'https://api.themoviedb.org/3/list/33003?api_key=%s' % (self.tmdb_key)
        self.johntravolta_link = 'https://api.themoviedb.org/3/list/33004?api_key=%s' % (self.tmdb_key)
        self.johnnydepp_link = 'https://api.themoviedb.org/3/list/33005?api_key=%s' % (self.tmdb_key)
        self.juliaroberts_link = 'https://api.themoviedb.org/3/list/33006?api_key=%s' % (self.tmdb_key)
        self.kevincostner_link = 'https://api.themoviedb.org/3/list/33015?api_key=%s' % (self.tmdb_key)
        self.liamneeson_link = 'https://api.themoviedb.org/3/list/33016?api_key=%s' % (self.tmdb_key)
        self.melgibson_link = 'https://api.themoviedb.org/3/list/33017?api_key=%s' % (self.tmdb_key)
        self.melissamccarthy_link = 'https://api.themoviedb.org/3/list/33020?api_key=%s' % (self.tmdb_key)
        self.merylstreep_link = 'https://api.themoviedb.org/3/list/33021?api_key=%s' % (self.tmdb_key)
        self.michellepfeiffer_link = 'https://api.themoviedb.org/3/list/33022?api_key=%s' % (self.tmdb_key)
        self.nicolascage_link = 'https://api.themoviedb.org/3/list/33024?api_key=%s' % (self.tmdb_key)
        self.nicolekidman_link = 'https://api.themoviedb.org/3/list/33025?api_key=%s' % (self.tmdb_key)
        self.paulnewman_link = 'https://api.themoviedb.org/3/list/33026?api_key=%s' % (self.tmdb_key)
        self.reesewitherspoon_link = 'https://api.themoviedb.org/3/list/33027?api_key=%s' % (self.tmdb_key)
        self.robertdeniro_link = 'https://api.themoviedb.org/3/list/33028?api_key=%s' % (self.tmdb_key)
        self.samueljackson_link = 'https://api.themoviedb.org/3/list/33029?api_key=%s' % (self.tmdb_key)
        self.seanconnery_link = 'https://api.themoviedb.org/3/list/33030?api_key=%s' % (self.tmdb_key)
        self.scarlettjohansson_link = 'https://api.themoviedb.org/3/list/33031?api_key=%s' % (self.tmdb_key)
        self.sharonstone_link = 'https://api.themoviedb.org/3/list/33032?api_key=%s' % (self.tmdb_key)
        self.sigourneyweaver_link = 'https://api.themoviedb.org/3/list/33033?api_key=%s' % (self.tmdb_key)
        self.stevenseagal_link = 'https://api.themoviedb.org/3/list/33035?api_key=%s' % (self.tmdb_key)
        self.tomhanks_link = 'https://api.themoviedb.org/3/list/33036?api_key=%s' % (self.tmdb_key)
        self.vindiesel_link = 'https://api.themoviedb.org/3/list/33037?api_key=%s' % (self.tmdb_key)
        self.wesleysnipes_link = 'https://api.themoviedb.org/3/list/33038?api_key=%s' % (self.tmdb_key)
        self.willsmith_link = 'https://api.themoviedb.org/3/list/33039?api_key=%s' % (self.tmdb_key)
        self.winonaryder_link = 'https://api.themoviedb.org/3/list/33040?api_key=%s' % (self.tmdb_key)

# Boxset Collection
        self.fortyeighthours_link = 'https://api.themoviedb.org/3/list/33259?api_key=%s' % (self.tmdb_key)
        self.aceventura_link = 'https://api.themoviedb.org/3/list/33260?api_key=%s' % (self.tmdb_key)
        self.airplane_link = 'https://api.themoviedb.org/3/list/33261?api_key=%s' % (self.tmdb_key)
        self.airport_link = 'https://api.themoviedb.org/3/list/33262?api_key=%s' % (self.tmdb_key)
        self.americangraffiti_link = 'https://api.themoviedb.org/3/list/33263?api_key=%s' % (self.tmdb_key)
        self.anaconda_link = 'https://api.themoviedb.org/3/list/33264?api_key=%s' % (self.tmdb_key)
        self.analyzethis_link = 'https://api.themoviedb.org/3/list/33265?api_key=%s' % (self.tmdb_key)
        self.anchorman_link = 'https://api.themoviedb.org/3/list/33266?api_key=%s' % (self.tmdb_key)
        self.austinpowers_link = 'https://api.themoviedb.org/3/list/33267?api_key=%s' % (self.tmdb_key)
        self.backtothefuture_link = 'https://api.themoviedb.org/3/list/33268?api_key=%s' % (self.tmdb_key)
        self.badboys_link = 'https://api.themoviedb.org/3/list/33269?api_key=%s' % (self.tmdb_key)
        self.badsanta_link = 'https://api.themoviedb.org/3/list/33270?api_key=%s' % (self.tmdb_key)
        self.basicinstinct_link = 'https://api.themoviedb.org/3/list/33271?api_key=%s' % (self.tmdb_key)
        self.beverlyhillscop_link = 'https://api.themoviedb.org/3/list/33272?api_key=%s' % (self.tmdb_key)
        self.bigmommashouse_link = 'https://api.themoviedb.org/3/list/33273?api_key=%s' % (self.tmdb_key)
        self.bluesbrothers_link = 'https://api.themoviedb.org/3/list/33274?api_key=%s' % (self.tmdb_key)
        self.bourne_link = 'https://api.themoviedb.org/3/list/33275?api_key=%s' % (self.tmdb_key)
        self.brucealmighty_link = 'https://api.themoviedb.org/3/list/33276?api_key=%s' % (self.tmdb_key)
        self.caddyshack_link = 'https://api.themoviedb.org/3/list/33277?api_key=%s' % (self.tmdb_key)
        self.cheaperbythedozen_link = 'https://api.themoviedb.org/3/list/33278?api_key=%s' % (self.tmdb_key)
        self.cheechandchong_link = 'https://api.themoviedb.org/3/list/33420?api_key=%s' % (self.tmdb_key)
        self.childsplay_link = 'https://api.themoviedb.org/3/list/33279?api_key=%s' % (self.tmdb_key)
        self.cityslickers_link = 'https://api.themoviedb.org/3/list/33280?api_key=%s' % (self.tmdb_key)
        self.conan_link = 'https://api.themoviedb.org/3/list/33281?api_key=%s' % (self.tmdb_key)
        self.crank_link = 'https://api.themoviedb.org/3/list/33282?api_key=%s' % (self.tmdb_key)
        self.crocodiledundee_link = 'https://api.themoviedb.org/3/list/33419?api_key=%s' % (self.tmdb_key)
        self.davincicode_link = 'https://api.themoviedb.org/3/list/33283?api_key=%s' % (self.tmdb_key)
        self.daddydaycare_link = 'https://api.themoviedb.org/3/list/33284?api_key=%s' % (self.tmdb_key)
        self.deathwish_link = 'https://api.themoviedb.org/3/list/33285?api_key=%s' % (self.tmdb_key)
        self.deltaforce_link = 'https://api.themoviedb.org/3/list/33286?api_key=%s' % (self.tmdb_key)
        self.diehard_link = 'https://api.themoviedb.org/3/list/33287?api_key=%s' % (self.tmdb_key)
        self.dirtydancing_link = 'https://api.themoviedb.org/3/list/33288?api_key=%s' % (self.tmdb_key)
        self.dirtyharry_link = 'https://api.themoviedb.org/3/list/33289?api_key=%s' % (self.tmdb_key)
        self.dumbanddumber_link = 'https://api.themoviedb.org/3/list/33290?api_key=%s' % (self.tmdb_key)
        self.escapefromnewyork_link = 'https://api.themoviedb.org/3/list/33291?api_key=%s' % (self.tmdb_key)
        self.everywhichwaybutloose_link = 'https://api.themoviedb.org/3/list/33292?api_key=%s' % (self.tmdb_key)
        self.exorcist_link = 'https://api.themoviedb.org/3/list/33293?api_key=%s' % (self.tmdb_key)
        self.theexpendables_link = 'https://api.themoviedb.org/3/list/33294?api_key=%s' % (self.tmdb_key)
        self.fastandthefurious_link = 'https://api.themoviedb.org/3/list/32779?api_key=%s' % (self.tmdb_key)
        self.fatherofthebride_link = 'https://api.themoviedb.org/3/list/33295?api_key=%s' % (self.tmdb_key)
        self.fletch_link = 'https://api.themoviedb.org/3/list/33296?api_key=%s' % (self.tmdb_key)
        self.friday_link = 'https://api.themoviedb.org/3/list/33297?api_key=%s' % (self.tmdb_key)
        self.fridaythe13th_link = 'https://api.themoviedb.org/3/list/33298?api_key=%s' % (self.tmdb_key)
        self.fugitive_link = 'https://api.themoviedb.org/3/list/33299?api_key=%s' % (self.tmdb_key)
        self.gijoe_link = 'https://api.themoviedb.org/3/list/33300?api_key=%s' % (self.tmdb_key)
        self.getshorty_link = 'https://api.themoviedb.org/3/list/33301?api_key=%s' % (self.tmdb_key)
        self.gettysburg_link = 'https://api.themoviedb.org/3/list/33302?api_key=%s' % (self.tmdb_key)
        self.ghostrider_link = 'https://api.themoviedb.org/3/list/33303?api_key=%s' % (self.tmdb_key)
        self.ghostbusters_link = 'https://api.themoviedb.org/3/list/33201?api_key=%s' % (self.tmdb_key)
        self.godsnotdead_link = 'https://api.themoviedb.org/3/list/33304?api_key=%s' % (self.tmdb_key)
        self.godfather_link = 'https://api.themoviedb.org/3/list/33305?api_key=%s' % (self.tmdb_key)
        self.godzilla_link = 'https://api.themoviedb.org/3/list/33306?api_key=%s' % (self.tmdb_key)
        self.grownups_link = 'https://api.themoviedb.org/3/list/33307?api_key=%s' % (self.tmdb_key)
        self.grumpyoldmen_link = 'https://api.themoviedb.org/3/list/33308?api_key=%s' % (self.tmdb_key)
        self.gunsofnavarone_link = 'https://api.themoviedb.org/3/list/33309?api_key=%s' % (self.tmdb_key)
        self.halloween_link = 'https://api.themoviedb.org/3/list/33310?api_key=%s' % (self.tmdb_key)
        self.hangover_link = 'https://api.themoviedb.org/3/list/33311?api_key=%s' % (self.tmdb_key)
        self.hanniballector_link = 'https://api.themoviedb.org/3/list/33312?api_key=%s' % (self.tmdb_key)
        self.hellraiser_link = 'https://api.themoviedb.org/3/list/33313?api_key=%s' % (self.tmdb_key)
        self.honeyishrunkthekids_link = 'https://api.themoviedb.org/3/list/33208?api_key=%s' % (self.tmdb_key)
        self.horriblebosses_link = 'https://api.themoviedb.org/3/list/33314?api_key=%s' % (self.tmdb_key)
        self.hostel_link = 'https://api.themoviedb.org/3/list/33315?api_key=%s' % (self.tmdb_key)
        self.hotshots_link = 'https://api.themoviedb.org/3/list/33316?api_key=%s' % (self.tmdb_key)
        self.independenceday_link = 'https://api.themoviedb.org/3/list/33317?api_key=%s' % (self.tmdb_key)
        self.indianajones_link = 'https://api.themoviedb.org/3/list/33318?api_key=%s' % (self.tmdb_key)
        self.insidious_link = 'https://api.themoviedb.org/3/list/33319?api_key=%s' % (self.tmdb_key)
        self.ironeagle_link = 'https://api.themoviedb.org/3/list/33320?api_key=%s' % (self.tmdb_key)
        self.jackreacher_link = 'https://api.themoviedb.org/3/list/33321?api_key=%s' % (self.tmdb_key)
        self.jackryan_link = 'https://api.themoviedb.org/3/list/33322?api_key=%s' % (self.tmdb_key)
        self.jackass_link = 'https://api.themoviedb.org/3/list/33323?api_key=%s' % (self.tmdb_key)
        self.jamesbond_link = 'https://api.themoviedb.org/3/list/33324?api_key=%s' % (self.tmdb_key)
        self.jaws_link = 'https://api.themoviedb.org/3/list/33325?api_key=%s' % (self.tmdb_key)
        self.jeeperscreepers_link = 'https://api.themoviedb.org/3/list/33326?api_key=%s' % (self.tmdb_key)
        self.johnwick_link = 'https://api.themoviedb.org/3/list/33327?api_key=%s' % (self.tmdb_key)
        self.jumanji_link = 'https://api.themoviedb.org/3/list/33328?api_key=%s' % (self.tmdb_key)
        self.jurassicpark_link = 'https://api.themoviedb.org/3/list/33217?api_key=%s' % (self.tmdb_key)
        self.kickass_link = 'https://api.themoviedb.org/3/list/33329?api_key=%s' % (self.tmdb_key)
        self.killbill_link = 'https://api.themoviedb.org/3/list/33330?api_key=%s' % (self.tmdb_key)
        self.kingkong_link = 'https://api.themoviedb.org/3/list/33331?api_key=%s' % (self.tmdb_key)
        self.laracroft_link = 'https://api.themoviedb.org/3/list/33332?api_key=%s' % (self.tmdb_key)
        self.legallyblonde_link = 'https://api.themoviedb.org/3/list/33333?api_key=%s' % (self.tmdb_key)
        self.lethalweapon_link = 'https://api.themoviedb.org/3/list/33334?api_key=%s' % (self.tmdb_key)
        self.lookwhostalking_link = 'https://api.themoviedb.org/3/list/33335?api_key=%s' % (self.tmdb_key)
        self.machete_link = 'https://api.themoviedb.org/3/list/33336?api_key=%s' % (self.tmdb_key)
        self.magicmike_link = 'https://api.themoviedb.org/3/list/33337?api_key=%s' % (self.tmdb_key)
        self.majorleague_link = 'https://api.themoviedb.org/3/list/33338?api_key=%s' % (self.tmdb_key)
        self.manfromsnowyriver_link = 'https://api.themoviedb.org/3/list/33339?api_key=%s' % (self.tmdb_key)
        self.mask_link = 'https://api.themoviedb.org/3/list/33340?api_key=%s' % (self.tmdb_key)
        self.matrix_link = 'https://api.themoviedb.org/3/list/33341?api_key=%s' % (self.tmdb_key)
        self.themechanic_link = 'https://api.themoviedb.org/3/list/33342?api_key=%s' % (self.tmdb_key)
        self.meettheparents_link = 'https://api.themoviedb.org/3/list/33343?api_key=%s' % (self.tmdb_key)
        self.meninblack_link = 'https://api.themoviedb.org/3/list/33344?api_key=%s' % (self.tmdb_key)
        self.mightyducks_link = 'https://api.themoviedb.org/3/list/33345?api_key=%s' % (self.tmdb_key)
        self.misscongeniality_link = 'https://api.themoviedb.org/3/list/33346?api_key=%s' % (self.tmdb_key)
        self.missinginaction_link = 'https://api.themoviedb.org/3/list/33347?api_key=%s' % (self.tmdb_key)
        self.missionimpossible_link = 'https://api.themoviedb.org/3/list/33348?api_key=%s' % (self.tmdb_key)
        self.nakedgun_link = 'https://api.themoviedb.org/3/list/33349?api_key=%s' % (self.tmdb_key)
        self.nationallampoon_link = 'https://api.themoviedb.org/3/list/33350?api_key=%s' % (self.tmdb_key)
        self.nationallampoonsvacation_link = 'https://api.themoviedb.org/3/list/33351?api_key=%s' % (self.tmdb_key)
        self.nationaltreasure_link = 'https://api.themoviedb.org/3/list/33352?api_key=%s' % (self.tmdb_key)
        self.neighbors_link = 'https://api.themoviedb.org/3/list/33353?api_key=%s' % (self.tmdb_key)
        self.nightatthemuseum_link = 'https://api.themoviedb.org/3/list/33354?api_key=%s' % (self.tmdb_key)
        self.nightmareonelmstreet_link = 'https://api.themoviedb.org/3/list/33355?api_key=%s' % (self.tmdb_key)
        self.nowyouseeme_link = 'https://api.themoviedb.org/3/list/33356?api_key=%s' % (self.tmdb_key)
        self.nuttyprofessor_link = 'https://api.themoviedb.org/3/list/33357?api_key=%s' % (self.tmdb_key)
        self.oceanseleven_link = 'https://api.themoviedb.org/3/list/33358?api_key=%s' % (self.tmdb_key)
        self.oddcouple_link = 'https://api.themoviedb.org/3/list/33359?api_key=%s' % (self.tmdb_key)
        self.ohgod_link = 'https://api.themoviedb.org/3/list/33360?api_key=%s' % (self.tmdb_key)
        self.olympushasfallen_link = 'https://api.themoviedb.org/3/list/33361?api_key=%s' % (self.tmdb_key)
        self.omen_link = 'https://api.themoviedb.org/3/list/33362?api_key=%s' % (self.tmdb_key)
        self.paulblartmallcop_link = 'https://api.themoviedb.org/3/list/33363?api_key=%s' % (self.tmdb_key)
        self.piratesofthecaribbean_link = 'https://api.themoviedb.org/3/list/33364?api_key=%s' % (self.tmdb_key)
        self.planetoftheapes_link = 'https://api.themoviedb.org/3/list/33365?api_key=%s' % (self.tmdb_key)
        self.policeacademy_link = 'https://api.themoviedb.org/3/list/33366?api_key=%s' % (self.tmdb_key)
        self.poltergeist_link = 'https://api.themoviedb.org/3/list/33367?api_key=%s' % (self.tmdb_key)
        self.porkys_link = 'https://api.themoviedb.org/3/list/33368?api_key=%s' % (self.tmdb_key)
        self.predator_link = 'https://api.themoviedb.org/3/list/33369?api_key=%s' % (self.tmdb_key)
        self.thepurge_link = 'https://api.themoviedb.org/3/list/33370?api_key=%s' % (self.tmdb_key)
        self.rambo_link = 'https://api.themoviedb.org/3/list/33371?api_key=%s' % (self.tmdb_key)
        self.red_link = 'https://api.themoviedb.org/3/list/33372?api_key=%s' % (self.tmdb_key)
        self.revengeofthenerds_link = 'https://api.themoviedb.org/3/list/33373?api_key=%s' % (self.tmdb_key)
        self.riddick_link = 'https://api.themoviedb.org/3/list/33374?api_key=%s' % (self.tmdb_key)
        self.ridealong_link = 'https://api.themoviedb.org/3/list/33375?api_key=%s' % (self.tmdb_key)
        self.thering_link = 'https://api.themoviedb.org/3/list/33418?api_key=%s' % (self.tmdb_key)
        self.robocop_link = 'https://api.themoviedb.org/3/list/33376?api_key=%s' % (self.tmdb_key)
        self.rocky_link = 'https://api.themoviedb.org/3/list/33377?api_key=%s' % (self.tmdb_key)
        self.romancingthestone_link = 'https://api.themoviedb.org/3/list/33378?api_key=%s' % (self.tmdb_key)
        self.rushhour_link = 'https://api.themoviedb.org/3/list/33379?api_key=%s' % (self.tmdb_key)
        self.santaclause_link = 'https://api.themoviedb.org/3/list/33380?api_key=%s' % (self.tmdb_key)
        self.saw_link = 'https://api.themoviedb.org/3/list/33381?api_key=%s' % (self.tmdb_key)
        self.sexandthecity_link = 'https://api.themoviedb.org/3/list/33382?api_key=%s' % (self.tmdb_key)
        self.shaft_link = 'https://api.themoviedb.org/3/list/33383?api_key=%s' % (self.tmdb_key)
        self.shanghainoon_link = 'https://api.themoviedb.org/3/list/33384?api_key=%s' % (self.tmdb_key)
        self.sincity_link = 'https://api.themoviedb.org/3/list/33385?api_key=%s' % (self.tmdb_key)
        self.sinister_link = 'https://api.themoviedb.org/3/list/33386?api_key=%s' % (self.tmdb_key)
        self.sisteract_link = 'https://api.themoviedb.org/3/list/33387?api_key=%s' % (self.tmdb_key)
        self.smokeyandthebandit_link = 'https://api.themoviedb.org/3/list/33388?api_key=%s' % (self.tmdb_key)
        self.speed_link = 'https://api.themoviedb.org/3/list/33389?api_key=%s' % (self.tmdb_key)
        self.stakeout_link = 'https://api.themoviedb.org/3/list/33390?api_key=%s' % (self.tmdb_key)
        self.startrek_link = 'https://api.themoviedb.org/3/list/33391?api_key=%s' % (self.tmdb_key)
        self.starwars_link = 'https://api.themoviedb.org/3/list/33237?api_key=%s' % (self.tmdb_key)
        self.thesting_link = 'https://api.themoviedb.org/3/list/33392?api_key=%s' % (self.tmdb_key)
        self.taken_link = 'https://api.themoviedb.org/3/list/33393?api_key=%s' % (self.tmdb_key)
        self.taxi_link = 'https://api.themoviedb.org/3/list/33394?api_key=%s' % (self.tmdb_key)
        self.ted_link = 'https://api.themoviedb.org/3/list/33395?api_key=%s' % (self.tmdb_key)
        self.teenwolf_link = 'https://api.themoviedb.org/3/list/33396?api_key=%s' % (self.tmdb_key)
        self.terminator_link = 'https://api.themoviedb.org/3/list/33397?api_key=%s' % (self.tmdb_key)
        self.termsofendearment_link = 'https://api.themoviedb.org/3/list/33398?api_key=%s' % (self.tmdb_key)
        self.texaschainsawmassacre_link = 'https://api.themoviedb.org/3/list/33399?api_key=%s' % (self.tmdb_key)
        self.thething_link = 'https://api.themoviedb.org/3/list/33400?api_key=%s' % (self.tmdb_key)
        self.thomascrownaffair_link = 'https://api.themoviedb.org/3/list/33401?api_key=%s' % (self.tmdb_key)
        self.transporter_link = 'https://api.themoviedb.org/3/list/33402?api_key=%s' % (self.tmdb_key)
        self.undersiege_link = 'https://api.themoviedb.org/3/list/33403?api_key=%s' % (self.tmdb_key)
        self.universalsoldier_link = 'https://api.themoviedb.org/3/list/33404?api_key=%s' % (self.tmdb_key)
        self.wallstreet_link = 'https://api.themoviedb.org/3/list/33405?api_key=%s' % (self.tmdb_key)
        self.waynesworld_link = 'https://api.themoviedb.org/3/list/33406?api_key=%s' % (self.tmdb_key)
        self.weekendatbernies_link = 'https://api.themoviedb.org/3/list/33407?api_key=%s' % (self.tmdb_key)
        self.wholenineyards_link = 'https://api.themoviedb.org/3/list/33408?api_key=%s' % (self.tmdb_key)
        self.xfiles_link = 'https://api.themoviedb.org/3/list/33409?api_key=%s' % (self.tmdb_key)
        self.xxx_link = 'https://api.themoviedb.org/3/list/33410?api_key=%s' % (self.tmdb_key)
        self.youngguns_link = 'https://api.themoviedb.org/3/list/33411?api_key=%s' % (self.tmdb_key)
        self.zoolander_link = 'https://api.themoviedb.org/3/list/33412?api_key=%s' % (self.tmdb_key)
        self.zorro_link = 'https://api.themoviedb.org/3/list/33413?api_key=%s' % (self.tmdb_key)

# Boxset Collection Kids
        self.onehundredonedalmations_link = 'https://api.themoviedb.org/3/list/33182?api_key=%s' % (self.tmdb_key)
        self.addamsfamily_link = 'https://api.themoviedb.org/3/list/33183?api_key=%s' % (self.tmdb_key)
        self.aladdin_link = 'https://api.themoviedb.org/3/list/33184?api_key=%s' % (self.tmdb_key)
        self.alvinandthechipmunks_link = 'https://api.themoviedb.org/3/list/33185?api_key=%s' % (self.tmdb_key)
        self.atlantis_link = 'https://api.themoviedb.org/3/list/33186?api_key=%s' % (self.tmdb_key)
        self.babe_link = 'https://api.themoviedb.org/3/list/33187?api_key=%s' % (self.tmdb_key)
        self.balto_link = 'https://api.themoviedb.org/3/list/33188?api_key=%s' % (self.tmdb_key)
        self.bambi_link = 'https://api.themoviedb.org/3/list/33189?api_key=%s' % (self.tmdb_key)
        self.beautyandthebeast_link = 'https://api.themoviedb.org/3/list/33190?api_key=%s' % (self.tmdb_key)
        self.beethoven_link = 'https://api.themoviedb.org/3/list/33191?api_key=%s' % (self.tmdb_key)
        self.brotherbear_link = 'https://api.themoviedb.org/3/list/33192?api_key=%s' % (self.tmdb_key)
        self.cars_link = 'https://api.themoviedb.org/3/list/33193?api_key=%s' % (self.tmdb_key)
        self.cinderella_link = 'https://api.themoviedb.org/3/list/33194?api_key=%s' % (self.tmdb_key)
        self.cloudywithachanceofmeatballs_link = 'https://api.themoviedb.org/3/list/33195?api_key=%s' % (self.tmdb_key)
        self.despicableme_link = 'https://api.themoviedb.org/3/list/33197?api_key=%s' % (self.tmdb_key)
        self.findingnemo_link = 'https://api.themoviedb.org/3/list/33198?api_key=%s' % (self.tmdb_key)
        self.foxandthehound_link = 'https://api.themoviedb.org/3/list/33199?api_key=%s' % (self.tmdb_key)
        self.freewilly_link = 'https://api.themoviedb.org/3/list/33200?api_key=%s' % (self.tmdb_key)
        self.ghostbusters_link = 'https://api.themoviedb.org/3/list/33201?api_key=%s' % (self.tmdb_key)
        self.gremlins_link = 'https://api.themoviedb.org/3/list/33202?api_key=%s' % (self.tmdb_key)
        self.happyfeet_link = 'https://api.themoviedb.org/3/list/33204?api_key=%s' % (self.tmdb_key)
        self.harrypotter_link = 'https://api.themoviedb.org/3/list/33205?api_key=%s' % (self.tmdb_key)
        self.homealone_link = 'https://api.themoviedb.org/3/list/33206?api_key=%s' % (self.tmdb_key)
        self.homewardbound_link = 'https://api.themoviedb.org/3/list/33207?api_key=%s' % (self.tmdb_key)
        self.honeyishrunkthekids_link = 'https://api.themoviedb.org/3/list/33208?api_key=%s' % (self.tmdb_key)
        self.hoteltransylvania_link = 'https://api.themoviedb.org/3/list/33209?api_key=%s' % (self.tmdb_key)
        self.howtotrainyourdragon_link = 'https://api.themoviedb.org/3/list/33210?api_key=%s' % (self.tmdb_key)
        self.hunchbackofnotredame_link = 'https://api.themoviedb.org/3/list/33211?api_key=%s' % (self.tmdb_key)
        self.iceage_link = 'https://api.themoviedb.org/3/list/33212?api_key=%s' % (self.tmdb_key)
        self.jurassicpark_link = 'https://api.themoviedb.org/3/list/33217?api_key=%s' % (self.tmdb_key)
        self.kungfupanda_link = 'https://api.themoviedb.org/3/list/33218?api_key=%s' % (self.tmdb_key)
        self.ladyandthetramp_link = 'https://api.themoviedb.org/3/list/33219?api_key=%s' % (self.tmdb_key)
        self.liloandstitch_link = 'https://api.themoviedb.org/3/list/33220?api_key=%s' % (self.tmdb_key)
        self.madagascar_link = 'https://api.themoviedb.org/3/list/33221?api_key=%s' % (self.tmdb_key)
        self.monstersinc_link = 'https://api.themoviedb.org/3/list/33222?api_key=%s' % (self.tmdb_key)
        self.mulan_link = 'https://api.themoviedb.org/3/list/33223?api_key=%s' % (self.tmdb_key)
        self.narnia_link = 'https://api.themoviedb.org/3/list/33224?api_key=%s' % (self.tmdb_key)
        self.newgroove_link = 'https://api.themoviedb.org/3/list/33225?api_key=%s' % (self.tmdb_key)
        self.openseason_link = 'https://api.themoviedb.org/3/list/33226?api_key=%s' % (self.tmdb_key)
        self.planes_link = 'https://api.themoviedb.org/3/list/33227?api_key=%s' % (self.tmdb_key)
        self.pocahontas_link = 'https://api.themoviedb.org/3/list/33228?api_key=%s' % (self.tmdb_key)
        self.problemchild_link = 'https://api.themoviedb.org/3/list/33229?api_key=%s' % (self.tmdb_key)
        self.rio_link = 'https://api.themoviedb.org/3/list/33230?api_key=%s' % (self.tmdb_key)
        self.sammysadventures_link = 'https://api.themoviedb.org/3/list/33231?api_key=%s' % (self.tmdb_key)
        self.scoobydoo_link = 'https://api.themoviedb.org/3/list/33232?api_key=%s' % (self.tmdb_key)
        self.shortcircuit_link = 'https://api.themoviedb.org/3/list/33233?api_key=%s' % (self.tmdb_key)
        self.shrek_link = 'https://api.themoviedb.org/3/list/33234?api_key=%s' % (self.tmdb_key)
        self.spongebobsquarepants_link = 'https://api.themoviedb.org/3/list/33235?api_key=%s' % (self.tmdb_key)
        self.spykids_link = 'https://api.themoviedb.org/3/list/33236?api_key=%s' % (self.tmdb_key)
        self.starwars_link = 'https://api.themoviedb.org/3/list/33237?api_key=%s' % (self.tmdb_key)
        self.stuartlittle_link = 'https://api.themoviedb.org/3/list/33238?api_key=%s' % (self.tmdb_key)
        self.tarzan_link = 'https://api.themoviedb.org/3/list/33239?api_key=%s' % (self.tmdb_key)
        self.teenagemutantninjaturtles_link = 'https://api.themoviedb.org/3/list/33240?api_key=%s' % (self.tmdb_key)
        self.thejunglebook_link = 'https://api.themoviedb.org/3/list/33216?api_key=%s' % (self.tmdb_key)
        self.thekaratekid_link = 'https://api.themoviedb.org/3/list/33241?api_key=%s' % (self.tmdb_key)
        self.thelionking_link = 'https://api.themoviedb.org/3/list/33242?api_key=%s' % (self.tmdb_key)
        self.thelittlemermaid_link = 'https://api.themoviedb.org/3/list/33243?api_key=%s' % (self.tmdb_key)
        self.theneverendingstory_link = 'https://api.themoviedb.org/3/list/33248?api_key=%s' % (self.tmdb_key)
        self.thesmurfs_link = 'https://api.themoviedb.org/3/list/33249?api_key=%s' % (self.tmdb_key)
        self.toothfairy_link = 'https://api.themoviedb.org/3/list/33251?api_key=%s' % (self.tmdb_key)
        self.tinkerbell_link = 'https://api.themoviedb.org/3/list/33252?api_key=%s' % (self.tmdb_key)
        self.tomandjerry_link = 'https://api.themoviedb.org/3/list/33253?api_key=%s' % (self.tmdb_key)
        self.toystory_link = 'https://api.themoviedb.org/3/list/33254?api_key=%s' % (self.tmdb_key)
        self.veggietales_link = 'https://api.themoviedb.org/3/list/33255?api_key=%s' % (self.tmdb_key)
        self.winniethepooh_link = 'https://api.themoviedb.org/3/list/33257?api_key=%s' % (self.tmdb_key)
        self.wizardofoz_link = 'https://api.themoviedb.org/3/list/33258?api_key=%s' % (self.tmdb_key)

# Superhero Collection
        self.avengers_link = 'https://api.themoviedb.org/3/list/33128?api_key=%s' % (self.tmdb_key)
        self.batman_link = 'https://api.themoviedb.org/3/list/33129?api_key=%s' % (self.tmdb_key)
        self.captainamerica_link = 'https://api.themoviedb.org/3/list/33130?api_key=%s' % (self.tmdb_key)
        self.darkknight_link = 'https://api.themoviedb.org/3/list/33132?api_key=%s' % (self.tmdb_key)
        self.fantasticfour_link = 'https://api.themoviedb.org/3/list/33133?api_key=%s' % (self.tmdb_key)
        self.hulk_link = 'https://api.themoviedb.org/3/list/33134?api_key=%s' % (self.tmdb_key)
        self.ironman_link = 'https://api.themoviedb.org/3/list/33135?api_key=%s' % (self.tmdb_key)
        self.spiderman_link = 'https://api.themoviedb.org/3/list/33126?api_key=%s' % (self.tmdb_key)
        self.superman_link = 'https://api.themoviedb.org/3/list/33136?api_key=%s' % (self.tmdb_key)
        self.xmen_link = 'https://api.themoviedb.org/3/list/33137?api_key=%s' % (self.tmdb_key)



    def get(self, url, idx=True, create_directory=True):
        try:
            try: url = getattr(self, url + '_link')
            except: pass

            try: u = urlparse.urlparse(url).netloc.lower()
            except: pass

            if u in self.tmdb_link and ('/user/' in url or '/list/' in url):
                self.list = self.tmdb_collections_list(url)
                self.worker()

            elif u in self.tmdb_link and not ('/user/' in url or '/list/' in url):
                self.list = cache.get(self.tmdb_list, 24, url)
                self.worker()

            elif u in self.trakt_link and '/users/' in url:
                try:
                    if url == self.trakthistory_link: raise Exception()
                    if not '/users/me/' in url: raise Exception()
                    if trakt.getActivity() > cache.timeout(self.trakt_list, url, self.trakt_user): raise Exception()
                    self.list = cache.get(self.trakt_list, 720, url, self.trakt_user)
                except:
                    self.list = cache.get(self.trakt_list, 0, url, self.trakt_user)

                if '/users/me/' in url and '/collection/' in url:
                    self.list = sorted(self.list, key=lambda k: utils.title_key(k['title']))

                if idx == True: self.worker()

            elif u in self.trakt_link and self.search_link in url:
                self.list = cache.get(self.trakt_list, 1, url, self.trakt_user)
                if idx == True: self.worker(level=0)

            elif u in self.trakt_link:
                self.list = cache.get(self.trakt_list, 24, url, self.trakt_user)
                if idx == True: self.worker()


            elif u in self.imdb_link and ('/user/' in url or '/list/' in url):
                self.list = cache.get(self.imdb_list, 0, url)
                if idx == True: self.worker()

            elif u in self.imdb_link:
                self.list = cache.get(self.imdb_list, 24, url)
                if idx == True: self.worker()


            if idx == True and create_directory == True: self.movieDirectory(self.list)
            return self.list
        except:
            pass


    def userlists(self):
        try:
            userlists = []
            if trakt.getTraktCredentialsInfo() == False: raise Exception()
            activity = trakt.getActivity()
        except:
            pass

        try:
            if trakt.getTraktCredentialsInfo() == False: raise Exception()
            try:
                if activity > cache.timeout(self.trakt_user_list, self.traktlists_link, self.trakt_user): raise Exception()
                userlists += cache.get(self.trakt_user_list, 720, self.traktlists_link, self.trakt_user)
            except:
                userlists += cache.get(self.trakt_user_list, 0, self.traktlists_link, self.trakt_user)
        except:
            pass
        try:
            self.list = []
            if self.imdb_user == '': raise Exception()
            userlists += cache.get(self.imdb_user_list, 0, self.imdblists_link)
        except:
            pass
        try:
            self.list = []
            if trakt.getTraktCredentialsInfo() == False: raise Exception()
            try:
                if activity > cache.timeout(self.trakt_user_list, self.traktlikedlists_link, self.trakt_user): raise Exception()
                userlists += cache.get(self.trakt_user_list, 720, self.traktlikedlists_link, self.trakt_user)
            except:
                userlists += cache.get(self.trakt_user_list, 0, self.traktlikedlists_link, self.trakt_user)
        except:
            pass

        self.list = userlists
        for i in range(0, len(self.list)): self.list[i].update({'image': 'userlists.png', 'action': 'movies'})
        self.addDirectory(self.list, queue=True)
        return self.list


    def trakt_list(self, url, user):
        try:
            q = dict(urlparse.parse_qsl(urlparse.urlsplit(url).query))
            q.update({'extended': 'full'})
            q = (urllib.urlencode(q)).replace('%2C', ',')
            u = url.replace('?' + urlparse.urlparse(url).query, '') + '?' + q

            result = trakt.getTraktAsJson(u)

            items = []
            for i in result:
                try: items.append(i['movie'])
                except: pass
            if len(items) == 0:
                items = result
        except:
            return

        try:
            q = dict(urlparse.parse_qsl(urlparse.urlsplit(url).query))
            if not int(q['limit']) == len(items): raise Exception()
            q.update({'page': str(int(q['page']) + 1)})
            q = (urllib.urlencode(q)).replace('%2C', ',')
            next = url.replace('?' + urlparse.urlparse(url).query, '') + '?' + q
            next = next.encode('utf-8')
        except:
            next = ''

        for item in items:
            try:
                title = item['title']
                title = client.replaceHTMLCodes(title)

                year = item['year']
                year = re.sub('[^0-9]', '', str(year))

                if int(year) > int((self.datetime).strftime('%Y')): raise Exception()

                imdb = item['ids']['imdb']
                if imdb == None or imdb == '': raise Exception()
                imdb = 'tt' + re.sub('[^0-9]', '', str(imdb))

                tmdb = str(item.get('ids', {}).get('tmdb', 0))

                try: premiered = item['released']
                except: premiered = '0'
                try: premiered = re.compile('(\d{4}-\d{2}-\d{2})').findall(premiered)[0]
                except: premiered = '0'

                try: genre = item['genres']
                except: genre = '0'
                genre = [i.title() for i in genre]
                if genre == []: genre = '0'
                genre = ' / '.join(genre)

                try: duration = str(item['runtime'])
                except: duration = '0'
                if duration == None: duration = '0'

                try: rating = str(item['rating'])
                except: rating = '0'
                if rating == None or rating == '0.0': rating = '0'

                try: votes = str(item['votes'])
                except: votes = '0'
                try: votes = str(format(int(votes),',d'))
                except: pass
                if votes == None: votes = '0'

                try: mpaa = item['certification']
                except: mpaa = '0'
                if mpaa == None: mpaa = '0'

                try: plot = item['overview']
                except: plot = '0'
                if plot == None: plot = '0'
                plot = client.replaceHTMLCodes(plot)

                try: tagline = item['tagline']
                except: tagline = '0'
                if tagline == None: tagline = '0'
                tagline = client.replaceHTMLCodes(tagline)

                self.list.append({'title': title, 'originaltitle': title, 'year': year, 'premiered': premiered, 'genre': genre, 'duration': duration, 'rating': rating, 'votes': votes, 'mpaa': mpaa, 'plot': plot, 'tagline': tagline, 'imdb': imdb, 'tmdb': tmdb, 'tvdb': '0', 'poster': '0', 'next': next})
            except:
                pass

        return self.list


    def trakt_user_list(self, url, user):
        try:
            items = trakt.getTraktAsJson(url)
        except:
            pass

        for item in items:
            try:
                try: name = item['list']['name']
                except: name = item['name']
                name = client.replaceHTMLCodes(name)

                try: url = (trakt.slug(item['list']['user']['username']), item['list']['ids']['slug'])
                except: url = ('me', item['ids']['slug'])
                url = self.traktlist_link % url
                url = url.encode('utf-8')

                self.list.append({'name': name, 'url': url, 'context': url})
            except:
                pass

        self.list = sorted(self.list, key=lambda k: utils.title_key(k['name']))
        return self.list


    def imdb_list(self, url):
        try:
            for i in re.findall('date\[(\d+)\]', url):
                url = url.replace('date[%s]' % i, (self.datetime - datetime.timedelta(days = int(i))).strftime('%Y-%m-%d'))

            def imdb_watchlist_id(url):
                return client.parseDOM(client.request(url), 'meta', ret='content', attrs = {'property': 'pageId'})[0]

            if url == self.imdbwatchlist_link:
                url = cache.get(imdb_watchlist_id, 8640, url)
                url = self.imdblist_link % url

            elif url == self.imdbwatchlist2_link:
                url = cache.get(imdb_watchlist_id, 8640, url)
                url = self.imdblist2_link % url

            result = client.request(url)

            result = result.replace('\n', ' ')

            items = client.parseDOM(result, 'div', attrs = {'class': 'lister-item mode-advanced'})
            items += client.parseDOM(result, 'div', attrs = {'class': 'list_item.+?'})
        except:
            return

        try:
            next = client.parseDOM(result, 'a', ret='href', attrs = {'class': 'lister-page-next.+?'})

            if len(next) == 0:
                next = client.parseDOM(result, 'div', attrs = {'class': 'pagination'})[0]
                next = zip(client.parseDOM(next, 'a', ret='href'), client.parseDOM(next, 'a'))
                next = [i[0] for i in next if 'Next' in i[1]]

            next = url.replace(urlparse.urlparse(url).query, urlparse.urlparse(next[0]).query)
            next = client.replaceHTMLCodes(next)
            next = next.encode('utf-8')
        except:
            next = ''

        for item in items:
            try:
                title = client.parseDOM(item, 'a')[1]
                title = client.replaceHTMLCodes(title)
                title = title.encode('utf-8')

                year = client.parseDOM(item, 'span', attrs = {'class': 'lister-item-year.+?'})
                year += client.parseDOM(item, 'span', attrs = {'class': 'year_type'})
                try: year = re.compile('(\d{4})').findall(year)[0]
                except: year = '0'
                year = year.encode('utf-8')

                if int(year) > int((self.datetime).strftime('%Y')): raise Exception()

                imdb = client.parseDOM(item, 'a', ret='href')[0]
                imdb = re.findall('(tt\d*)', imdb)[0]
                imdb = imdb.encode('utf-8')

                try: poster = client.parseDOM(item, 'img', ret='loadlate')[0]
                except: poster = '0'
                if '/nopicture/' in poster: poster = '0'
                poster = re.sub('(?:_SX|_SY|_UX|_UY|_CR|_AL)(?:\d+|_).+?\.', '_SX500.', poster)
                poster = client.replaceHTMLCodes(poster)
                poster = poster.encode('utf-8')

                try: genre = client.parseDOM(item, 'span', attrs = {'class': 'genre'})[0]
                except: genre = '0'
                genre = ' / '.join([i.strip() for i in genre.split(',')])
                if genre == '': genre = '0'
                genre = client.replaceHTMLCodes(genre)
                genre = genre.encode('utf-8')

                try: duration = re.findall('(\d+?) min(?:s|)', item)[-1]
                except: duration = '0'
                duration = duration.encode('utf-8')

                rating = '0'
                try: rating = client.parseDOM(item, 'span', attrs = {'class': 'rating-rating'})[0]
                except: pass
                try: rating = client.parseDOM(rating, 'span', attrs = {'class': 'value'})[0]
                except: rating = '0'
                try: rating = client.parseDOM(item, 'div', ret='data-value', attrs = {'class': '.*?imdb-rating'})[0]
                except: pass
                if rating == '' or rating == '-': rating = '0'
                rating = client.replaceHTMLCodes(rating)
                rating = rating.encode('utf-8')

                try: votes = client.parseDOM(item, 'div', ret='title', attrs = {'class': '.*?rating-list'})[0]
                except: votes = '0'
                try: votes = re.findall('\((.+?) vote(?:s|)\)', votes)[0]
                except: votes = '0'
                if votes == '': votes = '0'
                votes = client.replaceHTMLCodes(votes)
                votes = votes.encode('utf-8')

                try: mpaa = client.parseDOM(item, 'span', attrs = {'class': 'certificate'})[0]
                except: mpaa = '0'
                if mpaa == '' or mpaa == 'NOT_RATED': mpaa = '0'
                mpaa = mpaa.replace('_', '-')
                mpaa = client.replaceHTMLCodes(mpaa)
                mpaa = mpaa.encode('utf-8')

                try: director = re.findall('Director(?:s|):(.+?)(?:\||</div>)', item)[0]
                except: director = '0'
                director = client.parseDOM(director, 'a')
                director = ' / '.join(director)
                if director == '': director = '0'
                director = client.replaceHTMLCodes(director)
                director = director.encode('utf-8')

                try: cast = re.findall('Stars(?:s|):(.+?)(?:\||</div>)', item)[0]
                except: cast = '0'
                cast = client.replaceHTMLCodes(cast)
                cast = cast.encode('utf-8')
                cast = client.parseDOM(cast, 'a')
                if cast == []: cast = '0'

                plot = '0'
                try: plot = client.parseDOM(item, 'p', attrs = {'class': 'text-muted'})[0]
                except: pass
                try: plot = client.parseDOM(item, 'div', attrs = {'class': 'item_description'})[0]
                except: pass
                plot = plot.rsplit('<span>', 1)[0].strip()
                plot = re.sub('<.+?>|</.+?>', '', plot)
                if plot == '': plot = '0'
                plot = client.replaceHTMLCodes(plot)
                plot = plot.encode('utf-8')

                self.list.append({'title': title, 'originaltitle': title, 'year': year, 'genre': genre, 'duration': duration, 'rating': rating, 'votes': votes, 'mpaa': mpaa, 'director': director, 'cast': cast, 'plot': plot, 'tagline': '0', 'imdb': imdb, 'tmdb': '0', 'tvdb': '0', 'poster': poster, 'next': next})
            except:
                pass

        return self.list


    def imdb_person_list(self, url):
        try:
            result = client.request(url)
            items = client.parseDOM(result, 'tr', attrs = {'class': '.+? detailed'})
        except:
            return

        for item in items:
            try:
                name = client.parseDOM(item, 'a', ret='title')[0]
                name = client.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                url = client.parseDOM(item, 'a', ret='href')[0]
                url = re.findall('(nm\d*)', url, re.I)[0]
                url = self.person_link % url
                url = client.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                image = client.parseDOM(item, 'img', ret='src')[0]
                if not ('._SX' in image or '._SY' in image): raise Exception()
                image = re.sub('(?:_SX|_SY|_UX|_UY|_CR|_AL)(?:\d+|_).+?\.', '_SX500.', image)
                image = client.replaceHTMLCodes(image)
                image = image.encode('utf-8')

                self.list.append({'name': name, 'url': url, 'image': image})
            except:
                pass

        return self.list


    def imdb_user_list(self, url):
        try:
            result = client.request(url)
            items = client.parseDOM(result, 'div', attrs = {'class': 'list_name'})
        except:
            pass

        for item in items:
            try:
                name = client.parseDOM(item, 'a')[0]
                name = client.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                url = client.parseDOM(item, 'a', ret='href')[0]
                url = url.split('/list/', 1)[-1].replace('/', '')
                url = self.imdblist_link % url
                url = client.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                self.list.append({'name': name, 'url': url, 'context': url})
            except:
                pass

        self.list = sorted(self.list, key=lambda k: utils.title_key(k['name']))
        return self.list


    def tmdb_list(self, url):
        next = url
        for i in re.findall('date\[(\d+)\]', url):
            url = url.replace('date[%s]' % i, (self.datetime - datetime.timedelta(days = int(i))).strftime('%Y-%m-%d'))
        try:
            result = client.request(url % self.tmdb_key)
            result = json.loads(result)
            items = result['results']
        except:
            return
        try:
            page = int(result['page'])
            total = int(result['total_pages'])
            if page >= total: raise Exception()
            url2 = '%s&page=%s' % (url.split('&page=', 1)[0], str(page+1))
            result = client.request(url2 % self.tmdb_key)
            result = json.loads(result)
            items += result['results']
        except:
            pass
        try:
            page = int(result['page'])
            total = int(result['total_pages'])
            if page >= total: raise Exception()
            if not 'page=' in url: raise Exception()
            next = '%s&page=%s' % (next.split('&page=', 1)[0], str(page+1))
            next = next.encode('utf-8')
        except:
            next = ''
        for item in items:
            try:
                title = item['title']
                title = item['title']
                title = client.replaceHTMLCodes(title)
                title = title.encode('utf-8')
                year = item['release_date']
                year = re.compile('(\d{4})').findall(year)[-1]
                year = year.encode('utf-8')
                tmdb = item['id']
                tmdb = re.sub('[^0-9]', '', str(tmdb))
                tmdb = tmdb.encode('utf-8')
                poster = item['poster_path']
                if poster == '' or poster == None:
                    raise Exception()
                else:
                    poster = '%s%s' % (self.tmdb_poster, poster)
                poster = poster.encode('utf-8')
                fanart = item['backdrop_path']
                if fanart == '' or fanart == None: fanart = '0'
                if not fanart == '0': fanart = '%s%s' % (self.tmdb_image, fanart)
                fanart = fanart.encode('utf-8')
                premiered = item['release_date']
                try   : premiered = re.compile('(\d{4}-\d{2}-\d{2})').findall(premiered)[0]
                except: premiered = '0'
                premiered = premiered.encode('utf-8')
                rating = str(item['vote_average'])
                if rating == '' or rating == None: rating = '0'
                rating = rating.encode('utf-8')
                votes = str(item['vote_count'])
                try   : votes = str(format(int(votes),',d'))
                except: pass
                if votes == '' or votes == None: votes = '0'
                votes = votes.encode('utf-8')
                plot = item['overview']
                if plot == '' or plot == None: plot = '0'
                plot = client.replaceHTMLCodes(plot)
                plot = plot.encode('utf-8')
                tagline = re.compile('[.!?][\s]{1,2}(?=[A-Z])').split(plot)[0]
                try   : tagline = tagline.encode('utf-8')
                except: pass
                self.list.append({'title': title, 'originaltitle': title, 'year': year, 'premiered': premiered, 'studio': '0', 'genre': '0', 'duration': '0', 'rating': rating, 'votes': votes, 'mpaa': '0', 'director': '0', 'writer': '0', 'cast': '0', 'plot': plot, 'tagline': tagline, 'code': '0', 'imdb': '0', 'tmdb': tmdb, 'tvdb': '0', 'poster': poster, 'banner': '0', 'fanart': fanart, 'next': next})
            except:
                pass
        return self.list


    def tmdb_collections_list(self, url):
        try:
            result = client.request(url)
            result = json.loads(result)
            items = result['items']
        except:
            return
        next = ''
        for item in items:
            try:
                title = item['title']
                title = item['title']
                title = client.replaceHTMLCodes(title)
                title = title.encode('utf-8')
                year = item['release_date']
                year = re.compile('(\d{4})').findall(year)[-1]
                year = year.encode('utf-8')
                tmdb = item['id']
                tmdb = re.sub('[^0-9]', '', str(tmdb))
                tmdb = tmdb.encode('utf-8')
                poster = item['poster_path']
                if poster == '' or poster == None: raise Exception()
                else: poster = '%s%s' % (self.tmdb_poster, poster)
                poster = poster.encode('utf-8')
                fanart = item['backdrop_path']
                if fanart == '' or fanart == None: fanart = '0'
                if not fanart == '0': fanart = '%s%s' % (self.tmdb_image, fanart)
                fanart = fanart.encode('utf-8')
                premiered = item['release_date']
                try: premiered = re.compile('(\d{4}-\d{2}-\d{2})').findall(premiered)[0]
                except: premiered = '0'
                premiered = premiered.encode('utf-8')
                rating = str(item['vote_average'])
                if rating == '' or rating == None: rating = '0'
                rating = rating.encode('utf-8')
                votes = str(item['vote_count'])
                try: votes = str(format(int(votes),',d'))
                except: pass
                if votes == '' or votes == None: votes = '0'
                votes = votes.encode('utf-8')
                plot = item['overview']
                if plot == '' or plot == None: plot = '0'
                plot = client.replaceHTMLCodes(plot)
                plot = plot.encode('utf-8')
                tagline = re.compile('[.!?][\s]{1,2}(?=[A-Z])').split(plot)[0]
                try: tagline = tagline.encode('utf-8')
                except: pass
                self.list.append({'title': title, 'originaltitle': title, 'year': year, 'premiered': premiered, 'studio': '0', 'genre': '0', 'duration': '0', 'rating': rating, 'votes': votes, 'mpaa': '0', 'director': '0', 'writer': '0', 'cast': '0', 'plot': plot, 'tagline': tagline, 'code': '0', 'imdb': '0', 'tmdb': tmdb, 'tvdb': '0', 'poster': poster, 'banner': '0', 'fanart': fanart, 'next': next})
            except:
                pass
        return self.list


#     def worker(self, level=1):
#         self.meta = []
#         total = len(self.list)
# 
#         self.fanart_tv_headers = {'api-key': 'MDA4M2JmZDMyZjNkOTE4NzZkYzYyNTU2YjQ1MTY0MWU='.decode('base64')}
#         if not self.fanart_tv_user == '':
#             self.fanart_tv_headers.update({'client-key': self.fanart_tv_user})
# 
#         for i in range(0, total): self.list[i].update({'metacache': False})
# 
#         self.list = metacache.fetch(self.list, self.lang, self.user)
# 
#         for r in range(0, total, 40):
#             threads = []
#             for i in range(r, r+40):
#                 if i <= total: threads.append(workers.Thread(self.super_info, i))
#             [i.start() for i in threads]
#             [i.join() for i in threads]
# 
#             if self.meta: metacache.insert(self.meta)
# 
#         self.list = [i for i in self.list if not i['imdb'] == '0']
# 
#         self.list = metacache.local(self.list, self.tm_img_link, 'poster3', 'fanart2')
# 
#         if self.fanart_tv_user == '':
#             for i in self.list: i.update({'clearlogo': '0', 'clearart': '0'})


    def worker(self, level=1):
        self.meta = []
        total = len(self.list)

        self.fanart_tv_headers = {'api-key': 'MDA4M2JmZDMyZjNkOTE4NzZkYzYyNTU2YjQ1MTY0MWU='.decode('base64')}
        if not self.fanart_tv_user == '':
            self.fanart_tv_headers.update({'client-key': self.fanart_tv_user})

        for i in range(0, total): self.list[i].update({'metacache': False})

        self.list = metacache.fetch(self.list, self.lang, self.user)

        for r in range(0, total, 100):
            threads = []
            for i in range(r, r+100):
                if i <= total: threads.append(workers.Thread(self.super_info, i))
            [i.start() for i in threads]
            [i.join() for i in threads]

            if self.meta: metacache.insert(self.meta)

        self.list = [i for i in self.list]

        self.list = metacache.local(self.list, self.tm_img_link, 'poster3', 'fanart2')

        if self.fanart_tv_user == '':
            for i in self.list: i.update({'clearlogo': '0', 'clearart': '0'})


    def super_info(self, i):
        try:
            if self.list[i]['metacache'] == True: raise Exception()

            try: tmdb = self.list[i]['tmdb']
            except: tmdb = '0'
            if not tmdb == '0': url = self.tmdb_info_link % tmdb
            else: raise Exception()
            item = client.request(url, timeout='10')
            item = json.loads(item)
            title = item['title']
            if not title == '0': self.list[i].update({'title': title})
            year = item['release_date']

            try: year = re.compile('(\d{4})').findall(year)[0]
            except: year = '0'
            if year == '' or year == None: year = '0'
            year = year.encode('utf-8')
            if not year == '0': self.list[i].update({'year': year})
            tmdb = item['id']
            if tmdb == '' or tmdb == None: tmdb = '0'
            tmdb = re.sub('[^0-9]', '', str(tmdb))
            tmdb = tmdb.encode('utf-8')
            if not tmdb == '0': self.list[i].update({'tmdb': tmdb})
            imdb = item['imdb_id']
            if imdb == '' or imdb == None: imdb = '0'
            imdb = imdb.encode('utf-8')
            if not imdb == '0' and "tt" in imdb: self.list[i].update({'imdb': imdb, 'code': imdb})
            poster = item['poster_path']
            if poster == '' or poster == None: poster = '0'
            if not poster == '0': poster = '%s%s' % (self.tmdb_poster, poster)
            poster = poster.encode('utf-8')
            if not poster == '0': self.list[i].update({'poster': poster})
            fanart = item['backdrop_path']
            if fanart == '' or fanart == None: fanart = '0'
            if not fanart == '0': fanart = '%s%s' % (self.tmdb_image, fanart)
            fanart = fanart.encode('utf-8')
            if not fanart == '0' and self.list[i]['fanart'] == '0': self.list[i].update({'fanart': fanart})
            premiered = item['release_date']

            try: premiered = re.compile('(\d{4}-\d{2}-\d{2})').findall(premiered)[0]
            except: premiered = '0'
            if premiered == '' or premiered == None: premiered = '0'
            premiered = premiered.encode('utf-8')
            if not premiered == '0': self.list[i].update({'premiered': premiered})
            studio = item['production_companies']

            try: studio = [x['name'] for x in studio][0]
            except: studio = '0'
            if studio == '' or studio == None: studio = '0'
            studio = studio.encode('utf-8')
            if not studio == '0': self.list[i].update({'studio': studio})
            genre = item['genres']

            try: genre = [x['name'] for x in genre]
            except: genre = '0'
            if genre == '' or genre == None or genre == []: genre = '0'
            genre = ' / '.join(genre)
            genre = genre.encode('utf-8')
            if not genre == '0': self.list[i].update({'genre': genre})

            try: duration = str(item['runtime'])
            except: duration = '0'
            if duration == '' or duration == None: duration = '0'
            duration = duration.encode('utf-8')
            if not duration == '0': self.list[i].update({'duration': duration})
            rating = str(item['vote_average'])
            if rating == '' or rating == None: rating = '0'
            rating = rating.encode('utf-8')
            if not rating == '0': self.list[i].update({'rating': rating})
            votes = str(item['vote_count'])

            try: votes = str(format(int(votes),',d'))
            except: pass
            if votes == '' or votes == None: votes = '0'
            votes = votes.encode('utf-8')
            if not votes == '0': self.list[i].update({'votes': votes})
            mpaa = item['releases']['countries']

            try: mpaa = [x for x in mpaa if not x['certification'] == '']
            except: mpaa = '0'

            try: mpaa = ([x for x in mpaa if x['iso_3166_1'].encode('utf-8') == 'US'] + [x for x in mpaa if not x['iso_3166_1'].encode('utf-8') == 'US'])[0]['certification']
            except: mpaa = '0'
            mpaa = mpaa.encode('utf-8')
            if not mpaa == '0': self.list[i].update({'mpaa': mpaa})
            director = item['credits']['crew']

            try: director = [x['name'] for x in director if x['job'].encode('utf-8') == 'Director']
            except: director = '0'
            if director == '' or director == None or director == []: director = '0'
            director = ' / '.join(director)
            director = director.encode('utf-8')
            if not director == '0': self.list[i].update({'director': director})
            writer = item['credits']['crew']

            try: writer = [x['name'] for x in writer if x['job'].encode('utf-8') in ['Writer', 'Screenplay']]
            except: writer = '0'

            try: writer = [x for n,x in enumerate(writer) if x not in writer[:n]]
            except: writer = '0'
            if writer == '' or writer == None or writer == []: writer = '0'
            writer = ' / '.join(writer)
            writer = writer.encode('utf-8')
            if not writer == '0': self.list[i].update({'writer': writer})
            cast = item['credits']['cast']

            try: cast = [(x['name'].encode('utf-8'), x['character'].encode('utf-8')) for x in cast]
            except: cast = []
            if len(cast) > 0: self.list[i].update({'cast': cast})
            plot = item['overview']
            if plot == '' or plot == None: plot = '0'
            plot = plot.encode('utf-8')
            if not plot == '0': self.list[i].update({'plot': plot})
            tagline = item['tagline']
            if (tagline == '' or tagline == None) and not plot == '0': tagline = re.compile('[.!?][\s]{1,2}(?=[A-Z])').split(plot)[0]
            elif tagline == '' or tagline == None: tagline = '0'

            try: tagline = tagline.encode('utf-8')
            except: pass
            if not tagline == '0': self.list[i].update({'tagline': tagline})

            try:
                if not imdb == None or imdb == '0':
                    url = self.imdbinfo % imdb
                    item = client.request(url, timeout='10')
                    item = json.loads(item)
                    plot2 = item['Plot']
                    if plot2 == '' or plot2 == None: plot = plot
                    plot = plot.encode('utf-8')
                    if not plot == '0': self.list[i].update({'plot': plot})
                    rating2 = str(item['imdbRating'])
                    if rating2 == '' or rating2 == None: rating = rating2
                    rating = rating.encode('utf-8')
                    if not rating == '0': self.list[i].update({'rating': rating})
                    votes2 = str(item['imdbVotes'])

                    try: votes2 = str(votes2)
                    except: pass
                    if votes2 == '' or votes2 == None: votes = votes2
                    votes = votes.encode('utf-8')
                    if not votes == '0': self.list[i].update({'votes': votes2})
            except:
                pass

            self.meta.append({'tmdb': tmdb, 'imdb': imdb, 'tmdb': tmdb, 'tvdb': '0', 'lang': self.tmdb_lang, 'item': {'title': title, 'year': year, 'code': imdb, 'imdb': imdb, 'tmdb': tmdb, 'poster': poster, 'fanart': fanart, 'premiered': premiered, 'studio': studio, 'genre': genre, 'duration': duration, 'rating': rating, 'votes': votes, 'mpaa': mpaa, 'director': director, 'writer': writer, 'cast': cast, 'plot': plot, 'tagline': tagline}})
        except:
            pass


    def movieDirectory(self, items):
        if items == None or len(items) == 0: control.idle() ; sys.exit()

        sysaddon = sys.argv[0]

        syshandle = int(sys.argv[1])

        addonPoster, addonBanner = control.addonPoster(), control.addonBanner()

        addonFanart, settingFanart = control.addonFanart(), control.setting('fanart')

        traktCredentials = trakt.getTraktCredentialsInfo()

        try: isOld = False ; control.item().getArt('type')
        except: isOld = True

        isPlayable = 'true' if not 'plugin' in control.infoLabel('Container.PluginName') else 'false'

        indicators = playcount.getMovieIndicators(refresh=True) if action == 'movies' else playcount.getMovieIndicators()

        playbackMenu = control.lang(32063).encode('utf-8') if control.setting('hosts.mode') == '2' else control.lang(32064).encode('utf-8')

        watchedMenu = control.lang(32068).encode('utf-8') if trakt.getTraktIndicatorsInfo() == True else control.lang(32066).encode('utf-8')

        unwatchedMenu = control.lang(32069).encode('utf-8') if trakt.getTraktIndicatorsInfo() == True else control.lang(32067).encode('utf-8')

        queueMenu = control.lang(32065).encode('utf-8')

        traktManagerMenu = control.lang(32070).encode('utf-8')

        nextMenu = control.lang(32053).encode('utf-8')

        movieToLibraryMenu = control.lang(32211).encode('utf-8')

        for i in items:
            try:
                label = '%s (%s)' % (i['title'], i['year'])
                imdb, tmdb, title, year = i['imdb'], i['tmdb'], i['originaltitle'], i['year']
                sysname = urllib.quote_plus('%s (%s)' % (title, year))
                systitle = urllib.quote_plus(title)

                meta = dict((k,v) for k, v in i.iteritems() if not v == '0')
                meta.update({'code': imdb, 'imdbnumber': imdb, 'imdb_id': imdb})
                meta.update({'tmdb_id': tmdb})
                meta.update({'mediatype': 'movie'})
                meta.update({'trailer': '%s?action=trailer&name=%s' % (sysaddon, urllib.quote_plus(label))})
                #meta.update({'trailer': 'plugin://script.extendedinfo/?info=playtrailer&&id=%s' % imdb})
                if not 'duration' in i: meta.update({'duration': '120'})
                elif i['duration'] == '0': meta.update({'duration': '120'})
                try: meta.update({'duration': str(int(meta['duration']) * 60)})
                except: pass
                try: meta.update({'genre': cleangenre.lang(meta['genre'], self.lang)})
                except: pass

                poster = [i[x] for x in ['poster3', 'poster', 'poster2'] if i.get(x, '0') != '0']
                poster = poster[0] if poster else addonPoster
                meta.update({'poster': poster})

                sysmeta = urllib.quote_plus(json.dumps(meta))

                url = '%s?action=play&title=%s&year=%s&imdb=%s&meta=%s&t=%s' % (sysaddon, systitle, year, imdb, sysmeta, self.systime)
                sysurl = urllib.quote_plus(url)

                path = '%s?action=play&title=%s&year=%s&imdb=%s' % (sysaddon, systitle, year, imdb)


                cm = []

                cm.append((queueMenu, 'RunPlugin(%s?action=queueItem)' % sysaddon))

                try:
                    overlay = int(playcount.getMovieOverlay(indicators, imdb))
                    if overlay == 7:
                        cm.append((unwatchedMenu, 'RunPlugin(%s?action=moviePlaycount&imdb=%s&query=6)' % (sysaddon, imdb)))
                        meta.update({'playcount': 1, 'overlay': 7})
                    else:
                        cm.append((watchedMenu, 'RunPlugin(%s?action=moviePlaycount&imdb=%s&query=7)' % (sysaddon, imdb)))
                        meta.update({'playcount': 0, 'overlay': 6})
                except:
                    pass

                if traktCredentials == True:
                    cm.append((traktManagerMenu, 'RunPlugin(%s?action=traktManager&name=%s&imdb=%s&content=movie)' % (sysaddon, sysname, imdb)))

                cm.append((playbackMenu, 'RunPlugin(%s?action=alterSources&url=%s&meta=%s)' % (sysaddon, sysurl, sysmeta)))

                if isOld == True:
                    cm.append((control.lang2(19033).encode('utf-8'), 'Action(Info)'))

                cm.append((movieToLibraryMenu, 'RunPlugin(%s?action=movieToLibrary&name=%s&title=%s&year=%s&imdb=%s&content=movie)' % (sysaddon, sysname, systitle, year, imdb)))

                item = control.item(label=label)

                art = {}
                art.update({'icon': poster, 'thumb': poster, 'poster': poster})

                if 'banner' in i and not i['banner'] == '0':
                    art.update({'banner': i['banner']})
                else:
                    art.update({'banner': addonBanner})

                if 'clearlogo' in i and not i['clearlogo'] == '0':
                    art.update({'clearlogo': i['clearlogo']})

                if 'clearart' in i and not i['clearart'] == '0':
                    art.update({'clearart': i['clearart']})


                if settingFanart == 'true' and 'fanart2' in i and not i['fanart2'] == '0':
                    item.setProperty('Fanart_Image', i['fanart2'])
                elif settingFanart == 'true' and 'fanart' in i and not i['fanart'] == '0':
                    item.setProperty('Fanart_Image', i['fanart'])
                elif not addonFanart == None:
                    item.setProperty('Fanart_Image', addonFanart)

                item.setArt(art)
                item.addContextMenuItems(cm)
                item.setProperty('IsPlayable', isPlayable)
                item.setInfo(type='Video', infoLabels = meta)

                video_streaminfo = {'codec': 'h264'}
                item.addStreamInfo('video', video_streaminfo)

                control.addItem(handle=syshandle, url=url, listitem=item, isFolder=False)
            except:
                pass

        try:
            url = items[0]['next']
            if url == '': raise Exception()

            icon = control.addonNext()
            url = '%s?action=moviePage&url=%s' % (sysaddon, urllib.quote_plus(url))

            item = control.item(label=nextMenu)

            item.setArt({'icon': icon, 'thumb': icon, 'poster': icon, 'banner': icon})
            if not addonFanart == None: item.setProperty('Fanart_Image', addonFanart)

            control.addItem(handle=syshandle, url=url, listitem=item, isFolder=True)
        except:
            pass

        control.content(syshandle, 'movies')
        control.directory(syshandle, cacheToDisc=True)
        views.setView('movies', {'skin.estuary': 55, 'skin.confluence': 500})


    def addDirectory(self, items, queue=False):
        if items == None or len(items) == 0: control.idle() ; sys.exit()

        sysaddon = sys.argv[0]

        syshandle = int(sys.argv[1])

        addonFanart, addonThumb, artPath = control.addonFanart(), control.addonThumb(), control.artPath()

        queueMenu = control.lang(32065).encode('utf-8')

        playRandom = control.lang(32535).encode('utf-8')

        for i in items:
            try:
                name = i['name']

                if i['image'].startswith('http'): thumb = i['image']
                elif not artPath == None: thumb = os.path.join(artPath, i['image'])
                else: thumb = addonThumb

                url = '%s?action=%s' % (sysaddon, i['action'])
                try: url += '&url=%s' % urllib.quote_plus(i['url'])
                except: pass

                cm = []

                cm.append((playRandom, 'RunPlugin(%s?action=random&rtype=movie&url=%s)' % (sysaddon, urllib.quote_plus(i['url']))))

                if queue == True:
                    cm.append((queueMenu, 'RunPlugin(%s?action=queueItem)' % sysaddon))

                item = control.item(label=name)

                item.setArt({'icon': thumb, 'thumb': thumb})
                if not addonFanart == None: item.setProperty('Fanart_Image', addonFanart)

                item.addContextMenuItems(cm)

                control.addItem(handle=syshandle, url=url, listitem=item, isFolder=True)
            except:
                pass

        control.content(syshandle, 'addons')
        control.directory(syshandle, cacheToDisc=True)
