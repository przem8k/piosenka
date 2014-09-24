$(document).ready(function() {
  var max_length = 200;
  $commentDiv = $("#last-comments");
  $.get("https://disqus.com/api/3.0/forums/listPosts.json?forum=piosenka&limit=5&related=thread&api_key=iAruOUIdDbkbz8yMfYkDqbfPCjc2vclRu7tnSOoCr6cbYC4TiBmDrVyxpQb0yBFM", function(res, code) {
    if (res.code === 0) {
      var result = "";
      for (var i = 0, len = res.response.length; i < len; i++) {
        var post = res.response[i];
        var content = post.raw_message.length < max_length ? post.raw_message : post.raw_message.substring(0, max_length) + " (...)";
        var html = "<div class='comment'>";
        html += "<p class='source'><a href='" + post.thread.link + "'>" + post.thread.title + "</a></p>";
        html += "<p class='content'>" + content + "</p>";
        html += "<p class='author'>" + post.author.name + "</p>";
        html += "</div>";
        result += html;
      }
      $commentDiv.html(result);
    }
  });
});
