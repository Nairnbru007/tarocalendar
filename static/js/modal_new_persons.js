$(function() {
    // Проверяем запись в куках о посещении
    // Если запись есть - ничего не делаем
    if (!$.cookie('hideModal')) {
   // если cookie не установлено появится окно
   // с задержкой 5 секунд
    var delay_popup = 3000;
    setTimeout("document.getElementById('overlay').style.display='block'", delay_popup);
    }
    // Запоминаем в куках, что посетитель уже заходил
    $.cookie('hideModal', true, {
    // Время хранения cookie в днях
        expires: 21,
        path: '/'
    });
});