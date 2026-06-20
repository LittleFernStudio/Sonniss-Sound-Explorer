document.addEventListener('DOMContentLoaded', () => {
  const audios = Array.from(document.querySelectorAll('audio'));

  // Only one audio at a time when playing manually
  audios.forEach(a => a.addEventListener('play', () => {
    audios.forEach(other => { if (other !== a) other.pause(); });
  }));

  const playAllBtn = document.getElementById('playAll');
  const pauseAllBtn = document.getElementById('pauseAll');
  const stopAllBtn  = document.getElementById('stopAll');

  function stopAll(){
    audios.forEach(a => { a.pause(); a.currentTime = 0; });
  }

  // Sequential play-through
  playAllBtn.addEventListener('click', () => {
    stopAll();
    let i = 0;
    const playNext = () => {
      if (i >= audios.length) return; // done
      const current = audios[i];
      current.currentTime = 0;
      current.play().catch(() => {/* ignore autoplay block */});
      const onEnded = () => { current.removeEventListener('ended', onEnded); i++; playNext(); };
      current.addEventListener('ended', onEnded);
    };
    playNext();
  });

  pauseAllBtn.addEventListener('click', () => {
    audios.forEach(a => a.pause());
  });

  stopAllBtn.addEventListener('click', stopAll);
});

  // Delegate clicks for any link with class "copy-link"
  document.addEventListener('click', async (e) => {
    const a = e.target.closest('a.copy-link');
    if (!a) return;

    e.preventDefault(); // don't try to open it in the browser
    const textToCopy = a.getAttribute('href'); // copy the raw attribute text

    try {
      if (navigator.clipboard && window.isSecureContext) {
        await navigator.clipboard.writeText(textToCopy);
      } else {
        // Fallback for non-HTTPS/older browsers
        const ta = document.createElement('textarea');
        ta.value = textToCopy;
        ta.setAttribute('readonly', '');
        ta.style.position = 'fixed';
        ta.style.opacity = '0';
        document.body.appendChild(ta);
        ta.select();
        document.execCommand('copy');
        document.body.removeChild(ta);
      }
      // Optional: quick visual confirmation
      a.title = 'Copied!';
      setTimeout(() => (a.title = ''), 1200);
    } catch (err) {
      console.error('Copy failed:', err);
      alert('Could not copy path. You can right-click and choose “Copy link address” instead.');
    }
  });
