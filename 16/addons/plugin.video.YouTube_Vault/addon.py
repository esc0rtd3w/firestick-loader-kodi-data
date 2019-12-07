"""
 Author: Tvaddons

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
 
 """

import urllib,urllib2,re,xbmcplugin,xbmcgui,os,sys,datetime
from resources.lib.common_variables import *
from resources.lib.directory import *
from resources.lib.youtubewrapper import *
from resources.lib.watched import * 

fanart = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.YouTube_Vault', 'fanart.jpg'))
art = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.YouTube_Vault/resources/img', ''))

def CATEGORIES():
        addDir('[COLOR blue]Movies[/COLOR]','url',10,art + 'movies.png')
        addDir('[COLOR blue]Tv[/COLOR]','url',11,art + 'Tv.png')
        addDir('[COLOR blue]Cartoons[/COLOR]','url',12,art + 'Cartoons.png')
        addDir('[COLOR blue]Music[/COLOR]','url',13,art + 'Music.png')
        addDir('[COLOR blue]News[/COLOR]','url',14,art + 'news.png')
        addDir('[COLOR blue]Sports[/COLOR]','url',15,art + 'Sports.png')
        #addDir('[COLOR blue]youtube-dl Control[/COLOR]','url',16,art + 'youtube-dlControl.png')
        logo = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.YouTube_Vault','logo.png'))
        xbmcgui.Dialog().notification('YouTube Vault is brought to you','In association with TvAddons',logo,5000,False)
        

def Movies():
        addDir('[COLOR blue]Popcornflix[/COLOR]','url',17,art + 'Sports.png')
        addDir('[COLOR blue]HD Movies[/COLOR]','PLKkDjgBOPjWFMth5U6cUGKqqE-rkLHm8b',1,art + 'movies.png')
        addDir('[COLOR blue]Action Movies[/COLOR]','PLAA9E622BC2614112',1,art + 'movies.png')
        addDir('[COLOR blue]Anime Movies[/COLOR]','PLX0yDcKZhjGyd3SPqKOh8VTuXzhuWIyea',1,art + 'Movies.png')
        addDir('[COLOR blue]Christian Movies[/COLOR]','PL7DEonMNS4tGWRx1NFRvcmUvab5jW-PjI',1,art + 'Movies.png')
        addDir('[COLOR blue]Comedy Movies[/COLOR]','PLjuR5ouJJf7oFy9kYTjeOdc8n6yGm_U64',1,art + 'Movies.png')
        addDir('[COLOR blue]HORROR Movies[/COLOR]','PLC2C9BFC77856C976',1,art + 'Movies.png')
        addDir('[COLOR blue]Family Movies[/COLOR]','PLKkDjgBOPjWE3t8xy7gO6w1gc2dy2R_r_',1,art + 'Movies.png')
        addDir('[COLOR blue]Romance/Drama Movies[/COLOR]','PL3R5u7N6Bi3Rg-EKzpJ2EvBTgcB9HFIzR',1,art + 'Movies.png')
        addDir('[COLOR blue]Sci-Fi Movies[/COLOR]','PLm28lpCzRlQme34bn8hNtamOKd8IkdVX4',1,art + 'Movies.png')
        addDir('[COLOR blue]Western Movies(1)[/COLOR]','PLttOfW_IF8ou_WTDOId6S2ay7Vkqc1aKd',1,art + 'Movies.png')
        addDir('[COLOR blue]Western Movies(2)[/COLOR]','PLJPKPjW6O7SvK3nrQssKGYmaJyMIqX731',1,art + 'Movies.png')
        addDir('[COLOR blue]LMN Movies[/COLOR]','PLuUIACjjMlWODq95IAHdMgUTRFEMGfJ3y',1,art + 'Movies.png')
        addDir('[COLOR blue]Hallmark Movies[/COLOR]','PLITE87HGJ5s-DbS7HiGOT33s3bcl6YOVd',1,art + 'Movies.png')
        addDir('[COLOR blue]1920-1939 Movies[/COLOR]','PLsQEhfECqlFaCk_rdvaYf4EwBIFYQfeh3',1,art + 'Movies.png')
        addDir('[COLOR blue]1940-1959 Movies[/COLOR]','PLsQEhfECqlFb0twj4EX0nNUViCj58RxOk',1,art + 'Movies.png')
        addDir('[COLOR blue]1960-1979 Movies[/COLOR]','PLsQEhfECqlFaibL0k032xIj2IbkfKoJd9',1,art + 'Movies.png')
        addDir('[COLOR blue]1980-1999 Movies[/COLOR]','PLsQEhfECqlFbT2HQd8qQMsF2jWxXj6xzB',1,art + 'Movies.png')
        addDir('[COLOR blue]2000-2009 Movies[/COLOR]','PLsQEhfECqlFbhv2s_3pmhRE20bJx_1lZY',1,art + 'Movies.png')
        addDir('[COLOR blue]80s Movies[/COLOR]','PLwby6XrbM4tBQrEKliMUZGJsqM_0WItsr',1,art + 'Movies.png')
        
