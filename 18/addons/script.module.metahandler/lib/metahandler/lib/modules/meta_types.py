def init_movie_meta(imdb_id, tmdb_id, name, year=0):
    '''
    Initializes a movie_meta dictionary with default values, to ensure we always
    have all fields
    
    Args:
        imdb_id (str): IMDB ID
        tmdb_id (str): TMDB ID
        name (str): full name of movie you are searching
        year (int): 4 digit year
                    
    Returns:
        DICT in the structure of what is required to write to the DB
    '''                
    
    if year:
        int(year)
    else:
        year = 0
        
    meta = {}
    meta['imdb_id'] = imdb_id
    meta['tmdb_id'] = str(tmdb_id)
    meta['title'] = name
    meta['year'] = int(year)
    meta['writer'] = ''
    meta['director'] = ''
    meta['tagline'] = ''
    meta['cast'] = []
    meta['rating'] = 0
    meta['votes'] = ''
    meta['duration'] = ''
    meta['plot'] = ''
    meta['mpaa'] = ''
    meta['premiered'] = ''
    meta['trailer_url'] = ''
    meta['genre'] = ''
    meta['studio'] = ''       
    meta['thumb_url'] = ''
    meta['cover_url'] = ''
    meta['backdrop_url'] = ''
    meta['overlay'] = 6
    return meta


def init_tvshow_meta(imdb_id, tvdb_id, name, year=0):
    '''
    Initializes a tvshow_meta dictionary with default values, to ensure we always
    have all fields
    
    Args:
        imdb_id (str): IMDB ID
        tvdb_id (str): TVDB ID
        name (str): full name of movie you are searching
        year (int): 4 digit year
                    
    Returns:
        DICT in the structure of what is required to write to the DB
    '''
    
    if year:
        int(year)
    else:
        year = 0
        
    meta = {}
    meta['imdb_id'] = imdb_id
    meta['tvdb_id'] = tvdb_id
    meta['title'] = name
    meta['TVShowTitle'] = name
    meta['rating'] = 0
    meta['duration'] = ''
    meta['plot'] = ''
    meta['mpaa'] = ''
    meta['premiered'] = ''
    meta['year'] = int(year)
    meta['trailer_url'] = ''
    meta['genre'] = ''
    meta['studio'] = ''
    meta['status'] = ''        
    meta['cast'] = []
    meta['banner_url'] = ''  
    meta['cover_url'] = ''
    meta['backdrop_url'] = ''
    meta['overlay'] = 6
    meta['episode'] = 0
    meta['playcount'] = 0
    return meta


def init_episode_meta(imdb_id, tvdb_id, episode_title, season, episode, air_date):
    '''
    Initializes a movie_meta dictionary with default values, to ensure we always
    have all fields
    
    Args:
        imdb_id (str): IMDB ID
        tvdb_id (str): TVDB ID
        episode_title (str): full name of Episode you are searching - NOT TV Show name
        season (int): episode season number
        episode (int): episode number
        air_date (str): air date (premiered data) of episode - YYYY-MM-DD
                    
    Returns:
        DICT in the structure of what is required to write to the DB
    '''

    meta = {}
    meta['imdb_id']=imdb_id
    meta['tvdb_id']=''
    meta['episode_id'] = ''                
    meta['season']= int(season)
    meta['episode']= int(episode)
    meta['title']= episode_title
    meta['director'] = ''
    meta['writer'] = ''
    meta['plot'] = ''
    meta['rating'] = 0
    meta['premiered'] = air_date
    meta['poster'] = ''
    meta['cover_url']= ''
    meta['trailer_url']=''
    meta['premiered'] = ''
    meta['backdrop_url'] = ''
    meta['overlay'] = 6
    return meta