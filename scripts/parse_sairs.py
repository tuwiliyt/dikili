#!/usr/bin/env python3
"""
Parse the Dikili manuscript text into structured Sair data.
Extract Arabic text, transliteration, translation, and jābu for each sair.
Source: Naskah D (Mustapa Taha) via Suntingan Teks (Edisi Kritis).
"""
import re
import json
import pypdf

PDF_PATH = '/content/dikili/KEARIFAN LOKAL DALAM NASKAH DIKILI.pdf'

def is_arabic_line(line):
    """Check if a line is predominantly Arabic."""
    arabic = sum(1 for c in line if '\u0600' <= c <= '\u06FF' or '\uFB50' <= c <= '\uFDFF' or '\uFE70' <= c <= '\uFEFF')
    return arabic > len(line.strip()) * 0.3 and arabic > 5

def has_translit_chars(line):
    """Check if line has transliteration diacritical marks."""
    return any(c in line for c in 'āīūṣḍṭżẓḥŝ')

def classify_line(line):
    """Classify a line of text into type."""
    s = line.strip()
    if not s:
        return 'empty', s
    
    if is_arabic_line(s):
        return 'arabic', s
    
    if has_translit_chars(s.lower()):
        # Could be transliteration or translation with translit words mixed in
        # If it starts with a quote or translation marker, it's translation
        if s.startswith('"') or s.startswith('"') or s.startswith("'"):
            return 'translation', s
        return 'transliteration', s
    
    # Check for footnote
    if re.match(r'^\d+[A-Z]', s) or re.match(r'^\d+\s*[A-Z]', s):
        return 'footnote', s
    
    # If in quotes, likely translation
    if s.startswith('"') or s.startswith('"') or s.startswith("'"):
        return 'translation', s
    
    return 'text', s

def extract_suntingan_text(reader):
    """Extract all text from Suntingan Teks section."""
    full_text = ""
    for pi in range(30, 94):  # PDF pages 31-94 (0-indexed)
        text = reader.pages[pi].extract_text()
        lines = text.strip().split('\n')
        cleaned = []
        for i, line in enumerate(lines):
            s = line.strip()
            # Skip page numbers
            if i == 0 and s.isdigit() and int(s) >= 27 and int(s) <= 92:
                continue
            cleaned.append(line)
        full_text += '\n'.join(cleaned) + '\n'
    return full_text

def parse_sairs(full_text):
    """Parse the full text into 17 sairs + doa."""
    lines = full_text.split('\n')
    
    # Define sair boundaries
    sair_starts = []
    for i, line in enumerate(lines):
        s = line.strip().lower()
        if re.match(r'^[a-q]\.\s+sair\s+(ke|pertama)', s):
            sair_starts.append(i)
        elif s.startswith('3. doa'):
            sair_starts.append(i)
    
    # Add end marker
    sair_starts.append(len(lines))
    
    sair_names = [
        "Sair Pertama",
        "Sair Kedua", 
        "Sair Ketiga",
        "Sair Keempat",
        "Sair Kelima",
        "Sair Keenam",
        "Sair Ketujuh",
        "Sair Kedelapan",
        "Sair Kesembilan",
        "Sair Kesepuluh",
        "Sair Kesebelas",
        "Sair Kedua Belas",
        "Sair Ketiga Belas",
        "Sair Keempat Belas",
        "Sair Kelima Belas",
        "Sair Keenam Belas",
        "Sair Ketujuh Belas",
        "Doa Khatmul Dikili"
    ]
    
    sairs = []
    for idx in range(len(sair_starts) - 1):
        start = sair_starts[idx]
        end = sair_starts[idx + 1] if idx + 1 < len(sair_starts) else len(lines)
        
        sair_lines = lines[start:end]
        sair_id = idx + 1 if idx < 17 else 'doa'
        name = sair_names[idx] if idx < len(sair_names) else f"Bagian {idx+1}"
        
        # Parse the sair content into blocks
        blocks = parse_sair_blocks(sair_lines, sair_id)
        
        sairs.append({
            'id': sair_id,
            'name': name,
            'blocks': blocks,
            'raw_line_count': len(sair_lines)
        })
    
    return sairs

