/* ============================================================
   publications.js — renders publications.json onto the page.
   ------------------------------------------------------------
   The publication records are cached locally in publications.json
   (a snapshot of the OU Profiles list). The site never calls the
   OU server; only the per-record links point out to ORO.
   No dependencies, no build step.
   ============================================================ */
(function () {
  "use strict";

  var host = document.getElementById("pub-app");
  if (!host) return;

  /* ---------- tiny DOM helpers ---------- */
  function el(tag, cls, text) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text != null) n.textContent = text;
    return n;
  }
  function esc(s) {
    return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }
  /* bold the professor's name inside a citation string — single pass with
     longest alternative first, so the output is never re-scanned */
  function highlightCitation(s) {
    return esc(s).replace(/White,\s*G\.?\s*J\.|White,\s*G\./g, function (m) {
      return "<strong>" + m + "</strong>";
    });
  }

  /* ---------- state ---------- */
  var pubs = [];            // all records
  var typeNames = {};       // id -> pretty name
  var activeType = "all";   // filter
  var query = "";           // search box

  /* ---------- rendering ---------- */
  function visible(r) {
    if (activeType !== "all" && r.type !== activeType) return false;
    if (query) {
      var hay = (r.title + " " + r.citation + " " + r.year).toLowerCase();
      if (hay.indexOf(query) === -1) return false;
    }
    return true;
  }

  function render() {
    var list = host.querySelector(".pub-list");
    var count = host.querySelector(".pub-count");
    list.innerHTML = "";

    var shown = pubs.filter(visible);
    count.textContent = shown.length.toLocaleString() + " of " +
                        pubs.length.toLocaleString() + " records";

    var byYear = {};
    shown.forEach(function (r) {
      (byYear[r.year] = byYear[r.year] || []).push(r);
    });
    var years = Object.keys(byYear).map(Number).sort(function (a, b) { return b - a; });

    years.forEach(function (y) {
      var h2 = el("h2", "year-head", String(y));
      h2.id = "y" + y;
      list.appendChild(h2);
      byYear[y].forEach(function (r) {
        var d = el("div", "pub");

        var title = el("div", "pub-title");
        var a = el("a", null, r.title);
        a.href = r.url;
        a.target = "_blank";
        a.rel = "noopener";
        title.appendChild(a);
        d.appendChild(title);

        var badge = el("span", "pub-type", typeNames[r.type] || r.type);
        title.appendChild(document.createTextNode(" "));
        title.appendChild(badge);

        var cit = el("div", "pub-authors");
        cit.innerHTML = highlightCitation(r.citation);
        d.appendChild(cit);

        var links = el("div", "pub-links");
        var oro = el("a", null, "ORO record →");
        oro.href = r.url;
        oro.target = "_blank";
        oro.rel = "noopener";
        links.appendChild(oro);
        d.appendChild(links);

        list.appendChild(d);
      });
    });

    if (!years.length) {
      var p = el("p", null, "No records match the current filter.");
      p.style.color = "var(--muted)";
      list.appendChild(p);
    }
  }

  /* ---------- controls ---------- */
  function buildControls() {
    var bar = host.querySelector(".pub-controls");
    bar.innerHTML = "";

    var search = el("input");
    search.type = "search";
    search.placeholder = "Search title, author, year…";
    search.setAttribute("aria-label", "Search publications");
    search.addEventListener("input", function () {
      query = search.value.trim().toLowerCase();
      render();
    });
    bar.appendChild(search);

    var counts = {};
    pubs.forEach(function (r) { counts[r.type] = (counts[r.type] || 0) + 1; });

    var mk = function (id, label) {
      var b = el("button", "chip" + (activeType === id ? " chip-on" : ""),
                 label + " (" + (id === "all" ? pubs.length : counts[id]) + ")");
      b.type = "button";
      b.addEventListener("click", function () {
        activeType = id;
        bar.querySelectorAll(".chip").forEach(function (c) { c.classList.remove("chip-on"); });
        b.classList.add("chip-on");
        render();
      });
      bar.appendChild(b);
    };
    mk("all", "All");
    Object.keys(counts).sort(function (a, b) { return counts[b] - counts[a]; })
      .forEach(function (t) { mk(t, typeNames[t] || t); });
  }

  /* ---------- boot ---------- */
  fetch("publications.json")
    .then(function (r) {
      if (!r.ok) throw new Error("HTTP " + r.status);
      return r.json();
    })
    .then(function (data) {
      pubs = data.publications || [];
      typeNames = (data.meta && data.meta.type_names) || {};
      buildControls();
      render();
    })
    .catch(function (err) {
      var note = host.querySelector(".pub-fallback");
      if (note) note.hidden = false;
      var c = host.querySelector(".pub-count");
      if (c) c.textContent = "Could not load publications.json (" + err.message + ").";
    });
})();
