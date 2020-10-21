$(function() {
    if (Cookies.get('cookie_notice_accepted')) {
        return;
    }
    $('.cookie').fadeIn('fast');
    $('.cookie__btn').click(function(ev) {
        ev.preventDefault();
        $('.cookie').fadeOut('slow');
        Cookies.set('cookie_notice_accepted', true, { expires: 360 });
    });
});