def Popcornflix():
        addDir('[COLOR blue]Recent Uploads[/COLOR]','PLsZQnDqnebk4NY9xP9uZSwJ-XeysrEZi6',1,art + 'movies.png')
        addDir('[COLOR blue]Fan Favorites[/COLOR]','PLsZQnDqnebk4YzGIPJLYeJSI1F67d7jkm',1,art + 'movies.png')
        addDir('[COLOR blue]Action Movies[/COLOR]','PLsZQnDqnebk4kN-oGYb2JmTU0ofZHqZTg',1,art + 'movies.png')
        addDir('[COLOR blue]Family-friendly Movies[/COLOR]','PLsZQnDqnebk6HK71JAkgigKthwe9XvEbz',1,art + 'movies.png')
        addDir('[COLOR blue]Horror Movies[/COLOR]','PLsZQnDqnebk4P4a5SQHveJQWkooCkY8sn',1,art + 'movies.png')
        addDir('[COLOR blue]Thriller Movies[/COLOR]','PLsZQnDqnebk4ag9hhJd2AWerYn0CTzK5L',1,art + 'movies.png')
        addDir('[COLOR blue]Dramas Movies[/COLOR]','PLsZQnDqnebk6N7EchSMbmLXkGTFguhUba',1,art + 'movies.png')
        addDir('[COLOR blue]Comedie Movies[/COLOR]','PLsZQnDqnebk5HQZ7Wh5dblxRumNWbzJJC',1,art + 'movies.png')
        addDir('[COLOR blue]Romantic Comedies[/COLOR]','PLsZQnDqnebk57K1G7_cO7z_Zqzyg3X84R',1,art + 'movies.png')
        

