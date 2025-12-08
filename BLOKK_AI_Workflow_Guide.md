# 🤖 AI-POWERED BLOKK WORKFLOW: Power Automate + Claude API

---

## 📊 **KÖLTSÉGBECSLÉS (Napi használat)**

| Szolgáltatás | Költség/hó | Megjegyzés |
|-------------|-----------|-----------|
| **Microsoft 365** | $0 | Már megvan |
| **Power Automate** | $0 | M365-ben benne (2,000 runs/hó) |
| **Claude 3.5 Sonnet API** | ~$5-8 | Napi 4 dokumentum, ~10K tokens/nap |
| **GitHub Private Repo** | $4 | 1 repo |
| **Microsoft Lists** | $0 | M365-ben benne |
| **OneDrive** | $0 | M365-ben benne |
| **TOTAL** | **~$9-12/hó** | ✅ **Budget alatt!** |

**Claude API részletes számítás:**
- Input: $3/1M tokens → Napi 4 DOCX × 2K tokens = 8K tokens/nap × 30 nap = 240K tokens/hó = **$0.72**
- Output: $15/1M tokens → Napi 4 JSON × 1K tokens = 4K tokens/nap × 30 nap = 120K tokens/hó = **$1.80**
- **Total Claude:** ~$2.52/hó (konzervatív becslés: $5-8/hó)

---

## 🏗️ **ARCHITEKTÚRA**

```
┌─────────────────────────────────────────────────────────────┐
│                    ONEDRIVE (Forrás)                        │
│  📄 BLOKK1_Orszagok.docx                                    │
│  📄 BLOKK2_Kutatasok.docx                                   │
│  📄 BLOKK3_Termekek.docx                                    │
│  📄 BLOKK4_Mukodesi_keretek.docx                            │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│              POWER AUTOMATE (Orchestration)                 │
│  🔄 Trigger: Scheduled (Naponta 8:00)                       │
│  🔄 Action 1: Get file content (OneDrive)                   │
│  🔄 Action 2: Convert DOCX → Text                           │
│  🔄 Action 3: HTTP Request → Claude API                     │
│  🔄 Action 4: Parse JSON response                           │
│  🔄 Action 5: Update Microsoft Lists                        │
│  🔄 Action 6: Commit to GitHub                              │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│                  CLAUDE 3.5 SONNET API                      │
│  🧠 Prompt: "Kinyerni táblázat, lista, szabad szöveg"      │
│  🧠 Response: JSON (országok, %, függőségek)                │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│              MICROSOFT LISTS (Adattár)                      │
│  📋 BLOKK1_Lista: Országok, tevékenységek                   │
│  📋 BLOKK2_Lista: Kutatások, készültség %                   │
│  📋 BLOKK3_Lista: Termékek, készültség %                    │
│  📋 BLOKK4_Lista: Működési keretek                          │
│  🔗 Lookup columns: BLOKK2 → BLOKK3 függőségek             │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│                 GITHUB (Verziókövetés)                      │
│  📦 Private Repo: blokk-management                          │
│  📝 Commit: "AI update: BLOKK2 kutatás 75% → 80%"          │
└─────────────────────────────────────────────────────────────┘
                          ↓
┌─────────────────────────────────────────────────────────────┐
│              POWER BI / EXCEL (Dashboard)                   │
│  📊 Real-time adatok Microsoft Lists-ből                    │
│  📊 Gantt chart, progress bars, kapcsolatok                 │
└─────────────────────────────────────────────────────────────┘
```

---

## 🔧 **POWER AUTOMATE FLOW - RÉSZLETES LÉPÉSEK**

### **1. TRIGGER: Scheduled (Naponta)**

```
Trigger: Recurrence
- Frequency: Day
- Interval: 1
- Time zone: (UTC+01:00) Budapest
- At these hours: 8
- At these minutes: 0
```

**Miért naponta 8:00?**
- Reggel frissülnek a BLOKK dokumentumok
- Claude API olcsóbb off-peak időben (nincs rate limit)
- Elég idő van a nap folyamán ellenőrizni az eredményeket

---

### **2. ACTION: Get File Content (OneDrive)**

