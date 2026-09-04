import json
import re

# We will run parse_sairs to get a fresh start, then apply the safe logic
import os
os.system('python3 parse_sairs.py')

with open('/content/dikili/repo/dikili_final.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 1. Fix Arabic Reversals
from fix_arabic import is_chunk_reversed, fix_line
for sair in data['sairs']:
    for block in sair['blocks']:
        if block['type'] == 'arabic':
            lines = block['text'].split('\n')
            new_lines = []
            for line in lines:
                new_lines.append(fix_line(line))
            block['text'] = '\n'.join(new_lines)
            
            # Also fix specific known unhandled ones like Isa Ruhullah
            block['text'] = block['text'].replace('ﷲ حورو ىسيع', 'عيسى وروح ﷲ')

# 2. Fix Quranic block (Al-Fath)
for i, block in enumerate(data['sairs'][0]['blocks']):
    if block['type'] == 'arabic' and 'الفتح' in block['text']:
        block['text'] = "بسم ﷲ الرحمن الرحيم\nإِنَّا فَتَحْنَا لَكَ فَتْحًا مُّبِينًا * لِّيَغْفِرَ لَكَ اللَّهُ مَا تَقَدَّمَ مِن ذَنبِكَ وَمَا تَأَخَّرَ وَيُتِمَّ نِعْمَتَهُ عَلَيْكَ وَيَهْدِيَكَ صِرَاطًا مُّسْتَقِيمًا * وَيَنصُرَكَ اللَّهُ نَصْرًا عَزِيزًا * (سورة الفتح : 1 - 3)\nلَقَدْ جَاءَكُمْ رَسُولٌ مِّنْ أَنفُسِكُمْ عَزِيزٌ عَلَيْهِ مَا عَنِتُّمْ حَرِيصٌ عَلَيْكُم بِالْمُؤْمِنِينَ رَءُوفٌ رَّحِيمٌ * فَإِن تَوَلَّوْا فَقُلْ حَسْبِيَ اللَّهُ لَا إِلَٰهَ إِلَّا هُوَ عَلَيْهِ تَوَكَّلْتُ وَهُوَ رَبُّ الْعَرْشِ الْعَظِيمِ * (سورة التوبة : 128 - 129)"

# 3. Strip stray Latin from Arabic
for sair in data['sairs']:
    for block in sair['blocks']:
        if block['type'] == 'arabic':
            lines = block['text'].split('\n')
            new_lines = []
            for line in lines:
                match_start = re.match(r'^([a-zA-Zāīūṣḍṭżẓḥŝ\s\’\'\-\,]+)', line)
                if match_start and len(match_start.group(1).strip()) > 2:
                    line = line[match_start.end():].strip(' *٭')
                
                match_end = re.search(r'([a-zA-Zāīūṣḍṭżẓḥŝ\s\’\'\-\,]+)$', line)
                if match_end and len(match_end.group(1).strip()) > 2:
                    line = line[:match_end.start()].strip(' *٭')
                
                new_lines.append(line)
            block['text'] = '\n'.join(new_lines)
            
# specific translit fix for Sair 1 block 2 ('alaih)
if data['sairs'][0]['blocks'][2]['text'] == 'Allāhumma ṣalli wa sallim wa bārik':
    data['sairs'][0]['blocks'][2]['text'] = "Allāhumma ṣalli wa sallim wa bārik 'alaih"


# 4. Fix Footnotes
for sair in data['sairs']:
    merged_blocks = []
    i = 0
    blocks = sair['blocks']
    while i < len(blocks):
        current = blocks[i]
        if current['type'] == 'footnote':
            j = i + 1
            while j < len(blocks) and blocks[j]['type'] == 'text':
                text = blocks[j]['text'].strip()
                if re.match(r'^[a-q]\.\s+Sair', text, re.IGNORECASE) or text.startswith('3. Doa'):
                    break
                current['text'] += ' ' + text
                j += 1
            merged_blocks.append(current)
            i = j
        else:
            merged_blocks.append(current)
            i += 1
    sair['blocks'] = merged_blocks


# 5. SAFE Fix for Translation Fragmentation
# We iterate over the blocks. If a block starts a translation (e.g., contains quotes, or is 'translation' type),
# we merge subsequent 'transliteration' and 'text' blocks ONLY IF they do not look like a completely different verse
# (e.g. they don't start with Arabic text, they are short or clearly part of the sentence).
# Actually, an even safer approach: ONLY merge 'text' and 'transliteration' blocks that don't contain Arabic
# and are sandwiched before the next 'arabic' or 'footnote' block.

for sair in data['sairs']:
    merged_blocks = []
    i = 0
    blocks = sair['blocks']
    while i < len(blocks):
        block = blocks[i]
        
        # Split mixed transliteration/translation
        if block['type'] == 'transliteration' and '"' in block['text']:
            idx = block['text'].find('"')
            tlit = block['text'][:idx].strip()
            tlat = block['text'][idx:].strip()
            if tlit:
                merged_blocks.append({'type': 'transliteration', 'text': tlit})
            block = {'type': 'translation', 'text': tlat}
        
        if block['type'] == 'translation':
            j = i + 1
            trans_text = block['text']
            while j < len(blocks):
                nb = blocks[j]
                
                # Never merge arabic or footnotes
                if nb['type'] in ('arabic', 'footnote'):
                    break
                    
                # If it's a Sair marker text
                if nb['type'] == 'text' and (re.match(r'^[a-q]\.\s+Sair', nb['text'], re.IGNORECASE) or nb['text'].startswith('3. Doa') or nb['text'].startswith('Catatan:')):
                    break
                
                # If it's a transliteration block, but actually it's just Indonesian with translit words
                # We can safely merge it because if it were a new transliteration stanza, it would usually
                # come AFTER an arabic block! Translations are always at the end of the stanza.
                
                # Wait, what if the NEXT stanza starts with Transliteration instead of Arabic?
                # In this manuscript, every stanza starts with Arabic.
                # So any text or translit block that follows a translation block (and before the next Arabic block)
                # is ALMOST CERTAINLY part of the translation!
                
                trans_text += '\n' + nb['text'].strip()
                j += 1
            
            # Clean up newlines in translation to make it a paragraph
            trans_text = trans_text.replace('\n', ' ').replace('  ', ' ')
            merged_blocks.append({'type': 'translation', 'text': trans_text})
            i = j
        else:
            merged_blocks.append(block)
            i += 1
            
    sair['blocks'] = merged_blocks

with open('/content/dikili/repo/dikili_final.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

