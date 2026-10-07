# Machine Learning Projekt Kontextus és Áttekintés
## Spotify Dalnépszerűség Előrejelzése (Song Popularity Prediction)

Ez a dokumentum összefoglalja a projekt aktuális állapotát, az 1. mérföldkő során elvégzett vizsgálatokat, az adatbázis tényeit, a kialakított könyvtárstruktúrát és a 2. mérföldkőhöz szükséges teendőket, hogy a munka bármilyen gépről vagy új beszélgetésből zökkenőmentesen folytatható legyen.

---

## 1. Projekt Áttekintés és Célkitűzés
* **Tantárgy / Feladat:** Gépi Tanulás – 1. Mérföldkő (Exploratory Data Analysis, Adatminőség és Modellezési Terv).
* **Cél:** A Spotify platformján közzétett dalok népszerűségének (`song_popularity`) becslése akusztikai és zenei audio feature-ök alapján.
* **Feladat típusa:** **Regresszió (Supervised Regression)**. A célváltozó $[0, 100]$ skálájú, egész értékű pontszám, amely folytonos intenzitást fejez ki.
* **Státusz:** **Az 1. mérföldkő 100%-ban lezárva.** A dokumentáció pontosan **5 oldalas formátumban** PDF-ben és Markdownban is elkészült.

---

## 2. Az Adathalmaz Tényei és Adatminőségi Eredmények
* **Fájl helye:** `1_milestone/data/song_data.csv` (2.2 MB, Kaggle Song Popularity Dataset / Spotify Web API).
* **Méret:** **18 835 sor** és **15 oszlop** (1 szöveges metaadat + 13 audio feature + 1 célváltozó).
* **Hiányzó adatok:** **0 db hiányzó érték (100.0% teljesség).** Semmilyen oszlopban nincs NaN / üres mező. *(Korábbi piszkozatokban felmerült 2 hiányzó érték létezése, de kóddal bizonyítottuk, hogy fiktív volt).*
* **Duplikációk:** **3 909 sor (20.75%)** teljes egészében, minden oszlopában duplikátum!
  * A duplikációk a nemzetközi popslágereknél koncentrálódnak (*FEFE*: 19x, *MIA*: 18x, *Taki Taki*: 18x, *No Stylist*: 17x).
  * A duplikátumok eltávolítása után **14 926 egyedi sor** marad.
  * Hatás: A duplikátumok eltávolításával a célváltozó átlaga **52.99-ről 48.75-re** esik vissza, és a korrelációk feleződnek (pl. `danceability` korrelációja +0.104-ről +0.056-ra). A dedublikálás kötelező lépés a Data Leakage megelőzésére.
* **Dalcímek nem-egyedisége:** 13 070 egyedi cím jut a 18 835 sorra (pl. *"Better"* 21-szer szerepel, 1–95 népszerűséggel). A `song_name` kizárandó a modellezésből.
* **Outlier-ek és technikai anomáliák:**
  * Időtartam: 12 másodperctől közel 30 percig (Fela Kuti: *"Army Arrangement"* – 1 799 346 ms, népszerűsége 23; Martin Luther King beszéd: 17.5 perc).
  * Hibás sorok: `time_signature == 0` (3 sor), `tempo == 0` (2 sor), `loudness > 0 dB` (7 sor, digitális clipping).
* **Korrelációk:**
  * Gyenge lineáris kapcsolat a népszerűséggel: `instrumentalness` ($-0.131$), `danceability` ($+0.104$), `loudness` ($+0.099$), `energy` ($+0.001$).
  * Multikollinearitás a változók között: `energy` $\leftrightarrow$ `loudness` ($+0.756$), `acousticness` $\leftrightarrow$ `energy` ($-0.663$).
  * Nem-lineáris mintázat: A 80–100-as slágersávban ugrásszerűen magasabb az átlagos táncolhatóság ($0.701$ vs. $0.62$) és a hangerő ($-5.89\text{ dB}$ vs. $-7.9\text{ dB}$).

---

## 3. Könyvtárstruktúra és Fájlok Szerepe

```text
H:\machine learning\
├── context.md                                  # Ez a projektösszefoglaló fájl
└── 1_milestone/
    ├── 1_merfoldko_dokumentacio.md             # Végleges, 5 oldalra kalibrált Markdown forrás
    ├── 1_merfoldko_dokumentacio_5oldal.pdf     # Végleges, ellenőrzött 5 oldalas kész PDF beadandó
    ├── data/
    │   └── song_data.csv                       # A projekt nyers adathalmaza (18 835 sor)
    ├── figures/
    │   ├── dashboard_eda_summary.png           # 2x2-es összefoglaló EDA Dashboard (a 4. oldal ábrája)
    │   ├── fig1_popularity_distribution.png    # Célváltozó eloszlása (eredeti vs. dedublikált)
    │   ├── fig2_correlation_heatmap.png        # Teljes Pearson-korrelációs hőtérkép
    │   ├── fig3_danceability_loudness_by_cat.png# Danceability és loudness népszerűségi sávokban
    │   ├── fig4_duplicate_bias_comparison.png  # Duplikációk torzító hatása
    │   └── fig5_time_signature_dist.png        # Ütemmutató megoszlása
    ├── scripts/
    │   ├── verify_milestone.py                 # Tételes ellenőrző szkript (1-16. állítás vizsgálata)
    │   ├── generate_dashboard.py               # A 2x2-es EDA dashboard ábrát generáló kód
    │   ├── generate_figures.py                 # Az egyedi ábrákat generáló kód
    │   ├── compile_pdf.py                      # Chrome headless-szel 5 oldalas PDF-et készítő fordító
    │   └── calc_stats.py                       # Leíró statisztikákat számító segédszkript
    └── reference/
        ├── Gépitan 1. mérföldkő dokumentáció.pdf # Az eredeti kiadott feladatleírás / piszkozat
        └── extracted_pdf_text.txt              # Az eredeti PDF kinyert szövege
```

---

## 4. Dokumentáció és PDF Renderelési Tudnivalók
* **A pontosan 5 oldal biztosítása:**
  * A Markdown fájl elején be van állítva a Puppeteer front-matter és egy szigorúan méretezett nyomtatási CSS (`A4`, `8mm 10mm` margók, `8.5pt` betűméret, kompakt táblázatok, `220px` max képmagasság).
  * Mind az 5 oldal végén `<div class="page-break"></div>` oldaltörés található.
* **PDF újragenerálása parancssorból:**
  ```powershell
  python 1_milestone/scripts/compile_pdf.py
  ```
  Ez a parancs a Chrome headless nyomtatójával azonnal legenerálja az 5 oldalas `1_milestone/1_merfoldko_dokumentacio_5oldal.pdf` fájlt, és a terminálon ellenőrzi az oldalszámot.

---