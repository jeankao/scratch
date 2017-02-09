# -*- coding: UTF-8 -*-
from models import Log
from django.db.models import Q
from student.video import *
from django.utils import timezone
from django.utils.timezone import localtime
from datetime import datetime
from django.utils import timezone

class VideoLogHelper:
		def _calculate(self, events):
				searching = False
				start_time = ""
				videos = {}
				for event in events:
						video = event.event.split("|")
						lesson = video[0][video[0].find("<")+1:video[0].find(">")].encode("utf-8")
						action = video[2][1:video[2].find("[")]            
						tabName = video[1][1:-1].encode("utf-8")
						time = video[2][video[2].find("[")+1:video[2].find("]")]
						if not searching and action == "PLAY" :
								start_log_time = event.publish
								start_time = time
								searching = True
						if searching and ( action == "PAUSE" or action == "STOP") :
								if (lesson, tabName) in video_url :
										if (lesson, tabName) not in videos:
												videos[lesson, tabName] = []
										tmp = start_time.split(":")
										tfrom = int(tmp[0])*3600+int(tmp[1])*60+int(tmp[2])
										tmp = time.split(":")
										length = int((event.publish - start_log_time).total_seconds())
										tto = tfrom + length
										videos[lesson, tabName].append({'stamp':str(localtime(start_log_time).strftime("%Y-%m-%d %H:%M:%S")),'from':tfrom,'to':tto,'length':length, 'duration':video_duration[video_url[lesson, tabName.encode("UTF-8")]]})
										start_time = ""
										searching = False
				return videos
				
		def getLogByUserid(self, userid):
				event_list = ['PLAY', 'PAUSE', 'STOP']
				events = Log.objects.filter(Q(user_id=userid), reduce(lambda x, y: x | y, [Q(event__contains=word) for word in event_list])).order_by("id")
				return self._calculate(events)

		def getLogByUserid_Lesson_Tab(self, userid, lesson, tab):
				events = self.getLogByUserid(userid)
				try:
						return events[lesson, tab]
 				except:
						return []
