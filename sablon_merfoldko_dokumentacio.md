---
puppeteer:
  preferCSSPageSize: true
  displayHeaderFooter: false
  margin:
    top: 10mm
    bottom: 10mm
    left: 11mm
    right: 11mm
---

<style>
  @page {
    size: A4 portrait !important;
    margin: 10mm 11mm 10mm 11mm !important;
  }
  html, body, .markdown-preview, .markdown-preview.markdown-preview {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif !important;
    font-size: 10pt !important;
    line-height: 1.4 !important;
    color: #1f2328 !important;
    padding: 0 !important;
    margin: 0 !important;
    background-color: #ffffff !important;
  }
  h1, .markdown-preview h1 {
    font-size: 15.5pt !important;
    margin: 0 0 5px 0 !important;
    color: #0f172a !important;
    text-align: center !important;
    font-weight: 700 !important;
  }
  h2, .markdown-preview h2 {
    font-size: 12pt !important;
    margin: 7px 0 4px 0 !important;
    color: #1e3a8a !important;
    border-bottom: 1.2px solid #cbd5e1 !important;
    padding-bottom: 2px !important;
    font-weight: 700 !important;
  }
  h3, .markdown-preview h3 {
    font-size: 10.5pt !important;
    margin: 6px 0 3px 0 !important;
    color: #334155 !important;
    font-weight: 700 !important;
  }
  table, .markdown-preview table {
    width: 100% !important;
    border-collapse: collapse !important;
    font-size: 8.8pt !important;
    margin: 5px 0 7px 0 !important;
  }
  th, td, .markdown-preview th, .markdown-preview td {
    border: 0.8px solid #cbd5e1 !important;
    padding: 4.0px 5.5px !important;
    text-align: left !important;
  }
  th, .markdown-preview th {
    background-color: #f1f5f9 !important;
    color: #0f172a !important;
    font-weight: 600 !important;
  }
  tr:nth-child(even) td {
    background-color: #f8fafc !important;
  }
  ul, ol, .markdown-preview ul, .markdown-preview ol {
    margin: 3px 0 5px 0 !important;
    padding-left: 20px !important;
  }
  li, .markdown-preview li {
    margin-bottom: 2.5px !important;
    line-height: 1.38 !important;
  }
  p, .markdown-preview p {
    margin: 3px 0 4px 0 !important;
  }
  img, .markdown-preview img {
    max-height: 275px !important;
    width: auto !important;
    max-width: 98% !important;
    display: block !important;
    margin: 3px auto 5px auto !important;
  }
  .header-box {
    background-color: #f8fafc !important;
    border: 1px solid #cbd5e1 !important;
    border-radius: 4px !important;
    padding: 5px 12px !important;
    margin-bottom: 6px !important;
    font-size: 9.2pt !important;
    text-align: center !important;
  }
  .formula-box {
    background-color: #f1f5f9 !important;
    border-left: 3.5px solid #2563eb !important;
    padding: 6px 14px !important;
    margin: 6px 0 !important;
    font-size: 9.6pt !important;
    font-weight: 600 !important;
    text-align: center !important;
  }
  pre, code, .markdown-preview pre, .markdown-preview code {
    font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, monospace !important;
    font-size: 8.2pt !important;
    padding: 1.5px 3.5px !important;
    margin: 1px 0 !important;
    line-height: 1.24 !important;
  }
  pre {
    background-color: #f8fafc !important;
    border: 0.8px solid #cbd5e1 !important;
    border-radius: 3px !important;
    padding: 6px 8px !important;
  }
  .page-break, .pagebreak, div.page-break {
    page-break-after: always !important;
    break-after: page !important;
    height: 0 !important;
    margin: 0 !important;
    padding: 0 !important;
  }
</style>

<!-- ========================================================================================= -->
<!-- 1. OLDAL: CÍM, PROJEKT FEJLÉC ÉS BEVEZETÉS -->
<!-- ========================================================================================= -->

# Gépi Tanulás – [N.] Mérföldkő Dokumentáció
## [Projekt Alcíme / Témája]

<div class="header-box">
  <strong>Projekt:</strong> [Projekt Neve] &nbsp;|&nbsp; 
  <strong>Szerzők:</strong> [Csapatnév / Szerzők] &nbsp;|&nbsp; 
  <strong>Dátum:</strong> [2026. hónap] &nbsp;|&nbsp; 
  <strong>Terjedelem:</strong> 5 oldal (1. oldal / 5)
</div>

### 1.1. Fejezet Alcím
Ide kerül a fejezet bevezető szövege. Ügyelj arra, hogy a felsorolások előtt mindig legyen egy üres sor!

* **Fő pont 1:** Részletes leírás az elvégzett lépésekről.
* **Fő pont 2:** További kulcsfontosságú összefüggések.

<div class="formula-box">
  Kiemelt formula / képlet: RMSE = √( 1/N · Σ (y - ŷ)² )
</div>

### 1.2. Táblázatos Összefoglaló

| Oszlop 1 | Oszlop 2 | Oszlop 3 | Oszlop 4 |
| :--- | :---: | :---: | :--- |
| Adat 1 | Érték A | Érték B | Leírás és magyarázat |
| Adat 2 | Érték C | Érték D | Leírás és magyarázat |

<div class="page-break"></div>

<!-- ========================================================================================= -->
<!-- 2. OLDAL: FEJEZET CÍM -->
<!-- ========================================================================================= -->

## 2. Oldal: [Fejezet Címe]

### 2.1. [Alfejezet Címe]
Ide jön a tartalom...

<div class="page-break"></div>

<!-- ========================================================================================= -->
<!-- 3. OLDAL: FEJEZET CÍM -->
<!-- ========================================================================================= -->

## 3. Oldal: [Fejezet Címe]

### 3.1. [Alfejezet Címe]
Ide jön a tartalom...

<div class="page-break"></div>

<!-- ========================================================================================= -->
<!-- 4. OLDAL: VIZUALIZÁCIÓ ÉS GRAFIKONOK -->
<!-- ========================================================================================= -->

## 4. Oldal: [Feltáró Elemzés / Ábrák / Eredmények]

![Ábra megnevezése](figures/[abra_fajlneve].png)

### 4.1. Az Ábra Értelmezése
Ide jön az ábra részletes szöveges magyarázata...

<div class="page-break"></div>

<!-- ========================================================================================= -->
<!-- 5. OLDAL: ÖSSZEGZÉS ÉS MODELLEZÉSI STRATÉGIA -->
<!-- ========================================================================================= -->

## 5. Oldal: [Módszertan / Eredmények / Konklúzió]

### 5.1. Eredmények Összegzése
Ide jön a záró fejezet tartalma...
