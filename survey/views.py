# -*- coding: UTF-8 -*-
from django.shortcuts import render
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.core.exceptions import ObjectDoesNotExist
from survey.models import PreSurvey, PostSurvey
from student.models import Enroll
from teacher.models import Classroom
from account.models import Log

pre_questions = [
        '1. 我很崇拜程式設計很厲害的人',
        '2. 我對學習程式設計感到有興趣',
        '3. 我認為程式設計可以讓我創作有趣的作品',
        '4. 我希望將來能夠自己設計應用軟體或電腦遊戲',
        '5. 學好程式設計在現代社會中是很重要的',
        '6. 我自信能夠將程式設計所教的基本概念學好',
        '7. 我會盡力將程式設計課程的作業寫好',
        '8. 我覺得程式設計的過程將會非常單調、枯燥',
        '9. 如果老師出的程式設計作業很難，我想我會直接放棄',
        '10. 我和同學或朋友聊天時會談到程式設計相關的事情',
]


sections = [
        '一、學習動機',
		'二、學習自信',
		'三、學習經驗',
		'四、學習氣氛',
		'五、未來發展',
]

post_questions = [
        ['一、學習動機', [
		    ['1. 創作遊戲能夠提高我學習Scratch程式設計的興趣',11,2,3,4],
            ['2. 使用Scratch程式設計撰寫遊戲，讓我覺得很有成就感',11,2,3,4],
            ['3. 學過Scratch創作遊戲後，我覺得學習程式設計概念很無趣',11,2,3,4],
            ['4. 網站積分式的學習，可以促發我的學習動機',11,2,3,4],
            ['5. 網站循序漸進、個別化的學習方式可以促進我學習的動機',11,2,3,4],
        ]],
        ['二、學習自信', [
            ['6. 我覺得Scratch程式設計軟體容易學習',11,2,3,4],
            ['7. 我認為Scratch程式設計可以讓我創作有趣的作品',11,2,3,4],
            ['8. 使用Scratch程式設計撰寫遊戲，讓我覺得很有成就感',11,2,3,4],
            ['9. 學完此門課後，我能精通程式設計的方法與技能',11,2,3,4],
            ['10. 學完此門課後，我能理解程式設計這門課最困難的部分',11,2,3,4],
        ]],
        ['三、學習經驗', [
            ['11. 我能從Scratch程式設計課程中得到很大的收穫',11,2,3,4],
            ['12. 我能了解影片所講解的觀念並順利完成指派的題目',11,2,3,4],
            ['13. 在實作遊戲時，我很清楚知道自己在做什麼',11,2,3,4],
            ['14. 我會拿自己的學習狀況與同學做比較',11,2,3,4],
            ['15. 學完此課程後，我喜歡程式設計課程的內容',11,2,3,4],
        ]],
        ['四、學習氣氛', [
            ['16. 上課時，多數同學都認真學習並解決問題',11,2,3,4],
            ['17. 上課時，同學會互相觀摩作品與分享彼此想法',11,2,3,4],
            ['18. 上課時，我會詢問老師我不懂的地方，以澄清概念',11,2,3,4],
            ['19. 上課時，當我在這門課遇到不懂的地方時，我會尋求其他同學的幫忙',11,2,3,4],
            ['20. 上課時，教室上課氣氛很愉悅',11,2,3,4],
        ]],
        ['五、未來發展', [
            ['21. 我希望將來能夠自己設計應用軟體或電腦遊戲',11,2,3,4],
            ['22. 學完此課程後，我對學習其他的程式設計感到有興趣',11,2,3,4],
            ['23. 如果學校有開設遊戲設計的社團，我會想要參加',11,2,3,4],
            ['24. 學完此課程後，我認為學好程式設計在現代社會中是很重要的',11,2,3,4],
            ['25. 學完此課程後，我認為我能夠將程式設計課程所學到的（如問題解決、邏輯思考、自學能力與創造力等），運用到其他科目上',11,2,3,4],
        ]],
]
	
