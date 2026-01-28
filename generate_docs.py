#!/usr/bin/env python3
"""
Generuje linki z BASE_PATH=/starlight/ + nazwa folderu w tytule
"""

import re
from datetime import datetime
from pathlib import Path

BASE_PATH = "/starlight"
DOCS_DIR = Path("src/content/docs")
INDEX_FILE = DOCS_DIR / "index.mdx"
SECTION_START = "## 📋 Wszystkie dokumenty"

def parse_doc_file(file_path):
    """Parsuje z nazwą folderu <8l."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    pub = re.search(r'pubDate:\s*"([^"]*)"', content)
    title = re.search(r'title:\s*"([^"]*)"', content)
    
    pub_date = pub.group(1) if pub else None
    title_base = title.group(1) if title else file_path.stem.replace('-', ' ').title()
    
    # NAZWA FOLDERU + plik
    parent_folder = file_path.parent.name if file_path.parent.name != 'docs' else ''
    display_title = f"{parent_folder}/{title_base}" if parent_folder else title_base
    
    # SLUG: /starlight/folder/plik/
    slug_parts = file_path.relative_to(DOCS_DIR).parts[:-1] + (file_path.stem,)
    slug = BASE_PATH + '/' + '/'.join(p.replace('\\', '/') for p in slug_parts) + '/'
    
    return {
        'title': display_title,
        'pub_date': pub_date,
        'slug': slug
    }

def find_all_docs():
    """Rekurencyjne .md/.mdx."""
    docs = []
    for ext in ['*.mdx', '*.md']:
        for file_path in DOCS_DIR.rglob(ext):
            if file_path.name == 'index.mdx':
                continue
            docs.append(parse_doc_file(file_path))
    
    print(f"🔍 {len(docs)} plików:", [d['title'] for d in docs[:3]])
    
    no_dates = sorted([d for d in docs if not d['pub_date']], key=lambda x: x['title'].lower())
    with_dates = sorted([d for d in docs if d['pub_date']], 
                       key=lambda x: datetime.fromisoformat(x['pub_date'].replace('Z','+00:00')), reverse=True)
    
    return no_dates + with_dates

def update_index():
    """Generuje index.mdx."""
    docs = find_all_docs()
    
    lines = [SECTION_START, "", f"Lista wszystkich ({len(docs)}):", ""]
    for doc in docs:
        lines += [f"- **[{doc['title']}]({doc['slug']})**",
                 f"  _{datetime.fromisoformat(doc['pub_date'].replace('Z','+00:00')).strftime('%Y-%m-%d')}_" if doc['pub_date'] else "  _brak daty_",
                 ""]
    
    lines.append("> **Uwaga**: Sidebar automatycznie pokazuje wszystkie dokumenty")
    
    with open(INDEX_FILE, 'r', encoding='utf-8') as f:
        content = f.read()
    
    content = re.split(re.escape(SECTION_START), content, 1)[0] + '\n'.join(lines)
    
    with open(INDEX_FILE, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ Wygenerowano {len(docs)} dokumentów")
    print("📁 Przykłady:", [f"{d['title']} → {d['slug']}" for d in docs[:3]])

if __name__ == "__main__":
    update_index()
