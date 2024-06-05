from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

# Web sitesi URL'si
url = "https://cagematch.net"

# WebDriver'ı başlatma (Chrome kullanarak)
driver = webdriver.Chrome()

try:
    print("Web sitesine gitme...")
    # Web sitesine gitme
    driver.get(url)

    print("Sayfanın tam olarak yüklenmesini bekliyor...")
    # Sayfanın tam olarak yüklenmesini bekleyin (en fazla 10 saniye)
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "TRow1")))

    print("Sayfa kaynağını alınıyor...")
    # Sayfa kaynağını alın
    page_source = driver.page_source

    print("HTML içeriği işleniyor...")
    # HTML içeriğini işleme
    soup = BeautifulSoup(page_source, "html.parser")

    print("WWE etkinliklerini aranıyor...")
    # Belirli bir sınıf içinde sadece "WWE" içeren tüm öğeleri bulma
    wwe_events = soup.find_all("a", string=lambda text: "WWE" in text)

    # WWE etkinliklerinin linklerini saklama
    wwe_event_links = [event["href"] for event in wwe_events]

    # WWE etkinliklerinin adlarını saklama
    wwe_event_names = [event.text.strip() for event in wwe_events]

    # HTML formatında WWE içeriklerini yazdırma ve index.html dosyasına kaydetme
    if wwe_event_names:
        print("Bulunan WWE içeriği:")
        with open("index.html", "w", encoding="utf-8") as file:
            file.write("<html><head><title>WWE İçerikleri</title>")
            file.write("<style>")
            file.write("body { background-color: black; color: white; font-family: Arial, sans-serif; }")
            file.write("table { width: 80%; margin: auto; border-collapse: collapse; }")
            file.write("th, td { padding: 8px; text-align: left; border-bottom: 1px solid #ddd; }")
            file.write("tr:hover { background-color: #f5f5f5; }")
            file.write("</style>")
            file.write("</head><body>")
            file.write("<h1 style='text-align: center;'>WWE İçerikleri</h1>")
            file.write("<table>")
            file.write("<tr><th style='width: 10%;'>Sıra</th><th>İçerik</th><th>Tarih</th><th>Kanal</th></tr>")
            for i, (name, link) in enumerate(zip(wwe_event_names, wwe_event_links), 1):
                # Her etkinlik sayfasına gitme
                driver.get(url + link)
                # Sayfanın tam olarak yüklenmesini bekleyin
                wait.until(EC.presence_of_element_located((By.CLASS_NAME, "InformationBoxRow")))
                # Sayfa kaynağını alın
                event_page_source = driver.page_source
                # HTML içeriğini işleme
                event_soup = BeautifulSoup(event_page_source, "html.parser")
                # Etkinlik bilgilerini bulma
                event_info_boxes = event_soup.select(".InformationBoxRow")
                event_info = {}
                for info_box in event_info_boxes:
                    title = info_box.find(class_="InformationBoxTitle").text.strip()
                    content = info_box.find(class_="InformationBoxContents").text.strip()
                    event_info[title] = content
                # Etkinlik bilgilerini HTML dosyasına yazdırma
                file.write(f"<tr><td>{i}</td><td>{name}</td><td>{event_info.get('Date', '')}</td><td>{event_info.get('TV station/network', '')}</td></tr>")
            file.write("</table>")
            file.write("</body></html>")
        print("index.html dosyası oluşturuldu.")
    else:
        print("WWE içeriği bulunamadı.")

except Exception as e:
    print("Bir hata oluştu:", e)

finally:
    print("WebDriver kapatılıyor...")
    # WebDriver'ı kapatma
    driver.quit()