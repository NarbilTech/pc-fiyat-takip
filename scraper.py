#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Akakce Fiyat Scraper v3 - Playwright (gercek tarayici ile)
Cloudflare'i atlatmak icin gercek Chromium kullanir.
"""

import json
import re
import time
import random
from datetime import datetime
from urllib.parse import quote

from playwright.sync_api import sync_playwright

# ============================================================
# URUN LISTESI (script.js ile ayni olmali)
# ============================================================
URUNLER = {
    "cpu1": "AMD Ryzen 3 1200", "cpu2": "AMD Ryzen 5 1600", "cpu3": "AMD Ryzen 5 2600",
    "cpu4": "AMD Ryzen 7 2700X", "cpu5": "AMD Ryzen 5 3600", "cpu6": "AMD Ryzen 7 3700X",
    "cpu7": "AMD Ryzen 5 5500", "cpu8": "AMD Ryzen 5 5600", "cpu9": "AMD Ryzen 7 5700X",
    "cpu10": "AMD Ryzen 7 5800X3D", "cpu11": "AMD Ryzen 9 5900X", "cpu12": "AMD Ryzen 5 7600X",
    "cpu13": "AMD Ryzen 7 7700X", "cpu14": "AMD Ryzen 7 7800X3D", "cpu15": "AMD Ryzen 9 7950X",
    "cpu16": "Intel Core i3-6100", "cpu17": "Intel Core i5-7400", "cpu18": "Intel Core i5-8400",
    "cpu19": "Intel Core i5-9400F", "cpu20": "Intel Core i7-9700K", "cpu21": "Intel Core i9-9900K",
    "cpu22": "Intel Core i5-10400F", "cpu23": "Intel Core i5-11400F", "cpu24": "Intel Core i7-10700K",
    "cpu25": "Intel Core i7-11700K", "cpu26": "Intel Core i9-11900K", "cpu27": "Intel Core i3-12100F",
    "cpu28": "Intel Core i5-12400F", "cpu29": "Intel Core i5-13400F", "cpu30": "Intel Core i5-14600K",
    "cpu31": "Intel Core i7-12700K", "cpu32": "Intel Core i7-13700K", "cpu33": "Intel Core i7-14700K",
    "cpu34": "Intel Core i9-12900K", "cpu35": "Intel Core i9-13900K", "cpu36": "Intel Core i9-14900K",
    "mb1": "MSI A320M-A Pro", "mb2": "MSI B450M-A Pro Max II", "mb3": "Gigabyte B550M DS3H",
    "mb4": "ASUS Prime B550-Plus", "mb5": "MSI MAG X570 Tomahawk", "mb6": "ASRock A620M Pro RS",
    "mb7": "MSI MAG B650 Tomahawk", "mb8": "ASUS TUF B650-Plus WiFi", "mb9": "ASUS ROG Strix X670E-E",
    "mb10": "Gigabyte H110M-S2H", "mb11": "ASUS Prime B250M-K", "mb12": "MSI B360M Pro-VDH",
    "mb13": "Gigabyte B365M DS3H", "mb14": "ASUS ROG Strix Z390-E", "mb15": "ASRock H410M-HDV",
    "mb16": "MSI B460M Pro-VDH", "mb17": "Gigabyte B560M DS3H", "mb18": "MSI MAG Z590 Tomahawk",
    "mb19": "ASRock H610M-HDV", "mb20": "Gigabyte B760M DS3H", "mb21": "ASRock B760M Pro RS",
    "mb22": "MSI PRO Z790-A WiFi", "mb23": "ASUS ROG Maximus Z790 Hero",
    "ram1": "Kingston Fury Beast 8GB DDR4 2666", "ram2": "Kingston Fury Beast 8GB DDR4 3200",
    "ram3": "Corsair Vengeance 16GB DDR4 3200", "ram4": "Kingston Fury 32GB DDR4 3200",
    "ram5": "Corsair Vengeance 32GB DDR4 3600", "ram6": "G.Skill Ripjaws 64GB DDR4 3600",
    "ram7": "Kingston Fury 16GB DDR5 5200", "ram8": "Corsair Vengeance 16GB DDR5 5600",
    "ram9": "G.Skill Trident Z5 32GB DDR5 6000", "ram10": "TeamGroup T-Force 32GB DDR5 6400",
    "ram11": "G.Skill Trident Z5 64GB DDR5 6000", "ram12": "Corsair Dominator 128GB DDR5 5600",
    "gpu1": "NVIDIA GeForce GTX 750 Ti", "gpu2": "NVIDIA GeForce GTX 1050 Ti",
    "gpu3": "NVIDIA GeForce GTX 1060 6GB", "gpu4": "NVIDIA GeForce GTX 1070",
    "gpu5": "NVIDIA GeForce GTX 1080", "gpu6": "NVIDIA GeForce GTX 1650",
    "gpu7": "NVIDIA GeForce GTX 1660 Super", "gpu8": "NVIDIA GeForce RTX 2060",
    "gpu9": "NVIDIA GeForce RTX 2060 Super", "gpu10": "NVIDIA GeForce RTX 2070 Super",
    "gpu11": "NVIDIA GeForce RTX 2080 Ti", "gpu12": "NVIDIA GeForce RTX 3050",
    "gpu13": "NVIDIA GeForce RTX 3060", "gpu14": "NVIDIA GeForce RTX 3060 Ti",
    "gpu15": "NVIDIA GeForce RTX 3070", "gpu16": "NVIDIA GeForce RTX 3070 Ti",
    "gpu17": "NVIDIA GeForce RTX 3080", "gpu18": "NVIDIA GeForce RTX 3080 Ti",
    "gpu19": "NVIDIA GeForce RTX 3090", "gpu20": "NVIDIA GeForce RTX 4060",
    "gpu21": "NVIDIA GeForce RTX 4060 Ti", "gpu22": "NVIDIA GeForce RTX 4070",
    "gpu23": "NVIDIA GeForce RTX 4070 Super", "gpu24": "NVIDIA GeForce RTX 4070 Ti Super",
    "gpu25": "NVIDIA GeForce RTX 4080 Super", "gpu26": "NVIDIA GeForce RTX 4090",
    "gpu27": "AMD Radeon RX 470", "gpu28": "AMD Radeon RX 570", "gpu29": "AMD Radeon RX 580",
    "gpu30": "AMD Radeon RX 5500 XT", "gpu31": "AMD Radeon RX 5600 XT", "gpu32": "AMD Radeon RX 5700 XT",
    "gpu33": "AMD Radeon RX 6600", "gpu34": "AMD Radeon RX 6600 XT", "gpu35": "AMD Radeon RX 6700 XT",
    "gpu36": "AMD Radeon RX 6800 XT", "gpu37": "AMD Radeon RX 6900 XT", "gpu38": "AMD Radeon RX 7600",
    "gpu39": "AMD Radeon RX 7700 XT", "gpu40": "AMD Radeon RX 7800 XT", "gpu41": "AMD Radeon RX 7900 XTX",
    "gpu42": "Intel Arc A750", "gpu43": "Intel Arc A770",
    "st1": "Kingston A400 240GB SSD", "st2": "Kingston NV2 500GB", "st3": "Kingston NV2 1TB",
    "st4": "Samsung 980 PRO 1TB", "st5": "Samsung 990 PRO 2TB", "st6": "WD Black SN850X 1TB",
    "st7": "WD Black SN850X 2TB", "st8": "Crucial P3 Plus 4TB", "st9": "Seagate Barracuda 1TB",
    "st10": "Seagate Barracuda 2TB", "st11": "Seagate Barracuda 4TB", "st12": "Samsung 870 EVO 1TB",
    "psu1": "Corsair CV450 450W", "psu2": "Corsair CV550 550W", "psu3": "Seasonic Focus GX-650",
    "psu4": "Corsair RM750e 750W", "psu5": "be quiet Pure Power 12M 850W", "psu6": "Corsair RM1000x",
    "psu7": "Seasonic Prime PX-1300", "psu8": "Corsair AX1600i", "psu9": "be quiet System Power 10 400W",
    "psu10": "Seasonic Prime TX-1000",
    "cs1": "Fractal Pop Mini Air", "cs2": "Cooler Master NR200P", "cs3": "NZXT H5 Flow",
    "cs4": "Corsair 4000D Airflow", "cs5": "Lian Li Lancool 216", "cs6": "Fractal North",
    "cs7": "Lian Li O11 Dynamic Evo", "cs8": "Deepcool Matrexx 40", "cs9": "Zalman i3 Neo",
    "cs10": "Corsair 7000D Airflow",
    "cl3": "Cooler Master Hyper 212", "cl4": "Deepcool AK400", "cl5": "Thermalright Peerless Assassin 120",
    "cl6": "Noctua NH-U12S Redux", "cl7": "Noctua NH-D15", "cl8": "NZXT Kraken 240",
    "cl9": "Corsair iCUE H150i", "cl10": "Arctic Liquid Freezer II 420",
    "mn1": "Samsung Odyssey G3 24", "mn2": "LG 24GN60R", "mn3": "AOC 24G2SPU",
    "mn4": "ASUS VG27AQ", "mn5": "LG 27GP850", "mn6": "Samsung Odyssey G7 32",
    "mn7": "LG 34GP950", "mn8": "ASUS ProArt PA278CV", "mn9": "AOC 24B2XH",
    "kb1": "Logitech K120", "kb2": "Redragon K552 Kumara", "kb3": "Redragon K617 Fizz",
    "kb4": "Razer BlackWidow V4", "kb5": "Logitech G Pro X TKL", "kb6": "Corsair K100 RGB",
    "kb7": "Logitech MX Keys S",
    "ms1": "Logitech M90", "ms2": "Logitech G102", "ms3": "Razer DeathAdder V3",
    "ms4": "Logitech G Pro X Superlight 2", "ms5": "Razer Viper V3 Pro",
    "ms6": "Logitech MX Master 3S", "ms7": "SteelSeries Rival 5",
    "hs1": "Logitech G335", "hs2": "Razer BlackShark V2 X", "hs3": "HyperX Cloud II",
    "hs4": "SteelSeries Arctis 7+", "hs5": "HyperX Cloud Alpha Wireless",
    "hs6": "Logitech G Pro X 2", "hs7": "Corsair Virtuoso Max",
}


def fiyat_cek(page, urun_adi):
    """Playwright ile Akakce'de ara ve en dusuk fiyati cek."""
    url = f"https://www.akakce.com/arama/?q={quote(urun_adi)}"

    try:
        page.goto(url, wait_until='domcontentloaded', timeout=30000)
        # Fiyatlarin yuklenmesi icin bekle
        page.wait_for_timeout(2000)

        # Tum sayfa HTML'ini al
        html = page.content()

        fiyatlar = []

        # Pattern 1: Akakce pt_v8 / pt_v9
        for m in re.finditer(r'class="p[tb]_[^"]*"[^>]*>\s*([\d.]+),(\d+)', html):
            try:
                tam = m.group(1).replace('.', '')
                fiyatlar.append(float(f"{tam}.{m.group(2)}"))
            except:
                pass

        # Pattern 2: JSON-LD price
        for m in re.finditer(r'"price"\s*:\s*"?([\d]+(?:[.,][\d]+)?)"?', html):
            try:
                f = float(m.group(1).replace(',', '.'))
                if f > 100:
                    fiyatlar.append(f)
            except:
                pass

        # Pattern 3: Genel "X.XXX,XX TL"
        for m in re.finditer(r'([\d]{1,3}(?:\.[\d]{3})*),(\d{2})\s*TL', html):
            try:
                tam = m.group(1).replace('.', '')
                fiyatlar.append(float(f"{tam}.{m.group(2)}"))
            except:
                pass

        gecerli = [f for f in fiyatlar if 100 < f < 500000]
        return min(gecerli) if gecerli else None

    except Exception as e:
        print(f"  EXC: {str(e)[:80]}", end="")
        return None


