/**
 * BiblioQ demo — full Flet shell with mock data, modals, and page inits
 */
(function (global) {
  "use strict";

  const STORAGE_KEY = "biblioq_demo_last_question";

  const DEMO_DATA = {
    members: [
      { id: "2026-0348", name: "Maria Santos", grade: 10, section: "Integrity", status: "active", visits: 18, lastEntry: "Today 10:42 AM" },
      { id: "2026-0312", name: "Juan Dela Cruz", grade: 10, section: "Integrity", status: "active", visits: 16, lastEntry: "Today 9:15 AM" },
      { id: "2026-0289", name: "Ana Reyes", grade: 9, section: "Hope", status: "active", visits: 15, lastEntry: "Yesterday" },
      { id: "2026-0198", name: "Carlo Mendoza", grade: 11, section: "Charity", status: "active", visits: 14, lastEntry: "Yesterday" },
      { id: "2026-0156", name: "Sofia Garcia", grade: 10, section: "Faith", status: "active", visits: 13, lastEntry: "Jun 5" },
      { id: "2026-0142", name: "Miguel Torres", grade: 8, section: "Peace", status: "active", visits: 11, lastEntry: "Jun 4" },
      { id: "2025-0891", name: "Isabella Cruz", grade: 12, section: "Love", status: "active", visits: 10, lastEntry: "Jun 3" },
      { id: "2025-0765", name: "Diego Ramos", grade: 7, section: "Joy", status: "inactive", visits: 3, lastEntry: "May 20" },
      { id: "2025-0654", name: "Patricia Lim", grade: 11, section: "Charity", status: "active", visits: 9, lastEntry: "Jun 2" },
      { id: "2024-0999", name: "Rafael Santos", grade: 12, section: "Love", status: "graduated", visits: 45, lastEntry: "Mar 15" },
    ],
    scans: [
      { name: "Maria Santos", grade: 10, section: "Integrity", time: "10:42" },
      { name: "Juan Dela Cruz", grade: 10, section: "Integrity", time: "10:38" },
      { name: "Ana Reyes", grade: 9, section: "Hope", time: "10:35" },
      { name: "Carlo Mendoza", grade: 11, section: "Charity", time: "10:30" },
      { name: "Sofia Garcia", grade: 10, section: "Faith", time: "10:28" },
      { name: "Miguel Torres", grade: 8, section: "Peace", time: "10:22" },
      { name: "Isabella Cruz", grade: 12, section: "Love", time: "10:18" },
      { name: "Patricia Lim", grade: 11, section: "Charity", time: "10:12" },
    ],
    books: [
      { title: "Introduction to Physics", author: "Young & Freedman", isbn: "978-0321973610", available: 3, total: 5 },
      { title: "Noli Me Tangere", author: "Jose Rizal", isbn: "978-971080649-8", available: 1, total: 3 },
      { title: "The Great Gatsby", author: "F. Scott Fitzgerald", isbn: "978-0743273565", available: 0, total: 2 },
      { title: "Filipino Grammar", author: "Lopez & Santos", isbn: "978-9712312345", available: 4, total: 4 },
      { title: "World History", author: "Spielvogel", isbn: "978-130509021-5", available: 2, total: 5 },
      { title: "Algebra Fundamentals", author: "Hall & Knight", isbn: "978-048664761-9", available: 5, total: 6 },
    ],
    borrowRecords: [
      { date: "Jun 7", student: "Maria Santos", gradeSection: "Grade 10 - Integrity", book: "Introduction to Physics", status: "borrowed", fine: 0 },
      { date: "Jun 5", student: "Juan Dela Cruz", gradeSection: "Grade 10 - Integrity", book: "Noli Me Tangere", status: "overdue", fine: 30 },
      { date: "Jun 4", student: "Ana Reyes", gradeSection: "Grade 9 - Hope", book: "Filipino Grammar", status: "returned", fine: 0 },
      { date: "Jun 3", student: "Carlo Mendoza", gradeSection: "Grade 11 - Charity", book: "World History", status: "borrowed", fine: 0 },
      { date: "Jun 1", student: "Sofia Garcia", gradeSection: "Grade 10 - Faith", book: "The Great Gatsby", status: "overdue", fine: 50 },
    ],
    topBooks: [
      { rank: 1, title: "Introduction to Physics", isbn: "978-0321973610", count: 42 },
      { rank: 2, title: "Noli Me Tangere", isbn: "978-971080649-8", count: 38 },
      { rank: 3, title: "Filipino Grammar", isbn: "978-9712312345", count: 31 },
      { rank: 4, title: "World History", isbn: "978-130509021-5", count: 27 },
      { rank: 5, title: "Algebra Fundamentals", isbn: "978-048664761-9", count: 22 },
    ],
    overdueBooks: [
      { title: "Noli Me Tangere", student: "Juan Dela Cruz", gradeSection: "Grade 10 - Integrity", due: "Jun 1", days: 6, fine: 30 },
      { title: "The Great Gatsby", student: "Sofia Garcia", gradeSection: "Grade 10 - Faith", due: "May 28", days: 10, fine: 50 },
      { title: "Introduction to Physics", student: "Miguel Torres", gradeSection: "Grade 8 - Peace", due: "May 30", days: 8, fine: 40 },
    ],
    gradeActivity: [
      { grade: 7, pct: 62 }, { grade: 8, pct: 71 }, { grade: 9, pct: 78 },
      { grade: 10, pct: 92 }, { grade: 11, pct: 85 }, { grade: 12, pct: 68 },
    ],
    bookActivity: [
      { type: "borrow", text: "Maria Santos borrowed Introduction to Physics", time: "2m ago" },
      { type: "return", text: "Ana Reyes returned Filipino Grammar", time: "15m ago" },
      { type: "overdue", text: "Juan Dela Cruz — Noli Me Tangere overdue", time: "1h ago" },
      { type: "borrow", text: "Carlo Mendoza borrowed World History", time: "2h ago" },
    ],
    printHistory: [
      "Attendance_2026-06-01_2026-06-07.pdf",
      "TopVisitors_2026-06_Top10.pdf",
      "Overdue_Books_2026-06-07.pdf",
    ],
    dashboardHistory: [
      "Maria Santos · 10:42 AM", "Juan Dela Cruz · 9:15 AM", "Ana Reyes · Yesterday",
      "Carlo Mendoza · Yesterday", "Sofia Garcia · Jun 5",
    ],
    dashboardBookmarks: ["Introduction to Physics", "Noli Me Tangere", "Filipino Grammar"],
    dashboardActivity: [
      "Checked in at library", "Borrowed Introduction to Physics", "Returned Filipino Grammar",
    ],
  };

  const DEMO_RESPONSES = {
    "Show me today's library statistics":
      "247 students checked in today across 12 sections. 8 books borrowed, 5 returned. Peak hour: 10:00–11:00 AM.",
    "Who are the top visitors this month?":
      "1. Maria Santos (18 visits)\n2. Juan Dela Cruz (16)\n3. Ana Reyes (15)\n4. Carlo Mendoza (14)\n5. Sofia Garcia (13)",
    "Which books are low on stock?":
      "Low stock alerts:\n• Noli Me Tangere — 1/3 (Low)\n• The Great Gatsby — 0/2 (Out)\n• Introduction to Physics — 3/5 (OK, trending low)",
    "List overdue books with fines":
      "14 overdue titles · ₱420 total fines.\nTop: Noli Me Tangere (Juan Dela Cruz, ₱30), The Great Gatsby (Sofia Garcia, ₱50).",
    "Predict attendance for next week":
      "Based on 4-week trends: expect 820–910 weekly visits. Peak days: Tue–Thu. Recommend extra staffing 10–11 AM.",
    "Draft a letter to parents about overdue books":
      "Dear Parent/Guardian,\n\nThis is a reminder that your child has overdue library materials. Please return them to avoid accumulating fines.\n\nThank you,\nSchool Library",
    "Today's attendance?":
      "247 students checked in today across 12 sections. Peak hour: 10:00–11:00 AM (89 scans).",
    "Overdue books with fines":
      "14 overdue titles · ₱420 total fines. Top title: 'Introduction to Physics' (3 copies, 7 days late).",
    "Top 5 students this month":
      "1. Maria Santos (18 visits)\n2. Juan Dela Cruz (16)\n3. Ana Reyes (15)\n4. Carlo Mendoza (14)\n5. Sofia Garcia (13)",
    "Email this month's attendance report to principal@school.edu":
      "Confirmed: June attendance report → principal@school.edu.\n\nGenerated Attendance_2026-06-01_2026-06-30.pdf from your library database (1,420 visits, 14.5% increase vs prior month).\n\nReport emailed automatically via school SMTP.\n\nReport sent successfully.",
  };

  const AI_REPORT_QUESTION = "Email this month's attendance report to principal@school.edu";

  const AI_SUGGESTIONS = [
    "Show me today's library statistics",
    "Who are the top visitors this month?",
    "Which books are low on stock?",
    "List overdue books with fines",
    "Predict attendance for next week",
    "Draft a letter to parents about overdue books",
    AI_REPORT_QUESTION,
  ];

  const AI_QUICK = ["Today", "Top Visitors", "Overdue", "Inventory", "Predict", "Letter", "Email Report"];

  const AI_KEYWORDS = [
    { keys: ["attendance", "today", "check"], q: "Show me today's library statistics" },
    { keys: ["top", "visitor", "rank"], q: "Who are the top visitors this month?" },
    { keys: ["stock", "inventory", "low"], q: "Which books are low on stock?" },
    { keys: ["overdue", "fine"], q: "List overdue books with fines" },
    { keys: ["predict", "forecast", "next week"], q: "Predict attendance for next week" },
    { keys: ["letter", "parent", "draft"], q: "Draft a letter to parents about overdue books" },
    { keys: ["report", "email", "send", "principal"], q: AI_REPORT_QUESTION },
  ];

  const CHART_DATA = {
    day: { labels: ["8am", "10am", "12pm", "2pm", "4pm"], attendance: [18, 42, 78, 55, 32], sections: [2, 4, 7, 5, 3], students: [12, 28, 52, 38, 22] },
    week: { labels: ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"], attendance: [120, 185, 210, 175, 230, 45, 20], sections: [8, 10, 12, 11, 12, 4, 2], students: [95, 140, 165, 130, 180, 35, 15] },
    month: { labels: ["W1", "W2", "W3", "W4"], attendance: [680, 820, 750, 910], sections: [38, 42, 40, 45], students: [520, 640, 590, 720] },
  };

  const LINE_COLORS = { attendance: "#F7944D", sections: "#4CAF50", students: "#2196F3" };

  const REPORT_CARDS = [
    { id: "attendance", title: "Attendance Report", sub: "Daily, weekly, monthly or custom date range", icon: "fa-chart-line" },
    { id: "top-visitors", title: "Top Visitors", sub: "Monthly rankings with selection methodology", icon: "fa-trophy" },
    { id: "overdue", title: "Overdue Books", sub: "List of overdue books with fines", icon: "fa-triangle-exclamation" },
    { id: "qr", title: "QR Codes", sub: "Individual or bulk QR code sheet", icon: "fa-qrcode" },
    { id: "clearance", title: "Library Clearance", sub: "Student clearance for graduation", icon: "fa-circle-check" },
    { id: "grade-section", title: "Grade & Section Report", sub: "Detailed breakdown by grade and section", icon: "fa-school" },
  ];

  function escapeHtml(s) {
    return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;");
  }

  function initials(name) {
    return name.split(" ").map(function (p) { return p[0]; }).join("").slice(0, 2).toUpperCase();
  }

  function stockBadge(available, total) {
    var level = available === 0 ? "Out" : available <= 2 ? "Low" : "OK";
    var cls = level === "Out" ? "stock-out" : level === "Low" ? "stock-low" : "stock-ok";
    return '<span class="stock-badge ' + cls + '">' + available + "/" + total + " " + level + "</span>";
  }

  function statusDot(status) {
    return '<span class="status-dot status-dot--' + status + '"></span> ' + status.charAt(0).toUpperCase() + status.slice(1);
  }

  function typewriter(el, text, speed) {
    speed = speed || 18;
    return new Promise(function (resolve) {
      el.textContent = "";
      var i = 0;
      function tick() {
        if (i < text.length) { el.textContent += text.charAt(i); i += 1; setTimeout(tick, speed); }
        else resolve();
      }
      tick();
    });
  }

  function animateValue(el, target, duration) {
    if (!target || isNaN(parseInt(String(target).replace(/[^\d]/g, ""), 10))) { el.textContent = target; return; }
    var numericTarget = parseInt(String(target).replace(/[^\d]/g, ""), 10);
    var startTime = null;
    function frame(ts) {
      if (!startTime) startTime = ts;
      var progress = Math.min((ts - startTime) / duration, 1);
      var eased = 1 - Math.pow(1 - progress, 3);
      el.textContent = Math.floor(numericTarget * eased).toLocaleString();
      if (progress < 1) requestAnimationFrame(frame);
      else el.textContent = target;
    }
    requestAnimationFrame(frame);
  }

  function showFletToast(msg) {
    var t = document.getElementById("flet-toast");
    if (!t) return;
    t.textContent = msg;
    t.classList.add("is-visible");
    setTimeout(function () { t.classList.remove("is-visible"); }, 2800);
  }

  function showScanToast(name, grade, count) {
    var toast = document.getElementById("scan-toast");
    if (!toast) return;
    toast.innerHTML = '<div class="scan-toast__row"><div class="scan-toast__icon"><i class="fa-solid fa-check"></i></div><div><div class="scan-toast__title">Welcome, ' + escapeHtml(name) + '!</div><div class="scan-toast__sub">' + escapeHtml(grade) + '</div></div><span class="scan-toast__count">' + count + " today</span></div>";
    toast.classList.add("is-visible");
    setTimeout(function () { toast.classList.remove("is-visible"); }, 3400);
  }

  /* ── Modals ── */
  var DemoModals = {
    _step: 0,
    _ctx: {},
    _onComplete: null,

    open: function (type, ctx, onComplete) {
      this._type = type;
      this._ctx = ctx || {};
      this._step = 0;
      this._onComplete = onComplete || null;
      var modal = document.getElementById("demo-modal");
      if (modal) { modal.hidden = false; this._render(); }
    },

    close: function () {
      var modal = document.getElementById("demo-modal");
      if (modal) modal.hidden = true;
      document.getElementById("demo-modal-panel").innerHTML = "";
    },

    _render: function () {
      var panel = document.getElementById("demo-modal-panel");
      var html = "";
      var self = this;

      function header(title) {
        return '<div class="demo-modal__header"><h2>' + escapeHtml(title) + '</h2><button type="button" class="demo-modal__close" id="modal-close">&times;</button></div>';
      }
      function footer(primary, primaryLabel, showBack) {
        return '<div class="demo-modal__footer">' +
          (showBack ? '<button type="button" class="btn-outline" id="modal-back">Back</button>' : '<button type="button" class="btn-outline" id="modal-cancel">Cancel</button>') +
          '<button type="button" class="btn-primary" id="modal-primary">' + primaryLabel + '</button></div>';
      }
      function steps(n, current) {
        var s = '<div class="demo-modal__steps">';
        for (var i = 0; i < n; i++) s += '<span class="demo-modal__step' + (i <= current ? " is-done" : "") + '"></span>';
        return s + "</div>";
      }

      if (this._type === "add-member") {
        if (this._step === 0) {
          html = header("Add Member") + steps(2, 0) +
            '<div class="demo-modal__body"><label>First Name<input class="flet-input" id="m-first" value="' + escapeHtml(this._ctx.first || "") + '"></label>' +
            '<label>Last Name<input class="flet-input" id="m-last" value="' + escapeHtml(this._ctx.last || "") + '"></label>' +
            '<label>Grade<select class="flet-input" id="m-grade"><option>7</option><option>8</option><option>9</option><option' + (this._ctx.grade === "10" || !this._ctx.grade ? " selected" : "") + '>10</option><option>11</option><option>12</option></select></label>' +
            '<label>Section<input class="flet-input" id="m-section" value="' + escapeHtml(this._ctx.section || "Integrity") + '"></label>' +
            '<label>Student ID<input class="flet-input" id="m-id" value="' + escapeHtml(this._ctx.id || "2026-0400") + '"></label></div>' +
            footer(true, "Next →", false);
        } else {
          var fn = this._ctx.first || "New";
          var ln = this._ctx.last || "Student";
          html = header("QR Preview") + steps(2, 1) +
            '<div class="demo-modal__body demo-modal__qr"><div class="demo-qr-box"><i class="fa-solid fa-qrcode"></i></div>' +
            '<p><strong>' + escapeHtml(fn + " " + ln) + '</strong><br>Grade ' + escapeHtml(this._ctx.grade || "10") + " - " + escapeHtml(this._ctx.section || "Integrity") + '<br>ID: ' + escapeHtml(this._ctx.id || "2026-0400") + '</p></div>' +
            footer(true, "Save & Print QR", true);
        }
      } else if (this._type === "import-members") {
        if (this._step === 0) {
          html = header("Import Members") + steps(3, 0) +
            '<div class="demo-modal__body"><div class="demo-upload-zone"><i class="fa-solid fa-cloud-arrow-up"></i><p>Drop CSV file or click to browse</p><small>members_template.csv</small></div></div>' +
            footer(true, "Next →", false);
        } else if (this._step === 1) {
          html = header("Column Mapping") + steps(3, 1) +
            '<div class="demo-modal__body"><table class="flet-table"><thead><tr><th>CSV Column</th><th>Maps To</th></tr></thead><tbody>' +
            '<tr><td>first_name</td><td>First Name</td></tr><tr><td>last_name</td><td>Last Name</td></tr>' +
            '<tr><td>grade</td><td>Grade</td></tr><tr><td>section</td><td>Section</td></tr></tbody></table></div>' +
            footer(true, "Import", true);
        } else {
          html = header("Import Complete") + steps(3, 2) +
            '<div class="demo-modal__body"><p class="demo-success"><i class="fa-solid fa-circle-check"></i> 3 members imported successfully.</p>' +
            '<ul class="demo-import-list"><li>Juan Dela Cruz</li><li>Maria Santos</li><li>Pedro Reyes</li></ul></div>' +
            '<div class="demo-modal__footer"><button type="button" class="btn-primary" id="modal-primary">Done</button></div>';
        }
      } else if (this._type === "add-book") {
        html = header("Add New Book") +
          '<div class="demo-modal__body"><label>Title<input class="flet-input" id="b-title" value=""></label>' +
          '<label>Author<input class="flet-input" id="b-author" value=""></label>' +
          '<label>ISBN<input class="flet-input" id="b-isbn" value=""></label>' +
          '<label>Copies<input class="flet-input" type="number" id="b-copies" value="3"></label></div>' +
          footer(true, "Add Book", false);
      } else if (this._type === "borrow-book") {
        if (this._step === 0) {
          html = header("Borrow Book") + steps(2, 0) +
            '<div class="demo-modal__body"><label>Search Student<input class="flet-input" id="br-student" placeholder="Maria Santos"></label>' +
            '<div class="demo-picker-list">' + DEMO_DATA.members.slice(0, 5).map(function (m) {
              return '<button type="button" class="demo-picker-item" data-name="' + escapeHtml(m.name) + '">' + escapeHtml(m.name) + " · Grade " + m.grade + "</button>";
            }).join("") + '</div></div>' + footer(true, "Next →", false);
        } else {
          html = header("Select Book") + steps(2, 1) +
            '<div class="demo-modal__body"><div class="demo-picker-list">' + DEMO_DATA.books.map(function (b) {
              return '<button type="button" class="demo-picker-item" data-book="' + escapeHtml(b.title) + '">' + escapeHtml(b.title) + " (" + b.available + " avail)</button>";
            }).join("") + '</div></div>' + footer(true, "Confirm Borrow", true);
        }
      } else if (this._type === "return-book") {
        html = header("Return Book") +
          '<div class="demo-modal__body"><p>Select an active borrow:</p><div class="demo-picker-list">' +
          DEMO_DATA.borrowRecords.filter(function (r) { return r.status === "borrowed" || r.status === "overdue"; }).map(function (r) {
            return '<button type="button" class="demo-picker-item" data-return="' + escapeHtml(r.book) + '">' + escapeHtml(r.student) + " — " + escapeHtml(r.book) + "</button>";
          }).join("") + '</div></div>' + footer(true, "Confirm Return", false);
      } else if (this._type === "attendance-report") {
        html = header("Attendance Report") +
          '<div class="demo-modal__body"><div class="demo-preset-btns"><button type="button" class="demo-preset is-active">Today</button><button type="button" class="demo-preset">This Week</button><button type="button" class="demo-preset">This Month</button></div>' +
          '<label>From<input class="flet-input" type="date" value="2026-06-01"></label><label>To<input class="flet-input" type="date" value="2026-06-07"></label>' +
          '<label>Grade Filter<select class="flet-input"><option>All Grades</option><option>10</option><option>11</option></select></label></div>' +
          footer(true, "Generate PDF", false);
      } else if (this._type === "top-visitors") {
        html = header("Top Visitors Report") +
          '<div class="demo-modal__body"><label>Month<select class="flet-input"><option>June</option><option>May</option></select></label>' +
          '<label>Year<input class="flet-input" value="2026"></label><label>Top N<select class="flet-input"><option>10</option><option>25</option><option>50</option></select></label></div>' +
          footer(true, "Generate PDF", false);
      } else if (this._type === "overdue-report") {
        html = header("Overdue Books Report") +
          '<div class="demo-modal__body"><p>Generate a PDF listing all overdue books with fines as of today.</p><p><strong>14 overdue</strong> · <strong>₱420</strong> total fines</p></div>' +
          footer(true, "Generate PDF", false);
      } else if (this._type === "qr-codes") {
        if (this._step === 0) {
          html = header("QR Codes") + steps(2, 0) +
            '<div class="demo-modal__body"><label>Grade<select class="flet-input"><option>All</option><option>10</option></select></label>' +
            '<label>Section<select class="flet-input"><option>All</option><option>Integrity</option></select></label>' +
            '<div class="demo-check-list">' + DEMO_DATA.members.slice(0, 6).map(function (m, i) {
              return '<label><input type="checkbox" checked> ' + escapeHtml(m.name) + "</label>";
            }).join("") + '</div><button type="button" class="btn-outline demo-select-all">Select All</button></div>' +
            footer(true, "Preview", false);
        } else {
          html = header("QR Preview") + steps(2, 1) +
            '<div class="demo-modal__body"><div class="demo-qr-grid">' +
            DEMO_DATA.members.slice(0, 4).map(function (m) {
              return '<div class="demo-qr-card"><i class="fa-solid fa-qrcode"></i><span>' + escapeHtml(m.name) + "</span></div>";
            }).join("") + '</div><div class="demo-progress"><div class="demo-progress__bar" style="width:100%"></div></div></div>' +
            footer(true, "Print QR Sheet", true);
        }
      } else if (this._type === "clearance") {
        html = header("Library Clearance") +
          '<div class="demo-modal__body"><input class="flet-input" placeholder="Search student..."><div class="demo-picker-list">' +
          DEMO_DATA.members.filter(function (m) { return m.grade === 12; }).map(function (m) {
            return '<div class="demo-clearance-row"><span>' + escapeHtml(m.name) + " · Grade " + m.grade + '</span><button type="button" class="btn-outline demo-gen-clearance">Generate</button></div>';
          }).join("") + '</div></div>' + footer(true, "Close", false);
      } else if (this._type === "grade-section") {
        html = header("Grade & Section Report") +
          '<div class="demo-modal__body"><div class="demo-preset-btns"><button type="button" class="demo-preset is-active">This Week</button><button type="button" class="demo-preset">This Month</button></div>' +
          '<label>From<input class="flet-input" type="date"></label><label>To<input class="flet-input" type="date"></label></div>' +
          footer(true, "Generate PDF", false);
      } else if (this._type === "member-history") {
        var mem = this._ctx.member || DEMO_DATA.members[0];
        html = header("Visit History — " + mem.name) +
          '<div class="demo-modal__body"><ul class="demo-history-list">' +
          ["Jun 7 10:42 AM", "Jun 6 9:30 AM", "Jun 5 11:15 AM", "Jun 4 10:00 AM", "Jun 3 2:45 PM"].map(function (d) {
            return "<li>" + d + "</li>";
          }).join("") + '</ul></div><div class="demo-modal__footer"><button type="button" class="btn-primary" id="modal-primary">Close</button></div>';
      } else if (this._type === "top-users") {
        html = header("Top 3 Rankings") +
          '<div class="demo-modal__body"><ol class="demo-rank-list">' +
          DEMO_DATA.members.slice(0, 3).map(function (m, i) {
            return '<li><span class="demo-rank-num">' + (i + 1) + '</span><strong>' + escapeHtml(m.name) + '</strong><span>' + m.visits + " visits</span></li>";
          }).join("") + '</ol></div><div class="demo-modal__footer"><button type="button" class="btn-primary" id="modal-primary">Close</button></div>';
      }

      panel.innerHTML = html;
      document.getElementById("modal-close").addEventListener("click", function () { self.close(); });
      var cancel = document.getElementById("modal-cancel");
      if (cancel) cancel.addEventListener("click", function () { self.close(); });
      var back = document.getElementById("modal-back");
      if (back) back.addEventListener("click", function () { self._step--; self._render(); });
      var primary = document.getElementById("modal-primary");
      if (primary) primary.addEventListener("click", function () { self._primary(); });

      panel.querySelectorAll(".demo-preset").forEach(function (btn) {
        btn.addEventListener("click", function () {
          panel.querySelectorAll(".demo-preset").forEach(function (b) { b.classList.remove("is-active"); });
          btn.classList.add("is-active");
        });
      });
      panel.querySelectorAll(".demo-gen-clearance").forEach(function (btn) {
        btn.addEventListener("click", function () {
          showFletToast("Clearance generated (demo).");
          if (self._onComplete) self._onComplete("Clearance_" + Date.now() + ".pdf");
        });
      });
    },

    _primary: function () {
      var self = this;
      if (this._type === "add-member" && this._step === 0) {
        this._ctx.first = document.getElementById("m-first").value;
        this._ctx.last = document.getElementById("m-last").value;
        this._ctx.grade = document.getElementById("m-grade").value;
        this._ctx.section = document.getElementById("m-section").value;
        this._ctx.id = document.getElementById("m-id").value;
      }
      var multiStep = {
        "add-member": 2, "import-members": 3, "borrow-book": 2, "qr-codes": 2,
      };
      var max = multiStep[this._type] || 1;
      if (this._step < max - 1) {
        this._step++;
        this._render();
        return;
      }
      var messages = {
        "add-member": "Member added with QR code (demo).",
        "import-members": "Import complete (demo).",
        "add-book": "Book added to catalog (demo).",
        "borrow-book": "Book borrowed successfully (demo).",
        "return-book": "Book returned successfully (demo).",
        "attendance-report": "Attendance_2026-06-01_2026-06-07.pdf",
        "top-visitors": "TopVisitors_2026-06_Top10.pdf",
        "overdue-report": "Overdue_Books_2026-06-07.pdf",
        "qr-codes": "QR_Codes_6students.pdf",
        "grade-section": "GradeSection_2026-06.pdf",
        "clearance": null,
        "member-history": null,
        "top-users": null,
      };
      var msg = messages[this._type];
      if (msg && msg.indexOf(".pdf") >= 0) {
        showFletToast("Report generated (demo).");
        if (this._onComplete) this._onComplete(msg);
      } else if (msg) {
        showFletToast(msg);
      }
      this.close();
    },
  };

  document.addEventListener("click", function (e) {
    if (e.target.id === "demo-modal-backdrop") DemoModals.close();
  });

  /* ── Page inits ── */
  function initDashboardDemo() {
    var panels = {
      history: DEMO_DATA.dashboardHistory.map(function (h) { return "<li>" + escapeHtml(h) + "</li>"; }).join(""),
      bookmarks: DEMO_DATA.dashboardBookmarks.map(function (b) { return "<li><i class='fa-regular fa-bookmark'></i> " + escapeHtml(b) + "</li>"; }).join(""),
      stats: "<div class='dash-mini-stats'><div><strong>18</strong><span>Total visits</span></div><div><strong>2</strong><span>Books out</span></div><div><strong>0</strong><span>Fines</span></div></div>",
      activity: DEMO_DATA.dashboardActivity.map(function (a) { return "<li>" + escapeHtml(a) + "</li>"; }).join(""),
    };
    Object.keys(panels).forEach(function (key) {
      var el = document.querySelector('.dash-student-panel[data-panel="' + key + '"]');
      if (el) el.innerHTML = key === "stats" ? panels[key] : "<ul class='dash-student-list'>" + panels[key] + "</ul>";
    });
    document.querySelectorAll(".dash-student-tab").forEach(function (tab) {
      tab.addEventListener("click", function () {
        var t = tab.getAttribute("data-tab");
        document.querySelectorAll(".dash-student-tab").forEach(function (x) { x.classList.remove("is-active"); });
        document.querySelectorAll(".dash-student-panel").forEach(function (x) { x.classList.remove("is-active"); });
        tab.classList.add("is-active");
        var panel = document.querySelector('.dash-student-panel[data-panel="' + t + '"]');
        if (panel) panel.classList.add("is-active");
      });
    });
  }

  function initAttendanceDemo() {
    var list = document.getElementById("att-scan-list");
    var dateEl = document.getElementById("att-today-date");
    if (dateEl) dateEl.textContent = new Date().toLocaleDateString("en-US", { month: "long", day: "numeric", year: "numeric" });

    function renderScans() {
      if (!list) return;
      list.innerHTML = DEMO_DATA.scans.map(function (s, i) {
        return '<li><span class="att-scan-num">' + (i + 1) + '</span><div><strong>' + escapeHtml(s.name) + '</strong><span>Grade ' + s.grade + " - " + escapeHtml(s.section) + " • " + s.time + "</span></div></li>";
      }).join("");
    }
    renderScans();

    var input = document.getElementById("att-manual-input");
    var suggestions = document.getElementById("att-suggestions");
    var result = document.getElementById("att-result");

    if (input && suggestions) {
      input.addEventListener("input", function () {
        var q = input.value.toLowerCase().trim();
        if (q.length < 2) { suggestions.hidden = true; return; }
        var matches = DEMO_DATA.members.filter(function (m) {
          return m.name.toLowerCase().indexOf(q) >= 0 || m.id.indexOf(q) >= 0;
        }).slice(0, 6);
        if (!matches.length) { suggestions.hidden = true; return; }
        suggestions.innerHTML = matches.map(function (m) {
          return '<li data-id="' + m.id + '">' + escapeHtml(m.name) + " · " + m.id + " · Grade " + m.grade + "</li>";
        }).join("");
        suggestions.hidden = false;
      });
      suggestions.addEventListener("click", function (e) {
        var li = e.target.closest("li");
        if (!li) return;
        var mem = DEMO_DATA.members.find(function (m) { return m.id === li.getAttribute("data-id"); });
        if (mem) input.value = mem.name;
        suggestions.hidden = true;
      });
    }

    function doScan(name) {
      var mem = DEMO_DATA.members.find(function (m) { return m.name === name; });
      if (!mem) {
        if (result) { result.textContent = "❌ Student not found."; result.className = "att-result att-result--error"; }
        return;
      }
      var already = DEMO_DATA.scans.some(function (s) { return s.name === name && s.time.indexOf("10:") === 0; });
      if (already && DEMO_DATA.scans[0].name === name) {
        if (result) { result.textContent = "⚠ " + name + " already scanned today."; result.className = "att-result att-result--warn"; }
        return;
      }
      var now = new Date();
      var timeStr = now.toLocaleTimeString("en-US", { hour: "numeric", minute: "2-digit" });
      DEMO_DATA.scans.unshift({ name: mem.name, grade: mem.grade, section: mem.section, time: timeStr.replace(" ", "").toLowerCase() });
      if (DEMO_DATA.scans.length > 20) DEMO_DATA.scans.pop();
      var count = parseInt(document.getElementById("att-today-count").textContent, 10) + 1;
      document.getElementById("att-today-count").textContent = count;
      document.getElementById("att-last-name").textContent = mem.name;
      document.getElementById("att-last-time").textContent = timeStr;
      if (result) { result.textContent = "✅ Welcome, " + mem.name + "!"; result.className = "att-result att-result--ok"; }
      renderScans();
      showScanToast(mem.name, "Grade " + mem.grade + " - " + mem.section, String(count));
    }

    document.getElementById("att-submit").addEventListener("click", function () {
      doScan(input.value.trim());
    });
    if (input) input.addEventListener("keydown", function (e) { if (e.key === "Enter") doScan(input.value.trim()); });
  }

  function initMembersDemo() {
    var pageSize = 5;
    var page = 0;
    var selected = DEMO_DATA.members[0];
    var filtered = DEMO_DATA.members.slice();

    function applyFilters() {
      var q = (document.getElementById("mem-search").value || "").toLowerCase();
      var grade = document.getElementById("mem-filter-grade").value;
      var section = document.getElementById("mem-filter-section").value;
      var status = document.getElementById("mem-filter-status").value;
      filtered = DEMO_DATA.members.filter(function (m) {
        if (q && m.name.toLowerCase().indexOf(q) < 0 && m.id.indexOf(q) < 0) return false;
        if (grade && String(m.grade) !== grade) return false;
        if (section && m.section !== section) return false;
        if (status && m.status !== status) return false;
        return true;
      });
      page = 0;
      renderTable();
      renderStats();
    }

    function renderStats() {
      document.getElementById("mem-stat-total").textContent = DEMO_DATA.members.length;
      document.getElementById("mem-stat-active").textContent = DEMO_DATA.members.filter(function (m) { return m.status === "active"; }).length;
      document.getElementById("mem-stat-inactive").textContent = DEMO_DATA.members.filter(function (m) { return m.status === "inactive" || m.status === "graduated"; }).length;
    }

    function renderOverview(m) {
      document.getElementById("mem-overview-avatar").textContent = initials(m.name);
      document.getElementById("mem-overview-name").textContent = m.name;
      document.getElementById("mem-overview-meta").textContent = "Grade " + m.grade + " – " + m.section;
      document.getElementById("mem-overview-stats").innerHTML =
        "<div><span>Learner ID</span><strong>" + m.id + "</strong></div>" +
        "<div><span>Total Visits</span><strong>" + m.visits + "</strong></div>" +
        "<div><span>Last Entry</span><strong>" + m.lastEntry + "</strong></div>";
    }

    function renderTable() {
      var tbody = document.getElementById("mem-table-body");
      var start = page * pageSize;
      var slice = filtered.slice(start, start + pageSize);
      tbody.innerHTML = slice.map(function (m, i) {
        return '<tr data-id="' + m.id + '" class="' + (selected.id === m.id ? "is-selected" : "") + '"><td>' + (start + i + 1) + '</td><td>' + escapeHtml(m.name) + '</td><td>' + m.grade + '</td><td>' + escapeHtml(m.section) + '</td><td>' + statusDot(m.status) + '</td><td><button type="button" class="flet-table-action" data-demo-toast="Edit member (demo)."><i class="fa-regular fa-pen-to-square"></i></button></td></tr>';
      }).join("");
      tbody.querySelectorAll("tr").forEach(function (tr) {
        tr.addEventListener("click", function () {
          selected = DEMO_DATA.members.find(function (m) { return m.id === tr.getAttribute("data-id"); });
          renderOverview(selected);
          tbody.querySelectorAll("tr").forEach(function (r) { r.classList.remove("is-selected"); });
          tr.classList.add("is-selected");
        });
      });
      var pag = document.getElementById("mem-pagination");
      var pages = Math.ceil(filtered.length / pageSize) || 1;
      pag.innerHTML = "";
      for (var p = 0; p < pages; p++) {
        var btn = document.createElement("button");
        btn.type = "button";
        btn.textContent = p + 1;
        btn.className = p === page ? "is-active" : "";
        (function (pi) { btn.addEventListener("click", function () { page = pi; renderTable(); }); })(p);
        pag.appendChild(btn);
      }
    }

    var sections = {};
    DEMO_DATA.members.forEach(function (m) { sections[m.section] = true; });
    var secSel = document.getElementById("mem-filter-section");
    Object.keys(sections).forEach(function (s) {
      var opt = document.createElement("option");
      opt.value = s; opt.textContent = s;
      secSel.appendChild(opt);
    });

    document.getElementById("mem-grade-bars").innerHTML = DEMO_DATA.gradeActivity.map(function (g) {
      return '<div class="mem-grade-bar"><span>G' + g.grade + '</span><div class="mem-grade-bar__track"><div class="mem-grade-bar__fill" style="width:' + g.pct + '%"></div></div><span>' + g.pct + '%</span></div>';
    }).join("");

    document.getElementById("mem-search").addEventListener("input", applyFilters);
    document.getElementById("mem-filter-grade").addEventListener("change", applyFilters);
    document.getElementById("mem-filter-section").addEventListener("change", applyFilters);
    document.getElementById("mem-filter-status").addEventListener("change", applyFilters);
    document.getElementById("mem-add-btn").addEventListener("click", function () { DemoModals.open("add-member"); });
    document.getElementById("mem-import-btn").addEventListener("click", function () { DemoModals.open("import-members"); });
    document.getElementById("mem-history-btn").addEventListener("click", function () { DemoModals.open("member-history", { member: selected }); });
    document.getElementById("mem-top-btn").addEventListener("click", function () { DemoModals.open("top-users"); });

    renderStats();
    renderOverview(selected);
    renderTable();
  }

  function initBooksDemo() {
    var activeTab = "analytics";

    function renderTabPanels() {
      var container = document.getElementById("book-tab-panels");
      var html = "";
      if (activeTab === "analytics") {
        html = '<div class="flet-tab-panel is-active"><div class="flet-stat-row flet-stat-row--4">' +
          '<div class="flet-stat-card"><div class="flet-stat-card__value">8</div><div class="flet-stat-card__label">Borrowed</div></div>' +
          '<div class="flet-stat-card"><div class="flet-stat-card__value">5</div><div class="flet-stat-card__label">Returned</div></div>' +
          '<div class="flet-stat-card"><div class="flet-stat-card__value">14</div><div class="flet-stat-card__label">Overdue</div></div>' +
          '<div class="flet-stat-card"><div class="flet-stat-card__value">₱420</div><div class="flet-stat-card__label">Fines</div></div></div>' +
          '<div class="book-analytics-grid"><div class="flet-card"><h4>Most Borrowed</h4><ol>' +
          DEMO_DATA.topBooks.slice(0, 5).map(function (b) { return "<li>" + escapeHtml(b.title) + " (" + b.count + ")</li>"; }).join("") +
          '</ol></div><div class="flet-card"><h4>By Grade Level</h4>' +
          DEMO_DATA.gradeActivity.map(function (g) { return '<div class="mem-grade-bar"><span>G' + g.grade + '</span><div class="mem-grade-bar__track"><div class="mem-grade-bar__fill" style="width:' + g.pct + '%"></div></div></div>'; }).join("") +
          '</div></div></div>';
      } else if (activeTab === "catalog") {
        html = '<div class="flet-tab-panel is-active"><div class="flet-card__title-row"><h3>Book Catalog</h3><button type="button" class="btn-primary" id="book-add-catalog">Add Book</button></div>' +
          '<div class="flet-table-wrap"><table class="flet-table"><thead><tr><th>Title</th><th>Author</th><th>ISBN</th><th>Stock</th><th></th></tr></thead><tbody>' +
          DEMO_DATA.books.map(function (b) {
            return "<tr><td>" + escapeHtml(b.title) + "</td><td>" + escapeHtml(b.author) + "</td><td>" + b.isbn + "</td><td>" + stockBadge(b.available, b.total) + '</td><td><button type="button" class="flet-table-action" data-demo-toast="Edit book (demo)."><i class="fa-regular fa-pen-to-square"></i></button></td></tr>";
          }).join("") + "</tbody></table></div></div>";
      } else if (activeTab === "borrowed") {
        html = '<div class="flet-tab-panel is-active"><div class="flet-stat-row flet-stat-row--3">' +
          '<div class="flet-stat-card"><div class="flet-stat-card__value">8</div><div class="flet-stat-card__label">Books Borrowed Today</div></div>' +
          '<div class="flet-stat-card"><div class="flet-stat-card__value">6</div><div class="flet-stat-card__label">Borrowers Today</div></div>' +
          '<div class="flet-stat-card"><div class="flet-stat-card__value">' + new Date().toLocaleDateString("en-US", { month: "short", day: "numeric" }) + '</div><div class="flet-stat-card__label">Date</div></div></div></div>';
      } else if (activeTab === "overdue") {
        html = '<div class="flet-tab-panel is-active"><div class="flet-scroll-cards">' +
          DEMO_DATA.overdueBooks.map(function (b) {
            return '<div class="book-overdue-card"><strong>' + escapeHtml(b.title) + '</strong><span>' + escapeHtml(b.student) + " · " + escapeHtml(b.gradeSection) + '</span><span class="book-overdue-fine">' + b.days + " days · ₱" + b.fine + "</span></div>";
          }).join("") + "</div></div>";
      } else if (activeTab === "topbooks") {
        html = '<div class="flet-tab-panel is-active"><div class="flet-scroll-cards">' +
          DEMO_DATA.topBooks.map(function (b) {
            return '<div class="book-top-card"><span class="book-top-rank">#' + b.rank + '</span><i class="fa-solid fa-book"></i><strong>' + escapeHtml(b.title) + '</strong><span>' + b.count + " borrows · " + b.isbn + "</span></div>";
          }).join("") + "</div></div>";
      }
      container.innerHTML = html;
      var addBtn = document.getElementById("book-add-catalog");
      if (addBtn) addBtn.addEventListener("click", function () { DemoModals.open("add-book"); });
    }

    function renderRecords() {
      var filter = document.getElementById("book-record-filter").value;
      var rows = DEMO_DATA.borrowRecords.filter(function (r) { return !filter || r.status === filter; });
      document.getElementById("book-records-body").innerHTML = rows.map(function (r) {
        return "<tr><td>" + r.date + "</td><td>" + escapeHtml(r.student) + "</td><td>" + escapeHtml(r.gradeSection) + "</td><td>" + escapeHtml(r.book) + "</td><td>" + statusDot(r.status) + "</td><td>" + (r.fine ? "₱" + r.fine : "—") + "</td></tr>";
      }).join("");
    }

    document.getElementById("book-summary").innerHTML =
      "<div><span>Borrowed</span><strong>8</strong></div><div><span>Returned</span><strong>5</strong></div><div><span>Overdue</span><strong>14</strong></div><div><span>Total Fines</span><strong>₱420</strong></div>";

    document.getElementById("book-activity-list").innerHTML = DEMO_DATA.bookActivity.map(function (a) {
      var icon = a.type === "borrow" ? "fa-book" : a.type === "return" ? "fa-rotate-left" : "fa-triangle-exclamation";
      return '<li><i class="fa-solid ' + icon + '"></i><div><span>' + escapeHtml(a.text) + '</span><small>' + a.time + "</small></div></li>";
    }).join("");

    document.querySelectorAll("#book-tabs .flet-tab").forEach(function (tab) {
      tab.addEventListener("click", function () {
        document.querySelectorAll("#book-tabs .flet-tab").forEach(function (t) { t.classList.remove("is-active"); });
        tab.classList.add("is-active");
        activeTab = tab.getAttribute("data-tab");
        renderTabPanels();
      });
    });

    document.getElementById("book-record-filter").addEventListener("change", renderRecords);
    document.getElementById("book-borrow-btn").addEventListener("click", function () { DemoModals.open("borrow-book"); });
    document.getElementById("book-return-btn").addEventListener("click", function () { DemoModals.open("return-book"); });
    document.getElementById("book-add-btn").addEventListener("click", function () { DemoModals.open("add-book"); });
    document.getElementById("book-search").addEventListener("input", function () {
      showFletToast("Search: " + (document.getElementById("book-search").value || "…") + " (demo filter)");
    });

    renderTabPanels();
    renderRecords();
  }

  function initPrintDemo() {
    var recentList = document.getElementById("print-recent-list");

    function addPrint(filename) {
      DEMO_DATA.printHistory.unshift(filename);
      if (DEMO_DATA.printHistory.length > 5) DEMO_DATA.printHistory.pop();
      renderRecent();
    }

    function renderRecent() {
      recentList.innerHTML = DEMO_DATA.printHistory.length
        ? DEMO_DATA.printHistory.map(function (f) { return '<li><i class="fa-regular fa-file-pdf"></i> ' + escapeHtml(f) + "</li>"; }).join("")
        : "<li class='flet-empty'>No prints yet.</li>";
    }

    document.getElementById("print-report-grid").innerHTML = REPORT_CARDS.map(function (c) {
      return '<div class="flet-report-card"><div class="flet-report-card__icon"><i class="fa-solid ' + c.icon + '"></i></div><h3>' + escapeHtml(c.title) + '</h3><p>' + escapeHtml(c.sub) + '</p><button type="button" class="btn-primary" data-report="' + c.id + '">Generate</button></div>';
    }).join("");

    document.querySelectorAll("[data-report]").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var id = btn.getAttribute("data-report");
        var typeMap = {
          "attendance": "attendance-report", "top-visitors": "top-visitors", "overdue": "overdue-report",
          "qr": "qr-codes", "clearance": "clearance", "grade-section": "grade-section",
        };
        DemoModals.open(typeMap[id], {}, addPrint);
      });
    });

    document.getElementById("print-qr-btn").addEventListener("click", function () {
      DemoModals.open("qr-codes", {}, addPrint);
    });
    document.getElementById("print-today-btn").addEventListener("click", function () {
      addPrint("Attendance_Today_" + new Date().toISOString().slice(0, 10) + ".pdf");
      showFletToast("Today's report sent to print queue (demo).");
    });

    renderRecent();
  }

  function initAiDemo() {
    var aiMessages = document.getElementById("ai-page-messages");
    var aiChips = document.getElementById("ai-page-chips");
    var aiQuick = document.getElementById("ai-page-quick");
    var aiInput = document.getElementById("ai-page-input");
    var aiSend = document.getElementById("ai-page-send");
    var aiTyping = false;

    function addAiBubble(text, role, isTyping) {
      var div = document.createElement("div");
      div.className = "ai-page__bubble ai-page__bubble--" + role + (isTyping ? " ai-page__bubble--typing" : "");
      if (isTyping) div.innerHTML = '<span></span><span></span><span></span>';
      else div.textContent = text;
      aiMessages.appendChild(div);
      aiMessages.scrollTop = aiMessages.scrollHeight;
      return div;
    }

    function matchQuestion(text) {
      if (DEMO_RESPONSES[text]) return text;
      var lower = text.toLowerCase();
      for (var i = 0; i < AI_KEYWORDS.length; i++) {
        if (AI_KEYWORDS[i].keys.some(function (k) { return lower.indexOf(k) >= 0; })) return AI_KEYWORDS[i].q;
      }
      return null;
    }

    function askAi(question) {
      if (aiTyping || !question.trim()) return;
      var canonical = DEMO_RESPONSES[question] ? question : matchQuestion(question);
      var answer = canonical ? DEMO_RESPONSES[canonical] : "Install BiblioQ for live database queries.";
      aiTyping = true;
      try { localStorage.setItem(STORAGE_KEY, question); } catch (e) { /* ignore */ }
      addAiBubble(question, "user");
      var typing = addAiBubble("", "bot", true);
      setTimeout(function () {
        typing.remove();
        var bot = addAiBubble("", "bot");
        typewriter(bot, answer).then(function () {
          aiTyping = false;
          aiMessages.scrollTop = aiMessages.scrollHeight;
          if (canonical === AI_REPORT_QUESTION) {
            showFletToast("Demo: Report emailed to principal@school.edu");
          }
        });
      }, 700);
    }

    AI_SUGGESTIONS.forEach(function (q) {
      var chip = document.createElement("button");
      chip.type = "button";
      chip.textContent = q;
      chip.addEventListener("click", function () { askAi(q); });
      aiChips.appendChild(chip);
    });

    AI_QUICK.forEach(function (label) {
      var pill = document.createElement("button");
      pill.type = "button";
      pill.className = "ai-page__quick-pill";
      pill.textContent = label;
      pill.addEventListener("click", function () {
        var map = { Today: AI_SUGGESTIONS[0], "Top Visitors": AI_SUGGESTIONS[1], Overdue: AI_SUGGESTIONS[3], Inventory: AI_SUGGESTIONS[2], Predict: AI_SUGGESTIONS[4], Letter: AI_SUGGESTIONS[5], "Email Report": AI_REPORT_QUESTION };
        askAi(map[label] || label);
      });
      aiQuick.appendChild(pill);
    });

    aiSend.addEventListener("click", function () { askAi(aiInput.value.trim()); aiInput.value = ""; });
    aiInput.addEventListener("keydown", function (e) { if (e.key === "Enter") { askAi(aiInput.value.trim()); aiInput.value = ""; } });

    document.getElementById("ai-new-chat").addEventListener("click", function () {
      aiMessages.innerHTML = "";
      addAiBubble("New chat started. Ask anything or try a suggestion below.", "bot");
      showFletToast("Chat cleared.");
    });

    try {
      var last = localStorage.getItem(STORAGE_KEY);
      if (last) setTimeout(function () { askAi(last); }, 600);
      else addAiBubble("Hello, Librarian! I'm the BiblioQ AI assistant demo. Try a suggestion or type a question — I can answer queries, generate PDF reports, and email them automatically.", "bot");
    } catch (e) {
      addAiBubble("Hello! Try a suggestion below.", "bot");
    }
  }

  function initFletShell() {
    var sidebar = document.getElementById("flet-sidebar");
    var indicator = document.getElementById("flet-indicator");
    var navBtns = document.querySelectorAll(".flet-nav-btn, .flet-sidebar__logo-btn");
    var pages = {
      0: document.getElementById("page-dashboard"),
      1: document.getElementById("page-attendance"),
      2: document.getElementById("page-members"),
      3: document.getElementById("page-books"),
      4: document.getElementById("page-print"),
      5: document.getElementById("page-ai"),
    };
    var chartMode = "week";
    var lineVisible = { attendance: true, sections: true, students: false };

    function moveIndicator(btn) {
      if (!indicator || !btn) return;
      var inner = document.querySelector(".flet-sidebar__inner");
      var rect = btn.getBoundingClientRect();
      var innerRect = inner.getBoundingClientRect();
      indicator.style.top = rect.top - innerRect.top + "px";
    }

    function showPage(navIndex) {
      navBtns.forEach(function (b) {
        b.classList.toggle("is-active", parseInt(b.getAttribute("data-nav"), 10) === navIndex);
      });
      Object.keys(pages).forEach(function (k) {
        if (pages[k]) pages[k].classList.remove("is-active");
      });
      if (pages[navIndex]) pages[navIndex].classList.add("is-active");
      var activeBtn = document.querySelector('[data-nav="' + navIndex + '"]');
      if (activeBtn) moveIndicator(activeBtn);
      if (sidebar) sidebar.classList.remove("is-open");
    }

    navBtns.forEach(function (btn) {
      btn.addEventListener("click", function () { showPage(parseInt(btn.getAttribute("data-nav"), 10)); });
    });

    document.getElementById("flet-logout").addEventListener("click", function () { showFletToast("Sign out is disabled in demo mode."); });

    document.addEventListener("click", function (e) {
      var t = e.target.closest("[data-demo-toast]");
      if (t) showFletToast(t.getAttribute("data-demo-toast"));
    });

    if (sidebar) {
      requestAnimationFrame(function () { sidebar.classList.add("is-entered"); });
      setTimeout(function () { moveIndicator(document.querySelector('.flet-nav-btn[data-nav="0"]')); }, 50);
    }

    var now = new Date();
    var monthDay = now.toLocaleDateString("en-US", { month: "long", day: "numeric" });
    var monthLabel = now.toLocaleDateString("en-US", { month: "long", day: "numeric", year: "numeric" });
    var dateVal = document.getElementById("stat-date-val");
    var dateLabel = document.getElementById("stat-date-label");
    var dashDate = document.getElementById("dash-date");
    if (dateVal) dateVal.textContent = monthDay.split(",")[0] || monthDay;
    if (dateLabel) dateLabel.textContent = monthLabel;
    if (dashDate) dashDate.textContent = monthLabel;

    document.querySelectorAll("#page-dashboard .flet-stat-card").forEach(function (card, i) {
      setTimeout(function () { card.classList.add("is-entering"); }, i * 150);
    });
    document.querySelectorAll("[data-stat-value]").forEach(function (el, i) {
      var target = el.getAttribute("data-stat-value");
      if (!target) return;
      setTimeout(function () { animateValue(el, target, 1200); }, 400 + i * 120);
    });

    function drawChart() {
      var svg = document.getElementById("line-chart");
      if (!svg) return;
      var data = CHART_DATA[chartMode];
      var w = 620, h = 250, pad = { t: 20, b: 30, l: 40, r: 20 };
      var innerW = w - pad.l - pad.r, innerH = h - pad.t - pad.b, n = data.labels.length, maxVal = 1;
      ["attendance", "sections", "students"].forEach(function (key) {
        if (lineVisible[key]) data[key].forEach(function (v) { if (v > maxVal) maxVal = v; });
      });
      maxVal = Math.ceil(maxVal * 1.1);
      function pointsFor(series) {
        return data[series].map(function (v, i) {
          var x = pad.l + (i / Math.max(n - 1, 1)) * innerW;
          var y = pad.t + innerH - (v / maxVal) * innerH;
          return x + "," + y;
        }).join(" ");
      }
      var parts = ['<rect width="' + w + '" height="' + h + '" fill="#FFFDF9"/>'];
      for (var g = 0; g <= 4; g++) {
        var gy = pad.t + (innerH / 4) * g;
        parts.push('<line x1="' + pad.l + '" y1="' + gy + '" x2="' + (w - pad.r) + '" y2="' + gy + '" stroke="#F0D5B0" stroke-width="1"/>');
      }
      data.labels.forEach(function (lbl, i) {
        var x = pad.l + (i / Math.max(n - 1, 1)) * innerW;
        parts.push('<text x="' + x + '" y="' + (h - 8) + '" text-anchor="middle" font-size="10" fill="#888" font-family="Poppins,sans-serif">' + lbl + "</text>");
      });
      ["attendance", "sections", "students"].forEach(function (key) {
        if (!lineVisible[key]) return;
        parts.push('<polyline fill="none" stroke="' + LINE_COLORS[key] + '" stroke-width="2.5" points="' + pointsFor(key) + '"/>');
      });
      svg.innerHTML = parts.join("");
    }

    document.querySelectorAll(".dash-chart-mode").forEach(function (btn) {
      btn.addEventListener("click", function () {
        document.querySelectorAll(".dash-chart-mode").forEach(function (b) { b.classList.remove("is-active"); });
        btn.classList.add("is-active");
        chartMode = btn.getAttribute("data-mode");
        drawChart();
      });
    });
    document.querySelectorAll(".dash-line-toggle").forEach(function (btn) {
      btn.addEventListener("click", function () {
        var key = btn.getAttribute("data-line");
        lineVisible[key] = !lineVisible[key];
        btn.classList.toggle("is-active", lineVisible[key]);
        drawChart();
      });
    });
    drawChart();

    var search = document.getElementById("dash-search");
    var list = document.getElementById("student-list");
    if (search && list) {
      search.addEventListener("input", function () {
        var q = search.value.toLowerCase().trim();
        list.querySelectorAll("li").forEach(function (li) {
          var name = (li.getAttribute("data-name") || li.textContent).toLowerCase();
          li.style.display = !q || name.indexOf(q) >= 0 ? "" : "none";
        });
      });
    }

    ["btn-settings", "btn-notifications", "btn-theme", "btn-account"].forEach(function (id) {
      var el = document.getElementById(id);
      if (el) el.addEventListener("click", function () { showFletToast(el.id === "btn-account" ? "Account: Librarian (demo)" : "Available in the installed app."); });
    });
    document.querySelectorAll(".flet-traffic").forEach(function (btn) {
      btn.addEventListener("click", function () { showFletToast("Window controls are disabled in demo mode."); });
    });

    var mobileToggle = document.getElementById("flet-mobile-toggle");
    if (mobileToggle && sidebar) mobileToggle.addEventListener("click", function () { sidebar.classList.toggle("is-open"); });

    initDashboardDemo();
    initAttendanceDemo();
    initMembersDemo();
    initBooksDemo();
    initPrintDemo();
    initAiDemo();

    setTimeout(function () { showScanToast("Maria Santos", "Grade 10 - Integrity", "247"); }, 3000);
  }

  function initChat(rootSelector) {
    var root = document.querySelector(rootSelector);
    if (!root) return;
  }

  global.BiblioQDemo = {
    initFletShell: initFletShell,
    initChat: initChat,
    DEMO_RESPONSES: DEMO_RESPONSES,
    DemoModals: DemoModals,
  };
})(window);
