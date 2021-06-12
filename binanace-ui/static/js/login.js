function on_login() {

    var username = $("#login_username").val();
    var password = $("#login_password").val();

    if (username == "" || password == "")
        return;

    var params = {
        "username": username,
        "password": password,
    };

    $.ajax({
        type: "POST",
        url: "/auth/login/",
        data: params,
        async: false,
        success: function (res) {
            if (res == "success") {

                window.location.href = "index";

            } else {

                alert("Access is not allowed!");

            }
        }
    });
}

function on_register() {

    window.location.href = "register";
}

function on_register_confirm() {

    var username = $("#reg_username").val();
    var firstname = $("#reg_firstname").val();
    var lastname = $("#reg_lastname").val();
    var password = $("#reg_password").val();
    var password_confirm = $("#reg_password_confirm").val();
    var email = $("#reg_email").val();
    var mobile = $("#reg_mobile").val();

    if (password !== password_confirm) {
        alert("password not same.");
        return;
    }

    var params = {
        "username": username,
        "first_name": firstname,
        "last_name": lastname,
        "password": password,
        "email": email,
        "mobile": mobile,
    };

    $.ajax({
        type: "POST",
        url: "/auth/register_user/",
        data: params,
        // async: false,
        success: function (res) {
            if (res == "success") {
                alert("Registered successfully.");
                window.location.href = "index";
            } else {
                alert("Error.");
            }
        }
    });
}

function on_register_cancel() {

    window.location.href = "index";
}

function on_logout() {

    $.ajax({
        type: "POST",
        url: "/user/logout/",
        async: false,
        success: function (res) {
            window.location.href = "/";
        }
    });
}

function on_reg_sign() {

    window.location.href = "login";
}