

class ViewerExperienceRequest(object):
   def __init__(self, URL, contentOverrides, experienceId, playerKey, TTLToken=''):
      self.TTLToken = TTLToken
      self.URL = URL
      self.deliveryType = float(0)
      self.contentOverrides = contentOverrides
      self.experienceId = experienceId
      self.playerKey = playerKey

class ContentOverride(object):
   def __init__(self, contentId = float(0), contentIds = None, contentRefId = None, contentRefIds = None, contentType = 0, featureId = float(0), featuredRefId = None, contentRefIdtarget='videoPlayer'):
      self.contentType = contentType
      self.contentId = contentId
      self.target = contentRefIdtarget
      self.contentIds = contentIds
      self.contentRefId = contentRefId
      self.contentRefIds = contentRefIds
      self.featureId = featureId
      self.featuredRefId = None

def BuildAmfRequest(amf_constant, url, experience_id, player_key, content_id=None, content_ref_id=None):

    import pyamf
    from pyamf import remoting
    
    pyamf.register_class(ViewerExperienceRequest, 'com.brightcove.experience.ViewerExperienceRequest')
    pyamf.register_class(ContentOverride, 'com.brightcove.experience.ContentOverride')
    content_override = ContentOverride(contentRefId = content_ref_id, contentId = content_id)
    viewer_exp_req = ViewerExperienceRequest(url, [content_override], int(experience_id), player_key)
    
    env = remoting.Envelope(amfVersion=3)
    env.bodies.append(
        ( 
            "/1",
            remoting.Request(
                target="com.brightcove.experience.ExperienceRuntimeFacade.getDataForExperience",
                body=[amf_constant, viewer_exp_req],
                envelope=env
            )
        )
    )
       
    return env
       
def GetPlayableUrl(amf_constant, url, experience_id, player_key, content_id=None, content_ref_id=None):       
    
    from pyamf import remoting
    from entertainment.net import Net
    net = Net()
    
    amf_request_data = BuildAmfRequest(amf_constant, url, experience_id, player_key, content_id=content_id, content_ref_id=content_ref_id)
    amf_encoded_request_data = remoting.encode(amf_request_data).read()
    
    amf_encoded_response_data = net.http_POST_BINARY(
                                    'http://c.brightcove.com', 
                                    "/services/messagebroker/amf?playerKey=" + player_key.encode('ascii'),
                                     amf_encoded_request_data, 
                                     headers = {'content-type': 'application/x-amf'} ).content
                                     
    amf_response_data = remoting.decode(amf_encoded_response_data).bodies[0][1].body
    
    playable_url = amf_response_data['programmedContent']['videoPlayer']['mediaDTO']['FLVFullLengthURL']
    
    # do something with renditions ... to get best quality
    # renditions = amf_response_data['programmedContent']['videoPlayer']['mediaDTO']['renditions']
    # sample renditions below
    '''
    'renditions': [{'videoCodec': u'ON2', 'defaultURL': u'http://brightcove03-f.akamaihd.net/3abnEnglishF_3ABN_250@100395', 
    'encodingRate': 250000, 'audioOnly': False, 'videoContainer': 1, 'mediaDeliveryType': 0, 'frameWidth': 384, 'size': 0.0, 'frameHeight': 512}, 
    {'videoCodec': u'ON2', 'defaultURL': u'http://brightcove03-f.akamaihd.net/3abnEnglishF_3ABN_600@100395', 'encodingRate': 600000, 'audioOnly': False, 
    'videoContainer': 1, 'mediaDeliveryType': 0, 'frameWidth': 480, 'size': 0.0, 'frameHeight': 640}, 
    {'videoCodec': u'ON2', 'defaultURL': u'http://brightcove03-f.akamaihd.net/3abnEnglishF_3ABN_64@100395', 'encodingRate': 64000, 'audioOnly': False, 
    'videoContainer': 1, 'mediaDeliveryType': 0, 'frameWidth': 240, 'size': 0.0, 'frameHeight': 320}, 
    {'videoCodec': u'ON2', 'defaultURL': u'http://brightcove03-f.akamaihd.net/3abnEnglishF_3ABN_1200@100395', 'encodingRate': 1200000, 'audioOnly': False, 
    'videoContainer': 1, 'mediaDeliveryType': 0, 'frameWidth': 480, 'size': 0.0, 'frameHeight': 720}]
    '''
    
    return playable_url