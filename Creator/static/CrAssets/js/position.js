
var scrollPosition = sessionStorage.getItem('scrollPosition');

if (scrollPosition) {
    document.querySelector('.body-container').scrollTop = scrollPosition;
}

window.addEventListener('beforeunload', function () {
    sessionStorage.setItem('scrollPosition', document.querySelector('.body-container').scrollTop);
});

document.addEventListener("DOMContentLoaded", function () {
    var bodyContainer = document.querySelector('.body-container');
    bodyContainer.addEventListener('scroll', function () {
       
    });
});