# 判斷是否開啟事件記錄
def is_event_open(request):
        enrolls = Enroll.objects.filter(student_id=request.user.id)
        for enroll in enrolls:
            classroom = Classroom.objects.get(id=enroll.classroom_id)
            if classroom.event_open:
                return True
        return False

# Create your views here.
def pre_result(request, classroom_id):
    classroom = Classroom.objects.get(id=classroom_id)
    enrolls = Enroll.objects.filter(classroom_id=classroom_id)
    questionaires = []
    questions = []
    questions.append(['我曾經學過程式設計。',0,0])
    for index, question in enumerate(pre_questions):
        questions.append([pre_questions[index],0,0,0,0])
    for enroll in enrolls:
        try:
            questionaire = PreSurvey.objects.get(student_id=enroll.student_id)
            questions[0][2-questionaire.p]+=1
            questions[1][5-questionaire.p1]+=1
            questions[2][5-questionaire.p2]+=1
            questions[3][5-questionaire.p3]+=1
            questions[4][5-questionaire.p4]+=1
            questions[5][5-questionaire.p5]+=1
            questions[6][5-questionaire.p6]+=1
            questions[7][5-questionaire.p7]+=1
            questions[8][5-questionaire.p8]+=1
            questions[9][5-questionaire.p9]+=1
            questions[10][5-questionaire.p10]+=1
            questionaires.append(questionaire)						
        except ObjectDoesNotExist : 
            pass
    return render_to_response('survey/pre_result.html', {'enrolls':enrolls, 'result':questions, 'questions': pre_questions, 'classroom':classroom, 'questionaires':questionaires},context_instance=RequestContext(request))


def post_result(request, classroom_id):
    return render_to_response('survey/post_result.html', {'questions': post_questions},context_instance=RequestContext(request))
	
def pre_survey(request):
    try:
        questionaire = PreSurvey.objects.get(student_id=request.user.id)
    except ObjectDoesNotExist :
        questionaire = PreSurvey(student_id=request.user.id)
    questions = []
    questions.append([pre_questions[0], questionaire.p1])		
    questions.append([pre_questions[1], questionaire.p2])		
    questions.append([pre_questions[2], questionaire.p3])		
    questions.append([pre_questions[3], questionaire.p4])
    questions.append([pre_questions[4], questionaire.p5])		
    questions.append([pre_questions[5], questionaire.p6])		
    questions.append([pre_questions[6], questionaire.p7])		
    questions.append([pre_questions[7], questionaire.p8])		
    questions.append([pre_questions[8], questionaire.p9])		
    questions.append([pre_questions[9], questionaire.p10])		
    if request.method == 'POST':
            questionaire.p = request.POST['p1']
            questionaire.p_t = request.POST['p1t']
            questionaire.p1 = request.POST['p2_1']
            questionaire.p2 = request.POST['p2_2']
            questionaire.p3 = request.POST['p2_3']
            questionaire.p4 = request.POST['p2_4']
            questionaire.p5 = request.POST['p2_5']
            questionaire.p6 = request.POST['p2_6']
            questionaire.p7 = request.POST['p2_7']
            questionaire.p8 = request.POST['p2_8']
            questionaire.p9 = request.POST['p2_9']
            questionaire.p10 = request.POST['p2_10']
            questionaire.save()

            # 記錄系統事
            if is_event_open(request) :                  
                log = Log(user_id=request.user.id, event=u'填寫課前問卷'+request.user.first_name+'>')
                log.save()        
        
            return redirect('/student/lesson/1')
    return render_to_response('survey/pre_survey.html', {'questionaire':questionaire,'questions': questions},context_instance=RequestContext(request))

def post_survey(request):
    return render_to_response('survey/post_survey.html', {'questions': post_questions, 'sections': sections},context_instance=RequestContext(request))
