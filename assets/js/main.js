// Sublyra Sciences site behavior: keeps the active tab visible and handles the contact form.
(function () {
  var current = document.querySelector('nav.tabs [aria-current="page"]');
  if (current) {
    var strip = current.closest(".tabs-scroll");
    strip.scrollLeft = current.offsetLeft - (strip.clientWidth - current.offsetWidth) / 2;
  }

  var year = document.querySelector("[data-year]");
  if (year) year.textContent = new Date().getFullYear();

  // Tabbed panels (Version 2 workflow section): click or arrow keys switch panels.
  Array.prototype.forEach.call(document.querySelectorAll("[data-tabs]"), function (box) {
    var tabs = Array.prototype.slice.call(box.querySelectorAll('[role="tab"]'));
    function select(tab) {
      tabs.forEach(function (t) {
        var on = t === tab;
        t.setAttribute("aria-selected", on ? "true" : "false");
        t.tabIndex = on ? 0 : -1;
        document.getElementById(t.getAttribute("aria-controls")).hidden = !on;
      });
    }
    tabs.forEach(function (t, i) {
      t.addEventListener("click", function () { select(t); });
      t.addEventListener("keydown", function (e) {
        var step = e.key === "ArrowRight" ? 1 : e.key === "ArrowLeft" ? -1 : 0;
        if (!step) return;
        var next = tabs[(i + step + tabs.length) % tabs.length];
        select(next);
        next.focus();
      });
    });
  });

  var form = document.getElementById("contact-form");
  if (!form) return;
  form.addEventListener("submit", function (e) {
    e.preventDefault();
    var done = document.getElementById("form-done");
    var name = document.getElementById("f-name").value.trim();
    var email = document.getElementById("f-email").value.trim();
    if (!name || !/^\S+@\S+\.\S+$/.test(email)) {
      done.textContent = "Add your name and a valid work email so we can reply.";
      done.hidden = false;
      return;
    }
    // No backend yet: connect this to a form service or CRM before launch (see README).
    done.textContent = "Thanks, " + name + ". This form isn't connected to an inbox yet, so nothing was sent.";
    done.hidden = false;
  });
})();
