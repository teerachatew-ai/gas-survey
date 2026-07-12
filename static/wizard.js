// PNGD SL-FO-014-09 survey wizard: step navigation, autosave, review summary.
// Pure progressive disclosure over the existing <form> — every field keeps
// its original name/value, so server-side handling (app.py) needs no changes.
(function () {
  "use strict";

  const ICONS = {
    building: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M4 21V9l8-6 8 6v12M9 21v-6h6v6"/></svg>',
    flame: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3c3 4 6 6.5 6 10a6 6 0 1 1-12 0c0-3.5 3-6 6-10z"/></svg>',
    gauge: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="8"/><path d="M12 8v4l3 2"/></svg>',
    bolt: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M13 2 4 14h6l-1 8 9-12h-6l1-8z"/></svg>',
    shield: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3l7 3v5c0 5-3.5 8-7 10-3.5-2-7-5-7-10V6l7-3z"/><path d="M9 12l2 2 4-4"/></svg>',
    clip: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="5" y="4" width="14" height="17" rx="2"/><path d="M9 4V2h6v2M9 12l2 2 4-5"/></svg>',
    check: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M5 13l4 4L19 7"/></svg>',
  };
  const STEP_ICONS = ["building", "flame", "gauge", "bolt", "shield", "clip"];
  const DRAFT_KEY = "pngd_survey_draft_v1";

  const form = document.getElementById("wizForm");
  const welcome = document.getElementById("wizWelcome");
  const panels = Array.from(document.querySelectorAll(".step-panel"));
  const stepper = document.getElementById("wizStepper");
  const progressRow = document.getElementById("wizProgressRow");
  const progressText = document.getElementById("wizProgressText");
  const cheerEl = document.getElementById("wizCheer");
  const backBtn = document.getElementById("wizBack");
  const nextBtn = document.getElementById("wizNext");
  const autosaveEl = document.getElementById("wizAutosave");
  const companyInput = form.elements["company_name"];
  const companyErr = document.getElementById("wizCompanyErr");
  const pdpaCheckbox = document.getElementById("wizPdpaCheckbox");
  const consentErr = document.getElementById("wizConsentErr");
  const reviewCards = document.getElementById("wizReviewCards");
  const addMachineBtn = document.getElementById("wizAddMachine");

  let step = 0; // 0 = welcome, 1..6 = steps

  function buildStepper() {
    stepper.innerHTML = STEP_ICONS.map((name, i) => {
      const n = i + 1;
      const state = n < step ? "done" : n === step ? "now" : "";
      const glyph = n < step ? ICONS.check : ICONS[name];
      const line = n < 6 ? `<div class="wiz-sline ${n < step ? "done" : ""}"></div>` : "";
      return `<div class="wiz-snode ${state}">${glyph}</div>${line}`;
    }).join("");
  }

  function render() {
    welcome.classList.toggle("active", step === 0);
    panels.forEach(p => p.classList.toggle("active", Number(p.dataset.step) === step));

    const inSteps = step >= 1 && step <= 6;
    stepper.hidden = !inSteps;
    progressRow.hidden = !inSteps;
    if (inSteps) {
      buildStepper();
      progressText.innerHTML = WIZ_I18N.stepOf.replace("{n}", step) + " &middot; " + WIZ_I18N.stepNames[step - 1];
      cheerEl.textContent = WIZ_I18N.cheers[step - 1] || "";
    }

    backBtn.hidden = step === 0;
    nextBtn.textContent = step === 0 ? WIZ_I18N.startBtn : step === 6 ? WIZ_I18N.confirmBtn : WIZ_I18N.nextBtn;
    nextBtn.classList.toggle("send", step === 6);

    if (step === 6) renderReview();

    document.querySelector(".wiz-card").scrollIntoView({ behavior: "smooth", block: "start" });
  }

  function goTo(n) { step = n; render(); }

  backBtn.addEventListener("click", () => { if (step > 0) goTo(step - 1); });

  nextBtn.addEventListener("click", () => {
    if (step === 0) { goTo(1); return; }

    if (step === 1) {
      if (!companyInput.value.trim()) {
        companyErr.style.display = "block";
        companyInput.classList.add("wiz-err");
        companyInput.focus();
        return;
      }
      companyErr.style.display = "none";
      companyInput.classList.remove("wiz-err");
      goTo(2);
      return;
    }

    if (step === 5) {
      if (!pdpaCheckbox.checked) {
        consentErr.style.display = "block";
        pdpaCheckbox.focus();
        return;
      }
      consentErr.style.display = "none";
      goTo(6);
      return;
    }

    if (step === 6) {
      try { localStorage.removeItem(DRAFT_KEY); } catch (e) { /* ignore */ }
      form.requestSubmit();
      return;
    }

    goTo(step + 1);
  });

  companyInput.addEventListener("input", () => {
    if (companyInput.value.trim()) {
      companyErr.style.display = "none";
      companyInput.classList.remove("wiz-err");
    }
  });
  pdpaCheckbox.addEventListener("change", () => {
    if (pdpaCheckbox.checked) consentErr.style.display = "none";
  });

  // ---------------------------------------------------------- copy-to-all-months
  document.querySelectorAll(".wiz-copy-btn").forEach(btn => {
    btn.addEventListener("click", () => {
      const n = btn.dataset.copyFuel;
      const cons = form.elements[`fuel${n}_cons_1`];
      const price = form.elements[`fuel${n}_price_1`];
      if (!cons || !price) return;
      for (let r = 2; r <= 12; r++) {
        const cEl = form.elements[`fuel${n}_cons_${r}`];
        const pEl = form.elements[`fuel${n}_price_${r}`];
        if (cEl) { cEl.value = cons.value; cEl.dispatchEvent(new Event("input", { bubbles: true })); }
        if (pEl) { pEl.value = price.value; pEl.dispatchEvent(new Event("input", { bubbles: true })); }
      }
    });
  });

  // ---------------------------------------------------------- add machine
  function refreshAddMachineVisibility() {
    const anyHidden = document.querySelector(".wiz-machine-box[hidden]");
    addMachineBtn.hidden = !anyHidden;
  }
  addMachineBtn.addEventListener("click", () => {
    const nextHidden = document.querySelector(".wiz-machine-box[hidden]");
    if (nextHidden) nextHidden.removeAttribute("hidden");
    refreshAddMachineVisibility();
  });
  refreshAddMachineVisibility();

  // ---------------------------------------------------------- autosave
  let saveTimer = null;
  function serializeForm() {
    const fd = new FormData(form);
    const obj = {};
    for (const [k, v] of fd.entries()) {
      if (obj[k] === undefined) obj[k] = v;
      else if (Array.isArray(obj[k])) obj[k].push(v);
      else obj[k] = [obj[k], v];
    }
    return obj;
  }
  function showAutosaved() {
    autosaveEl.classList.add("show");
    clearTimeout(showAutosaved._t);
    showAutosaved._t = setTimeout(() => autosaveEl.classList.remove("show"), 2000);
  }
  function scheduleSave() {
    clearTimeout(saveTimer);
    saveTimer = setTimeout(() => {
      try {
        localStorage.setItem(DRAFT_KEY, JSON.stringify(serializeForm()));
        showAutosaved();
      } catch (e) { /* storage unavailable — ignore */ }
    }, 500);
  }
  form.addEventListener("input", scheduleSave);
  form.addEventListener("change", scheduleSave);

  function restoreDraft() {
    let draft;
    try { draft = JSON.parse(localStorage.getItem(DRAFT_KEY) || "null"); } catch (e) { draft = null; }
    if (!draft) return;
    Object.keys(draft).forEach(name => {
      const els = form.querySelectorAll(`[name="${CSS.escape(name)}"]`);
      if (!els.length) return;
      const val = draft[name];
      const values = Array.isArray(val) ? val : [val];
      els.forEach(el => {
        if (el.type === "checkbox" || el.type === "radio") {
          if (values.includes(el.value)) el.checked = true;
        } else if (!el.value) {
          el.value = values[0];
        }
      });
    });
    refreshAddMachineVisibility();
  }
  if (!HAS_SERVER_DATA) restoreDraft();

  // ---------------------------------------------------------- review step
  function fieldVal(name) {
    const el = form.elements[name];
    return el ? (el.value || "").trim() : "";
  }
  function radioVal(name) {
    const el = form.querySelector(`input[name="${CSS.escape(name)}"]:checked`);
    return el ? el.value : "";
  }
  function multiVals(name) {
    return Array.from(form.querySelectorAll(`input[name="${CSS.escape(name)}"]:checked`)).map(el => el.value);
  }
  function card(iconName, label, value, gotoStep, ok) {
    return `<div class="wiz-sumcard ${ok ? "ok" : ""}">
      <span class="ic">${ICONS[iconName]}</span>
      <div><div class="k">${label}</div><div class="v">${value}</div></div>
      <button type="button" class="edit" data-goto="${gotoStep}">${WIZ_I18N.reviewEdit}</button>
    </div>`;
  }

  function renderReview() {
    const empty = WIZ_I18N.reviewEmpty;

    // company
    const company = fieldVal("company_name") || empty;

    // fuel
    const f1 = radioVal("fuel1_type");
    let fuelLine = empty;
    if (f1) {
      let label = REVIEW_I18N.fuel_type[f1] || f1;
      if (f1 === "fuel_oil") {
        const grade = radioVal("fuel1_grade");
        if (grade) label += " " + grade;
      }
      const cons = fieldVal("fuel1_cons_1");
      const unit = REVIEW_I18N.unit[radioVal("fuel1_unit")] || "";
      fuelLine = cons ? `${label} · ${cons} ${unit}` : label;
    }

    // gas plan
    const purposes = multiVals("purpose").map(v => REVIEW_I18N.purpose[v] || v);
    const supplyDate = fieldVal("ng_supply_date");
    let gasLine = purposes.length ? purposes.join(" + ") : empty;
    if (supplyDate) gasLine = (purposes.length ? gasLine + " · " : "") + supplyDate;

    // electricity
    const sources = multiVals("elec_source").map(v => REVIEW_I18N.elec_source[v] || v);
    const base = fieldVal("elec_base");
    let elecLine = sources.length ? sources.join(" + ") : empty;
    if (base) elecLine += ` · Base ${base} MWh`;

    // compliance
    const consentOk = pdpaCheckbox.checked;
    const signer = fieldVal("pdpa_name") || fieldVal("contact_person");
    const complianceLine = consentOk
      ? WIZ_I18N.reviewConsentYes + (signer ? " · " + signer : "")
      : WIZ_I18N.reviewConsentNo;

    reviewCards.innerHTML =
      card("building", WIZ_I18N.cardCompany, company, 1, false) +
      card("flame", WIZ_I18N.cardFuel, fuelLine, 2, false) +
      card("gauge", WIZ_I18N.cardGasplan, gasLine, 3, false) +
      card("bolt", WIZ_I18N.cardElec, elecLine, 4, false) +
      card("shield", WIZ_I18N.cardCompliance, complianceLine, 5, consentOk);
  }

  reviewCards && reviewCards.addEventListener("click", (e) => {
    const btn = e.target.closest("[data-goto]");
    if (btn) goTo(Number(btn.dataset.goto));
  });

  render();
})();
