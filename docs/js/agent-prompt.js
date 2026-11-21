// Кнопка «Скопировать» для блока с промптом на странице «ИИ-помощник».
document.addEventListener('DOMContentLoaded', function () {
  var blocks = document.querySelectorAll('code[class*="language-agent-prompt"]');
  blocks.forEach(function (code) {
    var pre = code.closest('pre');
    if (!pre || pre.querySelector('.prompt-copy-btn')) return;

    var btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'prompt-copy-btn';
    btn.textContent = 'Скопировать';
    pre.style.position = 'relative';
    pre.appendChild(btn);

    btn.addEventListener('click', function () {
      var text = code.innerText;
      function done() {
        var old = btn.textContent;
        btn.textContent = 'Скопировано ✓';
        btn.classList.add('copied');
        setTimeout(function () {
          btn.textContent = old;
          btn.classList.remove('copied');
        }, 2000);
      }
      function fallbackCopy() {
        var ta = document.createElement('textarea');
        ta.value = text;
        ta.style.position = 'fixed';
        ta.style.left = '-9999px';
        document.body.appendChild(ta);
        ta.select();
        try { document.execCommand('copy'); } catch (e) {}
        document.body.removeChild(ta);
      }
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(done).catch(function () {
          fallbackCopy();
          done();
        });
      } else {
        fallbackCopy();
        done();
      }
    });
  });
});