def main():
    print(f"=== Akakce Fiyat Scraper v3 (Playwright) ===")
    print(f"Baslangic: {datetime.utcnow().isoformat()}")
    print(f"Toplam urun: {len(URUNLER)}")
    print()

    sonuclar = {}
    basarili = 0
    basarisiz = 0

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            args=[
                '--no-sandbox',
                '--disable-blink-features=AutomationControlled',
                '--disable-dev-shm-usage',
            ]
        )
        context = browser.new_context(
            user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            viewport={'width': 1920, 'height': 1080},
            locale='tr-TR',
        )
        page = context.new_page()

        # Ilk acilista Cloudflare challenge'i gecmesini bekle
        print("Cloudflare kontrolu icin ana sayfa aciliyor...")
        try:
            page.goto('https://www.akakce.com/', wait_until='domcontentloaded', timeout=30000)
            page.wait_for_timeout(5000)
        except Exception as e:
            print(f"Ana sayfa hatasi: {e}")

        urun_listesi = list(URUNLER.items())

        for i, (urun_id, urun_adi) in enumerate(urun_listesi, 1):
            print(f"[{i}/{len(urun_listesi)}] {urun_adi}...", end=" ", flush=True)

            fiyat = fiyat_cek(page, urun_adi)

            if fiyat:
                sonuclar[urun_id] = round(fiyat, 2)
                print(f"=> {fiyat:.2f} TL")
                basarili += 1
            else:
                print("=> BULUNAMADI")
                basarisiz += 1

            # Her 30 urunde bir 5 saniye mola (ban yememek icin)
            if i % 30 == 0:
                print("  (kisa mola...)")
                time.sleep(5)
            else:
                time.sleep(random.uniform(1, 2))

        browser.close()

    cikti = {
        "guncelleme": datetime.utcnow().isoformat() + "Z",
        "toplam": len(URUNLER),
        "basarili": basarili,
        "basarisiz": basarisiz,
        "fiyatlar": sonuclar
    }

    with open("prices.json", "w", encoding="utf-8") as f:
        json.dump(cikti, f, ensure_ascii=False, indent=2)

    print()
    print(f"=== TAMAMLANDI ===")
    print(f"Basarili: {basarili}/{len(URUNLER)}")
    print(f"Cikti: prices.json")


if __name__ == "__main__":
    main()
