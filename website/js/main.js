/**
 * BiblioQ landing page — version fetch, nav, simulators, modals
 */
(function () {
  "use strict";

  var VERSION_URL =
    "https://raw.githubusercontent.com/JENGUEL/-BiblioQ-Updates/main/version.json";

  var FALLBACK = {
    latest_version: "3.0.3",
    version: "3.0.3",
    download_url:
      "https://github.com/JENGUEL/-BiblioQ-Updates/releases/download/v3.0.3/BiblioQ_Setup.exe",
    release_date: "2026-06-11",
    file_size: 325453594,
  };

  function formatBytes(bytes) {
    if (!bytes) return "";
    return Math.round(bytes / (1024 * 1024)) + " MB";
  }

  function applyVersion(data) {
    var version = data.latest_version || data.version || FALLBACK.version;
    var url = data.download_url || FALLBACK.download_url;

    document.querySelectorAll("[data-download-link]").forEach(function (el) {
      el.href = url;
    });

    document.querySelectorAll("[data-version]").forEach(function (el) {
      el.textContent = "v" + version;
    });
  }

  fetch(VERSION_URL)
    .then(function (r) {
      return r.json();
    })
    .then(applyVersion)
    .catch(function () {
      applyVersion(FALLBACK);
    });

  document.addEventListener("DOMContentLoaded", function () {
    initMobileNav();
    initStickyBar();
    initModals();
    initQrScanner();
    initAiAssistant();
    initMockSidebarNav();
  });

  function initMobileNav() {
    var toggleBtn = document.getElementById("globalNavToggle");
    var navLinks = document.getElementById("globalNavLinks");

    if (!toggleBtn || !navLinks) return;

    toggleBtn.addEventListener("click", function () {
      navLinks.classList.toggle("active");
      toggleBtn.textContent = navLinks.classList.contains("active") ? "✕" : "☰";
    });

    navLinks.querySelectorAll("a").forEach(function (link) {
      link.addEventListener("click", function () {
        navLinks.classList.remove("active");
        toggleBtn.textContent = "☰";
      });
    });
  }

  function initStickyBar() {
    var stickyBar = document.getElementById("stickyActionBar");
    if (!stickyBar) return;

    window.addEventListener("scroll", function () {
      if (window.scrollY > 450) {
        stickyBar.classList.add("visible");
      } else {
        stickyBar.classList.remove("visible");
      }
    });
  }

  function initModals() {
    var modal = document.getElementById("licensingModal");
    if (!modal) return;

    var openButtons = [
      document.getElementById("subNavLicenseBtn"),
      document.getElementById("licensingRequestBtn"),
      document.getElementById("stickyActionBtn"),
    ];
    var closeBtn = document.getElementById("modalCloseBtn");
    var cancelBtn = document.getElementById("formCancelBtn");
    var form = document.getElementById("licenseForm");

    function openModal() {
      modal.classList.add("active");
      document.body.style.overflow = "hidden";
    }

    function closeModal() {
      modal.classList.remove("active");
      document.body.style.overflow = "";
    }

    openButtons.forEach(function (btn) {
      if (btn) btn.addEventListener("click", openModal);
    });

    if (closeBtn) closeBtn.addEventListener("click", closeModal);
    if (cancelBtn) cancelBtn.addEventListener("click", closeModal);

    modal.addEventListener("click", function (e) {
      if (e.target === modal) closeModal();
    });

    if (form) {
      form.addEventListener("submit", function (e) {
        e.preventDefault();
        if (!form.checkValidity()) {
          form.reportValidity();
          return;
        }
        var name = document.getElementById("contactName").value;
        var email = document.getElementById("schoolEmail").value;
        var school = document.getElementById("schoolName").value;
        var students = document.getElementById("remarks").value || "Not specified";
        var subject = encodeURIComponent("BiblioQ Site License Quote — " + school);
        var body = encodeURIComponent(
          "Contact: " + name + "\nSchool: " + school + "\nEstimated students: " + students
        );
        window.location.href = "mailto:license@biblioq.com?subject=" + subject + "&body=" + body;
        showToast("Opening your email client to send the quote request…");
        closeModal();
        form.reset();
      });
    }
  }

  function initQrScanner() {
    var scanIndicator = document.getElementById("scanIndicator");
    var feedList = document.getElementById("attendanceFeedList");
    var mockVisitorCount = document.getElementById("mockVisitorCount");

    if (!feedList) return;

    var visitorCount = 142;
    var mockStudents = [
      { name: "Juan dela Cruz", grade: "Grade 10 - Integrity", id: "2026-0125" },
      { name: "Maria Santos", grade: "Grade 8 - Humility", id: "2026-0348" },
      { name: "Carl Smith", grade: "Grade 11 - Fidelity", id: "2026-0881" },
      { name: "Chloe Gonzalez", grade: "Grade 9 - Prudence", id: "2026-0412" },
      { name: "James Yap", grade: "Grade 7 - Faith", id: "2026-0094" },
      { name: "Aisha Ibrahim", grade: "Grade 12 - Piety", id: "2026-0610" },
    ];
    var studentIdx = 0;

    function playScanBeep() {
      try {
        var AudioCtx = window.AudioContext || window.webkitAudioContext;
        if (!AudioCtx) return;
        var ctx = new AudioCtx();
        var osc = ctx.createOscillator();
        var gain = ctx.createGain();
        osc.type = "sine";
        osc.frequency.setValueAtTime(1400, ctx.currentTime);
        gain.gain.setValueAtTime(0.06, ctx.currentTime);
        gain.gain.exponentialRampToValueAtTime(0.0001, ctx.currentTime + 0.15);
        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.start();
        osc.stop(ctx.currentTime + 0.15);
      } catch (err) {
        /* audio blocked */
      }
    }

    function runScanCycle() {
      setTimeout(function () {
        if (scanIndicator) scanIndicator.classList.add("active");
        playScanBeep();

        var student = mockStudents[studentIdx];
        studentIdx = (studentIdx + 1) % mockStudents.length;

        visitorCount += 1;
        if (mockVisitorCount) mockVisitorCount.textContent = visitorCount;

        var row = document.createElement("div");
        row.className = "attendance-row";
        row.innerHTML =
          '<div class="row-student">' +
          '<span class="row-name">' + student.name + "</span>" +
          '<span class="row-meta">' + student.grade + " · ID: " + student.id + "</span>" +
          "</div>" +
          '<span class="row-status">Check-In</span>';

        feedList.insertBefore(row, feedList.firstChild);
        if (feedList.children.length > 4) {
          feedList.removeChild(feedList.lastChild);
        }

        setTimeout(function () {
          if (scanIndicator) scanIndicator.classList.remove("active");
        }, 1000);
      }, 1200);
    }

    runScanCycle();
    setInterval(runScanCycle, 6000);
  }

  function initAiAssistant() {
    var simulator = document.getElementById("simulator");
    var chatHistory = document.getElementById("aiChatHistory");
    if (!simulator || !chatHistory) return;

    var qaDatabase = {
      trend: {
        question: "How is library attendance trending this month?",
        answer:
          "Based on SQLite logs for the last 30 days, we've registered 1,420 total visits, marking a 14.5% attendance increase vs the prior month. Grade 10 has the highest engagement frequency (4.2 visits/student).",
      },
      stock: {
        question: "Show me books with low stock.",
        answer:
          "SQLite database catalog returned 3 books at or below threshold (copy limit = 1):\n\n• 'The Great Gatsby' (0 copies available out of 2 lended)\n• 'To Kill a Mockingbird' (1 copy available out of 1)\n• '1984' (0 copies available out of 3)\n\nWould you like to draft a purchasing recommendation?",
      },
      overdue: {
        question: "Check for overdue books.",
        answer:
          "Identified 2 overdue items with active fine records:\n\n• Student: Albert Dinglasa (Grade 12 - Loyalty)\n  Book: 'Introduction to Algorithms' (12 days overdue)\n  Accrued Fine: ₱60.00 (charged at ₱5.00/day)\n\n• Student: Chloe Gonzalez (Grade 9 - Prudence)\n  Book: 'Calculus Vol 1' (3 days overdue)\n  Accrued Fine: ₱15.00\n\nDrafted notice templates for parents. Ready to email.",
      },
      report: {
        question: "Send this month's attendance report to principal@school.edu",
        answer:
          "Confirmed: June attendance report → principal@school.edu.\n\nGenerated Attendance_2026-06-01_2026-06-30.pdf from SQLite logs (1,420 visits, 14.5% increase vs prior month).\n\nReport emailed automatically via school SMTP.\n\nReport sent successfully.",
      },
    };

    var typingInterval = null;

    function typeText(element, text) {
      if (!element) return;
      var index = 0;
      element.textContent = "";

      if (typingInterval) clearInterval(typingInterval);

      typingInterval = setInterval(function () {
        if (index < text.length) {
          element.textContent = text.slice(0, index + 1);
          index += 1;
          chatHistory.scrollTop = chatHistory.scrollHeight;
        } else {
          clearInterval(typingInterval);
          typingInterval = null;
        }
      }, 15);
    }

    function renderExchange(qa) {
      chatHistory.innerHTML = "";

      var userBubble = document.createElement("div");
      userBubble.className = "chat-bubble user";
      userBubble.innerHTML =
        '<span class="sender">Librarian</span><div class="msg-content"></div>';
      userBubble.querySelector(".msg-content").textContent = qa.question;
      chatHistory.appendChild(userBubble);

      var responseBubble = document.createElement("div");
      responseBubble.className = "chat-bubble assistant";
      responseBubble.innerHTML =
        '<span class="sender">BiblioQ AI Agent</span><div class="msg-content"></div>';
      chatHistory.appendChild(responseBubble);

      typeText(responseBubble.querySelector(".msg-content"), qa.answer);
    }

    simulator.addEventListener("click", function (e) {
      var btn = e.target.closest(".ai-query-btn");
      if (!btn || !simulator.contains(btn)) return;

      simulator.querySelectorAll(".ai-query-btn").forEach(function (b) {
        b.classList.remove("active");
      });
      btn.classList.add("active");

      var queryType = btn.getAttribute("data-query");
      var qa = qaDatabase[queryType];
      if (!qa) return;

      renderExchange(qa);
    });
  }

  function initMockSidebarNav() {
    var items = document.querySelectorAll("[data-mock-nav]");
    var indicator = document.querySelector(".mock-sidebar-indicator");

    function moveMockIndicator(btn) {
      if (!indicator || !btn) return;
      var sidebar = btn.closest(".mock-sidebar");
      if (!sidebar) return;
      var rect = btn.getBoundingClientRect();
      var sRect = sidebar.getBoundingClientRect();
      indicator.style.top = rect.top - sRect.top + "px";
    }

    items.forEach(function (item) {
      item.addEventListener("click", function () {
        items.forEach(function (el) {
          el.classList.remove("active");
        });
        item.classList.add("active");
        moveMockIndicator(item);

        var label = item.getAttribute("aria-label") || "Feature";
        if (label.indexOf("AI") >= 0) {
          showToast('Open the <a href="demo.html#ai-chat">Live Demo</a> to chat with the AI assistant.');
          return;
        }
        showToast('Preview only — <a href="demo.html">open Live Demo</a> for the full dashboard.');
      });
    });

    var first = document.querySelector(".mock-sidebar-icon.active");
    if (first) moveMockIndicator(first);
  }

  var toastTimer = null;

  function showToast(html) {
    var toast = document.getElementById("landingToast");
    if (!toast) return;
    toast.innerHTML = html;
    toast.classList.add("is-visible");
    if (toastTimer) clearTimeout(toastTimer);
    toastTimer = setTimeout(function () {
      toast.classList.remove("is-visible");
    }, 3500);
  }
})();
