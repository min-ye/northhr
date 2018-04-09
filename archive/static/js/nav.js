$(document).ready(function () {
   var url = window.location.toString(),
       id = url.split("#")[1],
       cid = "#" + id,
       mid = "#l-" + id;
   $("div.tab-content").find("section").each(function () {
      $(this).removeClass("active");
   });
   $("ul.nav").find("li").each(function () {
      $(this).removeClass("active");
   });
   $(mid).addClass("active");
   $(cid).addClass("active");
   $(cid).addClass("in");

   var scroll_top = $('nav').offset().top;
   $('html, body').animate({ scrollTop: scroll_top}, 1000);
});