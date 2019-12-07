from operator import itemgetter
import threading
import traceback
import time
import xbmc
from ump import teamkodi


#simple task manager but quite handy one
#can monitor different task groups and wait them to finish seperately
#can also priotrize the tasks  
#concurrentcy may be set to CPU count however my app heavily uses network stuff so i use more than 10 or more.
#dont mess with thread names
class killbill(Exception):
	pass
	
class manager(object):
	def __init__(self, dialogpg,concurrent=4):
		self.dialogpg=dialogpg
		self.c = concurrent #concurrency count, runtime changable
		self.s = threading.Event() #stop flag
		self.q = [] #queue for the function when concurrency is not available
		self.p = [] #processed tasks
		self.g = [] #group ids
		self.m = teamkodi.backwards()

	def task(self,func,args):
		try:
			val=func(*args)
		except killbill:
			self.q=[]
			self.s.set()
			return None
		except Exception:
			print traceback.format_exc()
			val=None

		if threading.activeCount()-1<=self.c and len(self.q)>0 and not self.s.isSet(): 
			self.q=sorted(self.q,key=itemgetter(1),reverse=True)
			t=self.q.pop(0)
			self.p.append(t)
			t[2].start()
		return val

	
	def add_queue(self,target,args,gid=0,pri=0):
		if not self.s.isSet():
			args=(target,args)
			t=threading.Thread(target=self.task,args=args)
			g=self.g
			g.append(gid)
			self.g=list(set(g))
			q,a,p=self.stats(gid)
			if a<=self.c:
				t.start()
				self.p.append((gid,pri,t))
				return t.name
			else:
				self.q.append((gid,pri,t))
				return t.name
		else:
			return None

	def stop(self):
		self.dialogpg.close()
		self.s.set()
		self.q=[]
		while True:
			self.join()
			break
				

	def join(self,gid=None,cnt=0,noblock=0):
		q,a,p=self.stats(gid)
		if cnt=="all":
			cnt=q+a
		if noblock=="all":
			noblock=q+a
		i=0
		while not (self.m.abortRequested() or self.s.isSet()):
			xbmc.sleep(800)
			i+=1
			q,a,p=self.stats(gid)
			if cnt>0 and not q+a==0:
				self.dialogpg.update(100-100*(q+a)/cnt,message="%d of %d"%(cnt-q-a,cnt))
			if (self.s.isSet() or q==0) and a<=noblock:
				break
		return q,a,p
	
	def	create_gid(self):
		return time.time()
		
	def stats(self,gid=None):
		q=0 #on queue
		p=0	#already processed
		a=0 #active thread
		ps= self.p
		qs= self.q
		t=[x.name for x in threading.enumerate()] #all active thread names
		for p1 in ps:
			if not p1[2].name in t and (gid is None and p1[0] in self.g or gid==p1[0]):
				p+=1
			if p1[2].name in t and (gid is None and p1[0] in self.g or gid==p1[0]):
				a+=1
		for q1 in qs:
			if gid is None and q1[0] in self.g or gid==q1[0]:
				q+=1
		return q,a,p