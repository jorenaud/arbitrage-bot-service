
function user_register()
{
    if ($("#firstname").val() === '')
    {
        alert("first name error");
        return;
    }
    if ($("#lastname").val() === '')
    {
        alert("lastnamee error");
        return;
    }
    if ($("#email").val() === '')
    {
        alert("email error");
        return;
    }
    if ($("#country").val() === '')
    {
        alert("country name error");
        return;
    }
    if ($("#language").val() === '-1')
    {
        alert("language name error");
        return;
    }
    if ($("#phone").val() === '')
    {
        alert("phone name error");
        return;
    }
    if ($("#password").val() === '')
    {
        alert("password name error");
        return;
    }
    if ($("#confirm").val() === '')
    {
        alert("confirm name error");
        return;
    }
    var params = {
        "firstname" : $("#firstname").val(),
        "lastname" : $("#lastname").val(),
        "email" : $("#email").val(),
        "country" : $("#country").val(),
        "language" : $("#language").val(),
        "phone" : $("#phone").val(),
        "password" : $("#password").val(),
    };

    $.ajax({
        type: "POST",
        url: "/adduser",
        data: params,
        success: function(res){
            alert("success");
        },
    });

}