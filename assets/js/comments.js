// Disqus escapes these five characters in raw_message. Decoding them in one
// pass restores the text exactly as typed (e.g. "&amp;quot;" -> "&quot;").
var ENTITIES = { quot: '"', amp: "&", lt: "<", gt: ">", "#x27": "'" };

function decodeEntities(s) {
  return s.replace(/&(quot|amp|lt|gt|#x27);/g, function(m, name) { return ENTITIES[name]; });
}

document.addEventListener("DOMContentLoaded", function() {
  var max_length = 200;
  var commentDiv = document.getElementById("last-comments");
  fetch("https://disqus.com/api/3.0/forums/listPosts.json?forum=piosenka&limit=5&related=thread&api_key=iAruOUIdDbkbz8yMfYkDqbfPCjc2vclRu7tnSOoCr6cbYC4TiBmDrVyxpQb0yBFM").then(function(r) { return r.json(); }).then(function(res) {
    if (res.code === 0) {
      for (var i = 0, len = res.response.length; i < len; i++) {
        var post = res.response[i];
        // raw_message contains entities like &quot;. Decode before truncating.
        var raw = decodeEntities(post.raw_message);
        var content = raw.length < max_length ? raw : raw.substring(0, max_length) + " (...)";
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