def Tv():
        addDir('[COLOR blue]Bonanza[/COLOR]','PLmHgXUJMN1TX03VPVZHge8Wg9ZyBmEJal',1,art + 'Tv.png')
        addDir('[COLOR blue]Home Improvement[/COLOR]','PLCo0yXyrDeR648F9ibjVjm__kDb0RyEfq',1,art + 'Tv.png')
        addDir('[COLOR blue]Impulse[/COLOR]','PLINwjXK120_JpGB6mRJ0oJxOdFGjxekIp',1,art + 'Tv.png')
        addDir('[COLOR blue]Documentary[/COLOR]', 'PLi4lYGGXHIkODAkKFIXtLZpAjMptl-xSl', 1, art + 'Tv.png')
        addDir('[COLOR blue]My Classic Car[/COLOR]','PLMU_iGRst5xaE-fTWw35CksMPYqlxguNp',1,art + 'Tv.png')
        addDir('[COLOR blue]Beverly Hillbillies[/COLOR]','PLUtyelKnYB0DfRPeWCCcC-xfACPfgv1Po',1,art + 'Tv.png')
        addDir('[COLOR blue]Daniel Boone[/COLOR]','PLpZ94EUFzdpDE0s5O60J5dOeOhvt2gpL-',1,art + 'Tv.png')
        addDir('[COLOR blue]Have Gun Will Travel[/COLOR]','PLoXLTb9MXwazYf147EoQJt-wmkuVKZVfc',1,art + 'Tv.png')
        addDir('[COLOR blue]Liza on Demand[/COLOR]','PL5MGfQbdoiHOrAA11GmjKw0bllPlzMZDq',1,art + 'Tv.png')
        addDir('[COLOR blue]Highway Patrol[/COLOR]','PL-aJSrEGIGy4Muhw4lhuYII5kDrBlUqrv',1,art + 'Tv.png')
        addDir('[COLOR blue]Crime Stories[/COLOR]','PLUDizevuO8OonDbpnQk1pVOu2nxQKnoKy',1,art + 'Tv.png')
        addDir('[COLOR blue]Doomsday Preppers[/COLOR]','PLum50h_rWpG6qIKOwiUdqryoVyAAS4qPd',1,art + 'Tv.png')
        addDir('[COLOR blue]Beastmaster[/COLOR]','PL6fJmjt84zZjHtICMv908RZVxqO7HXUxa',1,art + 'Tv.png')
        addDir('[COLOR blue]Mr Bean[/COLOR]','PLe9kjFJ6bWHhZyRXzwK3XPBqXPSuJSyUp',1,art + 'Tv.png')
        addDir('[COLOR blue]Cobra Kai[/COLOR]', 'PLxm--8AYWEDelTYpYi2zulMEw-0T-M5IH', 1, art + 'Tv.png')
        addDir('[COLOR blue]12 Deadly Days [/COLOR]','PLjq6DwYksrzxaAwiRSDCCp8mF7CwdIX-n',1,art + 'Tv.png')
        addDir('[COLOR blue]Rescue Special Ops[/COLOR]','PLZVMGCh7sZUgxG1erdqZNTQiotE3ers6z',1,art + 'Tv.png')
        addDir('[COLOR blue]RoadKill[/COLOR]','PL12C0C916CECEA3BC',1,art + 'Tv.png')
        addDir('[COLOR blue]Urban Legends[/COLOR]','PLFtpZ659RpvF42PE6uKm6mQjuz8uDq2jp',1,art + 'Tv.png')
        addDir('[COLOR blue]Highlander[/COLOR]','PL551DB3E031657F74',1,art + 'Tv.png')
        addDir('[COLOR blue]We Are Savvy[/COLOR]','PLjq6DwYksrzz8ZdH1WKO0xugIR3C_a__b',1,art + 'Tv.png')
        addDir('[COLOR blue]The Green Hornet[/COLOR]','PL6fJmjt84zZijUX52K1F24557XEatByGT',1,art + 'Tv.png')
        addDir('[COLOR blue]Sideswiped[/COLOR]','PLjq6DwYksrzz66gCMBQWDQNi3L0S6cPfF',1,art + 'Tv.png')
        addDir('[COLOR blue]The King Of Queens[/COLOR]','PL5BmokrJRqVjcSP81F3gCQDt_FVywM-2_',1,art + 'Tv.png')
        addDir('[COLOR blue]Kitchen Nightmares[/COLOR]','PL9iRkjvEKSjsTEQtjdLDe5ovu7Q1GtMT7',1,art + 'Tv.png')
        addDir('[COLOR blue]Five Mile Creek[/COLOR]','PLeagipoZmyfkmMoopxMA06TvVMa2R2YzL',1,art + 'Tv.png')
        addDir('[COLOR blue]The Big Valley[/COLOR]','PLht_Yj17XWWpcipa-Dr6i-8_0c-eSWi0g',1,art + 'Tv.png')
        addDir('[COLOR blue]H2O - just add water[/COLOR]','PLU5KGt6g4OkFAUB_RwQ7Mgjg_O3W8A4Wf',1,art + 'Tv.png')
        addDir('[COLOR blue]The Rifleman[/COLOR]','PLLnN6aZ9EH9Fn9AItggnY7J1DoBsgN7Fg',1,art + 'Tv.png')
        addDir('[COLOR blue]Hawkeye and the Last of the Mohicans[/COLOR]','PLmHgXUJMN1TWiHtWel7yJzgB8Sw3-z1E5',1,art + 'Tv.png')
        addDir('[COLOR blue]The Golden Girls[/COLOR]','PLEAoZMx-ZHqqnst-QDef-wccG4n42pMJi',1,art + 'Tv.png')
        addDir('[COLOR blue]Youth & Consequences[/COLOR]', 'PLyVaF6bvPQ-Tc7pkEcmqSjQaoWftH8WAx', 1, art + 'Tv.png')
        addDir('[COLOR blue]The Jeffersons[/COLOR]','PLKuzFhxtS9BEtKqEjmCNzRIEYpFK7gzY6',1,art + 'Tv.png')
        addDir('[COLOR blue]The Lucy Show[/COLOR]','PLmHgXUJMN1TXCZbl3w_RYofN_XMCRDtdy',1,art + 'Tv.png')
        addDir('[COLOR blue]Amos n Andy[/COLOR]','PLsPbqGD7bfUApUGk6WXBsUJCEyYM94yTv',1,art + 'Tv.png')
        addDir('[COLOR blue]Relevations: The Initial Journey[/COLOR]','PL6fJmjt84zZj_v8zW90NRzNzsKx0SgzAW',1,art + 'Tv.png')
        addDir('[COLOR blue]Kolchak[/COLOR]','PLAPGcD5LGrp7PGyKooDu0_ru4zgBUuT9b',1,art + 'Tv.png')
        addDir('[COLOR blue]48 Hours Mystery[/COLOR]','PLyLrnNOEPdo430q3kcZmUHtbbPfv4vycg',1,art + 'Tv.png')
        addDir('[COLOR blue]The Sidemen Show[/COLOR]','PLjkZIuJPz3rPW7CiiVlXoCQ5Ua1BXbUJJ',1,art + 'Tv.png')
        addDir('[COLOR blue]Spellbinder[/COLOR]','PLZVMGCh7sZUj-YwN6wE2j13bPpEFv3qUF',1,art + 'Tv.png')
        addDir('[COLOR blue]Stingers[/COLOR]','PLZVMGCh7sZUgcRKEWehlxhEvWEfD3b_DF',1,art + 'Tv.png')
        addDir('[COLOR blue]The Bernie Mac Show[/COLOR]','PL1p5cydiDufi2rr-8jlkxIpJjBM_536O5',1,art + 'Tv.png')
        addDir('[COLOR blue]Biography[/COLOR]','PLCBLlrBlEN1skMs2pGboan7_lfio_s8Z-',1,art + 'Tv.png')
        addDir('[COLOR blue]Hope & Faith[/COLOR]','PLGsasc3CA1-mDbeIcl0fqd-wMTUkpxtdL',1,art + 'Tv.png')
        addDir('[COLOR blue]Blue Water High[/COLOR]','PLniM5dINvV6T0lKx4GYdXDU20B3XF9-Rb',1,art + 'Tv.png')
        addDir('[COLOR blue]Step Up High Water[/COLOR]', 'PL3DCab4b7B8BrlpLsRjK4MtzIVqQcP__v', 1, art + 'Tv.png')
        addDir('[COLOR blue]Robin Hood[/COLOR]','PLeagipoZmyfnGP2cUhKrGU-6nv7CrtoE7',1,art + 'Tv.png')
        addDir('[COLOR blue]White Fang[/COLOR]','PLqILPCsLMT1rtHSRaEt2iNWuvu7rUIb3d',1,art + 'Tv.png')
        addDir('[COLOR blue]The Tribe[/COLOR]','PLwM4m7Qh_bFjNAL7yr0V6JAm4X4RFvWzN',1,art + 'Tv.png')
        addDir('[COLOR blue]Women Behind Bars[/COLOR]','PLFtpZ659RpvF8AKUf-koTqQSLFda9g4TR',1,art + 'Tv.png')
        addDir('[COLOR blue]The FBI Files[/COLOR]','PLY5hFG53Fodrx8LASo63ygjtgxwBuKAhR',1,art + 'Tv.png')
        addDir('[COLOR blue]F2 Finding Football[/COLOR]','PLy2vrl3y6dIw-E0CHY62oFUZURsztYf4G',1,art + 'Tv.png')
        addDir('[COLOR blue]World of Discovery[/COLOR]','PLFtpZ659RpvFrw85hhnLGBXDAQhgwh5AT',1,art + 'Tv.png')
        addDir('[COLOR blue]Lifeline[/COLOR]', 'PLVK1Q9ppZiaDDkrG2pBaXFdVd0Tva6ymm', 1, art + 'Tv.png')
        addDir('[COLOR blue]Threshold[/COLOR]','PLAPGcD5LGrp4v8EjApDGKPxvOdJe18aNw',1,art + 'Tv.png')
        addDir('[COLOR blue]Americas Dumbest Criminals[/COLOR]','PLFtpZ659RpvHJpxUhfHW-cUz1uF2_iwQr',1,art + 'Tv.png')
        addDir('[COLOR blue]Escape the Night[/COLOR]','PLRfpyIF9ZtKJKUs8MAXjMMIYTJRwiEYNo',1,art + 'Tv.png')
        addDir('[COLOR blue]Three,s Company[/COLOR]','PLKuzFhxtS9BGelhLXNEFCCtLzy6jw4Cy_',1,art + 'Tv.png')
        addDir('[COLOR blue]PBS Nova Documentary[/COLOR]','PLlHanBMNk-DKQzkktkFKGvJR_9gSRDhBr',1,art + 'Tv.png')
        addDir('[COLOR blue]Firefly[/COLOR]','PLAPGcD5LGrp4j8q5LNGFOp1itXlxSHmaJ',1,art + 'Tv.png')
        addDir('[COLOR blue]Timecop[/COLOR]','PLzovi87vDfzKQRVSGmVx4OU4H21ikCKiW',1,art + 'Tv.png')
        addDir('[COLOR blue]Gomer Pyle USMC[/COLOR]','PL5olnhooIsWxr2j4lG8v08dX1h836BTzg',1,art + 'Tv.png')
        addDir('[COLOR blue]Single By 30[/COLOR]', 'PLSHabwxChOtXpXDFMBO26SqBGGLWLtdoo', 1, art + 'Tv.png')
        addDir('[COLOR blue]American Justice[/COLOR]','PLhJVGu09xd4HuWdibMhPH6IiNNgNe9kJz',1,art + 'Tv.png')
        addDir('[COLOR blue]Starman[/COLOR]','PLAPGcD5LGrp41E9Asloxu-BDZhx1SgHg2',1,art + 'Tv.png')
        addDir('[COLOR blue]Conan The Adventurer[/COLOR]','PLzovi87vDfzI6SV_MxjoRenMyvjziShfA',1,art + 'Tv.png')
        addDir('[COLOR blue]Sanford and Son[/COLOR]','PLkexxh-KfPFqmRIpBhzyO2lCNiV-Sfi41',1,art + 'Tv.png')
        addDir('[COLOR blue]Jay Lenos Garage[/COLOR]','PLcAFCEDZU39xYLamb1NBGW_14DrieamN2',1,art + 'Tv.png')
        
		
