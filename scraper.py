#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""TESHIS - sadece 3 urun dener, HTML'i kaydeder"""

import json
import time
from datetime import datetime
from urllib.parse import quote
from playwright.sync_api import sync_playwright

TEST_URUNLER = {
    "test1": "AMD Ryzen 5 5600",
    "test2": "NVIDIA RTX 4060",
    "test3": "Samsung 980 PRO 1TB",
}

def main():
    print("=== TESHIS BASLIYOR ===")
    sonuclar = {}

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=['--no-sandbox', '--disable-blink-features=AutomationControlled']
        )
        context = browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            viewport={'width': 1920, 'height': 1080},
            locale='tr-TR',
        )
        page = context.new_page()

        for key, urun in TEST_URUNLER.items():
            url = f"https://www.akakce.com/arama/?q={quote(urun)}"
            print(f"\n--- {urun} ---")
            print(f"URL: {url}")

            try:
                page.goto(url, wait_until='domcontentloaded', timeout=30000)
                page.wait_for_timeout(3000)

                title = page.title()
                html = page.content()
                print(f"Sayfa basligi: {title}")
                print(f"HTML boyutu: {len(html)} bytes")

                # Cloudflare kontrol
                if 'cloudflare' in html.lower():
                    print("!!! CLOUDFLARE TESPIT EDILDI !!!")
                if 'just a moment' in html.lower():
                    print("!!! 'JUST A MOMENT' SAYFASI !!!")
                if 'attention required' in html.lower():
                    print("!!! 'ATTENTION REQUIRED' SAYFASI !!!")
                if 'captcha' in html.lower():
                    print("!!! CAPTCHA TESPIT EDILDI !!!")

                # Ilk 500 karakter
                print("Ilk 500 karakter:")
                print(html[:500])
                print("...")

                # Debug kaydet
                with open(f'debug_{key}.html', 'w', encoding='utf-8') as f:
                    f.write(html)
                print(f"debug_{key}.html kaydedildi")

                sonuclar[key] = {
                    "urun": urun,
                    "title": title,
                    "html_size": len(html)
                }

            except Exception as e:
                print(f"HATA: {e}")
                sonuclar[key] = {"urun": urun, "error": str(e)}

            time.sleep(2)

        browser.close()

    with open("prices.json", "w", encoding="utf-8") as f:
        json.dump({
            "guncelleme": datetime.utcnow().isoformat() + "Z",
            "mod": "TESHIS",
            "testler": sonuclar
        }, f, ensure_ascii=False, indent=2)

    print("\n=== BITTI ===")

if __name__ == "__main__":
    main()
