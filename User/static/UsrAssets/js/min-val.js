const banIcon = $("#confirm-password").siblings("span").find(".bi-ban").hide();
const checkIcon = $("#confirm-password").siblings("span").find(".bi-check2-all").hide();
const changeButton = $("#changeButton");
const shieldXIcon = $("#new-password").siblings("span").find(".bi-shield-x").hide();
const shieldExclamationIcon = $("#new-password").siblings("span").find(".bi-shield-exclamation").hide();
const shieldCheckIcon = $("#new-password").siblings("span").find(".bi-shield-check").hide();

$("#new-password").on("input", function () {
    const newPasswordLength = $(this).val().length;
    if (newPasswordLength > 0){
        shieldXIcon.toggle(newPasswordLength < 4);
        shieldExclamationIcon.toggle(newPasswordLength >= 4 && newPasswordLength < 6);
        shieldCheckIcon.toggle(newPasswordLength >= 6);
    } else{
        shieldXIcon.hide();
        shieldExclamationIcon.hide();
        shieldCheckIcon.hide();
    }
});

$("#new-password, #confirm-password").on("input focus", function () {
    const newPassword = $("#new-password").val();
    const confirmPassword = $("#confirm-password").val();
    const confirmPasswordLength = confirmPassword.length;
    const newPasswordLength = $(this).val().length;

    if (confirmPasswordLength === 0) {
        banIcon.hide();
        checkIcon.hide();
    } else if (newPassword === confirmPassword) {
        banIcon.hide();
        checkIcon.show();
        changeButton.prop('disabled', false);
    } else {
        banIcon.show();
        checkIcon.hide();
        changeButton.prop('disabled', true);
    }

    if (confirmPasswordLength === 0 || newPasswordLength < 4 ){
        changeButton.prop('disabled', true);
    } else {
        changeButton.prop('diabled',false)
    }
});