def Cartoons():
        addDir('[COLOR blue]Super Mario Bros[/COLOR]','PLyUkLo8OvFU6pPVTZUHob6pP3FY-wUSlq',1,art + 'Cartoons.png')
        addDir('[COLOR blue]Teenage Mutant Ninja Turtles[/COLOR]','PL6fJmjt84zZgaB_DR1wE2O41fA8p2m7ro',1,art + 'Cartoons.png')
        addDir('[COLOR blue]3 Stooges[/COLOR]','PLZs0gQed9tMRAfBGlQhHCcqaJipEknlVM',1,art + 'Cartoons.png')
        addDir('[COLOR blue]The Backyardigans[/COLOR]','PLCjeNYXPBmHvdUEVlc_PIJUqChVpFbwtc',1,art + 'Cartoons.png')
        addDir('[COLOR blue]Kirby[/COLOR]','PL1E1DDEA933CD12FF',1,art + 'Cartoons.png')
        addDir('[COLOR blue]Street Fighter[/COLOR]','PLTLP-p6a1SEPXfKtkDEfBL2nM9kZ97jpb',1,art + 'Cartoons.png')
        addDir('[COLOR blue]Dennis The Menace[/COLOR]','PLZs0gQed9tMSHvfjWzZ2VOBU6GWh00slk',1,art + 'Cartoons.png')
        addDir('[COLOR blue]Gummi Bears[/COLOR]','PLZs0gQed9tMQX8dw4CiIjwFhsrNT-JRq6',1,art + 'Cartoons.png')
        addDir('[COLOR blue]Garfield and Friends[/COLOR]','PLQPfokIdb_NgpssOs_XX1VZt8Nbx3AuM7',1,art + 'Cartoons.png')
        addDir('[COLOR blue]Dungeons & Dragons[/COLOR]','PLZs0gQed9tMSMFfClSEL8EOZjayLKNINx',1,art + 'Cartoons.png')
        addDir('[COLOR blue]X Men Evolution[/COLOR]','PLrhuB2KrXOjikfPLJhTmz2qKDkltz9L8Y',1,art + 'Cartoons.png')
        addDir('[COLOR blue]He-Man[/COLOR]','PLJd8brL6u0uzm7A842UsNQkHm_T4Gmu56',1,art + 'Cartoons.png')
        addDir('[COLOR blue]M.A.S.K[/COLOR]','PLZs0gQed9tMQ2iX2H5PCWLCI9xPlIPyYk',1,art + 'Cartoons.png')
        addDir('[COLOR blue]Pink Panther[/COLOR]','PLtfPnJye9L3dxlbWP7OlJH-_yI3PYsh9r',1,art + 'Cartoons.png')
        addDir('[COLOR blue]Pippi Longstocking[/COLOR]','PLeagipoZmyfkWkyetCWsJMGy8yBvHdJs-',1,art + 'Cartoons.png')
        addDir('[COLOR blue]DC Heroes[/COLOR]','PLZs0gQed9tMS9BLYfxtyyd7OQlQe1n_-f',1,art + 'Cartoons.png')
        addDir('[COLOR blue]Animated Classics[/COLOR]','PLeagipoZmyfn9MhKB9Smgqob8CLNiaA51',1,art + 'Cartoons.png')
        addDir('[COLOR blue]The Wonderful Wizard Of Oz[/COLOR]','PLS3SOlSTtJcDe-vQ-T46r_cB1U_ENAuKF',1,art + 'Cartoons.png')
        addDir('[COLOR blue]Casper the Friendly Ghost[/COLOR]','PLeagipoZmyfl46t2ABPQitVy1V7qu2vrG',1,art + 'Cartoons.png')
        addDir('[COLOR blue]SNUFFY SMITH[/COLOR]','PL67492B3700EA9340',1,art + 'Cartoons.png')
        addDir('[COLOR blue]The Smurfs[/COLOR]','PLaE8D0PEpUTtHl3NzB3VfscnmW68cZC58',1,art + 'Cartoons.png')
        addDir('[COLOR blue]The Littles[/COLOR]','PLDJplukjMGFMD9ix6GOiKWc5sTnYih8OX',1,art + 'Cartoons.png')
        addDir('[COLOR blue]BATTLE OF THE PLANETS[/COLOR]','PLZs0gQed9tMSJwsr7nELmSe_wHWw-gFxL',1,art + 'Cartoons.png')
        addDir('[COLOR blue]SHE-RA[/COLOR]','PLZs0gQed9tMT5KX9M_PYxrVeVUiJ8aWuS',1,art + 'Cartoons.png')
        addDir('[COLOR blue]Star Wars Droids[/COLOR]','PLZs0gQed9tMQzdY8EKdrADeCZ7OJS-AZK',1,art + 'Cartoons.png')
        addDir('[COLOR blue]Dr Seuss[/COLOR]','PLeagipoZmyfkwcDThw6yIE3cqQAb8-KQ-',1,art + 'Cartoons.png')
        addDir('[COLOR blue]Chilly Willy[/COLOR]','PLnhtGTQWc2dumToZlzsKI8RCOwgzpykly',1,art + 'Cartoons.png')
        addDir('[COLOR blue]Woody Woodpecker[/COLOR]','PLB06DDF14D951C23C',1,art + 'Cartoons.png')
        addDir('[COLOR blue]Lone Ranger[/COLOR]','PLZxHX9waSzmv8CeVWGzqSPJK7KPC0HlSF',1,art + 'Cartoons.png')
        addDir('[COLOR blue]Lucky Luke[/COLOR]','PLCD5B9AD1151F3E0B',1,art + 'Cartoons.png')
        addDir('[COLOR blue]Tom And Jerry[/COLOR]','PLOLEQVkmI9eugSKUsrQBH0rxMN-qBLUyV',1,art + 'Cartoons.png')
        addDir('[COLOR blue]Dudley Do-Right[/COLOR]','PLeagipoZmyfm_yCiyU_LYR86ZcJFc0k6d',1,art + 'Cartoons.png')
        addDir('[COLOR blue]RUFF & REDDY[/COLOR]','PLZs0gQed9tMQdK9a6D3T0yfZtsc4fpMUx',1,art + 'Cartoons.png')
        addDir('[COLOR blue]CLUTCH CARGO[/COLOR]','PLZs0gQed9tMS9_E1aN8oCn0XopWZWopyn',1,art + 'Cartoons.png')
        addDir('[COLOR blue]LOONEY TUNES COMPILATION[/COLOR]','PLiBi9LVIrC-fVelw2-I2r-yrEk6SpXfO8',1,art + 'Cartoons.png')
        addDir('[COLOR blue]Christian Bible Cartoon[/COLOR]','PLKav3i3U4Xl58bqa1gmIxehnpDxA32HHc',1,art + 'Cartoons.png')

