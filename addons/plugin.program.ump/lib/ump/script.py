from sys import argv
import urllib
import xbmc

if len(argv)>1:
	if argv[1]=="addfav":
		from bookmark import add
		add(argv[2].lower()=="true",argv[3],argv[4],argv[5],argv[6])
	elif argv[1]=="delfav":
		from bookmark import rem
		rem(argv[2],argv[3],argv[4])
	elif argv[1]=="renfav":
		from bookmark import ren
		ren(argv[2],argv[3],argv[4])
	elif argv[1]=="forcebuf":
		from buffering import force
		force(argv[2])
	elif argv[1]=="setview":
		from prefs import set_view
		set_view(argv[2],argv[3])
	elif argv[1]=="markseen":
		from stats import stats
		import json
		st=stats()
		st.markseen(json.loads(urllib.unquote_plus(argv[2])),json.loads(urllib.unquote_plus(argv[3])))
		xbmc.executebuiltin("Container.Refresh")
	elif argv[1]=="markunseen":
		from stats import stats
		import json
		st=stats()
		st.markunseen(json.loads(urllib.unquote_plus(argv[2])),json.loads(urllib.unquote_plus(argv[3])))
		xbmc.executebuiltin("Container.Refresh")
		