def parse_sair_blocks(sair_lines, sair_id):
    """Parse lines of a sair into structured blocks."""
    blocks = []
    current_block = None
    
    for line in sair_lines:
        s = line.strip()
        if not s:
            if current_block:
                blocks.append(current_block)
                current_block = None
            continue
        
        line_type, content = classify_line(s)
        
        if line_type == 'arabic':
            if current_block and current_block['type'] == 'arabic':
                current_block['text'] += '\n' + content
            else:
                if current_block:
                    blocks.append(current_block)
                current_block = {'type': 'arabic', 'text': content}
        
        elif line_type == 'transliteration':
            if current_block and current_block['type'] == 'transliteration':
                current_block['text'] += '\n' + content
            else:
                if current_block:
                    blocks.append(current_block)
                current_block = {'type': 'transliteration', 'text': content}
        
        elif line_type == 'translation':
            if current_block and current_block['type'] == 'translation':
                current_block['text'] += '\n' + content
            else:
                if current_block:
                    blocks.append(current_block)
                current_block = {'type': 'translation', 'text': content}
        
        elif line_type == 'footnote':
            if current_block:
                blocks.append(current_block)
            blocks.append({'type': 'footnote', 'text': content})
            current_block = None
        
        else:  # text
            if current_block and current_block['type'] == 'text':
                current_block['text'] += '\n' + content
            else:
                if current_block:
                    blocks.append(current_block)
                current_block = {'type': 'text', 'text': content}
    
    if current_block:
        blocks.append(current_block)
    
    return blocks


def extract_kearifan_and_amanat(reader):
    """Extract D. Amanat section (book pages 92-97)."""
    sections = []
    for pi in range(94, 100):  # PDF pages 95-100
        text = reader.pages[pi].extract_text()
        lines = text.strip().split('\n')
        # Remove page number
        cleaned = []
        for i, line in enumerate(lines):
            s = line.strip()
            if i == 0 and s.isdigit():
                continue
            cleaned.append(s)
        sections.append('\n'.join(cleaned))
    return '\n\n'.join(sections)


def build_manuscripts():
    """Build manuscript descriptions - EXACT from document."""
    return [
        {
            "code": "A",
            "owner": "Hartati Mopangga",
            "pages": 117,
            "size": "21×16 cm",
            "lines_per_page": "15 baris",
            "colophon": "Ditulis 15-6-1986, penyalin: A.D. Laya, Kel. Huangobotu, Kec. Kota Barat, Kotamadya Gorontalo",
            "paper": "Kertas buku tulis bergaris",
            "ink": "Hitam dan merah (merah untuk basmalah, salawat, dan jābu)",
            "script": "Arab Pegon (sebagian bersyakal, sebagian tidak)",
            "quality": "Tulisan kurang bagus dan kurang rapi, banyak pemenggalan kata tidak sesuai kaidah",
            "content": "Sair-sair, jābu, hikayat Nabi Muhammad, doa. Terjemahan bahasa Indonesia dan Gorontalo (huruf Arab Pegon)",
            "notes": "Banyak kesalahan penulisan ayat Al-Quran (contoh: QS. Al-Fath ayat 2–3, QS. At-Taubah ayat 128–129)",
            "is_base": False
        },
        {
            "code": "B",
            "owner": "Hamu Ahmad",
            "pages": 121,
            "size": "15×10 cm",
            "lines_per_page": "9 baris",
            "colophon": "Tidak ada kolofon",
            "paper": "Kertas buatan Indonesia (dugaan era Orde Baru)",
            "ink": "Hitam dan merah",
            "script": "Arab Pegon",
            "quality": "Masih bisa dibaca, banyak pemenggalan kata tidak sesuai kaidah",
            "content": "Sair-sair, jābu, hikayat Nabi Muhammad, doa. Terjemahan hanya bahasa Gorontalo (tidak ada bahasa Indonesia)",
            "notes": "Banyak kesalahan penulisan ayat Al-Quran",
            "is_base": False
        },
        {
            "code": "C",
            "owner": "KH. Naha Akadji",
            "pages": 119,
            "size": "19×13 cm",
            "lines_per_page": "Bervariasi (5–15 baris)",
            "colophon": "7 Rabi'ul Awwal 1415 H / 16 Agustus 1994 (ditulis sendiri oleh pemilik)",
            "paper": "Buku tulis dibagi dua (fotokopi)",
            "ink": "Tidak disebutkan secara khusus",
            "script": "Huruf Latin (terjemahan Indonesia) dan Arab Pegon (terjemahan Gorontalo)",
            "quality": "Cukup rapi dan jelas, tidak banyak kesalahan",
            "content": "Sair-sair, jābu (lebih sedikit), hikayat Nabi Muhammad, doa",
            "notes": "Memiliki iluminasi: Basmalah berbentuk gambar itik, salawat berbentuk pesawat terbang",
            "is_base": False
        },
        {
            "code": "D",
            "owner": "Mustapa Taha",
            "pages": 188,
            "size": "20×14 cm",
            "lines_per_page": "Bervariasi (7–15 baris)",
            "colophon": "Dua kolofon: (1) huruf Latin — 1424 H/2003 M, Desa Bakti Pulubala; (2) huruf Arab Pegon — 1419 H/1999 M, Batu Layar",
            "paper": "Sair dan ayat Al-Quran = fotokopi dari sumber asli. Terjemahan dan jābu = tulisan tangan Arab Pegon",
            "ink": "Fotokopi dari sumber",
            "script": "Arab (fotokopi sumber asli) dan Arab Pegon (tulisan tangan untuk terjemahan dan jābu, bersyakal/bertanda baca)",
            "quality": "Fisik masih bagus, tulisan jelas, mudah dibaca. Jābu paling banyak dibanding naskah lain",
            "content": "Sair-sair, jābu (terbanyak), hikayat Nabi Muhammad, doa. Terjemahan bahasa Indonesia dan Gorontalo",
            "notes": "Dugaan penyalinan tahun 1999 M",
            "is_base": True,
            "base_rationale": [
                "Tulisannya jelas dan mudah dibaca",
                "Keadaan naskah masih baik dan utuh",
                "Sesuai dengan sumber dan fakta",
                "Isinya lengkap dan tidak menyimpang dari kebanyakan isi naskah lain"
            ]
        }
    ]