```
Action: Get file content (OneDrive for Business)
- File: /BLOKK1_Orszagok.docx
- Output: File Content (binary)
```

**Ismételd meg mind a 4 BLOKK-ra:**
- BLOKK1_Orszagok.docx
- BLOKK2_Kutatasok.docx
- BLOKK3_Termekek.docx
- BLOKK4_Mukodesi_keretek.docx

---

### **3. ACTION: Convert DOCX → Text**

**Probléma:** Power Automate nem tudja natívan konvertálni a DOCX-et szöveggé.

**Megoldás 1: OneDrive API (Egyszerűbb)**
```
Action: HTTP (Premium connector)
- Method: GET
- URI: https://graph.microsoft.com/v1.0/me/drive/items/{file-id}/content?format=pdf
- Headers: 
  - Authorization: Bearer @{body('Get_file_metadata')?['@microsoft.graph.downloadUrl']}
```

**Megoldás 2: Azure Logic Apps Connector (Ajánlott)**
```
Action: Convert File (OneDrive)
- File: @{outputs('Get_file_content_BLOKK1')?['body']}
- Convert to: Text
```

**Megoldás 3: Claude API közvetlenül (LEGEGYSZERŰBB!)**
- Claude API támogatja a DOCX fájlokat base64 encoding-gal
- Nem kell külön konverzió!

**Használjuk a Megoldás 3-at:**

```
Action: Compose
- Inputs: @{base64(outputs('Get_file_content_BLOKK1')?['body'])}
- Output: base64_content_BLOKK1
```

---

### **4. ACTION: HTTP Request → Claude API**

```
Action: HTTP
- Method: POST
- URI: https://api.anthropic.com/v1/messages
- Headers:
  - Content-Type: application/json
  - x-api-key: @{variables('ClaudeAPIKey')}
  - anthropic-version: 2023-06-01
- Body:
{
  "model": "claude-3-5-sonnet-20241022",
  "max_tokens": 2048,
  "messages": [
    {
      "role": "user",
      "content": [
        {
          "type": "document",
          "source": {
            "type": "base64",
            "media_type": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            "data": "@{outputs('Compose_base64_BLOKK1')}"
          }
        },
        {
          "type": "text",
          "text": "Elemezd ezt a BLOKK1 dokumentumot. Kinyerni a következő adatokat JSON formátumban:\n\n{\n  \"blokk_id\": \"BLOKK1\",\n  \"blokk_nev\": \"...\",\n  \"elemek\": [\n    {\n      \"id\": \"...\",\n      \"orszag\": \"...\",\n      \"tevekenyseg\": \"...\",\n      \"statusz\": \"...\",\n      \"keszultseg_szazalek\": 0,\n      \"fuggoségek\": [\"BLOKK2_elem_id\", ...],\n      \"megjegyzesek\": \"...\"\n    }\n  ],\n  \"utolso_frissites\": \"2025-12-08\"\n}\n\nFigyelem:\n- Táblázatokat, listákat, szabad szöveget is dolgozz fel\n- Készültség %-ot számokként add meg (0-100)\n- Függőségeket tömb formában\n- Ha nincs adat, használj null értéket"
        }
      ]
    }
  ]
}
```

**Claude API Key tárolása (BIZTONSÁGOS!):**
```
1. Power Automate → Settings → Connections
2. Új változó: ClaudeAPIKey (Secure String)
3. Érték: sk-ant-api03-... (Anthropic API key)
```

---

### **5. ACTION: Parse JSON Response**

```
Action: Parse JSON
- Content: @{outputs('HTTP_Claude_BLOKK1')?['body']?['content']?[0]?['text']}
- Schema:
{
  "type": "object",
  "properties": {
    "blokk_id": {"type": "string"},
    "blokk_nev": {"type": "string"},
    "elemek": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "id": {"type": "string"},
          "orszag": {"type": "string"},
          "tevekenyseg": {"type": "string"},
          "statusz": {"type": "string"},
          "keszultseg_szazalek": {"type": "integer"},
          "fuggoségek": {"type": "array", "items": {"type": "string"}},
          "megjegyzesek": {"type": "string"}
        }
      }
    },
    "utolso_frissites": {"type": "string"}
  }
}
```

