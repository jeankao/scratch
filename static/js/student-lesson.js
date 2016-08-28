CKEDITOR.plugins.add('dreamerpasteimage', {
    init: function(editor) {
        editor.on('paste', function(e) {
            var reader = new FileReader();
            reader.onload = function(evt) {
                var img = CKEDITOR.dom.element.createFromHtml("<img src='"+evt.target.result+"' />");
                e.editor.insertElement(img);
            }
            e.data.dataTransfer._.files.forEach(function(file, index) {
                console.log('paste: '+index);
                reader.readAsDataURL(file);
            });
        });
    },
});

function onYouTubeIframeAPIReady() {
    $('ul.tabs li a').each(function(index, element){
        tabName[$(element).attr('href').substr(1)] = $(element).text();
    });    
    $('iframe[src*="www.youtube.com"]').each(function(index,element){
        var playerID = $(element).parent().attr('id')+'_player';
        $(element).attr('id', playerID);
        player = new YT.Player(playerID, {
            events: {
                'onStateChange': onPlayerStateChange
            }
        });
        player.tabName = tabName[$(element).parent().attr('id')];
        playerPool[playerID] = player;
    });
}

function secToTime(sec) {
    return (new Date(sec*1000)).toUTCString().split(' ')[4];
}

function onPlayerStateChange(event) {
    activePlayer = event.target;
    currTime = secToTime(activePlayer.getCurrentTime().toFixed());
    switch(event.data) {
        case YT.PlayerState.ENDED:
            lesson_log(activePlayer.tabName+" | STOP["+currTime+"]"); break;
        case YT.PlayerState.PLAYING:
            lesson_log(activePlayer.tabName+" | PLAY["+currTime+"]"); break;
        case YT.PlayerState.PAUSED:
            lesson_log(activePlayer.tabName+" | PAUSE["+currTime+"]"); break;
    }
}

function openNote(evt, noteName) {
    // Declare all variables
    var i, tabcontent, tablinks;

    // Get all elements with class="tabcontent" and hide them
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }

    // Get all elements with class="tablinks" and remove the class "active"
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }

    // Show the current tab, and add an "active" class to the link that opened the tab
    document.getElementById(noteName).style.display = "block";
    evt.currentTarget.className += " active";
}

function note_add(noteName, classroom_id, lesson, note_id) {
    // Show the current tab, and add an "active" class to the link that opened the tab
	memo = "id_"+noteName+"_memo";
	if (note_id == 0) {
	    $('input.note_submit').attr('data-noteid',0);	
        document.getElementById(memo).value = "";
	} else {
	    $('input.note_submit').attr('data-noteid',note_id);
		document.getElementById(memo).value = $("div.note_content_"+note_id).html();
	}
	var editor = CKEDITOR.instances[memo];
    if (editor) { editor.destroy(true); }
    CKEDITOR.replace(memo, {
        extraPlugins: 'colorbutton,colordialog,dreamerpasteimage',
    } );
    document.getElementById(noteName).style.display = "none";
    document.getElementById(noteName+'_form').style.display = "block";
}

function lesson_log(tabname) {
    $.post('/student/lesson/log/{{lesson}}/',
        {'tabname': tabname},
        function(data){}
    );
}

var playerPool = [];
var tabName = [];
var activePlayer = null;
$(function () {
    $(document).scrollTop(0);
    $('.block article').hide();
    var defaultTab = $('ul.tabs li:first');
    var defaultArticle = $('.block article:first');
    var searchTab = (location.hash && $(location.hash));
    $('ul.tabs li a').each(function(index, element){
        tabName[$(element).attr('href').substr(1)] = $(element).text();
        if(searchTab && $(element).attr('href') === location.hash) {
            defaultTab = $(element).parent();
            defaultArticle = $(location.hash);
        }
    });
    $(defaultTab).addClass('active');
    $(defaultArticle).show();
	$.post('/account/video/log/',
    	{
  	    	'tabName' : defaultTab.text(),
        	'lesson' : "{{lesson}}",
   	    },
   	    function(data){	
   	        var logs = data['text'].split("##");
   	        var video = document.getElementById("videolog")
   	        video.innerHTML = ""   	        
    	    function myFunction(item, index) {
                video.innerHTML = video.innerHTML + item + "<br />"; 
            }
   	        logs.forEach(myFunction);
        }
    );
    
    lesson_log($(defaultTab).find('a').text());
    $('ul.tabs li').on('click', function () {
        if (activePlayer) {
            if (activePlayer.getPlayerState()==1) {
            activePlayer.pauseVideo();
            activePlayer = null;
            }
        }
        var activeTab = $(this).find('a');        
   	    var video = document.getElementById("videolog")        
        if (activeTab.text().startsWith("影片")) {
    		$.post('/account/video/log/',
	        	{
		  	    	'tabName' : activeTab.text(),
		        	'lesson' : "{{lesson}}",
		   	    },
		   	    function(data){	
   	                var logs = data['text'].split("##");
 		   	        video.innerHTML = ""  	                
    	            function myFunction(item, index) {
                        video.innerHTML = video.innerHTML + item + "<br />"; 
                    }
   	                logs.forEach(myFunction);
                }
            );
            video.style.display = "block";
        } else {
            video.style.display = "none";
        }
        $('ul.tabs li').removeClass('active');
        $(this).addClass('active');
        $('.block article').hide();
        $(activeTab.attr('href')).show();
        lesson_log(activeTab.text());
        return false;
    });
    $(window).on('beforeunload', function(){
        if (activePlayer) {
            if (activePlayer.getPlayerState()==1) {
            var currTime = secToTime(activePlayer.getCurrentTime().toFixed());
            lesson_log(activePlayer.tabName+" | PAUSE["+currTime+"]");
            }
        }
    });
    //------------------------------------------------------------------------
    // Load YouTube API library
    var tag = document.createElement('script');
    tag.id = 'iframe-demo';
    tag.src = 'https://www.youtube.com/iframe_api';
    var firstScriptTag = document.getElementsByTagName('script')[0];
    firstScriptTag.parentNode.insertBefore(tag, firstScriptTag);

	$('input.note_submit').click(function(e){
	    var classroomname = $(this).data('classroomname');
		var classroomid = $(this).data('classroomid');
		var lesson = $(this).data('lesson');
		var userid = $(this).data('userid');
		var noteid = $(this).attr('data-noteid');
        console.log('noteid = '+noteid);
        console.log('userid = '+userid);
        console.log('lesson = '+lesson);
        console.log('classroomid = '+classroomid);
        console.log('classroomname = '+classroomname);
        CKEDITOR.instances['id_'+classroomname+'_memo'].updateElement();
		var memo = document.getElementById("id_" + classroomname+ "_memo").value;
		$.post('/account/note/add/',
			{
				'classroomid' : classroomid,
				'lesson' : lesson,
				'memo': memo,
				'userid': userid,
				'noteid': noteid,
			},
			function(data){			
                $.post('/account/note/get/',
                    {
                        'classroomid' : classroomid,
                        'lesson' : lesson,
                        'userid' : userid,
                    },
                    function(data){
                        $('div.'+classroomname+'_note').html(data['note_text']);
                    }
                );         
                document.getElementById(classroomname+"_form").style.display = "none";        
                document.getElementById(classroomname).style.display = "block";			
            }
        );
	});
});
