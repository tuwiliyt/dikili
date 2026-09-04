#!/usr/bin/env python3
import json
import re

def is_chunk_reversed(chunk):
    chunk = chunk.strip()
    if not chunk: return False
    words = chunk.split()
    score = 0
    for w in words:
        if w == 'ىف': score += 2
        if w == 'ىلع': score += 2
        if w == 'نم': score += 1
        if w == 'هللا': score += 3
        if w == 'دمحم': score += 3
        if w == 'ّيبنلا': score += 2
        if w.startswith('ة'): score += 2
        if w.endswith('لا') and len(w) >= 4: score += 1
        
        if w == 'فى': score -= 2
        if w == 'على': score -= 2
        if w == 'من': score -= 1
        if w in ('الله', 'ﷲ'): score -= 2
        if w == 'محمد': score -= 2
        if w == 'النبي': score -= 2
        if w.endswith('ة'): score -= 2
        if w.startswith('ال'): score -= 1
    
    return score > 0

def fix_line(line):
    parts = re.split(r'([٭\*])', line)
    fixed = []
    for p in parts:
        if p in ('٭', '*'):
            fixed.append(p)
        else:
            if is_chunk_reversed(p):
                fixed.append(p[::-1])
            else:
                fixed.append(p)
    return ''.join(fixed)

def main():
    with open('/content/dikili/app/dikili_final.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    changes = 0
    for sair in data['sairs']:
        for block in sair['blocks']:
            if block['type'] == 'arabic':
                new_lines = []
                for line in block['text'].split('\n'):
                    fixed_line = fix_line(line)
                    if fixed_line != line:
                        changes += 1
                    new_lines.append(fixed_line)
                block['text'] = '\n'.join(new_lines)

    print(f'Fixed {changes} reversed Arabic lines.')
    
    with open('/content/dikili/app/dikili_final.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

if __name__ == '__main__':
    main()
