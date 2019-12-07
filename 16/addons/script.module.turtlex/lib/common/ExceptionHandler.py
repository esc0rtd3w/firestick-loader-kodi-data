'''
Created on Dec 17, 2011

@author: ajju
'''
import XBMCInterfaceUtils

USER_PWD_NOT_PROVIDED = 1
USER_PWD_INCORRECT = 2
CATEGORY_NOT_SELECTED = 3
TV_CHANNELS_NOT_LOADED = 4
VIDEO_PARSER_NOT_FOUND = 101
VIDEO_STOPPED = 102
PROCESS_STOPPED = 103

DONOT_DISPLAY_ERROR = 0
UNKNOWN_SYSTEM_ERROR = {'display':True, 'heading':'Unknown error occurred'}

EXCEPTIONS = {
                  USER_PWD_NOT_PROVIDED:{'display':True, 'heading':'User credential not provided'},
                  USER_PWD_INCORRECT:{'display':True, 'heading':'User credential incorrect'},
                  CATEGORY_NOT_SELECTED:{'display':True, 'heading':'Category not selected'},
                  TV_CHANNELS_NOT_LOADED:{'display':True, 'heading':'TV Channels loading failed'},
                  VIDEO_PARSER_NOT_FOUND:{'display':False, 'heading':'Video parser not found'},
                  VIDEO_STOPPED:{'display':False, 'heading':'Video is removed'},
                  PROCESS_STOPPED:{'display':True, 'heading':'Video is removed'},
                  DONOT_DISPLAY_ERROR:{'display':False, 'heading':''}
              }


def handle(e):
    exceptionObj = UNKNOWN_SYSTEM_ERROR
    if (EXCEPTIONS.has_key(e[0])):
        exceptionObj = EXCEPTIONS[e[0]]
        
    if exceptionObj['display']:
        heading = exceptionObj['heading']
        emessage = ''
        if exceptionObj == UNKNOWN_SYSTEM_ERROR:
            for msg in e:
                emessage = emessage + msg + '|'
        else:
            emessage = e[1]
        
        XBMCInterfaceUtils.displayDialogMessage(heading=heading, dmessage=emessage)

        