---

### **6. ACTION: Update Microsoft Lists**

**Microsoft Lists struktúra (előre létrehozva):**

**BLOKK1_Lista:**
| Oszlop | Típus | Megjegyzés |
|--------|-------|-----------|
| Title | Single line text | Elem ID (pl. "BLOKK1_001") |
| Orszag | Single line text | Ország neve |
| Tevekenyseg | Multiple lines text | Tevékenység leírása |
| Statusz | Choice | Tervezett / Folyamatban / Kész |
| Keszultseg | Number | 0-100 % |
| Fuggoségek | Multiple lines text | JSON array (később Lookup) |
| Megjegyzesek | Multiple lines text | Szabad szöveg |
| Utolso_frissites | Date | Automatikus |

```
Action: Apply to each
- Select: @{outputs('Parse_JSON_BLOKK1')?['body']?['elemek']}
- Actions:
  - Get items (Microsoft Lists)
    - Site: https://yourtenant.sharepoint.com/sites/BlokManagement
    - List: BLOKK1_Lista
    - Filter: Title eq '@{items('Apply_to_each')?['id']}'

  - Condition: @{outputs('Get_items')?['body/value']} is empty
    - If YES: Create item (Microsoft Lists)
      - Title: @{items('Apply_to_each')?['id']}
      - Orszag: @{items('Apply_to_each')?['orszag']}
      - Tevekenyseg: @{items('Apply_to_each')?['tevekenyseg']}
      - Statusz: @{items('Apply_to_each')?['statusz']}
      - Keszultseg: @{items('Apply_to_each')?['keszultseg_szazalek']}
      - Fuggoségek: @{string(items('Apply_to_each')?['fuggoségek'])}
      - Megjegyzesek: @{items('Apply_to_each')?['megjegyzesek']}
      - Utolso_frissites: @{utcNow()}

    - If NO: Update item (Microsoft Lists)
      - ID: @{outputs('Get_items')?['body/value'][0]?['ID']}
      - (ugyanazok a mezők mint fent)
```

**Ismételd meg mind a 4 BLOKK-ra!**

---

### **7. ACTION: Commit to GitHub**

```
Action: HTTP
- Method: PUT
- URI: https://api.github.com/repos/{owner}/blokk-management/contents/data/BLOKK1_data.json
- Headers:
  - Authorization: token @{variables('GitHubToken')}
  - Content-Type: application/json
- Body:
{
  "message": "AI update: BLOKK1 frissítve @{utcNow()}",
  "content": "@{base64(outputs('Parse_JSON_BLOKK1'))}",
  "sha": "@{outputs('Get_GitHub_file_sha')?['body']?['sha']}"
}
```

**GitHub Token tárolása:**
```
1. GitHub → Settings → Developer settings → Personal access tokens
2. Generate new token (classic)
3. Scopes: repo (full control)
4. Power Automate → Variables → GitHubToken (Secure String)
```

**Első commit előtt (SHA lekérése):**
```
Action: HTTP
- Method: GET
- URI: https://api.github.com/repos/{owner}/blokk-management/contents/data/BLOKK1_data.json
- Headers:
  - Authorization: token @{variables('GitHubToken')}
- Output: Get_GitHub_file_sha
```

---

### **8. ACTION: Send Notification (Opcionális)**

```
Action: Send an email (V2)
- To: your-email@example.com
- Subject: ✅ BLOKK rendszer frissítve - @{utcNow()}
- Body:
<h2>BLOKK Rendszer AI Frissítés</h2>
<ul>
  <li>BLOKK1: @{outputs('Parse_JSON_BLOKK1')?['body']?['elemek']?[0]?['keszultseg_szazalek']}% kész</li>
  <li>BLOKK2: @{outputs('Parse_JSON_BLOKK2')?['body']?['elemek']?[0]?['keszultseg_szazalek']}% kész</li>
  <li>BLOKK3: @{outputs('Parse_JSON_BLOKK3')?['body']?['elemek']?[0]?['keszultseg_szazalek']}% kész</li>
  <li>BLOKK4: @{outputs('Parse_JSON_BLOKK4')?['body']?['elemek']?[0]?['keszultseg_szazalek']}% kész</li>
</ul>
<p>GitHub commit: <a href="https://github.com/{owner}/blokk-management/commits/main">Nézd meg</a></p>
```