def Music():
        addDir('[COLOR blue]Billboard Top Songs 2015[/COLOR]','PL55713C70BA91BD6E',1,art + 'Music.png')
        addDir('[COLOR blue]Top Tracks Pop Music[/COLOR]','PLDcnymzs18LVXfO_x0Ei0R24qDbVtyy66',1,art + 'Music.png')
        addDir('[COLOR blue]80s & 90s Rock[/COLOR]','PL3485902CC4FB6C67',1,art + 'Music.png')
        addDir('[COLOR blue]Popular Music[/COLOR]','PLFgquLnL59alCl_2TQvOiD5Vgm1hCaGSI',1,art + 'Music.png')
        addDir('[COLOR blue]Greatest Hits Of The 70s[/COLOR]','PLGBuKfnErZlAkaUUy57-mR97f8SBgMNHh',1,art + 'Music.png')
        addDir('[COLOR blue]Hot Country Songs[/COLOR]','PL2BN1Zd8U_MsyMeK8r9Vdv1lnQGtoJaSa',1,art + 'Music.png')
        addDir('[COLOR blue]Country Music Mix[/COLOR]','PLnpWcMv6bu2X0xfAD6Kt-MgIIFOCNb067',1,art + 'Music.png')
        addDir('[COLOR blue]60s Classic Hits[/COLOR]','PLuK6flVU_Aj5EJ9Pp-C9N7XA0YJr_GrJI',1,art + 'Music.png')
        addDir('[COLOR blue]50s Classic Hits[/COLOR]','PLuK6flVU_Aj45QZ_A5ld0-pP3CIkoNQDk',1,art + 'Music.png')
        addDir('[COLOR blue]Country Radio Mix 2000 - 2014[/COLOR]','PLh__qJ1ro4JgQI6aAgk5dduKLZUGr1Tiw',1,art + 'Music.png')
        addDir('[COLOR blue]90s Country Music[/COLOR]','PLCEE7B2A4B9C9BCE7',1,art + 'Music.png')
        addDir('[COLOR blue]80s Country Music[/COLOR]','PL04199B0AF6C7C9F8',1,art + 'Music.png')
        addDir('[COLOR blue]Just-Released Music[/COLOR]','PLrEnWoR732-D67iteOI6DPdJH1opjAuJt',1,art + 'Music.png')

