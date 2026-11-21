# -*- coding: utf-8 -*-
"""
O'zbek alifbosi transliterator moduli.
Namangan davlat pedagogika instituti
Raqamli ta'lim texnologiyalari markazi (NamDPI RTTM)
"""

import re

# Standart tutuq belgilari va apostroflar
APOSTROPHES = ["'", "ʻ", "ʼ", "`", "‘", "’", "ʼ", "ʻ"]
APO_REGEX = "[" + "".join(APOSTROPHES) + "]"

VOWELS_LATIN = set("aeiouAEIOUöÖ")
VOWELS_CYRILLIC = set("аеёиоуэюяўАЕЁИОУЭЮЯЎ")

def is_upper_first(word: str) -> bool:
    return len(word) > 0 and word[0].isupper()

def is_all_upper(word: str) -> bool:
    letters = [ch for ch in word if ch.isalpha()]
    return len(letters) > 1 and all(ch.isupper() for ch in letters)

def latin_to_cyrillic(text: str) -> str:
    """Lotin yoki Yangi Lotin yozuvidan O'zbek Kirill yozuviga o'giradi."""
    if not text:
        return text

    # Maxsus holatlar: Is'hoq / s'h -> сҳ
    res = text
    for apo in APOSTROPHES:
        res = res.replace(f"S{apo}H", 'СҲ')
        res = res.replace(f"S{apo}h", 'Сҳ')
        res = res.replace(f"s{apo}h", 'сҳ')

    # Qo'sh harflar va maxsus birikmalar
    compound_rules = [
        # Yangi harflar (ö, ğ, ş, ç)
        ('ö', 'ў'), ('Ö', 'Ў'),
        ('ğ', 'ғ'), ('Ğ', 'Ғ'),
        ('ş', 'ш'), ('Ş', 'Ш'),
        ('ç', 'ч'), ('Ç', 'Ч'),
        
        # Standart harf birikmalari
        ('sh', 'ш'), ('Sh', 'Ш'), ('SH', 'Ш'),
        ('ch', 'ч'), ('Ch', 'Ч'), ('CH', 'Ч'),
        ('yo', 'ё'), ('Yo', 'Ё'), ('YO', 'Ё'),
        ('yu', 'ю'), ('Yu', 'Ю'), ('YU', 'Ю'),
        ('ya', 'я'), ('Ya', 'Я'), ('YA', 'Я'),
        ('ye', 'е'), ('Ye', 'Е'), ('YE', 'Е'),
        ('ts', 'ц'), ('Ts', 'Ц'), ('TS', 'Ц'),
    ]

    for apo in APOSTROPHES:
        compound_rules.extend([
            (f'o{apo}', 'ў'), (f'O{apo}', 'Ў'),
            (f'g{apo}', 'ғ'), (f'G{apo}', 'Ғ'),
        ])

    words = re.split(r'(\s+|[^\wʻʼ\'`‘’]+)', res)
    converted_words = []

    single_map = {
        'a': 'а', 'A': 'А',
        'b': 'б', 'B': 'Б',
        'd': 'д', 'D': 'Д',
        'f': 'ф', 'F': 'Ф',
        'g': 'г', 'G': 'Г',
        'h': 'ҳ', 'H': 'Ҳ',
        'i': 'и', 'I': 'И',
        'j': 'ж', 'J': 'Ж',
        'k': 'к', 'K': 'К',
        'l': 'л', 'L': 'Л',
        'm': 'м', 'M': 'М',
        'n': 'н', 'N': 'Н',
        'o': 'о', 'O': 'О',
        'p': 'п', 'P': 'П',
        'q': 'қ', 'Q': 'Қ',
        'r': 'р', 'R': 'Р',
        's': 'с', 'S': 'С',
        't': 'т', 'T': 'Т',
        'u': 'у', 'U': 'У',
        'v': 'в', 'V': 'В',
        'x': 'х', 'X': 'Х',
        'y': 'й', 'Y': 'Й',
        'z': 'з', 'Z': 'З',
    }

    for w in words:
        if not w or re.match(r'^\s+$', w) or re.match(r'^[^\wʻʼ\'`‘’]+$', w):
            converted_words.append(w)
            continue
        
        cur = w
        for pat, rep in compound_rules:
            cur = cur.replace(pat, rep)

        chars = list(cur)
        for i, ch in enumerate(chars):
            if ch in ('e', 'E'):
                is_cap = (ch == 'E')
                if i == 0:
                    chars[i] = 'Э' if is_cap else 'э'
                else:
                    prev_char = chars[i-1]
                    if prev_char.lower() in ('a', 'o', 'u', 'i', 'ў', 'ö', 'а', 'о', 'у', 'и', 'э'):
                        chars[i] = 'Э' if is_cap else 'э'
                    else:
                        chars[i] = 'Е' if is_cap else 'е'
        cur = "".join(chars)

        res_chars = []
        for ch in cur:
            if ch in single_map:
                res_chars.append(single_map[ch])
            elif ch in APOSTROPHES:
                res_chars.append('ъ')
            else:
                res_chars.append(ch)
        
        w_converted = "".join(res_chars)
        if is_all_upper(w):
            w_converted = w_converted.upper()

        converted_words.append(w_converted)

    return "".join(converted_words)