---

## 🧠 **CLAUDE PROMPT ENGINEERING (Vegyes formátumokhoz)**

**Példa BLOKK2 dokumentumra (Kutatások - táblázat, lista, szabad szöveg):**

```json
{
  "role": "user",
  "content": "Elemezd ezt a BLOKK2 kutatási dokumentumot. A dokumentum vegyes formátumú:

  - TÁBLÁZATOK: Kutatási projektek neve, felelős, határidő, készültség %
  - LISTÁK: Mérföldkövek, függőségek
  - SZABAD SZÖVEG: Megjegyzések, kockázatok

  Kinyerni a következő JSON struktúrát:

  {
    \"blokk_id\": \"BLOKK2\",
    \"blokk_nev\": \"Kutatások\",
    \"elemek\": [
      {
        \"id\": \"BLOKK2_001\",
        \"kutatas_nev\": \"...\",
        \"felelos\": \"...\",
        \"hatarido\": \"2025-12-31\",
        \"keszultseg_szazalek\": 75,
        \"merfoldkovek\": [
          {\"nev\": \"...\", \"statusz\": \"Kész/Folyamatban/Tervezett\"}
        ],
        \"fuggoségek\": [\"BLOKK1_001\", \"BLOKK3_002\"],
        \"kockazatok\": \"...\",
        \"megjegyzesek\": \"...\"
      }
    ],
    \"utolso_frissites\": \"2025-12-08\"
  }

  FONTOS:
  - Ha táblázatban van adat, onnan vedd
  - Ha listában van, tömb formában add meg
  - Ha szabad szövegben van, szöveges mezőbe rakd
  - Készültség %-ot MINDIG számként (0-100)
  - Dátumokat YYYY-MM-DD formátumban
  - Ha nincs adat, használj null értéket
  - Függőségeket BLOKK_ID formátumban (pl. BLOKK1_001)"
}
```

---

## 📋 **MICROSOFT LISTS STRUKTÚRA (Mind a 4 BLOKK-hoz)**

### **BLOKK1_Lista (Országok, tevékenységek)**

| Oszlop | Típus | Példa érték |
|--------|-------|------------|
| Title | Text | BLOKK1_001 |
| Orszag | Text | Delaware (USA) |
| Tevekenyseg | Text | C-Corp alapítás |
| Statusz | Choice | Folyamatban |
| Keszultseg | Number | 60 |
| Fuggoségek | Text | ["BLOKK2_001"] |
| Megjegyzesek | Text | Ügyvéd kiválasztva |
| Utolso_frissites | Date | 2025-12-08 |

### **BLOKK2_Lista (Kutatások)**

| Oszlop | Típus | Példa érték |
|--------|-------|------------|
| Title | Text | BLOKK2_001 |
| Kutatas_nev | Text | Piackutatás - EU |
| Felelos | Person | John Doe |
| Hatarido | Date | 2025-12-31 |
| Keszultseg | Number | 75 |
| Merfoldkovek | Text | [{"nev":"Adatgyűjtés","statusz":"Kész"}] |
| Fuggoségek | Lookup | BLOKK1_001 (Lookup to BLOKK1_Lista) |
| Kockazatok | Text | Adathiány |
| Megjegyzesek | Text | Q1 2025 befejezés |
| Utolso_frissites | Date | 2025-12-08 |

### **BLOKK3_Lista (Termékek)**

| Oszlop | Típus | Példa érték |
|--------|-------|------------|
| Title | Text | BLOKK3_001 |
| Termek_nev | Text | MVP v1.0 |
| Kategoria | Choice | Software |
| Keszultseg | Number | 45 |
| Fuggoségek | Lookup | BLOKK2_001 (Lookup to BLOKK2_Lista) |
| Megjegyzesek | Text | Beta teszt Q2 |
| Utolso_frissites | Date | 2025-12-08 |

### **BLOKK4_Lista (Működési keretek)**

