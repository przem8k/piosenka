document.addEventListener("DOMContentLoaded", function() {
  var max_length = 200;
  var commentDiv = document.getElementById("last-comments");
  fetch("https://disqus.com/api/3.0/forums/listPosts.json?forum=piosenka&limit=5&related=thread&api_key=iAruOUIdDbkbz8yMfYkDqbfPCjc2vclRu7tnSOoCr6cbYC4TiBmDrVyxpQb0yBFM").then(function(r) { return r.json(); }).then(function(res) {
    if (res.code === 0) {
      for (var i = 0, len = res.response.length; i < len; i++) {
        var post = res.response[i];
        var content = post.raw_message.length < max_length ? post.raw_message : post.raw_message.substring(0, max_length) + " (...)";
        // Build DOM nodes instead of concatenating into innerHTML — Disqus
        // post fields come from public user input and may contain HTML.
        var wrapper = document.createElement("div");
        wrapper.className = "comment";
        var contentP = document.createElement("p");
        contentP.className = "content";
        contentP.textContent = content;
        var attribP = document.createElement("p");
        attribP.className = "attribution";
        var author = document.createElement("b");
        author.textContent = post.author.name;
        var link = document.createElement("a");
        link.href = post.thread.link;
        link.textContent = post.thread.title;
        attribP.appendChild(author);
        attribP.appendChild(document.createTextNode(" - "));
        attribP.appendChild(link);
        wrapper.appendChild(contentP);
        wrapper.appendChild(attribP);
        commentDiv.appendChild(wrapper);
      }
    }
  });
});
