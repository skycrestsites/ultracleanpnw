(function () {
  var CONTACT_EMAIL = "info@ultracleanpnw.com";
  var root = document.documentElement;
  root.classList.remove("no-js");

  var header = document.querySelector(".site-header");
  var quickBar = document.querySelector(".quick-bar");
  function onScroll() {
    var y = window.scrollY || window.pageYOffset;
    if (header) header.classList.toggle("scrolled", y > 8);
    if (quickBar) quickBar.classList.toggle("show", y > 420);
  }
  window.addEventListener("scroll", onScroll, { passive: true });
  onScroll();

  var toggle = document.querySelector(".menu-toggle");
  var mobileNav = document.getElementById("mobile-nav");
  function setMenu(open) {
    document.body.classList.toggle("menu-open", open);
    if (toggle) toggle.setAttribute("aria-expanded", open ? "true" : "false");
    if (mobileNav) mobileNav.setAttribute("aria-hidden", open ? "false" : "true");
  }
  if (toggle) {
    toggle.addEventListener("click", function () {
      setMenu(!document.body.classList.contains("menu-open"));
    });
  }
  if (mobileNav) {
    mobileNav.addEventListener("click", function (e) {
      if (e.target.closest("a")) setMenu(false);
    });
  }
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") setMenu(false);
  });
  window.addEventListener("resize", function () {
    if (window.innerWidth >= 1080) setMenu(false);
  });

  var reveals = document.querySelectorAll(".reveal");
  if ("IntersectionObserver" in window) {
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add("in");
          io.unobserve(entry.target);
        }
      });
    }, { rootMargin: "0px 0px -8% 0px", threshold: 0.08 });
    reveals.forEach(function (el) { io.observe(el); });
  } else {
    reveals.forEach(function (el) { el.classList.add("in"); });
  }

  var params = new URLSearchParams(window.location.search);
  var preset = params.get("service");
  document.querySelectorAll("select[name='service']").forEach(function (sel) {
    if (preset && sel.querySelector("option[value='" + preset + "']")) sel.value = preset;
  });

  document.querySelectorAll("form.quote-form").forEach(function (form) {
    form.addEventListener("submit", function (e) {
      if (form.getAttribute("action")) return;
      e.preventDefault();
      if (!form.reportValidity()) return;
      var data = new FormData(form);
      var sel = form.querySelector("select[name='service']");
      var serviceLabel = sel && sel.selectedIndex > 0 ? sel.options[sel.selectedIndex].text : "Not sure yet";
      var lines = [
        "Name: " + (data.get("name") || ""),
        "Email: " + (data.get("email") || ""),
        "Phone: " + (data.get("phone") || ""),
        "Service: " + serviceLabel,
        "City or ZIP: " + (data.get("location") || ""),
        "",
        "Details:",
        data.get("message") || ""
      ];
      var subject = "Quote request: " + serviceLabel + " (" + (data.get("name") || "Website") + ")";
      window.location.href = "mailto:" + CONTACT_EMAIL +
        "?subject=" + encodeURIComponent(subject) +
        "&body=" + encodeURIComponent(lines.join("\n"));
      var status = form.querySelector(".form-status");
      if (status) {
        status.textContent = "Thanks! Your email app should open with your request ready to send. If it does not, email us at " + CONTACT_EMAIL + ".";
        status.classList.add("show");
      }
    });
  });

  document.querySelectorAll("[data-year]").forEach(function (el) {
    el.textContent = new Date().getFullYear();
  });
})();