def News():
        addDir('[COLOR blue]World News (Top Stories[/COLOR]','PLr1-FC1l_JLFcq9r9Y3uFLkH8G37WmMRQ',1,art + 'News.png')
        addDir('[COLOR blue]National News (Top Stories)[/COLOR]','PLNjtpXOAJhQLmUEyuWw4hW_6gX8JMJUof',1,art + 'News.png')
        addDir('[COLOR blue]Cnn (Top Stories)[/COLOR]','PL6XRrncXkMaUoSMd-1D5uIt7uZ0nWxkMy',1,art + 'News.png')
        addDir('[COLOR blue]Nbc News (Top stories)[/COLOR]','PL0tDb4jw6kPxZ7ZJtMk6gqiQIU-nMeaVS',1,art + 'News.png')
        addDir('[COLOR blue]ABC (World News)[/COLOR]','PL5E6638EB9ECF2329',1,art + 'News.png')
        addDir('[COLOR blue]Fox News (Latest Politics)[/COLOR]','PLlTLHnxSVuIyeEZPBIQF_krewJkY2JSwi',1,art + 'News.png')
        addDir('[COLOR blue]Cbs News (TOP STORIES)[/COLOR]','PLEb3ThbkPrFabMf542Iic5Hxw2xlrgusX',1,art + 'News.png')

