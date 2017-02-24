# -*- coding: UTF-8 -*-
from models import Log
from django.db.models import Q
from student.video import *
from django.utils import timezone
from django.utils.timezone import localtime
from datetime import datetime
from django.utils import timezone
import re


class VideoLogHelper:

    def _calculate(self, events):
        start_time = ''
        videos = {}
        for event in events:
            # 查看課程內容<1> | 影片：為什麼要學程式設計 | PAUSE[00:07:56]
            lesson, tabname, action, time = re.search(
                "<([^ ]+)> *\| *([^ ]+) *\| *(PLAY|PAUSE|STOP)\[(.+)\]", event.event).groups()
            tabname = tabname.encode('utf-8')
            if action == 'PLAY':
                start_log_time = event.publish
                start_time = time
            if start_time and (action in ['PAUSE', 'STOP']):
                if (lesson, tabname) in video_url:
                    if (lesson, tabname) not in videos:
                        videos[lesson, tabname] = []
                    tmp = start_time.split(":")
                    tfrom = int(tmp[0]) * 3600 + int(tmp[1]) * 60 + int(tmp[2])
                    length = int(
                        (event.publish - start_log_time).total_seconds())
                    tto = tfrom + length
                    videos[lesson, tabname].append({'stamp': str(localtime(start_log_time).strftime(
                        "%Y-%m-%d %H:%M:%S")), 'from': tfrom, 'to': tto, 'length': length, 'duration': video_duration[video_url[lesson, tabname.encode("UTF-8")]]})
                    searching = False
        return videos

    def getLogByUserid(self, userid):
        event_list = ['PLAY', 'PAUSE', 'STOP']
        events = Log.objects.filter(Q(user_id=userid), reduce(lambda x, y: x | y, [
                                    Q(event__contains=word) for word in event_list])).order_by("id")
        return self._calculate(events)

    def getLogByUserid_Lesson_Tab(self, userid, lesson, tab):
        events = self.getLogByUserid(userid)
        try:
            return events[lesson, tab]
        except:
            return []
