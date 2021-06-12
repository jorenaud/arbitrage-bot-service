
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
    if ($("#password").val() !== $("#confirm").val())
    {
        alert("password confirm failed");
        return;
    }

    var params = {
        "firstName" : $("#firstname").val(),
        "lastName" : $("#lastname").val(),
        "email" : $("#email").val(),
        "country" : $("#country").val(),
        "language" : $("#language").val(),
        "phone" : $("#phone").val(),
        "password" : $("#password").val(),
    };

    $.ajax({
        type: "POST",
        url: "/adduser/",
        data: params,
        success: function(res){
            //alert("Welcome to Join US.\n Please Check your email box. user ID: " + res);

            redirect("/login/");
        },
        error: function (res) {
            alert("Register Error:" + res["responseText"] + " status code: " + res.status);
            return;
        },
    });

}

function redirect(url)
{
    window.location.href=url;
}

function user_login()
{
    if ($("#loginuserid").val() === "")
    {
        alert("Please Insert user ID");
        return;
    }
    if ($("#loginpassword").val() === "")
    {
        alert("Please Insert Password");
        return;
    }
    var params = {
        "userid" : $("#loginuserid").val(),
        "password" : $("#loginpassword").val(),
    };
    $.ajax({
        type: "POST",
        url: "/auth/",
        data: params,

        success: function(res){
            //alert("Welcome to Login.\n");
            redirect("/user/");
        },
        error: function (res) {
            alert("Register Error:" + res["responseText"] + " status code: " + res.status);
            return;
        },
    });

}