def Sports():
        addDir('[COLOR blue]NFL[/COLOR]','PLyXm-hnmX1_qxDKgYmXzxABejOkwfkjBG',1,art + 'Sports.png')
        addDir('[COLOR blue]NBA[/COLOR]','PLlVlyGVtvuVkUpgWlBV44heQGeVpxFvU4',1,art + 'Sports.png')
        addDir('[COLOR blue]NHL[/COLOR]','PLrbOUcXk2JPVj8tD4xG1XNOmD_72qi8OM',1,art + 'Sports.png')
        addDir('[COLOR blue]Baseball[/COLOR]','PLL-lmlkrmJakIJrecH1tPCFgbLBGVpMrT',1,art + 'Sports.png')

def youtube_dl():
    xbmc.executebuiltin("RunAddon(script.module.youtube.dl)")
	

def get_params():
        param=[]
        paramstring=sys.argv[2]
        if len(paramstring)>=2:
                params=sys.argv[2]
                cleanedparams=params.replace('?','')
                if (params[len(params)-1]=='/'):
                        params=params[0:len(params)-2]
                pairsofparams=cleanedparams.split('&')
                param={}
                for i in range(len(pairsofparams)):
                        splitparams={}
                        splitparams=pairsofparams[i].split('=')
                        if (len(splitparams))==2:
                                param[splitparams[0]]=splitparams[1]
                                
        return param


