<div align="center">

# 🇬🇧 UK DATING POOL CALCULATOR — V3 EVIDENCE EXPLORER
### *Zero-Dependency Client-Side Demographic Requirements Engine*

[![Node.js](https://img.shields.io/badge/Node.js-20+-339933?style=for-the-badge&logo=nodedotjs&logoColor=white)](https://nodejs.org/)
[![Vanilla JS](https://img.shields.io/badge/Vanilla-ES%20Modules-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)](https://developer.mozilla.org/)
[![ONS Census](https://img.shields.io/badge/Data-ONS%20Census%202021-blue?style=for-the-badge)](https://www.ons.gov.uk/)
[![HMRC Data](https://img.shields.io/badge/Income-HMRC%20SPI%202024-green?style=for-the-badge)](https://www.gov.uk/)
[![Zero Dependencies](https://img.shields.io/badge/Dependencies-ZERO-black?style=for-the-badge)](package.json)

<p align="center">
  <b>A lightweight, ultra-performant client-side demographic engine built directly on official ONS Census 2021 joint observations and HMRC income percentiles.</b>
</p>

</div>

---

## 📸 Interface Preview

<div align="center">
  <img src="dating-desktop-qa.png" alt="V3 Requirements Calculator" width="100%" />
</div>

---

## 🏛️ Executive Summary

**V3 Evidence Explorer** is the modern standalone web implementation of the UK Dating Pool Calculator. It was built to eliminate framework bloat, external telemetry, and questionable statistical assumptions.

### Key Architectural Standards
1. **Zero External Dependencies**: Zero npm packages required at runtime. Runs directly with Node.js built-ins.
2. **Joint Probability Conditioning**: Uses Census 2021 `country × sex × age × qualification × ethnicity` cross-tabulations.
3. **Data Integrity & Traceability**: Every figure links to an exact official ONS or HMRC workbook cell reference with verifiable SHA-256 fingerprints.
4. **Instant Scenario Comparisons**: Test up to three filter combinations side-by-side with instantaneous client-side re-calculation.

---

## 🚀 Quick Start

### Prerequisites
- Node.js 20 or later

### Launch Server
```powershell
# In the v3 folder:
npm start
```
*The server binds to `127.0.0.1` on an OS-assigned random port and outputs its exact localhost URL.*

### Run Test Suite
```powershell
npm test
```

---

## 📁 Subdirectory Layout

```text
v3/
├── calculator.html             # Primary Requirements Calculator UI
├── index.html                  # Secondary Demographic Evidence Explorer
├── app.mjs                     # Application entry point & tab lifecycle
├── dating-model.mjs            # Joint subgroup demographic model
├── dating.mjs                  # UI event handlers & scenario rendering
├── server.mjs                  # Zero-dependency local preview server
├── style.css & dating.css      # Editorial luxury CSS design system
├── data/                       # Extracted JSON statistical tables
├── sources/                    # Retained original ONS & HMRC workbooks
├── scripts/                    # Python extraction utilities
├── tests/                      # Automated unit tests & Playwright QA
└── AUDIT.md                    # In-depth methodological audit ledger
```

---

## 👤 Author

**Otis Powell** ([@passportpowell](https://github.com/passportpowell))  
- 🌐 GitHub: [github.com/passportpowell](https://github.com/passportpowell)
- 📺 YouTube: [@PassportPowell](https://www.youtube.com/@PassportPowell)
