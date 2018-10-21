$(function () {
    // 加载运行状态
    loadStatus();
    // 启动
    $('#ss-start').on('click', function (e) {
        if ($(this).hasClass('weui-btn_plain-disabled')) {
            return
        }
        ssStart()
    });
    // 添加端口
    $('#add').on('click', function (e) {
        if (!$('#port').val()) {
            $('#iosDialog2').show();
            $('#alert-msg').text('缺少端口号');
            return
        }
        else if (!$('#pswd').val()) {
            $('#iosDialog2').show();
            $('#alert-msg').text('缺少密码');
            return
        }
        else if (!$('#add-auth').val()) {
            $('#iosDialog2').show();
            $('#alert-msg').text('缺少授权码');
            return
        }
        $('#dialog-msg').text('确定添加？');
        $('#iosDialog1').show();
        $('#confirm').attr('data-type', 'add');
    });
    // 删除端口
    $('#ports-list').on('click', function (e) {
        if ($(e.target).hasClass('delete-d')) {
            // 是否有授权码
            if (!$('#del-auth').val()) {
                $('#iosDialog2').show();
                $('#alert-msg').text('缺少授权码');
                return
            }
            $('#dialog-msg').text('确定删除？');
            $('#iosDialog1').show().attr('data-port', $(e.target).parent().attr('data-port'));
            $('#confirm').attr('data-type', 'del');
        }
    });
    // 添加/删除确认
    $('#confirm').on('click', function (e) {
        $('#iosDialog1').hide();
        var type = $(this).attr('data-type');
        if (type === 'del') {
            delPort($('#iosDialog1').attr('data-port'), $('#del-auth').val())
        }
        else {
            addPort($('#port').val(), $('#pswd').val(), $('#add-auth').val())
        }
    });
    // 标签页切换
    $('.weui-navbar').on('click', function (e) {
        var id = $(e.target).attr('data-id');
        $(e.target).addClass('weui-bar__item_on').siblings().removeClass('weui-bar__item_on');
        $('#' + id).show().siblings().hide();
        if (id === 'page3') {
            loadList();
        }
    });
    // dialog1取消
    $('#cancel').on('click', function (e) {
        $('#iosDialog1').hide().attr('data-port', '')
    });
    // alert确认
    $('#alert-confirm').on('click', function (e) {
        $('#iosDialog2').hide()
    });
});

function loadList() {
    $('#ports-list').empty();
    $('#loadingToast').show();
    $.ajax({
        type: "GET",
        url: '../ss/list',
        dataType: 'json',
        success: function (data) {
            if (data['errcode'] === 0) {
                var port_password = data['data'];
                if (port_password) {
                    // var p_p_obj = JSON.stringify(port_password);
                    var p_p_obj = port_password;
                    for (port in p_p_obj) {
                        var pswd = p_p_obj[port];
                        var $a = $('<a>').addClass('weui-cell weui-cell_access');
                        $a.attr({'href': 'javascript:;', 'style': 'text-decoration: none', 'data-port': port});
                        var $div1 = $('<div>').addClass('weui-cell__bd').append($('<p>').text(port));
                        // var $p = ;
                        var $div2 = $('<div>').addClass('weui-cell__ft delete-d').text(pswd);
                        $a.append($div1).append($div2);
                        $('#ports-list').append($a)
                    }
                }
            }
        },
        error: function (e) {
            console.log(e)
        },
        complete: function () {
            $('#loadingToast').hide();
        }
    });
}

function loadStatus() {
    $('#loadingToast').show();
    $.ajax({
        type: "GET",
        url: '../ss/status',
        dataType: 'json',
        success: function (data) {
            if (data['errcode'] === 0) {
                if (data['status'] === 'y') {
                    $('#status-icon').addClass('weui-icon-success');
                    $('#status-msg').text(data['msg']);
                    $('#ss-start').addClass('weui-btn_plain-disabled');
                    $('#status-container').show();
                }
                else {
                    $('#status-icon').addClass('weui-icon-warn');
                    $('#status-msg').text(data['msg']);
                    $('#ss-start').addClass('weui-btn_plain-primary');
                    $('#status-container').show();
                }
            }
        },
        error: function (e) {
            console.log(e)
        },
        complete: function () {
            $('#loadingToast').hide();
        }
    });
}

function ssStart() {
    $('#loadingToast').show();
    $.ajax({
        type: "GET",
        url: '../ss/start',
        dataType: 'json',
        success: function (data) {
            if (data['errcode'] === 0) {
                if (data['status'] === 'y') {
                    $('#status-icon').removeClass('weui-icon-warn').addClass('weui-icon-success');
                    $('#status-msg').text(data['msg']);
                    $('#ss-start').removeClass('weui-btn_plain-primary').addClass('weui-btn_plain-disabled');
                }
                else {
                    $('#iosDialog2').show();
                    $('#alert-msg').text(data['msg']);
                }
            }
        },
        error: function (e) {
            console.log(e)
        },
        complete: function () {
            $('#loadingToast').hide();
        }
    });
}

function addPort(port, pswd, auth) {
    $('#loadingToast').show();
    $.ajax({
        type: "GET",
        url: '../ss/add/' + port + '/' + pswd + '/' + auth,
        dataType: 'json',
        success: function (data) {
            if (data['errcode'] === 0) {
                $('#iosDialog2').show();
                $('#alert-msg').text(data['msg']);
                loadStatus();
                loadList();
            }
        },
        error: function (e) {
            console.log(e)
        },
        complete: function () {
            $('#loadingToast').hide();
        }
    });
}

function delPort(port, auth) {
    $('#loadingToast').show();
    $.ajax({
        type: "GET",
        url: '../ss/del/' + port + '/' + auth,
        dataType: 'json',
        success: function (data) {
            if (data['errcode'] === 0) {
                $('#iosDialog2').show();
                $('#alert-msg').text(data['msg']);
                loadStatus();
                loadList();
            }
        },
        error: function (e) {
            console.log(e)
        },
        complete: function () {
            $('#loadingToast').hide();
        }
    });
}