params=get_params()
url=None
name=None
mode=None
iconimage=None
page = None
token = None

try: url=urllib.unquote_plus(params["url"])
except: pass
try: name=urllib.unquote_plus(params["name"])
except: pass
try: mode=int(params["mode"])
except:
	try: 
		mode=params["mode"]
	except: pass
try: iconimage=urllib.unquote_plus(params["iconimage"])
except: pass
try: token=urllib.unquote_plus(params["token"])
except: pass
try: page=int(params["page"])
except: page = 1

print ("Mode: "+str(mode))
print ("URL: "+str(url))
print ("Name: "+str(name))
print ("iconimage: "+str(iconimage))
print ("Page: "+str(page))
print ("Token: "+str(token))

		
def addDir(name,url,mode,iconimage):
        u=sys.argv[0]+"?url="+urllib.quote_plus(url)+"&mode="+str(mode)+"&name="+urllib.quote_plus(name)
        ok=True
        liz=xbmcgui.ListItem(name, iconImage="DefaultFolder.png", thumbnailImage=iconimage)
        liz.setProperty('fanart_image', fanart)
        ok=xbmcplugin.addDirectoryItem(handle=int(sys.argv[1]),url=u,listitem=liz,isFolder=True)
        return ok

def create_directory(dir_path, dir_name=None):
    if dir_name:
        dir_path = os.path.join(dir_path, dir_name)
    dir_path = dir_path.strip()
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    return dir_path

if mode==None or url==None or len(url)<1:
        print ""
        CATEGORIES()
       
elif mode==1:
        return_youtubevideos(name,url,token,page)

elif mode==5: 
        play_youtube_video(url)

elif mode==6:
        mark_as_watched(url)

elif mode==7:
        removed_watched(url)

elif mode==8:
        add_to_bookmarks(url)

elif mode==9:
        remove_from_bookmarks(url)
		
elif mode==10:
        print ""+url
        Movies()
		
elif mode==11:
        print ""+url
        Tv()

elif mode==12:
        print ""+url
        Cartoons()

elif mode==13:
        print ""+url
        Music()
        
elif mode==14:
        print ""+url
        News()

elif mode==15:
        print ""+url
        Sports()

elif mode==16:
        print ""+url
        youtube_dl()

elif mode==17:
        print ""+url
        Popcornflix()
                
xbmcplugin.endOfDirectory(int(sys.argv[1]))
