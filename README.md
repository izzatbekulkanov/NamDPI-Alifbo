# NamDPI alifbo

**Namangan davlat pedagogika instituti**  
**Raqamli taʼlim texnologiyalari markazi (NamDPI RTTM)** tomonidan ishlab chiqilgan professional dasturiy taʼminot.

---

## 📌 Dastur haqida

**"NamDPI alifbo"** — kompyuterda (Windows 10 va Windows 11 tizimlarida) istalgan matn muharririda (**Microsoft Word, Telegram, Notepad, Brauzerlar, Excel** va barcha dasturlarda) matn terayotganda soʻzlarni probel (boʻsh joy) yoki tinish belgisi bosilishi bilan avtomatik ravishda tanlangan alifboga tezkor va xatosiz oʻgirib beruvchi professional dastur.

### 🌟 Asosiy imkoniyatlar:
1. **Yangi Oʻzbek Lotin alifbosi (2026):**
   - `sh` $\rightarrow$ `ş` (masalan: `shabnam` $\rightarrow$ `şabnam`, `shanba` $\rightarrow$ `şanba`)
   - `ch` $\rightarrow$ `ç` (masalan: `choy` $\rightarrow$ `çoy`)
   - `oʻ` / `o'` $\rightarrow$ `ö` (masalan: `o'zbekiston` $\rightarrow$ `özbekiston`, `o'quvchi` $\rightarrow$ `öquvçi`)
   - `gʻ` / `g'` $\rightarrow$ `ğ` (masalan: `bog'` $\rightarrow$ `boğ`, `g'alaba` $\rightarrow$ `ğalaba`)
   - Katta va bosh harflar toʻliq saqlanadi (`Shabnam` $\rightarrow$ `Şabnam`, `SHAHAR` $\rightarrow$ `ŞAHAR`).
2. **Oʻzbek Kirill alifbosi:**
   - `shanba` $\rightarrow$ `шанба`, `shabnam` $\rightarrow$ `шабнам`, `o'zbek` $\rightarrow$ `ўзбек`, `bog'` $\rightarrow$ `боғ`
   - Soʻz boshida `e` $\rightarrow$ `э`, undoshdan keyin `e` $\rightarrow$ `е`, `s'h` $\rightarrow$ `сҳ` (`Is'hoq` $\rightarrow$ `Исҳоқ`), tutuq belgilari `’` $\rightarrow$ `ъ` (`ma'no` $\rightarrow$ `маъно`).
3. **Amaldagi Lotin alifbosi (1995):**
   - Kirill yoki Yangi Lotindagi matnni standart Lotin (`sh`, `ch`, `oʻ`, `gʻ`) formatiga qaytarish.
4. **Oʻchirilgan (Bypass) rejim:**
   - Inglizcha matn yoki kod yozayotganda avto-almashtirishni vaqtincha toʻxtatish.
5. **Pastki Qatordagi Professional Panel (Taskbar Dock Panel):**
   - Ekranning oʻrtasida xalal bermaydi, pastki qatorda (Taskbar ustida, soat va til indikatori yonida) ixcham va chiroyli turadi.
   - Ixchamlashtirish imkoniyati: mini-kapsula rejimiga oʻtkazish mumkin.
   - Windows 11 Fluent Design talablariga mos zamonaviy quyuq (dark) interfeys.
6. **Koʻp tilli interfeys (UZ / RU / EN):**
   - Dastur toʻliq 3 ta tilda ishlaydi: **Oʻzbekcha**, **Русский**, **English**.
   - Paneldagi `[🌐 UZ]`, Sozlamalar oynasi yoki Tray menyusi orqali bir bosishda tilni almashtirish mumkin.
7. **GitHub orqali Avtomatik Yangilanish Tizimi (Auto-Updater):**
   - Dastur fonda GitHub releases orqali yangi versiyalarni tekshirib boradi.
   - Yangi versiya chiqqanda ekranning burchagida majburiy yangilanish oynasi paydo boʻladi va yangilanmaguncha matn oʻgirish toʻxtatiladi.
   - Bir tugma bilan avtomatik yangi versiyani yuklab olib oʻrnatadi.
8. **Dinamik Tizim Tepsisi (System Tray):**
   - Pastdagi Taskbar burchagida qaysi alifbo faolligiga qarab **`Ö`**, **`Ў`**, **`Oʻ`**, **`OFF`** (va yangilanish kerak boʻlsa **`!`**) belgilari aniq koʻrinib turadi.
9. **Tezkor klavishlar (Hotkeys):**
   - **`F8`** yoki **`Ctrl + Shift + U`** — sichqonchaga tegmasdan turib alifbo rejimini klaviaturaning oʻzidan zumda almashtirish.

---

## 🚀 Oʻrnatish (Cross-Platform Installers)

Barcha platformalar uchun tayyor oʻrnatuvchi fayllar **`I:\translate\installer_output`** papkasida joylashgan:

### 1. 🪟 Windows (10 / 11)
📁 Fayl: **`NamDPI_Alifbo_Setup.exe`**
- Faylni ishga tushiring va «Oʻrnatish» tugmasini bosing.
- Ish stolida va Bosh menyuda (Start Menu) **"NamDPI alifbo"** yorligʻi paydo boʻladi.
- Kompyuter yoqilganda avtomatik ishga tushadi.

---

### 2. 🐧 Linux (Ubuntu, Debian, Linux Mint, Fedora, Arch)
📁 Fayllar:
- **`NamDPI_Alifbo_Linux_Ubuntu_Debian.deb`** — Ubuntu/Debian uchun (.deb paket)
  ```bash
  sudo dpkg -i NamDPI_Alifbo_Linux_Ubuntu_Debian.deb
  sudo apt-get install -f   # Agar qo'shimcha paketlar kerak bo'lsa
  ```
- **`NamDPI_Alifbo_Linux_Universal.tar.gz`** — Barcha Linux distributivlari uchun
  ```bash
  tar -xzf NamDPI_Alifbo_Linux_Universal.tar.gz
  cd NamDPI_Alifbo_Linux
  sudo ./install.sh
  ```
- Tizim menyusida dastur paydo boʻladi va avtomatik ishga tushish sozlangan.

---

### 3. 🍏 macOS (Apple Silicon M1/M2/M3 & Intel)
📁 Fayllar:
- **`NamDPI_Alifbo_macOS.zip`** (ichida `NamDPI alifbo.app` va `NamDPI_Alifbo_macOS_Installer.command`)
- **`NamDPI_Alifbo_macOS_Installer.command`** (Mustaqil 1-klikli oʻrnatuvchi)
  - Arxivni oching va **`NamDPI_Alifbo_macOS_Installer.command`** faylini ikki marta bosing.
  - Yoki `NamDPI alifbo.app` ilovasini `/Applications` papkasiga koʻchiring.
  - Tizim sozlamalarida (`System Settings` $\rightarrow$ `Privacy & Security` $\rightarrow$ `Accessibility`) klaviatura ruxsatini yoqing.
