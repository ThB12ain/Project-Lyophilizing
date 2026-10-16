// Sublyra Sciences site behavior: keeps the active tab visible and handles the contact form.
(function () {
  var current = document.querySelector('nav.tabs [aria-current="page"]');
  if (current) {
    var strip = current.closest(".tabs-scroll");
    strip.scrollLeft = current.offsetLeft - (strip.clientWidth - current.offsetWidth) / 2;
  }

  var year = document.querySelector("[data-year]");
  if (year) year.textContent = new Date().getFullYear();

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
