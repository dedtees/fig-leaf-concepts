/* Video testimonial: the poster and play button stay on the page until a
   visitor presses play, then the YouTube player loads in their place
   (privacy-enhanced youtube-nocookie.com, so nothing from YouTube loads
   before the click).

   To change the video, change VIDEO_ID below. It is the part after
   "youtu.be/" or "watch?v=" in a YouTube link. A card can also set its
   own video with data-youtube-id="...". */
(function () {
  var VIDEO_ID = 'tWZyvQFi9bw';

  document.querySelectorAll('[data-vr-video]').forEach(function (card) {
    var id = card.getAttribute('data-youtube-id') || VIDEO_ID;
    var frame = card.querySelector('.vr-video__frame');
    var play = card.querySelector('.vr-video__play');
    var poster = card.querySelector('.vr-video__poster');
    if (!frame || !play) return;

    /* the video's own thumbnail as the poster; the local image stays if
       YouTube has none */
    if (poster) {
      var tries = ['maxresdefault', 'hqdefault'], local = poster.currentSrc || poster.src, localSet = poster.getAttribute('srcset');
      var next = function () {
        var name = tries.shift();
        if (!name) { poster.onerror = null; poster.onload = null; poster.src = local; if (localSet) poster.setAttribute('srcset', localSet); return; }
        poster.removeAttribute('srcset');
        poster.src = 'https://i.ytimg.com/vi/' + id + '/' + name + '.jpg';
      };
      /* YouTube answers a missing maxres thumbnail with a 120px grey image */
      poster.onload = function () { if (poster.naturalWidth <= 120) next(); else { poster.onload = null; poster.onerror = null; } };
      poster.onerror = next;
      next();
    }

    play.addEventListener('click', function () {
      var iframe = document.createElement('iframe');
      iframe.className = 'vr-video__media';
      iframe.src = 'https://www.youtube-nocookie.com/embed/' + encodeURIComponent(id) + '?autoplay=1&rel=0&playsinline=1';
      iframe.title = 'Video testimonial from a Fig Leaf client';
      iframe.allow = 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share';
      iframe.allowFullscreen = true;
      iframe.referrerPolicy = 'strict-origin-when-cross-origin';
      frame.appendChild(iframe);
      card.classList.add('is-playing');
      iframe.focus();
    });
  });
})();
