import asyncio
from playwright.async_api import async_playwright
from PIL import Image
import io
from pathlib import Path

# مصدر الحقيقة: كود الـ SVG الخاص بكِ
SVG_CODE = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 64 64" fill="none">
  <rect width="64" height="64" rx="8" fill="#05070a"/>
  <rect x="12" y="12" width="40" height="40" rx="3" stroke="#00ff41" stroke-width="2"/>
  <rect x="24" y="24" width="16" height="16" fill="#00ff41" fill-opacity="0.16" stroke="#00ff41" stroke-width="2"/>
  <path d="M32 12V24M32 40V52M12 32H24M40 32H52" stroke="#00ff41" stroke-width="2"/>
</svg>
"""

async def generate_favicon_pro():
    output_path = Path("output/favicon.ico")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={'width': 512, 'height': 512})
        
        # ضبط المحتوى كـ SVG مباشر
        await page.set_content(f"<html><body style='margin:0; background:transparent;'>{SVG_CODE}</body></html>")
        
        # التقاط لقطة شاشة بدقة عالية جداً مع شفافية
        img_data = await page.locator("svg").screenshot(omit_background=True)
        await browser.close()

        # تحويل البيانات إلى ICO باستخدام Pillow مع أحجام متعددة
        img = Image.open(io.BytesIO(img_data))
        img.save(
            output_path, 
            format="ICO", 
            sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128)]
        )
        print(f"✅ [SOVEREIGN_RENDER] Favicon generated with Chromium precision at: {output_path}")

if __name__ == "__main__":
    asyncio.run(generate_favicon_pro())
