const TEC_CLASS = ['python', 'java', 'C++', '数据库', '其他', 'C语言']
const NO_TEC_CLASS = ['sport', 'food', 'sign', 'relaxation', 'no-tec']


$(document).ready(function () {
    //检测ie 6789
    if (!(/msie [6|7|8|9]/i.test(navigator.userAgent))) {
        window.scrollReveal = new scrollReveal({
            reset: true
        });
    }
    // 弹窗回复评论
    var list = document.getElementsByClassName('replyComment');
    for (var i of list) {
        i.addEventListener("click", function (ev) {
            ev.preventDefault();
            var txt = "请输入回复：";
            window.wxc.xcConfirm(txt, window.wxc.xcConfirm.typeEnum.input, {
                onOk: function (reply) {
                    console.log(reply);
                }
            });
        }, false);
    }

    /*nav show or hide*/
    $('.nav>li').hover(function () {
        $(this).children('ul').stop(true, true).show(400);
    }, function () {
        $(this).children('ul').stop(true, true).hide(400);
    });
    /*search*/
    $('.search_ico').click(function () {
        $('.search_bar').toggleClass('search_open');
        if ($('#keyboard').val().length > 2) {
            $('#keyboard').val('');
            $('#searchform').submit();
        } else {
            return false;
        }
    });
    /*banner*/
    $('#banner').easyFader();


    //设置固定关注我们

    if (document.getElementById('follow-us')) {
        var followUsPosition = $('#follow-us').offset().top;
        window.onscroll = function () {
            var nowPosition = document.documentElement.scrollTop;
            if (nowPosition - followUsPosition > 0) {
                setTimeout(function () {
                    $('#follow-us').attr('class', 'guanzhu gd');
                }, 150);
            } else {
                $('#follow-us').attr('class', 'guanzhu');
            }
        };
    }


    //回到顶部
    // browser window scroll (in pixels) after which the "back to top" link is shown
    var offset = 300,
        //browser window scroll (in pixels) after which the "back to top" link opacity is reduced
        offset_opacity = 1200,
        //duration of the top scrolling animation (in ms)
        scroll_top_duration = 700,
        //grab the "back to top" link
        $back_to_top = $('.cd-top');

    //hide or show the "back to top" link
    $(window).scroll(function () {
        ($(this).scrollTop() > offset) ? $back_to_top.addClass('cd-is-visible') : $back_to_top.removeClass('cd-is-visible cd-fade-out');
        if ($(this).scrollTop() > offset_opacity) {
            $back_to_top.addClass('cd-fade-out');
        }
    });
    //smooth scroll to top
    $back_to_top.on('click', function (event) {
        event.preventDefault();
        $('body,html').animate({
            scrollTop: 0,
        }, scroll_top_duration);
    });

});


function makeHeader(blog_username, username) {
    //blog_username 当前访问的博客的作者
    //username   登陆的用户

    //博客作者-用户信息url
    var user_info_url = '/' + blog_username + '/' + 'info';
    var user_photo = '/' + blog_username + '/' + 'photo';
    //登陆用户发博客url
    if (username) {
        var topic_release_url = '/' + username + '/' + 'topic/release'
    } else {
        //没有登陆状态直接去登陆
        var topic_release_url = '/login'
    }

    //访问博主的博客文章
    var user_topics_url = '/' + blog_username + '/' + 'topics';

    var header_body = '';
    header_body += '<header id="header">';
    header_body += '<div class="menu">';
    header_body += '<nav class="nav" id="topnav">';
    header_body += '<h1 class="logo"><a href="/index">' + blog_username + '</a></h1>';
    header_body += '<li><a href="/index">主页</a></li>';
    header_body += '<li>';
    // header_body += '<a href=' + '"' + user_topics_url + '"' + '>文章列表</a>';
    header_body += '<ul class="sub-nav">';
    header_body += '<li><a href=' + '"' + user_topics_url + '?category=tec"' + '>技术</a></li>';
    header_body += '<li><a href=' + '"' + user_topics_url + '?category=no-tec"' + '>非技术</a></li>';
    header_body += '</ul>';
    header_body += '</li>';


    header_body += '<li>';
    header_body += '<a href=' + '"' + user_topics_url + '?category=tec" ' + '>技术类</a>';
    header_body += '<ul class="sub-nav">';
    header_body += '<li><a href=' + '"' + user_topics_url + '?category=python"' + '>python</a></li>';
    header_body += '<li><a href=' + '"' + user_topics_url + '?category=java"' + '>java</a></li>';
    header_body += '<li><a href=' + '"' + user_topics_url + '?category=C语言"' + '>C语言</a></li>';
    header_body += '<li><a href=' + '"' + user_topics_url + '?category=C++"' + '>C++</a></li>';
    header_body += '<li><a href=' + '"' + user_topics_url + '?category=数据库"' + '>数据库</a></li>';
    header_body += '<li><a href=' + '"' + user_topics_url + '?category=其他"' + '>其他</a></li>';
    header_body += '</ul>';
    header_body += '</li>';


    header_body += '<li>';
    header_body += '<a href=' + '"' + user_topics_url + '?category=no-tec"' + '>生活类</a>';
    header_body += '<ul class="sub-nav">';
    header_body += '<li><a href=' + '"' + user_topics_url + '?category=sport"' + '>运动</a></li>';
    header_body += '<li><a href=' + '"' + user_topics_url + '?category=food"' + '>美食</a></li>';
    header_body += '<li><a href=' + '"' + user_topics_url + '?category=sign"' + '>星座</a></li>';

    header_body += '<li><a href=' + '"' + user_topics_url + '?category=relaxation"' + '>休闲</a></li>';

    header_body += '<li><a href=' + '"' + user_topics_url + '?category=no-tec"' + '>其他</a></li>';
    header_body += '</ul>';
    header_body += '</li>';


    header_body += '<li><a href=' + '"' + user_info_url + '"' + '>关于我</a></li>';
    header_body += '<li><a href=' + '"' + topic_release_url + '"' + '>发表博客</a> </li>';

    header_body += '<li><input placeholder="请输入文章标题" id="search_title" /></li>';
    header_body += '<li><button  id="search_title" onclick="search_title()" >搜索</button></li>';

    header_body += '</nav>';
    header_body += '</div>';

    if (username) {
        header_body += '<li><a href= /' + username + '/change_info id="change_info" target="_blank">编辑</a></li>';
        //header_body += '<li><a href="/" id="login_out" target="_blank">登出</a></li>';


        header_body += '<li><span id="login_out" target="_blank">登出</span></li>';
    } else {
        header_body += '<a href="/login" id="login" target="_blank">登陆</a>';
        header_body += '<a href="/register" id="register" target="_blank">注册</a>';
    }
    header_body += '</header>';


    return header_body
}


function loginOut() {
    $('#login_out').on('click', function () {
            if (confirm("确定登出吗？")) {
                window.localStorage.removeItem('dnblog_token');
                window.localStorage.removeItem('dnblog_user');
                window.location.href = '/index';
            }
        }
    )
}

function search_title() {

    const title = $('#search_title').val()
    const user = window.localStorage.getItem('dnblog_user');
    window.location.href = `/${user}/topics/?title=${title}`;

}