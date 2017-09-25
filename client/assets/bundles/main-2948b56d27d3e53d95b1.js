/******/ (function(modules) { // webpackBootstrap
/******/ 	// The module cache
/******/ 	var installedModules = {};

/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {

/******/ 		// Check if module is in cache
/******/ 		if(installedModules[moduleId])
/******/ 			return installedModules[moduleId].exports;

/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = installedModules[moduleId] = {
/******/ 			exports: {},
/******/ 			id: moduleId,
/******/ 			loaded: false
/******/ 		};

/******/ 		// Execute the module function
/******/ 		modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);

/******/ 		// Flag the module as loaded
/******/ 		module.loaded = true;

/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}


/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = modules;

/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = installedModules;

/******/ 	// __webpack_public_path__
/******/ 	__webpack_require__.p = "";

/******/ 	// Load entry module and return exports
/******/ 	return __webpack_require__(0);
/******/ })
/************************************************************************/
/******/ ([
/* 0 */
/***/ function(module, exports, __webpack_require__) {

	// Relevant anywhere.
	__webpack_require__(1);

	__webpack_require__(8);
	__webpack_require__(11);

	__webpack_require__(13);
	__webpack_require__(15);

	// Frontpage.
	__webpack_require__(17);
	__webpack_require__(19);

	// Song page.
	__webpack_require__(21);
	__webpack_require__(23);

	// Lightbox (image viewer).
	__webpack_require__(25);
	__webpack_require__(27);


/***/ },
/* 1 */
/***/ function(module, exports) {

	// removed by extract-text-webpack-plugin

/***/ },
/* 2 */,
/* 3 */,
/* 4 */,
/* 5 */,
/* 6 */,
/* 7 */,
/* 8 */
/***/ function(module, exports, __webpack_require__) {

	__webpack_require__(9)(__webpack_require__(10))

/***/ },
/* 9 */
/***/ function(module, exports) {

	/*
		MIT License http://www.opensource.org/licenses/mit-license.php
		Author Tobias Koppers @sokra
	*/
	module.exports = function(src) {
		if (typeof execScript !== "undefined")
			execScript(src);
		else
			eval.call(null, src);
	}


/***/ },
/* 10 */
/***/ function(module, exports) {

	module.exports = "$(document).ready(function(){\n    var songs = new Bloodhound({\n        datumTokenizer: Bloodhound.tokenizers.obj.whitespace('value'),\n        queryTokenizer: Bloodhound.tokenizers.whitespace,\n        prefetch: '/index/songs',\n    });\n    songs.initialize();\n\n    var artists = new Bloodhound({\n        datumTokenizer: Bloodhound.tokenizers.obj.whitespace('value'),\n        queryTokenizer: Bloodhound.tokenizers.whitespace,\n        prefetch: '/index/artists',\n    });\n    artists.initialize();\n\n    var selected = false;\n\n    $('.search input').typeahead({\n        hint: false,\n        highlight: false,\n    }, {\n        name: 'songs',\n        source: songs.ttAdapter(),\n        templates: {\n            header: '<p class=\"dataset-header\">Piosenki</p>',\n        }\n    }, {\n        name: 'artists',\n        source: artists.ttAdapter(),\n        templates: {\n            header: '<p class=\"dataset-header\">Artyści</p>',\n        },\n    }).on('typeahead:selected', function($e, data) {\n      window.location = data.url;\n      selected = true;\n    }).on( \"keydown\", function(event) {\n      if(event.which == 13 && !selected) {\n        window.location = '/szukaj/?q=' + encodeURIComponent(this.value);\n      }\n    });\n});\n"

/***/ },
/* 11 */
/***/ function(module, exports) {

	// removed by extract-text-webpack-plugin

/***/ },
/* 12 */,
/* 13 */
/***/ function(module, exports, __webpack_require__) {

	__webpack_require__(9)(__webpack_require__(14))

/***/ },
/* 14 */
/***/ function(module, exports) {

	module.exports = "$(document).ready(function() {\nsetTimeout(function() {\n    $('.messages').fadeOut('fast');\n}, 5000);\n});\n"

/***/ },
/* 15 */
/***/ function(module, exports, __webpack_require__) {

	__webpack_require__(9)(__webpack_require__(16))

/***/ },
/* 16 */
/***/ function(module, exports) {

	module.exports = "$('.tip').tooltip({});\n"

/***/ },
/* 17 */
/***/ function(module, exports, __webpack_require__) {

	__webpack_require__(9)(__webpack_require__(18))

/***/ },
/* 18 */
/***/ function(module, exports) {

	module.exports = "$(document).ready(function() {\n  var max_length = 200;\n  $commentDiv = $(\"#last-comments\");\n  $.get(\"https://disqus.com/api/3.0/forums/listPosts.json?forum=piosenka&limit=5&related=thread&api_key=iAruOUIdDbkbz8yMfYkDqbfPCjc2vclRu7tnSOoCr6cbYC4TiBmDrVyxpQb0yBFM\", function(res, code) {\n    if (res.code === 0) {\n      var result = \"\";\n      for (var i = 0, len = res.response.length; i < len; i++) {\n        var post = res.response[i];\n        var content = post.raw_message.length < max_length ? post.raw_message : post.raw_message.substring(0, max_length) + \" (...)\";\n        var html = \"<div class='comment'>\";\n        html += \"<p class='content'>\" + content + \"</p>\";\n        html += \"<p class='attribution'><b>\" + post.author.name + \"</b> - <a href='\" + post.thread.link + \"'>\" + post.thread.title + \"</a></p>\";\n        html += \"</div>\";\n        result += html;\n      }\n      $commentDiv.html(result);\n    }\n  });\n});\n"

/***/ },
/* 19 */
/***/ function(module, exports) {

	// removed by extract-text-webpack-plugin

/***/ },
/* 20 */,
/* 21 */
/***/ function(module, exports, __webpack_require__) {

	__webpack_require__(9)(__webpack_require__(22))

/***/ },
/* 22 */
/***/ function(module, exports) {

	module.exports = "var GadgetStateEnum = {\n    NORMAL: 0,\n    REPEATED: 1,\n    NONE: 2\n};\n\nvar gadgetState = GadgetStateEnum.NORMAL;\nvar transposition = 0;\n\nfunction enableTransposition() {\n    $(\".trans-up-trigger\").prop('disabled', false);\n    $(\".trans-home-trigger\").prop('disabled', false);\n    $(\".trans-down-trigger\").prop('disabled', false);\n}\n\nfunction disableTransposition() {\n    $(\".trans-up-trigger\").prop('disabled', true);\n    $(\".trans-home-trigger\").prop('disabled', true);\n    $(\".trans-down-trigger\").prop('disabled', true);\n}\n\nfunction applyState() {\n    $(\".chords-trigger\").removeClass(\"btn-primary\");\n    $(\".chords-trigger\").addClass(\"btn-default\");\n    if (gadgetState == GadgetStateEnum.NORMAL) {\n        $(\".chord-section\").show();\n        $(\".extra-chords\").hide();\n        $(\".chords-normal-trigger\").addClass(\"btn-primary\").removeClass(\"btn-default\");\n        enableTransposition();\n    } else if (gadgetState == GadgetStateEnum.REPEATED) {\n        $(\".chord-section\").show();\n        $(\".extra-chords\").show();\n        $(\".chords-repeated-trigger\").addClass(\"btn-primary\").removeClass(\"btn-default\");\n        enableTransposition();\n    } else if (gadgetState == GadgetStateEnum.NONE) {\n        $(\".chord-section\").hide();\n        $(\".chords-none-trigger\").addClass(\"btn-primary\").removeClass(\"btn-default\");\n        disableTransposition();\n    }\n}\n\nfunction transpose() {\n    $.ajax({\n        url: transpositionUrls[transposition],\n    }).done(function(data) {\n        $(\".lyrics-content\").replaceWith(data['lyrics']);\n        applyState();\n    });\n}\n\n$(document).ready(function(){\n    $(\".chords-normal-trigger\").click(function() {\n        gadgetState = GadgetStateEnum.NORMAL;\n        applyState();\n    });\n    $(\".chords-repeated-trigger\").click(function() {\n        gadgetState = GadgetStateEnum.REPEATED;\n        applyState();\n    });\n    $(\".chords-none-trigger\").click(function() {\n        gadgetState = GadgetStateEnum.NONE;\n        applyState();\n    });\n\n    $(\".trans-up-trigger\").click(function() {\n        transposition = (transposition + 1) % 12;\n        transpose();\n    });\n    $(\".trans-home-trigger\").click(function() {\n        transposition = 0;\n        transpose();\n    });\n    $(\".trans-down-trigger\").click(function() {\n        transposition = (transposition + 11) % 12;\n        transpose();\n    });\n});\n"

/***/ },
/* 23 */
/***/ function(module, exports) {

	// removed by extract-text-webpack-plugin

/***/ },
/* 24 */,
/* 25 */
/***/ function(module, exports, __webpack_require__) {

	__webpack_require__(9)(__webpack_require__(26))

/***/ },
/* 26 */
/***/ function(module, exports) {

	module.exports = "$(document).ready(function() {\n  var elements = document.querySelectorAll('.pzt-lightbox');\n  elements.forEach(function (element) {\n    new Luminous(element);\n  });\n});\n"

/***/ },
/* 27 */
/***/ function(module, exports) {

	// removed by extract-text-webpack-plugin

/***/ }
/******/ ]);