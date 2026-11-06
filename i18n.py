# -*- coding: utf-8 -*-
"""
NamDPI alifbo - Ko'p tillilik tizimi (i18n)
O'zbek tili (uz), Rus tili (ru), Ingliz tili (en)
Namangan davlat pedagogika instituti
Raqamli ta'lim texnologiyalari markazi (NamDPI RTTM)
"""

LANGUAGES = {
    "uz": "Oʻzbekcha",
    "ru": "Русский",
    "en": "English"
}

TRANSLATIONS = {
    "uz": {
        # Asosiy brend
        "app_title": "NamDPI alifbo",
        "org_name": "Namangan davlat pedagogika instituti",
        "dept_name": "Raqamli taʼlim texnologiyalari markazi (NamDPI RTTM)",
        
        # Rejimlar
        "mode_yangi": "Ö Yangi",
        "mode_kril": "Ў Кирилл",
        "mode_lotin": "Oʻ Lotin",
        "mode_off": "✕ Oʻchiq",
        
        # Tooltiplar va holatlar
        "hotkey_hint": "💡 Tezkor almashtirish: F8 yoki Ctrl + Shift + U",
        "locked_title": "⚠️ DIQQAT: YANGILANISH TALAB ETILADI",
        "locked_desc": "Dasturning yangi versiyasi chiqarilgan. Yangilanmaguncha matn oʻgirish toʻxtatilgan.",
        "locked_badge": "⚠️ Yangilang!",
        
        # Sozlamalar oynasi
        "settings_title": "NamDPI alifbo - Sozlamalar va Maʼlumot",
        "rules_heading": "✨ Yangi Oʻzbek Lotin alifbosi (2026):",
        "rules_content": (
            "  •  sh  ➔  ş    (masalan:  shabnam  ➔  şabnam)\n"
            "  •  ch  ➔  ç    (masalan:  choy  ➔  çoy)\n"
            "  •  oʻ, o'  ➔  ö  (masalan:  o'zbekiston  ➔  özbekiston)\n"
            "  •  gʻ, g'  ➔  ğ  (masalan:  bog'  ➔  boğ,  g'alaba  ➔  ğalaba)\n"
            "  •  Kirill  ➔  shanba  ➔  шанба,  shabnam  ➔  шабнам"
        ),
        "autostart_label": "Tizim bilan birga avtomatik ishga tushish",
        "opacity_label": "Panel shaffofligi:",
        "language_label": "Interfeys tili / Язык / Language:",
        "check_updates_btn": "Yangilanishlarni tekshirish",
        "close_btn": "Yopish",
        "exit_btn": "Dasturdan chiqish",
        
        # Tray menyusi
        "tray_toggle": "Panelni koʻrsatish / yashirish",
        "tray_mode_yangi": "Rejim: Yangi Lotin (Ö, Ğ, Ş, Ç)",
        "tray_mode_kril": "Rejim: Oʻzbek Kirill (Ў, Ғ, Ш, Ч)",
        "tray_mode_lotin": "Rejim: Amaldagi Lotin (Oʻ, Gʻ, Sh, Ch)",
        "tray_mode_off": "Rejim: Oʻchirilgan (Bypass)",
        "tray_language": "Til / Language / Язык",
        "tray_check_update": "Yangilanishlarni tekshirish",
        "tray_settings": "Sozlamalar...",
        "tray_exit": "Chiqish",
        
        # Yangilanish oynasi (Corner Notification)
        "update_available_title": "🚀 Yangi versiya mavjud!",
        "update_version_label": "Yangi versiya: {new_ver} (Hozirgi: {cur_ver})",
        "update_paused_warning": "⚠️ Dastur yangilanmaguncha uning faoliyati toʻxtatiladi!",
        "update_download_btn": "📥 Avtomatik yangilash",
        "update_browser_btn": "🌐 GitHub'dan yuklab olish",
        "update_downloading": "Yuklanmoqda: {percent}% ({received} / {total})",
        "update_launching": "Oʻrnatuvchi yuklandi. Ishga tushirilmoqda...",
        "update_error": "Yuklab olishda xatolik: {err}",
        "update_retry": "Qayta urinish",
        "update_up_to_date": "Sizda eng soʻnggi versiya oʻrnatilgan ({cur_ver}).",
        "update_check_failed": "Yangilanishlarni tekshirib boʻlmadi. Internet aloqasini tekshiring."
    },
    
    "ru": {
        # Основной бренд
        "app_title": "NamDPI alifbo",
        "org_name": "Наманганский государственный педагогический институт",
        "dept_name": "Центр цифровых образовательных технологий (ЦЦОТ НамГПИ)",
        
        # Режимы
        "mode_yangi": "Ö Новый",
        "mode_kril": "Ў Кирилл",
        "mode_lotin": "Oʻ Латиница",
        "mode_off": "✕ Выкл",
        
        # Подсказки и статусы
        "hotkey_hint": "💡 Быстрое переключение: F8 или Ctrl + Shift + U",
        "locked_title": "⚠️ ВНИМАНИЕ: ТРЕБУЕТСЯ ОБНОВЛЕНИЕ",
        "locked_desc": "Вышла новая версия программы. До обновления автотранслитерация приостановлена.",
        "locked_badge": "⚠️ Обновите!",
        
        # Окно настроек
        "settings_title": "NamDPI alifbo - Настройки и информация",
        "rules_heading": "✨ Новый узбекский латинский алфавит (2026):",
        "rules_content": (
            "  •  sh  ➔  ş    (например:  shabnam  ➔  şabnam)\n"
            "  •  ch  ➔  ç    (например:  choy  ➔  çoy)\n"
            "  •  oʻ, o'  ➔  ö  (например:  o'zbekiston  ➔  özbekiston)\n"
            "  •  gʻ, g'  ➔  ğ  (например:  bog'  ➔  boğ,  g'alaba  ➔  ğalaba)\n"
            "  •  Кириллица  ➔  shanba  ➔  шанба,  shabnam  ➔  шабнам"
        ),
        "autostart_label": "Автозапуск вместе с операционной системой",
        "opacity_label": "Прозрачность панели:",
        "language_label": "Язык интерфейса / Interfeys tili / Language:",
        "check_updates_btn": "Проверить обновления",
        "close_btn": "Закрыть",
        "exit_btn": "Выйти из программы",
        
        # Меню в трее
        "tray_toggle": "Показать / скрыть панель",
        "tray_mode_yangi": "Режим: Новая латиница (Ö, Ğ, Ş, Ç)",
        "tray_mode_kril": "Режим: Узбекская кириллица (Ў, Ғ, Ш, Ч)",
        "tray_mode_lotin": "Режим: Текущая латиница (Oʻ, Gʻ, Sh, Ch)",
        "tray_mode_off": "Режим: Отключено (Bypass)",
        "tray_language": "Язык / Til / Language",
        "tray_check_update": "Проверить обновления",
        "tray_settings": "Настройки...",
        "tray_exit": "Выход",
        
        # Окно обновления
        "update_available_title": "🚀 Доступно обновление!",
        "update_version_label": "Новая версия: {new_ver} (Текущая: {cur_ver})",
        "update_paused_warning": "⚠️ Работа программы приостановлена до установки обновления!",
        "update_download_btn": "📥 Автоматическое обновление",
        "update_browser_btn": "🌐 Скачать с GitHub",
        "update_downloading": "Загрузка: {percent}% ({received} / {total})",
        "update_launching": "Установщик загружен. Запуск...",
        "update_error": "Ошибка загрузки обновления: {err}",
        "update_retry": "Повторить",
        "update_up_to_date": "У вас установлена последняя версия ({cur_ver}).",
        "update_check_failed": "Не удалось проверить обновления. Проверьте подключение к сети."
    },
    
    "en": {
        # Brand
        "app_title": "NamDPI alifbo",
        "org_name": "Namangan State Pedagogical Institute",
        "dept_name": "Digital Educational Technologies Center (NamSPI DETC)",
        
        # Modes
        "mode_yangi": "Ö New",
        "mode_kril": "Ў Cyrillic",
        "mode_lotin": "Oʻ Latin",
        "mode_off": "✕ Off",
        
        # Tooltips & Statuses
        "hotkey_hint": "💡 Quick toggle: F8 or Ctrl + Shift + U",
        "locked_title": "⚠️ ATTENTION: UPDATE REQUIRED",
        "locked_desc": "A new version of the app is available. Transliteration is suspended until updated.",
        "locked_badge": "⚠️ Update!",
        
        # Settings Dialog
        "settings_title": "NamDPI alifbo - Settings & About",
        "rules_heading": "✨ New Uzbek Latin Alphabet (2026):",
        "rules_content": (
            "  •  sh  ➔  ş    (e.g.:  shabnam  ➔  şabnam)\n"
            "  •  ch  ➔  ç    (e.g.:  choy  ➔  çoy)\n"
            "  •  oʻ, o'  ➔  ö  (e.g.:  o'zbekiston  ➔  özbekiston)\n"
            "  •  gʻ, g'  ➔  ğ  (e.g.:  bog'  ➔  boğ,  g'alaba  ➔  ğalaba)\n"
            "  •  Cyrillic  ➔  shanba  ➔  шанба,  shabnam  ➔  шабнам"
        ),
        "autostart_label": "Start automatically with operating system",
        "opacity_label": "Panel opacity:",
        "language_label": "Interface language / Til / Язык:",
        "check_updates_btn": "Check for updates",
        "close_btn": "Close",
        "exit_btn": "Exit Application",
        
        # Tray Menu
        "tray_toggle": "Show / Hide Panel",
        "tray_mode_yangi": "Mode: New Latin (Ö, Ğ, Ş, Ç)",
        "tray_mode_kril": "Mode: Uzbek Cyrillic (Ў, Ғ, Ш, Ч)",
        "tray_mode_lotin": "Mode: Standard Latin (Oʻ, Gʻ, Sh, Ch)",
        "tray_mode_off": "Mode: Disabled (Bypass)",
        "tray_language": "Language / Til / Язык",
        "tray_check_update": "Check for Updates",
        "tray_settings": "Settings...",
        "tray_exit": "Exit",
        
        # Update Corner Notification
        "update_available_title": "🚀 New Update Available!",
        "update_version_label": "New version: {new_ver} (Current: {cur_ver})",
        "update_paused_warning": "⚠️ App functionality is suspended until updated!",
        "update_download_btn": "📥 Automatic Update",
        "update_browser_btn": "🌐 Download from GitHub",
        "update_downloading": "Downloading: {percent}% ({received} / {total})",
        "update_launching": "Download complete. Launching installer...",
        "update_error": "Download error: {err}",
        "update_retry": "Retry",
        "update_up_to_date": "You have the latest version ({cur_ver}).",
        "update_check_failed": "Failed to check for updates. Check your internet connection."
    }
}

CURRENT_LANGUAGE = "uz"

def set_language(lang_code: str):
    global CURRENT_LANGUAGE
    if lang_code in TRANSLATIONS:
        CURRENT_LANGUAGE = lang_code

def get_language() -> str:
    return CURRENT_LANGUAGE

def t(key: str, lang: str = None, **kwargs) -> str:
    """Tarjima matnini qaytaruvchi yordamchi funksiya."""
    use_lang = lang or CURRENT_LANGUAGE
    lang_dict = TRANSLATIONS.get(use_lang, TRANSLATIONS["uz"])
    template = lang_dict.get(key, TRANSLATIONS["uz"].get(key, key))
    if kwargs:
        try:
            return template.format(**kwargs)
        except Exception:
            return template
    return template
