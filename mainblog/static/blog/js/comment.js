/**
 * Created by Administrator on 2017/12/31/0031.
 */
var submitflag = true;
var comment_id;
$(function () {
    $('#user_content').submit(function () {
        alert("submit");
        alert("come in ajax");
        if (submitflag) {
            $.ajax({
                type: "post",
                dataType: "json",
                url: "/detail/{{blog.id}}/",
                async: false,
                data: {'content': $("#id_content").val(), 'flag': 'comment'},
                success: function (data) {
                    alert(data.content);
                    $('#user_content')[0].reset();
                    var newcomment = "<div class=\"comment\">" + "<p>" + data.content + "</p>" + "</div>" +
                        "<div class=\"reply-lable\" style=\"color:blue\">" +
                        "<a href=\"#user_content\" onclick=\"reply(" + data.comment_id + ")\"" + ">" + "»Ø¸´" + "</a>" + "</div>" +
                        "<ul class=\"replycon\" id=\"" + data.comment_id + "\">" + "</ul>" +
                        "<hr>";
                    $(".con").append(newcomment);
                },
                error: function (data) {
                    alert(data);
                }
            });
            return false;
        }
        else {
            var commentid = comment_id;
            alert(commentid);
            $.ajax({
                type: "post",
                dataType: "json",
                url: "/detail/{{blog.id}}/",
                async: false,
                data: {'content': $("#id_content").val(), 'flag': 'reply', 'commentid': commentid},
                success: function (data) {
                    alert(data.content);
                    $('#user_content')[0].reset();
                    var newcomment = "<div class=\"reply-comment\">" + "<p>" + data.content + "</p>" + "</div>" +
                        "<div class=\"reply-lable\" style=\"color:blue\">" +
                        "<a href=\"#user_content\" onclick=\"reply(" + commentid + ")\"" + ">" + "»Ø¸´" + "</a>" + "</div>" +
                        "<hr>";
                    $("#" + commentid).append(newcomment);

                },
                error: function (data) {
                    alert(data);
                }
            });
            submitflag = true;
            return false;
        }
    });

});

function reply(id) {
    submitflag = false;
    comment_id = id;
    alert("huifu");
}
