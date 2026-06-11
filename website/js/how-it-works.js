/**
 * How It Works page — scroll-triggered workflow animations
 */
(function () {
  "use strict";

  document.addEventListener("DOMContentLoaded", function () {
    if (!document.body.classList.contains("hiw-page")) return;
    initHiwScrollReveal();
    initHiwMembersDemo();
    initHiwBarChart();
    initHiwAiTypewriter();
    initHiwEmailDemo();
    initHiwReportToast();
    initHiwE2e();
  });

  function initHiwScrollReveal() {
    var targets = document.querySelectorAll("[data-hiw-reveal]");
    if (!targets.length || !("IntersectionObserver" in window)) {
      targets.forEach(function (el) { el.classList.add("is-visible"); });
      return;
    }

    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.25, rootMargin: "0px 0px -10% 0px" }
    );

    targets.forEach(function (el) { observer.observe(el); });
  }

  function initHiwMembersDemo() {
    var section = document.getElementById("hiw-members");
    var tbody = document.getElementById("hiw-mock-tbody");
    var filter = document.getElementById("hiw-mock-filter");
    var table = document.getElementById("hiw-mock-table");
    if (!section || !tbody) return;

    var played = false;

    function runSequence() {
      if (played) return;
      played = true;

      setTimeout(function () {
        var row = document.createElement("tr");
        row.className = "hiw-row-enter";
        row.innerHTML = "<td>Ana Reyes</td><td>9</td><td>Hope</td><td><i class=\"fa-regular fa-pen-to-square\"></i></td>";
        tbody.appendChild(row);
      }, 400);

      setTimeout(function () {
        var icon = tbody.querySelector(".hiw-edit-icon");
        if (icon) icon.classList.add("hiw-edit-flash");
      }, 1200);

      setTimeout(function () {
        if (filter) filter.classList.add("hiw-filter-open");
        if (table) table.classList.add("hiw-filter-expanded");
      }, 1800);
    }

    if (!("IntersectionObserver" in window)) {
      runSequence();
      return;
    }

    var obs = new IntersectionObserver(
      function (entries) {
        if (entries[0].isIntersecting) {
          runSequence();
          obs.disconnect();
        }
      },
      { threshold: 0.3 }
    );
    obs.observe(section);
  }

  function initHiwBarChart() {
    var chart = document.getElementById("hiw-bar-chart");
    if (!chart) return;

    var played = false;

    function animateBars() {
      if (played) return;
      played = true;
      chart.classList.add("is-animated");
      chart.querySelectorAll(".hiw-bar").forEach(function (bar, i) {
        setTimeout(function () {
          bar.style.height = bar.getAttribute("data-h") + "%";
        }, i * 120);
      });
    }

    if (!("IntersectionObserver" in window)) {
      animateBars();
      return;
    }

    var obs = new IntersectionObserver(
      function (entries) {
        if (entries[0].isIntersecting) {
          animateBars();
          obs.disconnect();
        }
      },
      { threshold: 0.3 }
    );
    obs.observe(chart);
  }

  function initHiwAiTypewriter() {
    var section = document.getElementById("hiw-ai");
    var chat = document.getElementById("hiw-ai-chat");
    if (!section || !chat) return;

    var question = "Show me overdue books";
    var answer =
      "14 overdue titles · ₱420 total fines.\n\n• Juan Dela Cruz — Noli Me Tangere (₱30)\n• Sofia Garcia — The Great Gatsby (₱50)\n• Miguel Torres — Introduction to Physics (₱40)";

    var played = false;

    function typeText(element, text) {
      var index = 0;
      element.textContent = "";
      var cursor = document.createElement("span");
      cursor.className = "typing-cursor";
      element.appendChild(cursor);

      var interval = setInterval(function () {
        if (index < text.length) {
          cursor.before(text.charAt(index));
          index += 1;
          chat.scrollTop = chat.scrollHeight;
        } else {
          clearInterval(interval);
          cursor.remove();
        }
      }, 18);
    }

    function runChat() {
      if (played) return;
      played = true;

      chat.innerHTML =
        '<div class="chat-bubble user">' +
        '<span class="sender">Librarian</span>' +
        '<div class="msg-content">' + question + "</div></div>";

      var responseBubble = document.createElement("div");
      responseBubble.className = "chat-bubble assistant";
      responseBubble.innerHTML =
        '<span class="sender">BiblioQ AI</span>' +
        '<div class="msg-content" id="hiwAiResponse"></div>';
      chat.appendChild(responseBubble);

      setTimeout(function () {
        typeText(document.getElementById("hiwAiResponse"), answer);
      }, 500);
    }

    if (!("IntersectionObserver" in window)) {
      runChat();
      return;
    }

    var obs = new IntersectionObserver(
      function (entries) {
        if (entries[0].isIntersecting) {
          runChat();
          obs.disconnect();
        }
      },
      { threshold: 0.3 }
    );
    obs.observe(section);
  }

  function showHiwToast(msg) {
    var toast = document.getElementById("hiwToast");
    if (!toast) return;
    toast.textContent = msg;
    toast.classList.add("is-visible");
    setTimeout(function () { toast.classList.remove("is-visible"); }, 3200);
  }

  function initHiwEmailDemo() {
    var section = document.getElementById("hiw-ai");
    var stage = document.getElementById("hiw-email-anim");
    var btn = document.getElementById("hiw-email-demo-btn");
    var status = document.getElementById("hiw-email-status");
    if (!stage || !btn) return;

    var animPlayed = false;

    function playEmailAnimation() {
      if (animPlayed) return;
      animPlayed = true;
      stage.classList.add("is-animating");
      var reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
      var delay = reducedMotion ? 100 : 4200;
      setTimeout(function () {
        if (status) status.textContent = "Report sent successfully.";
      }, delay);
    }

    if (section && "IntersectionObserver" in window) {
      var obs = new IntersectionObserver(
        function (entries) {
          if (entries[0].isIntersecting) {
            playEmailAnimation();
            obs.disconnect();
          }
        },
        { threshold: 0.25 }
      );
      obs.observe(stage);
    } else {
      playEmailAnimation();
    }

    btn.addEventListener("click", function () {
      stage.classList.remove("is-animating");
      void stage.offsetWidth;
      stage.classList.add("is-animating");
      if (status) status.textContent = "";
      var reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
      setTimeout(function () {
        if (status) status.textContent = "Report sent successfully.";
      }, reducedMotion ? 100 : 4200);
      showHiwToast("Demo: Report would be emailed to principal@school.edu");
    });
  }

  function initHiwReportToast() {
    var btn = document.getElementById("hiw-download-report");
    if (!btn) return;

    btn.addEventListener("click", function () {
      showHiwToast("Attendance_Report_2026-06-07.pdf downloaded (demo).");
    });
  }

  function initHiwE2e() {
    var wrap = document.querySelector("[data-hiw-e2e]");
    if (!wrap) return;

    if (!("IntersectionObserver" in window)) {
      wrap.classList.add("is-visible");
      return;
    }

    var obs = new IntersectionObserver(
      function (entries) {
        if (entries[0].isIntersecting) {
          wrap.classList.add("is-visible");
        }
      },
      { threshold: 0.2 }
    );
    obs.observe(wrap);
  }
})();
