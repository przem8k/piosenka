$(document).ready(function() {
    var options = {
      showCloseButton: true
    };
    
    var elements = document.querySelectorAll('.pzt-lightbox');
    elements.forEach(function (element) {
      new Luminous(element, options);
    });
});
