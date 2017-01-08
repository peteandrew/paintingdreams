$(function() {
  var starImg = new Image();

  var addStars = function() {
    var starWidth = starImg.width;
    var starHeight = starImg.height;

    console.log(starWidth);
    console.log(starHeight);

    var docWidth = $(document).width();
    var docHeight = $(document).height();

    console.log(docWidth);
    console.log(docHeight);

    var wrapper = $('.wrapper')[0];

    var positions = [];

    var x, y;
    for (y = 0; y < docHeight; y += starHeight) {
      for (x = 0; x < docWidth; x += starWidth) {
        positions.push({x:x, y:y});
      }
    }

    console.log(positions);

    var numStars = Math.round(positions.length * 0.2);

    var i;
    for (i = 0; i < numStars; i++) {
      var positionIdx = Math.floor(Math.random() * positions.length);
      var position = positions[positionIdx];

      if (position) {
        var newStar = $(starImg).clone();
        newStar.css('display', 'none');
        newStar.css('position', 'absolute');
        newStar.css('top', position.y);
        newStar.css('left', position.x);

        var size = Math.floor(Math.random() * (starWidth / 2)) + (starWidth / 2);
        newStar.css('width', size + 'px');
        newStar.css('height', size + 'px');
        newStar.appendTo(wrapper);

        setTimeout(function(newStar) {
          return function() {
            newStar.fadeIn(1000);
          };
        }(newStar), i * 60);

        positions[positionIdx] = null;
      }
    }
  };

  $(starImg).load(addStars);
  starImg.src = '/static/single-star.png';
});
