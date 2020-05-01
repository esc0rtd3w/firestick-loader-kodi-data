import SimpleDownloader as downloader


addon_id = 'plugin.video.moviedb'
downloader = downloader.SimpleDownloader()

def downloadFile(url):
     download_folder = settings.getSetting('download_folder')
     if download_folder == '':
          addon.show_small_popup(title='File Not Downloadable', msg='You need to set your download folder in addon settings first', delay=int(5000), image=thumb)
     else:     
          if resolvable(url):
               url = resolve(url)
               ext = ''
               if '.mp4' in url:
                    ext = '.mp4'
               elif '.flv' in url:
                    ext = '.flv'
               elif '.avi' in url:
                    ext = '.avi'
               if not ext == '':
                    if not os.path.exists(download_folder):
                         os.makedirs(download_folder)

                    params = {"url":url, "download_path":download_folder}
                    downloader.download(name + ext, params)
               else:
                    addon.show_small_popup(title='Can Not Download File', msg='Unsupported Host', delay=int(5000), image=thumb)
          else:
               addon.show_small_popup(title='Can Not Download File', msg='Unable To Resolve Url', delay=int(5000), image=thumb)
                              