def latin_to_new_latin(text: str) -> str:
    """Standart Lotin yoki Kirill yozuvidan Yangi O'zbek Lotiniga o'giradi (Ö, Ğ, Ş, Ç)."""
    if not text:
        return text

    all_upper = is_all_upper(text)
    res = text

    # Maxsus holat: Is'hoq / Исҳоқ -> s'h ni saqlash (Ishoq/Işoq bo'lib ketmasligi uchun)
    res = res.replace('СҲ', "S'H").replace('Сҳ', "S'h").replace('сҳ', "s'h")

    # 1. Standart Lotin birikmalarini Yangi Lotinga almashtirish:
    res = res.replace('SH', 'Ş').replace('Sh', 'Ş').replace('sh', 'ş')
    res = res.replace('CH', 'Ç').replace('Ch', 'Ç').replace('ch', 'ç')
    
    for apo in APOSTROPHES:
        res = res.replace(f'o{apo}', 'ö').replace(f'O{apo}', 'Ö')
        res = res.replace(f'g{apo}', 'ğ').replace(f'G{apo}', 'Ğ')

    # 2. Kirill harflarini Yangi Lotinga almashtirish:
    cyr_to_new = {
        'ш': 'ş', 'Ш': 'Ş',
        'ч': 'ç', 'Ч': 'Ç',
        'ў': 'ö', 'Ў': 'Ö',
        'ғ': 'ğ', 'Ғ': 'Ğ',
        'қ': 'q', 'Қ': 'Q',
        'ҳ': 'h', 'Ҳ': 'H',
        'х': 'x', 'Х': 'X',
        'ж': 'j', 'Ж': 'J',
        'ц': 'ts', 'Ц': 'TS' if all_upper else 'Ts',
        'ё': 'yo', 'Ё': 'YO' if all_upper else 'Yo',
        'ю': 'yu', 'Ю': 'YU' if all_upper else 'Yu',
        'я': 'ya', 'Я': 'YA' if all_upper else 'Ya',
        'щ': 'ş', 'Щ': 'Ş',
        'ы': 'i', 'Ы': 'I',
        'э': 'e', 'Э': 'E',
        'а': 'a', 'А': 'A',
        'б': 'b', 'Б': 'B',
        'в': 'v', 'В': 'V',
        'г': 'g', 'Г': 'G',
        'д': 'd', 'Д': 'D',
        'з': 'z', 'З': 'Z',
        'и': 'i', 'И': 'I',
        'й': 'y', 'Й': 'Y',
        'к': 'k', 'К': 'K',
        'л': 'l', 'Л': 'L',
        'м': 'm', 'М': 'M',
        'н': 'n', 'Н': 'N',
        'о': 'o', 'О': 'O',
        'п': 'p', 'П': 'P',
        'р': 'r', 'Р': 'R',
        'с': 's', 'С': 'S',
        'т': 't', 'Т': 'T',
        'у': 'u', 'У': 'U',
        'ф': 'f', 'Ф': 'F',
        'ъ': 'ʼ', 'Ъ': 'ʼ',
        'ь': '', 'Ь': '',
    }

    chars = list(res)
    for i, ch in enumerate(chars):
        if ch in ('е', 'Е'):
            is_cap = (ch == 'Е')
            if is_cap and all_upper:
                ye_val, e_val = 'YE', 'E'
            elif is_cap:
                ye_val, e_val = 'Ye', 'E'
            else:
                ye_val, e_val = 'ye', 'e'

            if i == 0 or chars[i-1] in ' \t\n\r"\'([{-':
                chars[i] = ye_val
            elif chars[i-1].lower() in VOWELS_CYRILLIC:
                chars[i] = ye_val
            else:
                chars[i] = e_val
        elif ch in cyr_to_new:
            chars[i] = cyr_to_new[ch]

    res = "".join(chars)

    if all_upper:
        res = res.upper()

    return res


