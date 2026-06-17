/* ==========================================================================
   CARDINAL — shared site script
   Loads /data/affirmations.json once, then powers:
     - the homepage "pull a card" hero
     - the generator tool
     - favoriting (localStorage)
     - the "write your own" journal tool (localStorage)
     - newsletter form (stubbed — wire up a real provider, see README)
   ========================================================================== */

(function () {
  "use strict";

  /* ---------- data loading -------------------------------------------- */
  // Pages not at the site root pass a relative path override via
  // <body data-root="..">; we use that to find /data/affirmations.json.
  var ROOT = document.body.getAttribute("data-root") || "";

  function loadData() {
    if (window.__cardinalData) return Promise.resolve(window.__cardinalData);
    return fetch(ROOT + "data/affirmations.json")
      .then(function (r) { return r.json(); })
      .then(function (d) {
        window.__cardinalData = d;
        return d;
      })
      .catch(function (err) {
        console.error("Could not load affirmations.json — are you serving this over http(s), not file://?", err);
        return { categories: [], affirmations: [] };
      });
  }

  function randomFrom(arr) {
    return arr[Math.floor(Math.random() * arr.length)];
  }

  function pickAffirmation(data, category) {
    var pool = category && category !== "all"
      ? data.affirmations.filter(function (a) { return a.category === category; })
      : data.affirmations;
    return randomFrom(pool);
  }

  function categoryLabel(data, slug) {
    var cat = data.categories.find(function (c) { return c.slug === slug; });
    return cat ? cat.label : slug;
  }

  /* ---------- favorites (localStorage) ---------------------------------- */
  var FAV_KEY = "cardinal_favorites";

  function getFavorites() {
    try { return JSON.parse(localStorage.getItem(FAV_KEY)) || []; }
    catch (e) { return []; }
  }
  function isFavorite(id) { return getFavorites().indexOf(id) !== -1; }
  function toggleFavorite(id) {
    var favs = getFavorites();
    var idx = favs.indexOf(id);
    if (idx === -1) favs.push(id); else favs.splice(idx, 1);
    localStorage.setItem(FAV_KEY, JSON.stringify(favs));
    return idx === -1; // true if now favorited
  }

  /* ---------- journal entries (localStorage) ----------------------------- */
  var JOURNAL_KEY = "cardinal_journal";

  function getJournal() {
    try { return JSON.parse(localStorage.getItem(JOURNAL_KEY)) || []; }
    catch (e) { return []; }
  }
  function saveJournalEntry(entry) {
    var entries = getJournal();
    entries.unshift(entry);
    localStorage.setItem(JOURNAL_KEY, JSON.stringify(entries));
    return entries;
  }
  function deleteJournalEntry(id) {
    var entries = getJournal().filter(function (e) { return e.id !== id; });
    localStorage.setItem(JOURNAL_KEY, JSON.stringify(entries));
    return entries;
  }

  /* ---------- toast ------------------------------------------------------ */
  var toastTimer = null;
  function showToast(msg) {
    var t = document.getElementById("toast");
    if (!t) {
      t = document.createElement("div");
      t.id = "toast";
      t.className = "toast";
      document.body.appendChild(t);
    }
    t.textContent = msg;
    t.classList.add("show");
    clearTimeout(toastTimer);
    toastTimer = setTimeout(function () { t.classList.remove("show"); }, 2200);
  }

  function copyText(text) {
    if (navigator.clipboard) {
      navigator.clipboard.writeText(text).then(function () { showToast("Copied to clipboard"); });
    } else {
      showToast("Copy not supported in this browser");
    }
  }

  /* ---------- nav toggle --------------------------------------------------- */
  function initNav() {
    var btn = document.querySelector(".nav-toggle");
    var links = document.querySelector(".nav-links");
    if (!btn || !links) return;
    btn.addEventListener("click", function () {
      links.classList.toggle("open");
    });
  }

  /* ---------- card meta helpers --------------------------------------------- */
  function pad(n) { return String(n).padStart(4, "0"); }

  function renderCardMeta(metaEl, affirmation, data) {
    metaEl.innerHTML =
      "<span>CARD NO. " + pad(affirmation.id) + "</span>" +
      "<span>FILED: " + categoryLabel(data, affirmation.category).toUpperCase() + "</span>";
  }

  /* ---------- homepage hero: pull a card -------------------------------------- */
  function initHeroPull() {
    var stack = document.querySelector("[data-hero-pull]");
    if (!stack) return;
    var pulledCard = stack.querySelector(".pulled");
    var quoteEl = pulledCard.querySelector(".card-quote");
    var metaEl = pulledCard.querySelector(".card-meta");
    var btn = document.querySelector("[data-pull-btn]");

    loadData().then(function (data) {
      var first = pickAffirmation(data, "all");
      quoteEl.textContent = "\u201C" + first.text + "\u201D";
      renderCardMeta(metaEl, first, data);

      btn.addEventListener("click", function () {
        var a = pickAffirmation(data, "all");
        pulledCard.classList.remove("flip");
        quoteEl.textContent = "\u201C" + a.text + "\u201D";
        renderCardMeta(metaEl, a, data);
        // restart animation
        void pulledCard.offsetWidth;
        pulledCard.classList.add("flip");
      });
    });
  }

  /* ---------- generator tool page ---------------------------------------------- */
  function initGenerator() {
    var panel = document.querySelector("[data-generator]");
    if (!panel) return;
    var select = panel.querySelector("#gen-category");
    var btn = panel.querySelector("[data-generate-btn]");
    var resultCard = panel.querySelector(".result-card");
    var quoteEl = resultCard.querySelector(".card-quote");
    var metaEl = resultCard.querySelector(".card-meta");
    var favBtn = panel.querySelector("[data-fav-btn]");
    var copyBtn = panel.querySelector("[data-copy-btn]");
    var current = null;

    loadData().then(function (data) {
      data.categories.forEach(function (c) {
        var opt = document.createElement("option");
        opt.value = c.slug;
        opt.textContent = c.label;
        select.appendChild(opt);
      });

      function generate() {
        current = pickAffirmation(data, select.value);
        quoteEl.textContent = "\u201C" + current.text + "\u201D";
        renderCardMeta(metaEl, current, data);
        resultCard.style.display = "block";
        favBtn.classList.toggle("is-active", isFavorite(current.id));
        favBtn.textContent = isFavorite(current.id) ? "\u2605 Saved" : "\u2606 Save card";
      }

      btn.addEventListener("click", generate);
      generate();

      favBtn.addEventListener("click", function () {
        if (!current) return;
        var nowFav = toggleFavorite(current.id);
        favBtn.classList.toggle("is-active", nowFav);
        favBtn.textContent = nowFav ? "\u2605 Saved" : "\u2606 Save card";
        showToast(nowFav ? "Saved to your favorites" : "Removed from favorites");
        renderFavorites(data);
      });

      copyBtn.addEventListener("click", function () {
        if (current) copyText(current.text);
      });

      renderFavorites(data);
    });
  }

  function renderFavorites(data) {
    var holder = document.querySelector("[data-favorites-list]");
    if (!holder) return;
    var favs = getFavorites();
    if (!favs.length) {
      holder.innerHTML = "<p class=\"lede\">Cards you save will be filed here \u2014 stored only in this browser, nothing leaves your device.</p>";
      return;
    }
    var items = favs
      .map(function (id) { return data.affirmations.find(function (a) { return a.id === id; }); })
      .filter(Boolean);
    holder.innerHTML = "<div class=\"fan-grid\">" + items.map(function (a) {
      return (
        "<div class=\"card\">" +
        "<div class=\"card-meta\"><span>CARD NO. " + pad(a.id) + "</span><span>FILED: " + categoryLabel(data, a.category).toUpperCase() + "</span></div>" +
        "<div class=\"card-body\"><p class=\"card-quote\">\u201C" + a.text + "\u201D</p>" +
        "<div class=\"card-actions\"><button class=\"icon-btn\" data-unfav=\"" + a.id + "\">Remove</button></div></div>" +
        "</div>"
      );
    }).join("") + "</div>";

    holder.querySelectorAll("[data-unfav]").forEach(function (b) {
      b.addEventListener("click", function () {
        toggleFavorite(Number(b.getAttribute("data-unfav")));
        renderFavorites(data);
      });
    });
  }

  /* ---------- journal: write your own -------------------------------------------- */
  function initJournal() {
    var form = document.querySelector("[data-journal-form]");
    if (!form) return;
    var listEl = document.querySelector("[data-journal-list]");

    function render() {
      var entries = getJournal();
      if (!entries.length) {
        listEl.innerHTML = "<p class=\"lede\">Your written cards will be filed here \u2014 stored only in this browser.</p>";
        return;
      }
      listEl.innerHTML = "<div class=\"fan-grid\">" + entries.map(function (e) {
        return (
          "<div class=\"card\">" +
          "<div class=\"card-meta\"><span>" + e.date + "</span><span>SELF-FILED</span></div>" +
          "<div class=\"card-body\"><p class=\"card-quote\">\u201C" + e.text + "\u201D</p>" +
          (e.strength ? "<p style=\"font-family:var(--font-mono);font-size:0.72rem;color:var(--ink-faint);margin-top:10px;\">STRENGTH: " + e.strength.toUpperCase() + "</p>" : "") +
          "<div class=\"card-actions\"><button class=\"icon-btn\" data-del=\"" + e.id + "\">Delete</button></div></div>" +
          "</div>"
        );
      }).join("") + "</div>";

      listEl.querySelectorAll("[data-del]").forEach(function (b) {
        b.addEventListener("click", function () {
          deleteJournalEntry(Number(b.getAttribute("data-del")));
          render();
        });
      });
    }

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var situation = form.querySelector("#j-situation").value.trim();
      var strength = form.querySelector("#j-strength").value.trim();
      var statement = form.querySelector("#j-statement").value.trim();
      if (!statement) { showToast("Write your affirmation first"); return; }
      saveJournalEntry({
        id: Date.now(),
        date: new Date().toLocaleDateString(undefined, { month: "short", day: "numeric", year: "numeric" }),
        situation: situation,
        strength: strength,
        text: statement
      });
      form.reset();
      showToast("Filed");
      render();
    });

    render();
  }

  /* ---------- category page favoriting ------------------------------------------- */
  function initCategoryFavButtons() {
    var grid = document.querySelector("[data-category-grid]");
    if (!grid) return;
    grid.querySelectorAll("[data-card-id]").forEach(function (card) {
      var id = Number(card.getAttribute("data-card-id"));
      var favBtn = card.querySelector("[data-fav-toggle]");
      var copyBtn = card.querySelector("[data-copy-toggle]");
      if (favBtn) {
        favBtn.classList.toggle("is-active", isFavorite(id));
        favBtn.textContent = isFavorite(id) ? "\u2605 Saved" : "\u2606 Save";
        favBtn.addEventListener("click", function () {
          var nowFav = toggleFavorite(id);
          favBtn.classList.toggle("is-active", nowFav);
          favBtn.textContent = nowFav ? "\u2605 Saved" : "\u2606 Save";
          showToast(nowFav ? "Saved to your favorites" : "Removed from favorites");
        });
      }
      if (copyBtn) {
        copyBtn.addEventListener("click", function () {
          var text = card.querySelector(".card-quote").textContent.replace(/^\u201C|\u201D$/g, "");
          copyText(text);
        });
      }
    });
  }

  /* ---------- newsletter form (stub) ----------------------------------------------- */
  function initNewsletterForms() {
    document.querySelectorAll("[data-newsletter-form]").forEach(function (form) {
      form.addEventListener("submit", function (e) {
        e.preventDefault();
        // STUB: replace this block with a real request to your email provider
        // (Beehiiv / ConvertKit / Mailchimp form action or API). See README.md.
        showToast("Thanks \u2014 check your inbox to confirm");
        form.reset();
      });
    });
  }

  /* ---------- boot --------------------------------------------------------------------- */
  document.addEventListener("DOMContentLoaded", function () {
    initNav();
    initHeroPull();
    initGenerator();
    initJournal();
    initCategoryFavButtons();
    initNewsletterForms();
  });
})();
