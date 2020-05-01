# coding: utf-8
# from browser import *
#
# Browser.open("https://thepiratebay.se")
#
# print Browser.content
#

# from storage import Storage
#
# storage = Storage("C:\\Users\\resua\\AppData\\Roaming\\Kodi\\addons\\script.module.mctools\\lib")
#
# # print storage.cached()
#
# source = storage['source']
#
# # source['url'] = "IT IS WORKING better"
# #
# # source.sync()
#
# print source['url']




# from storage import Storage
#
# storage = Storage("C:\\Users\\resua\\AppData\\Roaming\\Kodi\\addons\\script.module.mctools\\lib")
#
# movie = storage["movie"]
# #
# movie["tt3498820"] = {"Title": "Captain America: Civil War", "Year": "2016", "Rated": "PG-13",
#                       "Released": "06 May 2016", "Runtime": "147 min", "Genre": "Action, Adventure, Sci-Fi",
#                       "Director": "Anthony Russo, Joe Russo",
#                       "Writer": "Christopher Markus (screenplay), Stephen McFeely (screenplay), Mark Millar (comic book), Joe Simon (characters), Jack Kirby (characters)",
#                       "Actors": "Chris Evans, Robert Downey Jr., Scarlett Johansson, Sebastian Stan",
#                       "Plot": "With many people fearing the actions of super heroes, the government decides to push for the Hero Registration Act, a law that limits a heroes actions. This results in a division in The Avengers. Iron Man stands with this Act, claiming that their actions must be kept in check otherwise cities will continue to be destroyed, but Captain America feels that saving the world is daring enough and that they cannot rely on the government to protect the world. This escalates into an all-out war between Team Iron Man (Iron Man, Black Panther, Vision, Black Widow, War Machine, and Spiderman) and Team Captain America (Captain America, Bucky Barnes, Falcon, Sharon Carter, Scarlett Witch, Hawkeye, and Ant Man) while a new villain emerges",
#                       "Language": "Xhosa, English, German, Russian, Romanian", "Country": "USA, Germany",
#                       "Awards": "N/A",
#                       "Poster": "http://ia.media-imdb.com/images/M/MV5BMjQ0MTgyNjAxMV5BMl5BanBnXkFtZTgwNjUzMDkyODE@._V1_SX300.jpg",
#                       "Metascore": "75", "imdbRating": "8.4", "imdbVotes": "181,302", "imdbID": "tt3498820",
#                       "Type": "movie", "Response": "True"}
# #
# # movie.sync()
# print movie["tt3498820"]

# from storage import Storage
#
# storage_info = Storage("C:\\Users\\resua\\AppData\\Roaming\\Kodi\\addons\\script.module.mctools\\lib")
#
# movie = storage_info["movie"]
#
# movie.add('hello')
# print movie.has('hello')
# movie.remove('hello')
# movie.sync()
# print movie.has('http://ia.media-imdb.com/images/M/MV5BMjQ0MTgyNjAxMV5BMl5BanBnXkFtZTgwNjUzMDkyODE@._V1_SX300.jpg')

import untangle

# print untangle.format_title("Spectre 2015 720p BRRip x264 AAC-ETRG")
#
# print untangle.format_title('[4k ultra hd] San Andreas 4K SBS 6 Channel AAC  ENG 3D [SEEDERS (0) LEECHERS (0)]')
#
# print untangle.format_title('Spectre (2015) James Bond 007 [MULTI-AUDIO] [ENG, FRE, POR, SPA, RUS] [1080p] [HEVC] [x265]')
#
# print untangle.format_title('[ISLAND]One Piece 744 [FRENCH SUBBED] [720p].mp4', type_video='SHOW')

# a = untangle.Untangle('Spectre (2015) James Bond 007 [MULTI-AUDIO] [ENG, FRE, POR, SPA, RUS] 1080p [HEVC] [x265]', tmdb_api="8d0e4dca86c779f4157fc2c469c372ca")
# a = untangle.Untangle('Spectre (2015) James Bond 007 [MULTI-AUDIO] [ENG, FRE, POR, SPA, RUS] 1080p [HEVC] [x265]')
# a = untangle.Untangle('The expanse S01E03', tmdb_api="8d0e4dca86c779f4157fc2c469c372ca")
# a = untangle.Untangle('One piece Ep744', tmdb_api="8d0e4dca86c779f4157fc2c469c372ca")

a = untangle.Untangle('The Revenant', ' http://torrentapi.org/pubapi_v2.php?mode=search&search_imdb=tt1663202&limit=100', imdb_id='tt1663202', tmdb_api="8d0e4dca86c779f4157fc2c469c372ca")

print a.title
print a.proper_title
print a.label
print a.imdb_id
print a.info_title
print a.info_labels
print a.info
print a.info_stream
print a.episode
print a.season
print a.cover
print a.fanart
del a

