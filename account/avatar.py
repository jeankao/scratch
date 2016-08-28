# -*- coding: UTF-8 -*-
from account.models import Profile

def update_avatar(user_id, kind, point):
	if kind == 1 : #作業		
		profile = Profile.objects.get(user_id=user_id)
		profile.work = profile.work + point
	elif kind == 2 : #小老師
		profile = Profile.objects.get(user_id=user_id)
		profile.assistant = profile.assistant + point
	elif kind == 3 : #除錯
		profile = Profile.objects.get(user_id=user_id)	
		profile.debug = profile.debug + point
	elif kind == 4 : #創意秀
		profile = Profile.objects.get(user_id=user_id)	
		profile.creative = profile.creative + point		
	total = profile.work + profile.assistant + profile.debug + profile.creative
	if total >= 300:
		avatar = 300
	elif total >=275:
		avatar = 275
	elif total >=250:
		avatar = 250
	elif total >=225:
		avatar = 225
	elif total >=200:
		avatar = 200
	elif total >=180:
		avatar = 180
	elif total >=160:
		avatar = 160
	elif total >=140:
		avatar = 140
	elif total >=120:
		avatar = 120
	elif total >=100:
		avatar = 100
	elif total >=90:
		avatar = 90
	elif total >=80:
		avatar = 80
	elif total >=70:
		avatar = 70
	elif total >=60:
		avatar = 60
	elif total >=50:
		avatar = 50
	elif total >=40:
		avatar = 40
	elif total >=30:
		avatar = 30
	elif total >=20:
		avatar = 20
	elif total >=10:
		avatar = 10
	else:
		avatar = 0
	profile.avatar = avatar
	profile.save()
	