| Oszlop | Típus | Példa érték |
|--------|-------|------------|
| Title | Text | BLOKK4_001 |
| Keret_nev | Text | ExO Framework |
| Leiras | Text | Exponential Org elvek |
| Statusz | Choice | Aktív |
| Fuggoségek | Lookup | BLOKK1_001, BLOKK2_001 |
| Megjegyzesek | Text | MTP definiálva |
| Utolso_frissites | Date | 2025-12-08 |

---

## 🔗 **BLOKKOK KÖZÖTTI KAPCSOLATOK (Lookup Columns)**

**Microsoft Lists Lookup beállítása:**

1. **BLOKK2_Lista → BLOKK1_Lista**
   - Oszlop: Fuggoségek_BLOKK1
   - Típus: Lookup
   - Get information from: BLOKK1_Lista
   - In this column: Title
   - Allow multiple values: Yes

2. **BLOKK3_Lista → BLOKK2_Lista**
   - Oszlop: Fuggoségek_BLOKK2
   - Típus: Lookup
   - Get information from: BLOKK2_Lista
   - In this column: Title
   - Allow multiple values: Yes

3. **BLOKK4_Lista → BLOKK1, BLOKK2, BLOKK3**
   - Oszlop: Fuggoségek_BLOKK1, Fuggoségek_BLOKK2, Fuggoségek_BLOKK3
   - Típus: Lookup (mindegyik külön oszlop)

**Vizualizáció Power BI-ban:**
```
BLOKK1 (Országok)
    ↓
BLOKK2 (Kutatások) → BLOKK3 (Termékek)
    ↓                      ↓
BLOKK4 (Működési keretek) ←
```

---

## 📊 **DASHBOARD (Power BI / Excel)**

**Power BI Desktop (Ingyenes):**

1. **Adatforrás:** Microsoft Lists (SharePoint connector)
2. **Vizualizációk:**
   - **Gantt Chart:** BLOKK2 kutatások idővonalon
   - **Progress Bars:** Mind a 4 BLOKK készültség %
   - **Network Diagram:** Blokkok közötti függőségek
   - **KPI Cards:** Összesített készültség, határidők

**Excel (Egyszerűbb):**

1. **Data → Get Data → From Online Services → SharePoint Online List**
2. **URL:** https://yourtenant.sharepoint.com/sites/BlokManagement
3. **Pivot Table:** Készültség % BLOKK-onként
4. **Charts:** Progress bars, pie charts

---

## 🚀 **IMPLEMENTÁCIÓS LÉPÉSEK (Sorrend)**

### **1. HÉTVÉGE (Előkészítés)**

1. **Claude API Key megszerzése:**
   - https://console.anthropic.com/
   - Sign up → API Keys → Create Key
   - Költsd el az ingyenes $5 creditet először!

2. **GitHub Private Repo létrehozása:**
   - https://github.com/new
   - Repo name: `blokk-management`
   - Private: ✅
   - Initialize with README: ✅

3. **Microsoft Lists létrehozása:**
   - SharePoint site: https://yourtenant.sharepoint.com/sites/BlokManagement
   - Új lista: BLOKK1_Lista, BLOKK2_Lista, BLOKK3_Lista, BLOKK4_Lista
   - Oszlopok hozzáadása (lásd fent)

### **2. HÉT ELEJE (Power Automate Flow)**

4. **Power Automate Flow létrehozása:**
   - https://make.powerautomate.com/
   - Create → Scheduled cloud flow
   - Flow name: "BLOKK AI Sync - Daily"
   - Recurrence: Daily, 8:00 AM

5. **Változók inicializálása:**
   - ClaudeAPIKey (Secure String)
   - GitHubToken (Secure String)

6. **OneDrive fájlok lekérése:**
   - Get file content × 4 (BLOKK1-4)

7. **Claude API hívások:**
   - HTTP action × 4 (BLOKK1-4)
   - Parse JSON × 4

8. **Microsoft Lists frissítése:**
   - Apply to each × 4
   - Create/Update items

9. **GitHub commit:**
   - HTTP PUT × 4

10. **Email notification:**
    - Send email (összefoglaló)

### **3. HÉT KÖZEPE (Tesztelés)**

