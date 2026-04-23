(function () {
  
  //configuration
  const SPEED_MIN = 1;
  const SPEED_MAX = 20;
  const SPEED_STEP = 1;
  const SPEED_DEFAULT = 6;
  const BASE = 0.02; //px to scroll per one frame at speed 1
  const TICK = 16; //frame duration in ms
  const LINE_MARGIN = 120; //to stop a few more px after lyrics bottom edge

  //state variables
  let autoscrollEnabled = false;
  let autoscrollRunning = false;
  let autoscrollSpeed = SPEED_DEFAULT;
  let rafId = null;
  let lastTimestamp = null;
  let exactScrollY = 0; //stores exact calculated scroll position

  //DOM elements
  const toggleBtn = document.querySelector('.autoscroll-toggle');
  const bar = document.querySelector('.autoscroll-bar');
  const speedLabel = document.querySelector('.autoscroll-speed');
  const pauseBtn = document.querySelector('.autoscroll-pause');
  const slowerBtn = document.querySelector('.autoscroll-slower');
  const fasterBtn = document.querySelector('.autoscroll-faster');
  const closeBtn = document.querySelector('.autoscroll-close');
  const content = document.querySelector('.lyrics-content');

  if (!toggleBtn || !bar || !content) {
    return;
  }

  //check where to stop scrolling
  function getScrollMax() {
    const rect = content.getBoundingClientRect();
    const contentBottom = window.scrollY + rect.bottom;
    return contentBottom - window.innerHeight + LINE_MARGIN;
  }

  //UI updates
  function updateSpeedLabel() {
    speedLabel.textContent = 'Tempo: ' + autoscrollSpeed;
  }

  function updatePauseBtn() {
    pauseBtn.innerHTML = autoscrollRunning ? '<span class="glyphicon glyphicon-pause"></span>' : '<span class="glyphicon glyphicon-play"></span>';
  }

  function updateSlowerFaster() {
    slowerBtn.disabled = autoscrollSpeed <= SPEED_MIN;
    fasterBtn.disabled = autoscrollSpeed >= SPEED_MAX;
  }

  function updateToggleBtn() {
    toggleBtn.classList.toggle('btn-primary', autoscrollEnabled);
  }

  //move the bar to the right column for desktop and fill width for mobile
  function positionBar() {
    const col = document.querySelector('.col-md-4');
    if (!col || window.innerWidth < 992) {
      bar.style.left = '';
      bar.style.width = '';
      return;
    }
    const rect = col.getBoundingClientRect();
    bar.style.left = rect.left + 'px';
    bar.style.width = rect.width + 'px';
  }

  //animation loop
  function scrollStep(timestamp) {
    if (!autoscrollRunning) return;
    
    //setup for the first animation frame
    if (lastTimestamp === null) {
      lastTimestamp = timestamp;
      exactScrollY = window.scrollY;
    } else {
      
      //for next frames, check if the page was manually scrolled (by more than 2px)
      if (Math.abs(window.scrollY - exactScrollY) > 2.0) {
        exactScrollY = window.scrollY;
      }
    }

    //calculate elapsed time
    const deltaMs = timestamp - lastTimestamp;
    lastTimestamp = timestamp;

    //calculate movement and apply scroll
    const ticks = deltaMs / TICK;
    exactScrollY += ticks * BASE * autoscrollSpeed;
    window.scrollTo(0, exactScrollY);

    //stop at the bottom of the lyrics
    const scrollMax  = getScrollMax();
    if (window.scrollY >= scrollMax) {
      autoscrollRunning = false;
      lastTimestamp = null;
      updatePauseBtn();
      return;
    }
    
    //request next frame with the new timestamp
    rafId = requestAnimationFrame(scrollStep);
  }

  //main functions
  function startScrolling() {
    //prevent from running multiple animation loops
    if (rafId) cancelAnimationFrame(rafId);
    
    //reset timing and base position
    lastTimestamp = null;
    exactScrollY = window.scrollY;
    
    //start a new animation loop
    rafId = requestAnimationFrame(scrollStep);
  }

  function stopScrolling() {
    if (rafId) {
      cancelAnimationFrame(rafId);
      rafId = null;
    }
    lastTimestamp = null;
  }

  function enableAutoscroll() {
    autoscrollEnabled = true;
    autoscrollRunning = true;
    autoscrollSpeed   = SPEED_DEFAULT;
    bar.classList.add('autoscroll-bar--visible');
    positionBar();
    updateToggleBtn();
    updateSpeedLabel();
    updatePauseBtn();
    updateSlowerFaster();
    startScrolling();
  }

  function disableAutoscroll() {
    autoscrollEnabled = false;
    autoscrollRunning = false;
    stopScrolling();
    bar.classList.remove('autoscroll-bar--visible');
    updateToggleBtn();
  }

  function togglePause() {
    if (!autoscrollEnabled) return;
    autoscrollRunning = !autoscrollRunning;
    if (autoscrollRunning) {
      startScrolling();
    } else {
      stopScrolling();
    }
    updatePauseBtn();
  }

  function changeSpeed(delta) {
    autoscrollSpeed = Math.min(SPEED_MAX, Math.max(SPEED_MIN, autoscrollSpeed + delta));
    updateSpeedLabel();
    updateSlowerFaster();
    lastTimestamp = null; 
    exactScrollY = window.scrollY;
  }

  //events
  toggleBtn.addEventListener('click', function () {
    if (autoscrollEnabled) {
      disableAutoscroll();
    } else {
      enableAutoscroll();
    }
  });

  window.addEventListener('resize', function() {
    if (autoscrollEnabled) positionBar();
  });

  pauseBtn.addEventListener('click', togglePause);
  slowerBtn.addEventListener('click', function () { changeSpeed(-SPEED_STEP); });
  fasterBtn.addEventListener('click', function () { changeSpeed(SPEED_STEP); });
  closeBtn.addEventListener('click', disableAutoscroll);

})();
