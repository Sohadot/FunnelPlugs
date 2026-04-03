import json
import os
from pathlib import Path
from datetime import datetime

# استدعاء الإعدادات من config.py
try:
    from config import get_config
except ImportError:
    # في حال التشغيل المباشر من مجلد scripts
    import sys
    sys.path.append(str(Path(__file__).resolve().parents[1]))
    from scripts.config import get_config

def load_site_data(path: Path):
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def build_asset():
    config = get_config()
    data = load_site_data(config.paths.data_dir / "site.json")
    
    # 1. تحميل القوالب (Templates)
    base_tpl_path = config.paths.templates_dir / "base.html"
    page_tpl_path = config.paths.templates_dir / "page.html"
    
    if not base_tpl_path.exists() or not page_tpl_path.exists():
        raise FileNotFoundError("Critical Error: Foundation templates (base/page) are missing.")

    with open(base_tpl_path, 'r', encoding='utf-8') as f:
        base_html = f.read()
    with open(page_tpl_path, 'r', encoding='utf-8') as f:
        page_html = f.read()

    print(f"--- Sovereign Build Initiated: {data['site']['name']} v{data['site_info'].get('version', '0.1.0')} ---")

    # 2. توليد الصفحات (Core Pages)
    for page in data['core_pages']:
        print(f"Processing Layer: {page['key']}...")
        
        # Quality Gate Check
        if not page['title'] or not page['description']:
            if data['validation']['require_titles']:
                raise ValueError(f"Sovereign Breach: Page '{page['key']}' missing required metadata.")

        # حقن المحتوى في قالب الصفحة
        # ملاحظة: سنفترض وجود ملفات محتوى منفصلة أو حقن من الـ JSON مباشرة
        page_content = page.get('content', f"")
        current_page_body = page_html.replace("{{ page_title }}", page['title'])
        current_page_body = current_page_body.replace("{{ page_content }}", page_content)

        # حقن الكل في القالب الأساسي
        final_output = base_html
        final_output = final_output.replace("{{ title }}", page['title'])
        final_output = final_output.replace("{{ description }}", page['description'])
        final_output = final_output.replace("{{ canonical }}", page['canonical'])
        final_output = final_output.replace("{{ content }}", current_page_body)
        
        # حقن بيانات البراند والملاحة
        final_output = final_output.replace("{{ site_name }}", data['site']['name'])
        final_output = final_output.replace("{{ tagline }}", data['site']['tagline'])
        
        # حفظ الملف في الجذر (Main Output)
        output_file = config.paths.output_dir / page['file']
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(final_output)
        
        print(f"Verified & Generated: {page['file']}")

    # 3. توليد الـ Sitemap
    generate_sitemap(config, data)

def generate_sitemap(config, data):
    today = datetime.now().strftime("%Y-%m-%d")
    sitemap = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
    
    for page in data['core_pages']:
        if page.get('indexable', True):
            sitemap.append(f"  <url>")
            sitemap.append(f"    <loc>{page['url']}</loc>")
            sitemap.append(f"    <lastmod>{today}</lastmod>")
            sitemap.append(f"    <priority>1.0</priority>")
            sitemap.append(f"  </url>")
    
    sitemap.append("</urlset>")
    with open(config.paths.output_dir / data['seo']['sitemap_filename'], 'w', encoding='utf-8') as f:
        f.write("\n".join(sitemap))
    print("Sitemap Engine: Execution Complete.")

if __name__ == "__main__":
    build_asset()
