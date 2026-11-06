# -*- coding: utf-8 -*-
"""
O'zbek alifbosi transliterator moduli.
Namangan davlat pedagogika instituti
Raqamli ta'lim texnologiyalari markazi (NDPI RTTM)
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
    return len(word) > 1 and word.isupper()

def latin_to_cyrillic(text: str) -> str:
    """Lotin yozuvidan O'zbek Kirill yozuviga o'giradi."""
    if not text:
        return text

    # Maxsus holatlar (s'h -> сҳ)
    res = text
    # s'h, sʻh -> сҳ
    for apo in APOSTROPHES:
        res = re.sub(f's{apo}h', 'сҳ', res, flags=re.IGNORECASE)
        res = re.sub(f'S{apo}h', 'Сҳ', res)
        res = re.sub(f'S{apo}H', 'СҲ', res)

    # Qo'sh harflar va maxsus birikmalar (katta/kichik harflar inobatga olingan)
    compound_rules = [
        # Yangi harflar (ö, ğ, ş, ç)
        ('ö', 'ў'), ('Ö', 'Ў'),
        ('ğ', 'ғ'), ('Ğ', 'Ғ'),
        ('ş', 'ш'), ('Ş', 'Ш'),
        ('ç', 'ч'), ('Ç', 'Ч'),
        
        # Eski harf birikmalari (o', g', sh, ch, yo, yu, ya, ye, ts)
        ('sh', 'ш'), ('Sh', 'Ш'), ('SH', 'Ш'),
        ('ch', 'ч'), ('Ch', 'Ч'), ('CH', 'Ч'),
        ('yo', 'ё'), ('Yo', 'Ё'), ('YO', 'Ё'),
        ('yu', 'ю'), ('Yu', 'Ю'), ('YU', 'Ю'),
        ('ya', 'я'), ('Ya', 'Я'), ('YA', 'Я'),
        ('ye', 'е'), ('Ye', 'Е'), ('YE', 'Е'),
        ('ts', 'ц'), ('Ts', 'Ц'), ('TS', 'Ц'),
    ]

    # oʻ, gʻ variantlari
    for apo in APOSTROPHES:
        compound_rules.extend([
            (f'o{apo}', 'ў'), (f'O{apo}', 'Ў'),
            (f'g{apo}', 'ғ'), (f'G{apo}', 'Ғ'),
        ])

    # Harflar bosqichma-bosqich almashtirish
    # So'z boshidagi 'e' / 'E' va unlilardan keyingi 'e' -> 'э'/'Э'
    # Boshqa o'rinlardagi 'e' -> 'е'
    # Buni so'zlar bo'yicha yoki belgi bo'yicha aniqlash:
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
        
        # Word processing
        cur = w
        # 1. compound replacements first
        for pat, rep in compound_rules:
            cur = cur.replace(pat, rep)

        # 2. handle 'e' / 'E'
        # Check positions of 'e' / 'E'
        chars = list(cur)
        for i, ch in enumerate(chars):
            if ch in ('e', 'E'):
                is_cap = (ch == 'E')
                if i == 0:
                    # So'z boshida -> 'э' / 'Э'
                    chars[i] = 'Э' if is_cap else 'э'
                else:
                    prev_char = chars[i-1]
                    # Agar oldingi belgi unli bo'lsa -> 'э' / 'Э'
                    if prev_char.lower() in ('a', 'o', 'u', 'i', 'ў', 'ö', 'а', 'о', 'у', 'и', 'э'):
                        chars[i] = 'Э' if is_cap else 'э'
                    else:
                        chars[i] = 'Е' if is_cap else 'е'
        cur = "".join(chars)

        # 3. single letter replacements
        res_chars = []
        for ch in cur:
            if ch in single_map:
                res_chars.append(single_map[ch])
            elif ch in APOSTROPHES:
                res_chars.append('ъ')
            else:
                res_chars.append(ch)
        
        w_converted = "".join(res_chars)

        # Butun so'z katta harflarda yozilgan bo'lsa
        if is_all_upper(w):
            w_converted = w_converted.upper()

        converted_words.append(w_converted)

    return "".join(converted_words)


def latin_to_new_latin(text: str) -> str:
    """Standart Lotin yoki Kirill yozuvidan Yangi O'zbek Lotiniga o'giradi (Ö, Ğ, Ş, Ç)."""
    if not text:
        return text

    # Agar matn Kirill bo'lsa, avval Kirilldan yangi lotinga o'girish qoidalari
    # Agar matn Lotin bo'lsa, sh -> ş, ch -> ç, o' -> ö, g' -> ğ
    res = text

    # 1. Standart Lotin birikmalarini Yangi Lotinga almashtirish:
    # sh -> ş
    res = re.sub(r'SH\b', 'Ş', res)
    res = res.replace('SH', 'Ş').replace('Sh', 'Ş').replace('sh', 'ş')
    # ch -> ç
    res = res.replace('CH', 'Ç').replace('Ch', 'Ç').replace('ch', 'ç')
    
    # oʻ, gʻ
    for apo in APOSTROPHES:
        res = res.replace(f'o{apo}', 'ö').replace(f'O{apo}', 'Ö')
        res = res.replace(f'g{apo}', 'ğ').replace(f'G{apo}', 'Ğ')

    # 2. Agar matnda Kirill harflari bo'lsa:
    cyr_to_new = {
        'ш': 'ş', 'Ш': 'Ş',
        'ч': 'ç', 'Ч': 'Ç',
        'ў': 'ö', 'Ў': 'Ö',
        'ғ': 'ğ', 'Ғ': 'Ğ',
        'қ': 'q', 'Қ': 'Q',
        'ҳ': 'h', 'Ҳ': 'H',
        'х': 'x', 'Х': 'X',
        'ж': 'j', 'Ж': 'J',
        'ц': 'ts', 'Ц': 'Ts',
        'ё': 'yo', 'Ё': 'Yo',
        'ю': 'yu', 'Ю': 'Yu',
        'я': 'ya', 'Я': 'Ya',
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

    # Kirill 'е' holati: so'z boshida yoki unlidan keyin 'ye', undoshdan keyin 'e'
    chars = list(res)
    for i, ch in enumerate(chars):
        if ch in ('е', 'Е'):
            is_cap = (ch == 'Е')
            if i == 0 or chars[i-1] in ' \t\n\r"\'([{-':
                chars[i] = 'Ye' if is_cap else 'ye'
            elif chars[i-1].lower() in VOWELS_CYRILLIC:
                chars[i] = 'Ye' if is_cap else 'ye'
            else:
                chars[i] = 'E' if is_cap else 'e'
        elif ch in cyr_to_new:
            chars[i] = cyr_to_new[ch]

    res = "".join(chars)
    return res


def cyrillic_to_latin(text: str) -> str:
    """Kirill yozuvidan Standart 1995 O'zbek Lotiniga o'giradi."""
    if not text:
        return text

    cyr_to_lat = {
        'ш': 'sh', 'Ш': 'Sh',
        'ч': 'ch', 'Ч': 'Ch',
        'ў': 'oʻ', 'Ў': 'Oʻ',
        'ғ': 'gʻ', 'Ғ': 'Gʻ',
        'қ': 'q', 'Қ': 'Q',
        'ҳ': 'h', 'Ҳ': 'H',
        'х': 'x', 'Х': 'X',
        'ж': 'j', 'Ж': 'J',
        'ц': 'ts', 'Ц': 'Ts',
        'ё': 'yo', 'Ё': 'Yo',
        'ю': 'yu', 'Ю': 'Yu',
        'я': 'ya', 'Я': 'Ya',
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
        'ş': 'sh', 'Ş': 'Sh',
        'ç': 'ch', 'Ç': 'Ch',
    }

    chars = list(text)
    for i, ch in enumerate(chars):
        if ch in ('е', 'Е'):
            is_cap = (ch == 'Е')
            if i == 0 or chars[i-1] in ' \t\n\r"\'([{-':
                chars[i] = 'Ye' if is_cap else 'ye'
            elif chars[i-1].lower() in VOWELS_CYRILLIC:
                chars[i] = 'Ye' if is_cap else 'ye'
            else:
                chars[i] = 'E' if is_cap else 'e'
        elif ch in cyr_to_lat:
            chars[i] = cyr_to_lat[ch]

    return "".join(chars)


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


if __name__ == '__main__':
    import sys
    sys.stdout.reconfigure(encoding='utf-8')
    # Test cases
    test_words = [
        "shanba", "Shanba", "SHANBA",
        "choy", "Choy", "CHOY",
        "o'zbekiston", "O'zbekiston", "Oʻzbekiston",
        "bog'", "Bog'", "G'alaba", "g'alaba",
        "eshik", "keldi", "aeroport",
        "ma'no", "she'r", "mas'ul", "Is'hoq"
    ]
    print("--- KRILGA O'GIRISH TESTLARI ---")
    for w in test_words:
        print(f"{w:15} -> {convert_word(w, 'kril')}")

    print("\n--- YANGI LOTINGA O'GIRISH TESTLARI ---")
    for w in test_words:
        print(f"{w:15} -> {convert_word(w, 'yangi')}")