def cyrillic_to_latin(text: str) -> str:
    """Kirill yoki Yangi Lotin yozuvidan Standart 1995 O'zbek Lotiniga o'giradi."""
    if not text:
        return text

    all_upper = is_all_upper(text)
    res = text

    # Maxsus holat: Is'hoq / Исҳоқ -> Ishoq bo'lib ketmasligi uchun
    res = res.replace('СҲ', "S'H").replace('Сҳ', "S'h").replace('сҳ', "s'h")

    sh_val = 'SH' if all_upper else 'Sh'
    ch_val = 'CH' if all_upper else 'Ch'
    yo_val = 'YO' if all_upper else 'Yo'
    yu_val = 'YU' if all_upper else 'Yu'
    ya_val = 'YA' if all_upper else 'Ya'
    ts_val = 'TS' if all_upper else 'Ts'

    cyr_to_lat = {
        'ш': 'sh', 'Ш': sh_val,
        'ч': 'ch', 'Ч': ch_val,
        'ў': 'oʻ', 'Ў': 'Oʻ',
        'ғ': 'gʻ', 'Ғ': 'Gʻ',
        'қ': 'q', 'Қ': 'Q',
        'ҳ': 'h', 'Ҳ': 'H',
        'х': 'x', 'Х': 'X',
        'ж': 'j', 'Ж': 'J',
        'ц': 'ts', 'Ц': ts_val,
        'ё': 'yo', 'Ё': yo_val,
        'ю': 'yu', 'Ю': yu_val,
        'я': 'ya', 'Я': ya_val,
        'щ': 'sh', 'Щ': sh_val,
        'ы': 'i', 'Ы': 'I',
        'э': 'e', 'Э': 'E',
        'а': 'a', 'А': 'A',
        'б': 'b', 'Б': 'B',
        'в': 'v', 'В': 'V',
        'г': 'g', 'Г': 'G',
        'д': 'd', 'Д': 'D',
        'з': 'z', 'З': 'Z',
        'и': 'i', 'И': 'I',
        'й': 'y', 'Й': 'Y',
        'к': 'k', 'К': 'K',
        'л': 'l', 'Л': 'L',
        'м': 'm', 'М': 'M',
        'н': 'n', 'Н': 'N',
        'о': 'o', 'О': 'O',
        'п': 'p', 'П': 'P',
        'р': 'r', 'Р': 'R',
        'с': 's', 'С': 'S',
        'т': 't', 'Т': 'T',
        'у': 'u', 'У': 'U',
        'ф': 'f', 'Ф': 'F',
        'ъ': 'ʼ', 'Ъ': 'ʼ',
        'ь': '', 'Ь': '',
        # Yangi lotin harflaridan qaytarish
        'ö': 'oʻ', 'Ö': 'Oʻ',
        'ğ': 'gʻ', 'Ğ': 'Gʻ',
        'ş': 'sh', 'Ş': sh_val,
        'ç': 'ch', 'Ç': ch_val,
    }

    chars = list(res)
    for i, ch in enumerate(chars):
        if ch in ('е', 'Е'):
            is_cap = (ch == 'Е')
            if is_cap and all_upper:
                ye_val, e_val = 'YE', 'E'
            elif is_cap:
                ye_val, e_val = 'Ye', 'E'
            else:
                ye_val, e_val = 'ye', 'e'

            if i == 0 or chars[i-1] in ' \t\n\r"\'([{-':
                chars[i] = ye_val
            elif chars[i-1].lower() in VOWELS_CYRILLIC:
                chars[i] = ye_val
            else:
                chars[i] = e_val
        elif ch in cyr_to_lat:
            chars[i] = cyr_to_lat[ch]

    res = "".join(chars)

    if all_upper:
        res = res.upper()

    return res


def convert_word(word: str, mode: str) -> str:
    """
    mode:
      - 'kril': Lotin/Yangi -> O'zbek Kirill
      - 'yangi': Lotin/Kirill -> O'zbek Yangi Lotin (ö, ğ, ş, ç)
      - 'lotin': Kirill/Yangi -> O'zbek Amaldagi Lotin (oʻ, gʻ, sh, ch)
      - 'off': O'zgarishsiz
    """
    if mode == 'kril':
        return latin_to_cyrillic(word)
    elif mode == 'yangi':
        return latin_to_new_latin(word)
    elif mode == 'lotin':
        return cyrillic_to_latin(word)
    return word