def build_kearifan():
    """Three forms of kearifan lokal from the document."""
    return [
        {
            "name": "Sisipan Jābu",
            "description": "Jābu adalah kata-kata atau kalimat puji-pujian terhadap Allah maupun Rasulullah, para sahabat, salawat, doa, syahadat, atau kalimat tayyibah yang disisipkan pada setiap sair. Merupakan ciptaan orang-orang tua dahulu atau penulis naskah. Dalam 17 sair terdapat 62 jābu.",
        },
        {
            "name": "Penulisan Huruf Arab Pegon",
            "description": "Naskah Dikili menggunakan huruf Arab Pegon (Arab Melayu) dengan adaptasi fonem: /ng/ = huruf ghain, /ny/ = huruf nun, /c/ = jim titik tiga (چ), /g/ = kaf. Keunikan: naskah Dikili tetap memakai harakat (syakal), termasuk untuk fonem /o/ dan /e/ yang dilambangkan dengan hamzah terbalik.",
        },
        {
            "name": "Penerjemahan Dwibahasa",
            "description": "Penerjemahan kisah-kisah Nabi Muhammad ke dalam bahasa Indonesia dan bahasa Gorontalo. Menariknya ada kisah yang hanya diterjemahkan ke bahasa Indonesia, dan ada yang hanya ke bahasa Gorontalo. Menggunakan kosakata lama yang sudah tidak dipahami generasi muda.",
        }
    ]


def main():
    reader = pypdf.PdfReader(PDF_PATH)
    
    # 1. Extract and parse suntingan text
    full_text = extract_suntingan_text(reader)
    sairs = parse_sairs(full_text)
    print(f"Parsed {len(sairs)} sairs")
    for s in sairs:
        print(f"  {s['name']}: {len(s['blocks'])} blocks, {s['raw_line_count']} lines")
    
    # 2. Build complete dataset
    data = {
        "info": {
            "title": "Naskah Dikili Gorontalo",
            "subtitle": "Edisi Kritis berdasarkan Naskah D (Mustapa Taha)",
            "authors": "Dr. Ayuba Pantu, M.Pd & Dr. H. Muh. Arif, M.Ag",
            "institution": "IAIN Sultan Amai Gorontalo",
            "year": 2015,
            "manuscript_base": "Naskah D milik Mustapa Taha (188 halaman, disalin ±1999 M)",
            "method": "Metode Landasan/Induk (Edisi Kritis)",
            "content_summary": "17 sair dikili dengan 62 sisipan jābu, hikayat Nabi Muhammad SAW, ayat Al-Quran, hadits, terjemahan bahasa Indonesia dan Gorontalo, serta doa khatmul dikili"
        },
        "sairs": sairs,
        "manuscripts": build_manuscripts(),
        "kearifan_lokal": build_kearifan()
    }
    
    output = '/content/dikili/repo/dikili_final.json'
    with open(output, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    
    import os
    print(f"\nWritten to {output}: {os.path.getsize(output):,} bytes")

if __name__ == '__main__':
    main()