11. **Manuális tesztelés:**
    - Flow futtatása "Test" gombbal
    - Ellenőrizd a Claude API response-t
    - Ellenőrizd a Microsoft Lists frissítést
    - Ellenőrizd a GitHub commit-ot

12. **Hibakezelés hozzáadása:**
    - Try-Catch blokkok
    - Error notification email

### **4. HÉT VÉGE (Dashboard)**

13. **Power BI Desktop telepítése:**
    - https://powerbi.microsoft.com/downloads/

14. **Dashboard létrehozása:**
    - SharePoint Lists connector
    - Vizualizációk (Gantt, Progress, Network)

15. **Publish to Power BI Service:**
    - Publish → My Workspace
    - Megosztás csapattal

---

## ⚠️ **HIBAKEZELÉS ÉS MONITORING**

### **Power Automate Error Handling:**

```
Action: Scope (Try)
- Actions: (összes Claude API hívás)

Action: Scope (Catch)
- Configure run after: has failed
- Actions:
  - Send email (V2)
    - To: admin@example.com
    - Subject: ❌ BLOKK AI Sync FAILED
    - Body: @{outputs('HTTP_Claude_BLOKK1')?['body']?['error']?['message']}
```

### **Claude API Rate Limits:**

- **Free tier:** $5 credit (kb. 1-2 hét teszteléshez)
- **Tier 1:** $100/hó limit (elég lesz!)
- **Rate limit:** 50 requests/minute (bőven elég napi 4 dokumentumhoz)

### **Power Automate Limits:**

- **M365 Free tier:** 2,000 runs/hó (napi 1 run = 30 runs/hó → OK!)
- **Premium connectors:** HTTP connector PREMIUM (de M365-ben benne van!)

---

## 💡 **OPTIMALIZÁCIÓS TIPPEK**

### **1. Költségcsökkentés:**

- **Csak változott fájlokat dolgozd fel:**
  ```
  Trigger: When a file is modified (OneDrive)
  → Csak az adott BLOKK-ot frissítsd
  ```

- **Batch processing:**
  ```
  Egy Claude API hívás mind a 4 BLOKK-hoz:
  "Elemezd ezt a 4 dokumentumot egyszerre..."
  → Kevesebb API hívás, olcsóbb!
  ```

### **2. Teljesítmény növelés:**

- **Parallel branches:**
  ```
  Power Automate → Parallel branch
  → Mind a 4 BLOKK egyszerre dolgozódik fel
  → 4x gyorsabb!
  ```

### **3. Adatminőség javítás:**

- **Claude prompt finomítása:**
  ```
  "Ha bizonytalan vagy, add meg a confidence score-t (0-100%)"
  → Manuális ellenőrzés csak alacsony confidence esetén
  ```

---

## 📞 **KÖVETKEZŐ LÉPÉSEK**

**Kérdések:**

1. **Szeretnéd, hogy elkészítsem a konkrét Power Automate Flow JSON export-ot?**
   - Importálható azonnal a Power Automate-be
   - Csak az API key-eket kell beállítani

2. **Kell segítség a Microsoft Lists struktúra létrehozásához?**
   - PowerShell script a listák automatikus létrehozásához

3. **Szeretnéd a Claude prompt template-eket a 4 BLOKK-hoz?**
   - Optimalizált promptok táblázat/lista/szabad szöveg feldolgozáshoz

4. **Kell Power BI dashboard template?**
   - .pbix fájl a vizualizációkhoz

---

## 📚 **HASZNOS LINKEK**

- **Claude API Dokumentáció:** https://docs.anthropic.com/claude/reference/getting-started-with-the-api
- **Power Automate Dokumentáció:** https://learn.microsoft.com/en-us/power-automate/
- **Microsoft Lists:** https://support.microsoft.com/en-us/office/get-started-with-microsoft-lists
- **GitHub API:** https://docs.github.com/en/rest
- **Power BI Desktop:** https://powerbi.microsoft.com/downloads/

---

**Készítette:** AI Assistant
**Dátum:** 2025-12-08
**Verzió:** 1.0
**Költségvetés:** $9-12/hó (Claude API + GitHub Private)


