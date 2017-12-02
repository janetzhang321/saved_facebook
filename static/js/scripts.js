$(document).ready(function() {
  $('[data-toggle=offcanvas]').click(function() {
    $('.row-offcanvas').toggleClass('active');
  });
});

//timer code
var date = ;//eval date
var reminder = new Date();
reminder.setFullYear(date);
var today = new Date();

if (reminder<=today) {
    alert("Reminder: Read this article");
}