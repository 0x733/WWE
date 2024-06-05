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

    print("WWE içeriği aranıyor...")
    # Belirli bir sınıf içinde sadece "WWE" içeren tüm öğeleri bulma
    wwe_content = soup.select(".TRow1")
    wwe_content = [item.text.strip() for item in wwe_content if "WWE" in item.text]

    # Saat, tarih ve kanal bilgisini içeren tüm öğeleri bulma
    wwe_details = soup.select(".FeatureCategory")

    # Saat, tarih ve kanal bilgisini ayıklama
    event_details = []
    for detail in wwe_details:
        text = detail.text.strip()
        if "Online Stream" in text:
            details = text.split(" - ")
            event_details.append(details)

    # HTML formatında WWE içeriklerini yazdırma ve index.html dosyasına kaydetme
    if wwe_content:
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
            file.write("<tr><th style='width: 10%;'>Sıra</th><th>İçerik</th><th>Tarih</th><th>Saat</th><th>Kanal</th></tr>")
            for i, (content, detail) in enumerate(zip(wwe_content, event_details), 1):
                file.write(f"<tr><td>{i}</td><td>{content}</td><td>{detail[0]}</td><td>{detail[1]}</td><td>{detail[2]}</td></tr>")
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