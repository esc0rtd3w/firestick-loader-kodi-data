# -*- coding: utf-8 -*-

'''
    Neptune Rising Add-on
    Copyright (C) 2016 Mr. Blamo

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

import os,sys,re,json,urllib,urlparse,datetime

params = dict(urlparse.parse_qsl(sys.argv[2].replace('?',''))) if len(sys.argv) > 1 else dict()

action = params.get('action')


class movies:
    def __init__(self):
        self.list = []

        self.imdb_link = 'http://www.imdb.com'
        self.trakt_link = 'http://api.trakt.tv'
        self.datetime = (datetime.datetime.utcnow() - datetime.timedelta(hours = 5))
        self.systime = (self.datetime).strftime('%Y%m%d%H%M%S%f')
        self.trakt_user = control.setting('trakt.user').strip()
        self.imdb_user = control.setting('imdb.user').replace('ur', '')
        self.tm_user = control.setting('tm.user')
        self.fanart_tv_user = control.setting('fanart.tv.user')
        self.user = str(control.setting('fanart.tv.user')) + str(control.setting('tm.user'))
        self.lang = control.apiLanguage()['trakt']

        self.search_link = 'http://api.trakt.tv/search/movie?limit=20&page=1&query='
        self.fanart_tv_art_link = 'http://webservice.fanart.tv/v3/movies/%s'
        self.fanart_tv_level_link = 'http://webservice.fanart.tv/v3/level'
        self.tm_art_link = 'http://api.themoviedb.org/3/movie/%s/images?api_key=' + self.tm_user
        self.tm_img_link = 'https://image.tmdb.org/t/p/w%s%s'

        self.persons_link = 'http://www.imdb.com/search/name?count=100&name='
        self.personlist_link = 'http://www.imdb.com/search/name?count=100&gender=male,female'
        self.popular_link = 'http://www.imdb.com/search/title?title_type=feature,tv_movie&num_votes=1000,&production_status=released&groups=top_1000&sort=moviemeter,asc&count=40&start=1'
        self.views_link = 'http://www.imdb.com/search/title?title_type=feature,tv_movie&num_votes=1000,&production_status=released&sort=num_votes,desc&count=40&start=1'
        self.featured_link = 'http://www.imdb.com/search/title?title_type=feature,tv_movie&num_votes=1000,&production_status=released&release_date=date[365],date[60]&sort=moviemeter,asc&count=40&start=1'
        self.person_link = 'http://www.imdb.com/search/title?title_type=feature,tv_movie&production_status=released&role=%s&sort=year,desc&count=40&start=1'
        self.genre_link = 'http://www.imdb.com/search/title?title_type=feature,tv_movie,documentary&num_votes=100,&release_date=,date[0]&genres=%s&sort=moviemeter,asc&count=40&start=1'
        self.keyword_link = 'http://www.imdb.com/search/title?title_type=feature,tv_movie,documentary&num_votes=100,&release_date=,date[0]&keywords=%s&sort=moviemeter,asc&count=40&start=1'
        self.language_link = 'http://www.imdb.com/search/title?title_type=feature,tv_movie&num_votes=100,&production_status=released&primary_language=%s&sort=moviemeter,asc&count=40&start=1'
        self.certification_link = 'http://www.imdb.com/search/title?title_type=feature,tv_movie&num_votes=100,&production_status=released&certificates=us:%s&sort=moviemeter,asc&count=40&start=1'
        self.year_link = 'http://www.imdb.com/search/title?title_type=feature,tv_movie&num_votes=100,&production_status=released&year=%s,%s&sort=moviemeter,asc&count=40&start=1'
        self.boxoffice_link = 'http://www.imdb.com/search/title?title_type=feature,tv_movie&production_status=released&sort=boxoffice_gross_us,desc&count=40&start=1'
        self.oscars_link = 'http://www.imdb.com/search/title?title_type=feature,tv_movie&production_status=released&groups=oscar_best_picture_winners&sort=year,desc&count=40&start=1'
        self.theaters_link = 'http://www.imdb.com/search/title?title_type=feature&num_votes=1000,&release_date=date[365],date[0]&sort=release_date_us,desc&count=40&start=1'
        self.trending_link = 'http://api.trakt.tv/movies/trending?limit=40&page=1'
        self.popular2_link = 'http://api.trakt.tv/movies/popular?limit=40&page=1'
        self.anticipated_link = 'http://api.trakt.tv/movies/anticipated?limit=40&page=1'
        self.boxoffice2_link = 'http://api.trakt.tv/movies/boxoffice?limit=40&page=1'
        self.update_link = 'http://api.trakt.tv/movies/updates/%s?limit=40&page=1'
        self.played1_link = 'http://api.trakt.tv/movies/played/weekly?limit=40&page=1'
        self.played2_link = 'http://api.trakt.tv/movies/played/monthly?limit=40&page=1'
        self.played3_link = 'http://api.trakt.tv/movies/played/yearly?limit=40&page=1'
        self.played4_link = 'http://api.trakt.tv/movies/played/all?limit=40&page=1'
        self.collected1_link = 'http://api.trakt.tv/movies/collected/weekly?limit=40&page=1'
        self.collected2_link = 'http://api.trakt.tv/movies/collected/monthly?limit=40&page=1'
        self.collected3_link = 'http://api.trakt.tv/movies/collected/yearly?limit=40&page=1'
        self.collected4_link = 'http://api.trakt.tv/movies/collected/all?limit=40&page=1'
        self.watched1_link = 'http://api.trakt.tv/movies/watched/weekly?limit=40&page=1'
        self.watched2_link = 'http://api.trakt.tv/movies/watched/monthly?limit=40&page=1'
        self.watched3_link = 'http://api.trakt.tv/movies/watched/yearly?limit=40&page=1'
        self.watched4_link = 'http://api.trakt.tv/movies/watched/all?limit=40&page=1'
        self.genre2_link = 'http://api.trakt.tv/movies/genres/%s?limit=40&page=1'
        self.recommendations_link = 'http://api.trakt.tv/movies/recommendations/%s?limit=40&page=1'
        self.search2_link = 'http://api.trakt.tv/movies/search/%s?limit=40&page=1'


        self.thousand_link = 'http://www.imdb.com/search/title?at=0&count=100&groups=top_1000&release_date=2000,2017&sort=moviemeter,asc&count=40&start=1'
        self.eighties_link = 'http://www.imdb.com/search/title?count=100&keywords%3Fsort=moviemeter,asc&mode=detail&page=1&title_type=movie,tvMovie&release_date=1980,1989&sort=moviemeter,asc&ref_=kw_ref_typ'
        self.docs_link = 'http://www.imdb.com/search/title?count=100&keywords=documentary-subject%27s-name-in-title&mode=detail&page=1&title_type=movie,tvMovie&genres=Documentary&sort=alpha,asc&ref_=kw_ref_typ'
        self.action_link = 'http://www.imdb.com/search/title?count=100&keywords=action-hero&sort=user_rating,desc&mode=detail&page=1&title_type=movie&release_date=2000%2C2017&ref_=kw_ref_yr'
        self.animated_link = 'http://www.imdb.com/search/title?count=100&keywords=2d-animation&sort=alpha,asc&mode=detail&page=1&title_type=movie%2Cvideo&ref_=kw_ref_typ'
        self.gangster_link = 'http://www.imdb.com/search/title?count=100&keywords=gangster&sort=user_rating,desc&mode=detail&page=1&title_type=movie&ref_=kw_ref_typ'
        self.box_link = 'http://www.imdb.com/list/ls057080540/?view=detail&sort=title:asc&title_type=feature,short,tv_movie,tv_special,video,documentary,game&start=1'
        self.horror_link = 'http://www.imdb.com/search/title?count=100&keywords=survival-horror&sort=alpha,asc&mode=detail&page=1&title_type=movie%2CtvMovie&ref_=kw_ref_typ'
        self.action2_link = 'http://www.imdb.com/search/title?count=100&keywords=action-hero&sort=user_rating,desc&mode=detail&page=1&title_type=movie&release_date=1960%2C1999&ref_=kw_ref_yr'
        self.loners_link = 'http://www.imdb.com/search/title?count=100&keywords=loner&sort=moviemeter,asc&mode=detail&page=1&title_type=movie&ref_=kw_ref_typ'
        self.remakes_link = 'http://www.imdb.com/search/title?count=100&keywords=horror-movie-remake&sort=moviemeter,asc&mode=detail&page=1&title_type=movie&ref_=kw_ref_typ'
        self.spike_link = 'http://www.imdb.com/list/ls068076067/?view=detail&sort=title:asc&title_type=feature,short,tv_movie,tv_special,video,documentary,game&start=1'
        self.alfred_link = 'http://www.imdb.com/list/ls068035844/?view=detail&sort=title:asc&title_type=feature,short,tv_movie,tv_special,video,documentary,game&start=1'
        self.clint_link = 'http://www.imdb.com/list/ls064776757/?view=detail&sort=title:asc&title_type=feature,short,tv_movie,tv_special,video,documentary,game&start=1'
        self.steven_link = 'http://www.imdb.com/list/ls064544420/?view=detail&sort=title:asc&title_type=feature,short,tv_movie,tv_special,video,documentary,game&start=1'
        self.james_link = 'http://www.imdb.com/list/ls064538686/?view=detail&sort=title:asc&title_type=feature,short,tv_movie,tv_special,video,documentary,game&start=1'
        self.quentin_link = 'http://www.imdb.com/list/ls064581875/?view=detail&sort=title:asc&title_type=feature,short,tv_movie,tv_special,video,documentary,game&start=1'
        self.mel_link = 'http://www.imdb.com/list/ls021173887/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.ben_link = 'http://www.imdb.com/list/ls064146888/?view=detail&sort=title:asc&title_type=feature,short,tv_movie,tv_special,video,documentary,game&start=1'
        self.martin_link = 'http://www.imdb.com/list/ls064562971/?view=detail&sort=title:asc&title_type=feature,short,tv_movie,tv_special,video,documentary,game&start=1'
        self.bond_link = 'http://www.imdb.com/search/title?count=100&keywords=official-james-bond-series'
        self.horror2_link = 'http://www.imdb.com/search/title?genres=horror&explore=title_type,genres&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=3449260402&pf_rd_r=1XFS1KBK4NWJ9KSAZSCV&pf_rd_s=center-2&pf_rd_t=15051&pf_rd_i=genre&title_type=movie&sort=user_rating,desc&ref_=adv_explore_rhs'
        self.scifi_link = 'http://www.imdb.com/search/title?genres=sci-fi&explore=title_type,genres&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=3449260382&pf_rd_r=0WQQE6JCA3PY3TAYEHS3&pf_rd_s=center-1&pf_rd_t=15051&pf_rd_i=genre&title_type=movie&sort=user_rating,desc&ref_=adv_explore_rhs'
        self.western_link = 'http://www.imdb.com/search/title?count=100&keywords=b-western&sort=user_rating,desc&mode=detail&page=1&title_type=movie&ref_=kw_ref_typ'
        self.cop_link = 'http://www.imdb.com/search/title?count=100&keywords=cop&sort=user_rating,desc&mode=detail&page=1&title_type=movie&ref_=kw_ref_typ'
        self.war_link = 'http://www.imdb.com/search/title?count=100&keywords=war-violence&sort=user_rating,desc&mode=detail&page=1&title_type=movie&ref_=kw_ref_rt_vt'
        self.women_link = 'http://www.imdb.com/list/ls006702639/?view=detail&sort=title:asc&title_type=feature,short,tv_movie,tv_special,video,documentary,game&start=1'
        self.star_link = 'http://www.imdb.com/search/title?count=100&keywords=star-wars&sort=moviemeter,asc&mode=detail&page=1&title_type=movie&ref_=kw_ref_typ'
        self.schiz_link = 'http://www.imdb.com/search/title?count=100&keywords=schizophrenia&sort=moviemeter,asc&mode=detail&page=1&title_type=movie&ref_=kw_ref_typ'
        self.sleeper_link = 'http://www.imdb.com/list/ls072566225/?view=detail&sort=title:asc&title_type=feature,short,tv_movie,tv_special,video,documentary,game&start=1'
        self.chase_link = 'http://www.imdb.com/search/title?count=100&keywords=chase&sort=moviemeter,asc&mode=detail&page=1&title_type=movie&ref_=kw_ref_typ'
        self.political_link = 'http://www.imdb.com/search/title?count=100&keywords=political&sort=user_rating,desc&mode=detail&page=1&ref_=kw_ref_rt_vt'
        self.private_link = 'http://www.imdb.com/search/title?count=100&keywords=private-eye&sort=moviemeter,asc&mode=detail&page=1&title_type=movie&ref_=kw_ref_typ'
        self.true_link = 'http://www.imdb.com/search/title?count=100&keywords=based-on-true-story&sort=moviemeter,asc&mode=detail&page=1&title_type=movie&ref_=kw_ref_typ'
        self.drugs_link = 'http://www.imdb.com/search/title?count=100&keywords=drugs&sort=moviemeter,asc&mode=detail&page=1&title_type=movie&ref_=kw_ref_typ'
        self.racist_link = 'http://www.imdb.com/search/title?count=100&keywords=racism&sort=moviemeter,asc&mode=detail&page=1&title_type=movie&ref_=kw_ref_typ'
        self.char_link = 'http://www.imdb.com/search/title?count=100&keywords=hearing-characters-thoughts'
        self.Existential_link = 'http://www.imdb.com/search/title?count=100&keywords=existential&mode=detail&page=1&title_type=short,movie,tvMovie&sort=alpha,asc&ref_=kw_ref_typ'
        self.romance_link = 'http://www.imdb.com/search/title?count=100&keywords=may-december-romance&sort=user_rating,desc&mode=detail&page=1&title_type=movie&ref_=kw_ref_typ'
        self.dc_link = 'http://www.imdb.com/search/title?count=100&keywords=dc-comics&sort=alpha,asc&mode=detail&page=1&title_type=movie%2CtvMovie&ref_=kw_ref_typ=dc-comics%2Csuperhero&mode=detail&page=1&title_type=video%2Cmovie%2CtvMovie&ref_=kw_ref_typ&sort=alpha,asc'
        self.marvel_link = 'http://www.imdb.com/search/title?count=100&keywords=marvel-comics&mode=detail&page=1&title_type=movie,tvMovie&sort=alpha,asc&ref_=kw_ref_typ'
        self.disney_link = 'http://www.imdb.com/list/ls000013316/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'


		
				###############################################################################################
				###################						Soulless							###################
				###################						  Was								###################
				###################						 Here!								###################
				###############################################################################################
				
        self.cyber_link = 'http://www.imdb.com/search/title?count=100&keywords=cyberpunk&num_votes=3000,&title_type=feature&ref_=gnr_kw_cy,desc&count=40&start=1'
        self.epic_link = 'http://www.imdb.com/search/title?count=100&keywords=epic&num_votes=3000,&title_type=feature&ref_=gnr_kw_ep,desc&count=40&start=1'
        self.espionage_link = 'http://www.imdb.com/search/title?count=100&keywords=espionage&num_votes=3000,&title_type=feature&ref_=gnr_kw_es,desc&count=40&start=1'
        self.fairytale_link = 'http://www.imdb.com/search/title?count=100&keywords=fairy-tale&num_votes=3000,&title_type=feature&ref_=gnr_kw_ft,desc&count=40&start=1'
        self.femme_link = 'http://www.imdb.com/search/title?count=100&keywords=femme-fatale&num_votes=3000,&title_type=feature&ref_=gnr_kw_ff,desc&count=40&start=1'
        self.futuristic_link = 'http://www.imdb.com/search/title?count=100&keywords=futuristic&num_votes=3000,&title_type=feature&ref_=gnr_kw_fu,desc&count=40&start=1'
        self.heist_link = 'http://www.imdb.com/search/title?count=100&keywords=heist&num_votes=3000,&title_type=feature&ref_=gnr_kw_he,desc&count=40&start=1'
        self.highschool_link = 'http://www.imdb.com/search/title?count=100&keywords=high-school&num_votes=3000,&title_type=feature&ref_=gnr_kw_hs,desc&count=40&start=1'
        self.kidnapped_link = 'http://www.imdb.com/search/title?count=100&keywords=kidnapping&num_votes=3000,&title_type=feature&ref_=gnr_kw_ki,desc&count=40&start=1'
        self.kungfu_link = 'http://www.imdb.com/search/title?count=100&keywords=kung-fu&num_votes=3000,&title_type=feature&ref_=gnr_kw_kf,desc&count=40&start=1'
        self.monster_link = 'http://www.imdb.com/search/title?count=100&keywords=monster&num_votes=3000,&title_type=feature&ref_=gnr_kw_mn,desc&count=40&start=1'
        self.parenthood_link = 'http://www.imdb.com/search/title?count=100&keywords=parenthood&num_votes=3000,&title_type=feature&ref_=gnr_kw_ph,desc&count=40&start=1'
        self.apocalypse_link = 'http://www.imdb.com/search/title?count=100&keywords=post-apocalypse&num_votes=3000,&title_type=feature&ref_=gnr_kw_pp,desc&count=40&start=1'
        self.remake_link = 'http://www.imdb.com/search/title?count=100&keywords=remake&num_votes=3000,&title_type=feature&ref_=gnr_kw_re,desc&count=40&start=1'
        self.road_link = 'http://www.imdb.com/search/title?count=100&keywords=road-movie&num_votes=3000,&title_type=feature&ref_=gnr_kw_rm,desc&count=40&start=1'
        self.robot_link = 'http://www.imdb.com/search/title?count=100&keywords=robot&num_votes=3000,&title_type=feature&ref_=gnr_kw_ro,desc&count=40&start=1'
        self.satire_link = 'http://www.imdb.com/search/title?count=100&keywords=satire&num_votes=3000,&title_type=feature&ref_=gnr_kw_sa,desc&count=40&start=1'
        self.serial_link = 'http://www.imdb.com/search/title?count=100&keywords=serial-killer&num_votes=3000,&title_type=feature&ref_=gnr_kw_sk,desc&count=40&start=1'
        self.slasher_link = 'http://www.imdb.com/search/title?count=100&keywords=slasher&num_votes=3000,&title_type=feature&ref_=gnr_kw_sl,desc&count=40&start=1'
        self.spoof_link = 'http://www.imdb.com/search/title?count=100&keywords=spoof&num_votes=3000,&title_type=feature&ref_=gnr_kw_sf,desc&count=40&start=1'
        self.superhero_link = 'http://www.imdb.com/search/title?count=100&keywords=superhero&num_votes=3000,&title_type=feature&ref_=gnr_kw_su,desc&count=40&start=1'
        self.supernatural_link = 'http://www.imdb.com/search/title?count=100&keywords=supernatural&num_votes=3000,&title_type=feature&ref_=gnr_kw_sn,desc&count=40&start=1'
        self.tech_link = 'http://www.imdb.com/search/title?count=100&keywords=tech-noir&num_votes=3000,&title_type=feature&ref_=gnr_kw_tn,desc&count=40&start=1'
        self.time_link = 'http://www.imdb.com/search/title?count=100&keywords=time-travel&num_votes=3000,&title_type=feature&ref_=gnr_kw_tt,desc&count=40&start=1'
        self.zombie_link = 'http://www.imdb.com/search/title?count=100&keywords=zombie&num_votes=3000,&title_type=feature&ref_=gnr_kw_zo,desc&count=40&start=1'
        self.parody_link = 'http://www.imdb.com/search/title?count=100&keywords=parody&num_votes=3000,&title_type=feature&ref_=gnr_kw_pd,desc&count=40&start=1'
        self.vampire_link = 'http://www.imdb.com/search/title?count=100&keywords=vampire&num_votes=3000,&title_type=feature&ref_=gnr_kw_va,desc&count=40&start=1'
        self.biker_link = 'http://www.imdb.com/search/title?count=100&keywords=biker&num_votes=3000,&title_type=feature&ref_=gnr_kw_bi,desc&count=40&start=1'
        self.caper_link = 'http://www.imdb.com/search/title?count=100&keywords=caper&num_votes=3000,&title_type=feature&ref_=gnr_kw_ca,desc&count=40&start=1'
        self.business_link = 'http://www.imdb.com/search/title?count=100&keywords=business&num_votes=3000,&title_type=feature&ref_=gnr_kw_bu,desc&count=40&start=1'
        self.car_link = 'http://www.imdb.com/search/title?count=100&keywords=car-chase&num_votes=3000,&title_type=feature&ref_=gnr_kw_cc,desc&count=40&start=1'
        self.chick_link = 'http://www.imdb.com/search/title?count=100&keywords=chick-flick&num_votes=3000,&title_type=feature&ref_=gnr_kw_cf,desc&count=40&start=1'
        self.spiritual_link = 'http://www.imdb.com/search/title?count=100&keywords=spirituality&num_votes=3000,&title_type=feature&ref_=gnr_kw_st,desc&count=40&start=1'
        self.steampunk_link = 'http://www.imdb.com/search/title?count=100&keywords=steampunk&num_votes=3000,&title_type=feature&ref_=gnr_kw_sk,desc&count=40&start=1'
        self.mock_link = 'http://www.imdb.com/search/title?count=100&keywords=mockumentary&num_votes=3000,&title_type=feature&ref_=gnr_kw_mo,desc&count=40&start=1'
        self.coming_link = 'http://www.imdb.com/search/title?count=100&keywords=coming-of-age&num_votes=3000,&title_type=feature&ref_=gnr_kw_co,desc&count=40&start=1'
        self.competition_link = 'http://www.imdb.com/search/title?count=100&keywords=competition&num_votes=3000,&title_type=feature&ref_=gnr_kw_cp,desc&count=40&start=1'
        self.cult_link = 'http://www.imdb.com/search/title?count=100&keywords=cult&num_votes=3000,&title_type=feature&ref_=gnr_kw_cu,desc&count=40&start=1'
        self.breaking_link = 'http://www.imdb.com/search/title?count=100&keywords=breaking-the-fourth-wall&num_votes=3000,&title_type=feature&ref_=gnr_kw_bw,desc&count=40&start=1'
        self.bmovie_link = 'http://www.imdb.com/search/title?count=100&keywords=b-movie&num_votes=3000,&title_type=feature&ref_=gnr_kw_bm,desc&count=40&start=1'
        self.anime_link = 'http://www.imdb.com/search/title?count=100&genres=animation&keywords=anime&num_votes=1000,&explore=title_type&ref_=gnr_kw_an,desc&count=40&start=1'
        self.neo_link = 'http://www.imdb.com/search/title?count=100&keywords=neo-noir&num_votes=3000,&title_type=feature&ref_=gnr_kw_nn,desc&count=40&start=1'
        self.expiremental_link = 'http://www.imdb.com/search/title?count=100&keywords=experimental-film&num_votes=3000,&title_type=feature&ref_=gnr_kw_ef,desc&count=40&start=1'
        self.farce_link = 'http://www.imdb.com/search/title?count=100&keywords=farce&num_votes=3000,&title_type=feature&ref_=gnr_kw_fa,desc&count=40&start=1'
        self.vr_link = 'http://www.imdb.com/search/title?count=100&keywords=virtual-reality&num_votes=3000,&title_type=feature&ref_=gnr_kw_vr,desc&count=40&start=1'
        self.wilhelm_link = 'http://www.imdb.com/search/title?count=100&keywords=wilhelm-scream&num_votes=2000,&title_type=feature&ref_=gnr_kw_ws,desc&count=40&start=1'
        self.dystopia_link = 'http://www.imdb.com/search/title?count=100&keywords=dystopia&num_votes=3000,&title_type=feature&ref_=gnr_kw_dy,desc&count=40&start=1'
        self.avant_link = 'http://www.imdb.com/search/title?count=100&keywords=avant-garde&num_votes=3000,&title_type=feature&ref_=gnr_kw_ag,desc&count=40&start=1'
        self.newyear_link = 'http://www.imdb.com/search/title?count=100&keywords=new-year&num_votes=3000,&title_type=feature&ref_=gnr_kw_ag,desc&count=40&start=1'
        self.easter_link = 'http://www.imdb.com/search/title?count=100&keywords=easter&num_votes=3000,&title_type=feature&ref_=gnr_kw_ag,desc&count=40&start=1'
        self.halloween_link = 'http://www.imdb.com/search/title?count=100&keywords=halloween&num_votes=3000,&title_type=feature&ref_=gnr_kw_ag,desc&count=40&start=1'
        self.thanx_link = 'http://www.imdb.com/search/title?count=100&keywords=thanksgiving&num_votes=3000,&title_type=feature&ref_=gnr_kw_ag,desc&count=40&start=1'
        self.xmass_link = 'http://www.imdb.com/search/title?count=100&keywords=christmas&num_votes=3000,&title_type=feature&ref_=gnr_kw_ag,desc&count=40&start=1'
#        self._link = 'http://www.imdb.com/search/title?,desc&count=40&start=1'
#        self._link = 'http://www.imdb.com/search/title?,desc&count=40&start=1'
#        self._link = 'http://www.imdb.com/search/title?,desc&count=40&start=1'
#        self._link = 'http://www.imdb.com/search/title?,desc&count=40&start=1'
        self.imdb1_link = 'http://www.imdb.com/list/ls004043006/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb2_link = 'http://www.imdb.com/list/ls054656838/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb3_link = 'http://www.imdb.com/list/ls027849454/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb4_link = 'http://www.imdb.com/list/ls076464829/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb5_link = 'http://www.imdb.com/list/ls009668082/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb6_link = 'http://www.imdb.com/list/ls057039446/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb7_link = 'http://www.imdb.com/list/ls003062015/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb8_link = 'http://www.imdb.com/list/ls027822154/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb9_link = 'http://www.imdb.com/list/ls004943234/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb10_link = 'http://www.imdb.com/list/ls020387857/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb11_link = 'http://www.imdb.com/list/ls062392787/?view=detail&sort=date_added,desc&title_type=movie,tvMovie&start=1'
        self.imdb12_link = 'http://www.imdb.com/list/ls051289348/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb13_link = 'http://www.imdb.com/list/ls063259747/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb14_link = 'http://www.imdb.com/list/ls063204479/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'		
        self.imdb15_link = 'http://www.imdb.com/list/ls062247190/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb16_link = 'http://www.imdb.com/list/ls062218265/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'		
        self.imdb17_link = 'http://www.imdb.com/list/ls075582795/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb18_link = 'http://www.imdb.com/list/ls075785141/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'		
        self.imdb19_link = 'http://www.imdb.com/list/ls058963815/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb20_link = 'http://www.imdb.com/list/ls069754038/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'		
        self.imdb21_link = 'http://www.imdb.com/list/ls070949682/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb22_link = 'http://www.imdb.com/list/ls077141747/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'		
        self.imdb23_link = 'http://www.imdb.com/list/ls062760686/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb24_link = 'http://www.imdb.com/list/ls020576693/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'		
        self.imdb25_link = 'http://www.imdb.com/list/ls066797820/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb26_link = 'http://www.imdb.com/list/ls066222382/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb27_link = 'http://www.imdb.com/list/ls062746803/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb28_link = 'http://www.imdb.com/list/ls066191116/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb29_link = 'http://www.imdb.com/list/ls066746282/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb30_link = 'http://www.imdb.com/list/ls066370089/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb31_link = 'http://www.imdb.com/list/ls066780524/?view=detail&sort=date_added,desc&title_type=movie,tvMovie&start=1'
        self.imdb32_link = 'http://www.imdb.com/list/ls066135354/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb33_link = 'http://www.imdb.com/list/ls066367722/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb34_link = 'http://www.imdb.com/list/ls066502835/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb35_link = 'http://www.imdb.com/list/ls066198904/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb36_link = 'http://www.imdb.com/list/ls068335911/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb37_link = 'http://www.imdb.com/list/ls057631565/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb38_link = 'http://www.imdb.com/list/ls064685738/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb39_link = 'http://www.imdb.com/list/ls066176690/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb40_link = 'http://www.imdb.com/list/ls066113037/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb41_link = 'http://www.imdb.com/list/ls069248253/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb42_link = 'http://www.imdb.com/list/ls063841856/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb43_link = 'http://www.imdb.com/list/ls066788382/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb44_link = 'http://www.imdb.com/list/ls066184124/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb45_link = 'http://www.imdb.com/list/ls021557769/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb46_link = 'http://www.imdb.com/list/ls008462416/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb47_link = 'http://www.imdb.com/list/ls057723258/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb48_link = 'http://www.imdb.com/list/ls057106830/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb49_link = 'http://www.imdb.com/list/ls064085103/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb50_link = 'http://www.imdb.com/list/ls057104247/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'		
        self.imdb51_link = 'http://www.imdb.com/list/ls070389024/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb52_link = 'http://www.imdb.com/list/ls051708902/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'		
        self.imdb53_link = 'http://www.imdb.com/list/ls057785252/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdb54_link = 'http://www.imdb.com/list/ls051072059/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'		

################# Critters IMDB Lists ####################
        self.bescritsfav_link = 'http://www.imdb.com/list/ls025926842/?start=1&view=detail&sort=listorian:asc&scb=0.3694954577617571'
        self.besgreatest_link = 'http://www.imdb.com/list/ls055592025/?start=1&view=detail&sort=user_rating:desc&defaults=1&scb=0.775061602469568'
        self.besaction_link = 'http://www.imdb.com/list/ls009668579/?start=1&view=detail&sort=user_rating:desc&defaults=1&scb=0.9494365460975143'
        self.beswar_link = 'http://www.imdb.com/list/ls009678583/?start=1&view=detail&sort=listorian:asc&defaults=1&scb=0.47816919475737607'
        self.besfantasy_link = 'http://www.imdb.com/list/ls009669258/?start=1&view=detail&sort=release_date_us:desc&defaults=1&scb=0.19679429634681167'
        self.beshistory_link = 'http://www.imdb.com/list/ls009668055/?start=1&view=detail&sort=release_date_us:desc&defaults=1&scb=0.9356958775568767' 
        self.besdrama_link = 'http://www.imdb.com/list/ls009668711/?start=1&view=detail&sort=release_date_us:desc&defaults=1&scb=0.5449555663113432'
        self.besthriller_link = 'http://www.imdb.com/list/ls009668314/?start=1&view=detail&sort=release_date_us:desc&defaults=1&scb=0.023704227518558163'
        self.besromance_link = 'http://www.imdb.com/list/ls000043052/?start=1&view=detail&sort=user_rating:desc&defaults=1&scb=0.6676421773922063'
        self.besbiography_link = 'http://www.imdb.com/list/ls009668766/?start=1&view=detail&sort=user_rating:desc&defaults=1&scb=0.15158221391953308'
        self.besmystery_link = 'http://www.imdb.com/list/ls009668531/?start=1&view=detail&sort=user_rating:desc&defaults=1&scb=0.5749739020940454'
        self.besfamily_link = 'http://www.imdb.com/list/ls009389114/?start=1&view=detail&sort=release_date_us:desc&defaults=1&scb=0.1277949649137693'
        self.bescomedy_link = 'http://www.imdb.com/list/ls058726648/?start=1&view=detail&sort=release_date_us:desc&defaults=1&scb=0.07671821496700626'
        self.besurban_link = 'http://www.imdb.com/list/ls054431555/?start=1&view=detail&sort=user_rating:desc&defaults=1&scb=0.9262405620396588'
        self.bescrime_link = 'http://www.imdb.com/list/ls009668704/?start=1&view=detail&sort=user_rating:desc&defaults=1&scb=0.3624139395302921'
        self.besmusical_link = 'http://www.imdb.com/list/ls000071646/?start=1&view=detail&sort=user_rating:desc&defaults=1&scb=0.5506929697318665'
        self.bessports_link = 'http://www.imdb.com/list/ls009674465/?start=1&view=detail&sort=release_date_us:desc&defaults=1&scb=0.3843845959247705'
        self.beshindi_link = 'http://www.imdb.com/list/ls051594496/?start=1&view=detail&sort=release_date_us:desc&defaults=1&scb=0.8070346927298022'
################# Critters IMDB Lists ####################

		
        self.traktlists_link = 'http://api.trakt.tv/users/me/lists'
        self.traktlikedlists_link = 'http://api.trakt.tv/users/likes/lists?limit=1000000'
        self.traktlist_link = 'http://api.trakt.tv/users/%s/lists/%s/items'
        self.traktcollection_link = 'http://api.trakt.tv/users/me/collection/movies'
        self.traktwatchlist_link = 'http://api.trakt.tv/users/me/watchlist/movies'
        self.traktfeatured_link = 'http://api.trakt.tv/recommendations/movies?limit=40'
        self.trakthistory_link = 'http://api.trakt.tv/users/me/history/movies?limit=40&page=1'
        self.imdblists_link = 'http://www.imdb.com/user/ur%s/lists?tab=all&sort=mdfd&order=desc&filter=titles' % self.imdb_user
        self.imdblist_link = 'http://www.imdb.com/list/%s/?view=detail&sort=alpha,asc&title_type=movie,tvMovie&start=1'
        self.imdblist2_link = 'http://www.imdb.com/list/%s/?view=detail&sort=date_added,desc&title_type=movie,tvMovie&start=1'
        self.imdbwatchlist_link = 'http://www.imdb.com/user/ur%s/watchlist?sort=alpha,asc' % self.imdb_user
        self.imdbwatchlist2_link = 'http://www.imdb.com/user/ur%s/watchlist?sort=date_added,desc' % self.imdb_user


    def get(self, url, idx=True, create_directory=True):
        try:
            try: url = getattr(self, url + '_link')
            except: pass

            try: u = urlparse.urlparse(url).netloc.lower()
            except: pass


            if u in self.trakt_link and '/users/' in url:
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


    def widget(self):
        setting = control.setting('movie.widget')

        if setting == '2':
            self.get(self.trending_link)
        elif setting == '3':
            self.get(self.popular_link)
        elif setting == '4':
            self.get(self.theaters_link)
        else:
            self.get(self.featured_link)


    def search(self):
        try:
            control.idle()

            t = control.lang(32010).encode('utf-8')
            k = control.keyboard('', t) ; k.doModal()
            q = k.getText() if k.isConfirmed() else None

            if (q == None or q == ''): return

            url = self.search_link + urllib.quote_plus(q)
            url = '%s?action=moviePage&url=%s' % (sys.argv[0], urllib.quote_plus(url))
            control.execute('Container.Update(%s)' % url)
        except:
            return


    def person(self):
        try:
            control.idle()

            t = control.lang(32010).encode('utf-8')
            k = control.keyboard('', t) ; k.doModal()
            q = k.getText() if k.isConfirmed() else None

            if (q == None or q == ''): return

            url = self.persons_link + urllib.quote_plus(q)
            url = '%s?action=moviePersons&url=%s' % (sys.argv[0], urllib.quote_plus(url))
            control.execute('Container.Update(%s)' % url)
        except:
            return


    def genres(self):
        genres = [
            ('Action', 'action', True),
            ('Adventure', 'adventure', True),
            ('Animation', 'animation', True),
            ('Anime', 'anime', False),
            ('Biography', 'biography', True),
            ('Comedy', 'comedy', True),
            ('Crime', 'crime', True),
            ('Documentary', 'documentary', True),
            ('Drama', 'drama', True),
            ('Family', 'family', True),
            ('Fantasy', 'fantasy', True),
            ('History', 'history', True),
            ('Horror', 'horror', True),
            ('Music ', 'music', True),
            ('Musical', 'musical', True),
            ('Mystery', 'mystery', True),
            ('Romance', 'romance', True),
            ('Science Fiction', 'sci_fi', True),
            ('Sport', 'sport', True),
            ('Thriller', 'thriller', True),
            ('War', 'war', True),
            ('Western', 'western', True)
        ]

        for i in genres: self.list.append(
            {
                'name': cleangenre.lang(i[0], self.lang),
                'url': self.genre_link % i[1] if i[2] else self.keyword_link % i[1],
                'image': 'genres.jpg',
                'action': 'movies'
            })

        self.addDirectory(self.list)
        return self.list


    def languages(self):
        languages = [
            ('Arabic', 'ar'),
            ('Bulgarian', 'bg'),
            ('Chinese', 'zh'),
            ('Croatian', 'hr'),
            ('Dutch', 'nl'),
            ('English', 'en'),
            ('Finnish', 'fi'),
            ('French', 'fr'),
            ('German', 'de'),
            ('Greek', 'el'),
            ('Hebrew', 'he'),
            ('Hindi ', 'hi'),
            ('Hungarian', 'hu'),
            ('Icelandic', 'is'),
            ('Italian', 'it'),
            ('Japanese', 'ja'),
            ('Korean', 'ko'),
            ('Norwegian', 'no'),
            ('Persian', 'fa'),
            ('Polish', 'pl'),
            ('Portuguese', 'pt'),
            ('Punjabi', 'pa'),
            ('Romanian', 'ro'),
            ('Russian', 'ru'),
            ('Spanish', 'es'),
            ('Swedish', 'sv'),
            ('Turkish', 'tr'),
            ('Ukrainian', 'uk')
        ]

        for i in languages: self.list.append({'name': str(i[0]), 'url': self.language_link % i[1], 'image': 'languages.png', 'action': 'movies'})
        self.addDirectory(self.list)
        return self.list


    def certifications(self):
        certificates = ['G', 'PG', 'PG-13', 'R', 'NC-17']

        for i in certificates: self.list.append({'name': str(i), 'url': self.certification_link % str(i).replace('-', '_').lower(), 'image': 'certificates.png', 'action': 'movies'})
        self.addDirectory(self.list)
        return self.list


    def years(self):
        year = (self.datetime.strftime('%Y'))

        for i in range(int(year)-0, 1900, -1): self.list.append({'name': str(i), 'url': self.year_link % (str(i), str(i)), 'image': 'years.png', 'action': 'movies'})
        self.addDirectory(self.list)
        return self.list


    def persons(self, url):
        if url == None:
            self.list = cache.get(self.imdb_person_list, 24, self.personlist_link)
        else:
            self.list = cache.get(self.imdb_person_list, 1, url)

        for i in range(0, len(self.list)): self.list[i].update({'action': 'movies'})
        self.addDirectory(self.list)
        return self.list


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

            items = client.parseDOM(result, 'div', attrs = {'class': 'lister-item .+?'})
            items += client.parseDOM(result, 'div', attrs = {'class': 'list_item.+?'})
        except:
            return

        try:
            next = client.parseDOM(result, 'a', ret='href', attrs = {'class': 'lister-page-next .+?'})
            if len(next) == 0:
                next = client.parseDOM(result, 'a', ret='href', attrs = {'class': '.+?lister-page-next .+?'})

            if len(next) == 0:
                next = client.parseDOM(result, 'div', attrs = {'class': 'list-pagination'})[0]
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
            items = client.parseDOM(result, 'div', attrs = {'class': '.+? mode-detail'})
        except:
            return

        for item in items:
            try:
                name = client.parseDOM(item, 'img', ret='alt')[0]
                name = client.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                url = client.parseDOM(item, 'a', ret='href')[0]
                url = re.findall('(nm\d*)', url, re.I)[0]
                url = self.person_link % url
                url = client.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                image = client.parseDOM(item, 'img', ret='src')[0]
                # if not ('._SX' in image or '._SY' in image): raise Exception()
                # image = re.sub('(?:_SX|_SY|_UX|_UY|_CR|_AL)(?:\d+|_).+?\.', '_SX500.', image)
                image = client.replaceHTMLCodes(image)
                image = image.encode('utf-8')

                self.list.append({'name': name, 'url': url, 'image': image})
            except:
                pass

        return self.list


    def imdb_user_list(self, url):
        try:
            result = client.request(url)
            items = client.parseDOM(result, 'li', attrs = {'class': 'ipl-zebra-list__item user-list'})
        except:
            pass

        for item in items:
            try:
                name = client.parseDOM(item, 'a')[0]
                name = client.replaceHTMLCodes(name)
                name = name.encode('utf-8')

                url = client.parseDOM(item, 'a', ret='href')[0]
                url = url.split('/list/', 1)[-1].strip('/')
                url = self.imdblist_link % url
                url = client.replaceHTMLCodes(url)
                url = url.encode('utf-8')

                self.list.append({'name': name, 'url': url, 'context': url})
            except:
                pass

        self.list = sorted(self.list, key=lambda k: utils.title_key(k['name']))
        return self.list


    def worker(self, level=1):
        self.meta = []
        total = len(self.list)

        self.fanart_tv_headers = {'api-key': 'YTc2MGMyMTEzYTM1OTk5NzFiN2FjMWU0OWUzMTAyMGQ='.decode('base64')}
        if not self.fanart_tv_user == '':
            self.fanart_tv_headers.update({'client-key': self.fanart_tv_user})

        for i in range(0, total): self.list[i].update({'metacache': False})

        self.list = metacache.fetch(self.list, self.lang, self.user)

        for r in range(0, total, 40):
            threads = []
            for i in range(r, r+40):
                if i <= total: threads.append(workers.Thread(self.super_info, i))
            [i.start() for i in threads]
            [i.join() for i in threads]

            if self.meta: metacache.insert(self.meta)

        self.list = [i for i in self.list if not i['imdb'] == '0']

        self.list = metacache.local(self.list, self.tm_img_link, 'poster3', 'fanart2')

        if self.fanart_tv_user == '':
            for i in self.list: i.update({'clearlogo': '0', 'clearart': '0'})


    def super_info(self, i):
        try:
            if self.list[i]['metacache'] == True: raise Exception()

            imdb = self.list[i]['imdb']

            item = trakt.getMovieSummary(imdb)

            title = item.get('title')
            title = client.replaceHTMLCodes(title)

            originaltitle = title

            year = item.get('year', 0)
            year = re.sub('[^0-9]', '', str(year))

            imdb = item.get('ids', {}).get('imdb', '0')
            imdb = 'tt' + re.sub('[^0-9]', '', str(imdb))

            tmdb = str(item.get('ids', {}).get('tmdb', 0))

            premiered = item.get('released', '0')
            try: premiered = re.compile('(\d{4}-\d{2}-\d{2})').findall(premiered)[0]
            except: premiered = '0'

            genre = item.get('genres', [])
            genre = [x.title() for x in genre]
            genre = ' / '.join(genre).strip()
            if not genre: genre = '0'

            duration = str(item.get('Runtime', 0))

            rating = item.get('rating', '0')
            if not rating or rating == '0.0': rating = '0'

            votes = item.get('votes', '0')
            try: votes = str(format(int(votes), ',d'))
            except: pass

            mpaa = item.get('certification', '0')
            if not mpaa: mpaa = '0'

            tagline = item.get('tagline', '0')

            plot = item.get('overview', '0')

            people = trakt.getPeople(imdb, 'movies')

            director = writer = ''
            if 'crew' in people and 'directing' in people['crew']:
                director = ', '.join([director['person']['name'] for director in people['crew']['directing'] if director['job'].lower() == 'director'])
            if 'crew' in people and 'writing' in people['crew']:
                writer = ', '.join([writer['person']['name'] for writer in people['crew']['writing'] if writer['job'].lower() in ['writer', 'screenplay', 'author']])

            cast = []
            for person in people.get('cast', []):
                cast.append({'name': person['person']['name'], 'role': person['character']})
            cast = [(person['name'], person['role']) for person in cast]

            try:
                if self.lang == 'en' or self.lang not in item.get('available_translations', [self.lang]): raise Exception()

                trans_item = trakt.getMovieTranslation(imdb, self.lang, full=True)

                title = trans_item.get('title') or title
                tagline = trans_item.get('tagline') or tagline
                plot = trans_item.get('overview') or plot
            except:
                pass

            try:
                artmeta = True
                #if self.fanart_tv_user == '': raise Exception()
                art = client.request(self.fanart_tv_art_link % imdb, headers=self.fanart_tv_headers, timeout='10', error=True)
                try: art = json.loads(art)
                except: artmeta = False
            except:
                pass

            try:
                poster2 = art['movieposter']
                poster2 = [x for x in poster2 if x.get('lang') == self.lang][::-1] + [x for x in poster2 if x.get('lang') == 'en'][::-1] + [x for x in poster2 if x.get('lang') in ['00', '']][::-1]
                poster2 = poster2[0]['url'].encode('utf-8')
            except:
                poster2 = '0'

            try:
                if 'moviebackground' in art: fanart = art['moviebackground']
                else: fanart = art['moviethumb']
                fanart = [x for x in fanart  if x.get('lang') == self.lang][::-1] + [x for x in fanart if x.get('lang') == 'en'][::-1] + [x for x in fanart if x.get('lang') in ['00', '']][::-1]
                fanart = fanart[0]['url'].encode('utf-8')
            except:
                fanart = '0'

            try:
                banner = art['moviebanner']
                banner = [x for x in banner if x.get('lang') == self.lang][::-1] + [x for x in banner if x.get('lang') == 'en'][::-1] + [x for x in banner if x.get('lang') in ['00', '']][::-1]
                banner = banner[0]['url'].encode('utf-8')
            except:
                banner = '0'

            try:
                if 'hdmovielogo' in art: clearlogo = art['hdmovielogo']
                else: clearlogo = art['clearlogo']
                clearlogo = [x for x in clearlogo if x.get('lang') == self.lang][::-1] + [x for x in clearlogo if x.get('lang') == 'en'][::-1] + [x for x in clearlogo if x.get('lang') in ['00', '']][::-1]
                clearlogo = clearlogo[0]['url'].encode('utf-8')
            except:
                clearlogo = '0'

            try:
                if 'hdmovieclearart' in art: clearart = art['hdmovieclearart']
                else: clearart = art['clearart']
                clearart = [x for x in clearart if x.get('lang') == self.lang][::-1] + [x for x in clearart if x.get('lang') == 'en'][::-1] + [x for x in clearart if x.get('lang') in ['00', '']][::-1]
                clearart = clearart[0]['url'].encode('utf-8')
            except:
                clearart = '0'

            try:
                if self.tm_user == '': raise Exception()

                art2 = client.request(self.tm_art_link % imdb, timeout='10', error=True)
                art2 = json.loads(art2)
            except:
                pass

            try:
                poster3 = art2['posters']
                poster3 = [x for x in poster3 if x.get('iso_639_1') == self.lang] + [x for x in poster3 if x.get('iso_639_1') == 'en'] + [x for x in poster3 if not x.get('iso_639_1') not in [self.lang, 'en']]
                poster3 = [(x['width'], x['file_path']) for x in poster3]
                poster3 = [(x[0], x[1]) if x[0] < 300 else ('300', x[1]) for x in poster3]
                poster3 = self.tm_img_link % poster3[0]
                poster3 = poster3.encode('utf-8')
            except:
                poster3 = '0'

            try:
                fanart2 = art2['backdrops']
                fanart2 = [x for x in fanart2 if x.get('iso_639_1') == self.lang] + [x for x in fanart2 if x.get('iso_639_1') == 'en'] + [x for x in fanart2 if not x.get('iso_639_1') not in [self.lang, 'en']]
                fanart2 = [x for x in fanart2 if x.get('width') == 1920] + [x for x in fanart2 if x.get('width') < 1920]
                fanart2 = [(x['width'], x['file_path']) for x in fanart2]
                fanart2 = [(x[0], x[1]) if x[0] < 1280 else ('1280', x[1]) for x in fanart2]
                fanart2 = self.tm_img_link % fanart2[0]
                fanart2 = fanart2.encode('utf-8')
            except:
                fanart2 = '0'

            item = {'title': title, 'originaltitle': originaltitle, 'year': year, 'imdb': imdb, 'tmdb': tmdb, 'poster': '0', 'poster2': poster2, 'poster3': poster3, 'banner': banner, 'fanart': fanart, 'fanart2': fanart2, 'clearlogo': clearlogo, 'clearart': clearart, 'premiered': premiered, 'genre': genre, 'duration': duration, 'rating': rating, 'votes': votes, 'mpaa': mpaa, 'director': director, 'writer': writer, 'cast': cast, 'plot': plot, 'tagline': tagline}
            item = dict((k,v) for k, v in item.iteritems() if not v == '0')
            self.list[i].update(item)

            if artmeta == False: raise Exception()

            meta = {'imdb': imdb, 'tmdb': tmdb, 'tvdb': '0', 'lang': self.lang, 'user': self.user, 'item': item}
            self.meta.append(meta)
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

        addToLibrary = control.lang(32551).encode('utf-8')

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

                cm.append((addToLibrary, 'RunPlugin(%s?action=movieToLibrary&name=%s&title=%s&year=%s&imdb=%s&tmdb=%s)' % (sysaddon, sysname, systitle, year, imdb, tmdb)))

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

        addToLibrary = control.lang(32551).encode('utf-8')

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

                try: cm.append((addToLibrary, 'RunPlugin(%s?action=moviesToLibrary&url=%s)' % (sysaddon, urllib.quote_plus(i['context']))))
                except: pass

                item = control.item(label=name)

                item.setArt({'icon': thumb, 'thumb': thumb})
                if not addonFanart == None: item.setProperty('Fanart_Image', addonFanart)

                item.addContextMenuItems(cm)

                control.addItem(handle=syshandle, url=url, listitem=item, isFolder=True)
            except:
                pass

        control.content(syshandle, 'addons')
        control.directory(syshandle, cacheToDisc=True)
