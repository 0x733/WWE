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
    wait.until(EC.presence_of_element_located((By.CLASS_NAME, "LayoutContent")))

    print("Sayfa kaynağını alınıyor...")
    # Sayfa kaynağını alın
    page_source = driver.page_source

    print("HTML içeriği işleniyor...")
    # HTML içeriğini işleme
    soup = BeautifulSoup(page_source, "html.parser")

    print("WWE içeriği aranıyor...")
    # Belirli bir sınıf içinde sadece "WWE" içeren tüm öğeleri bulma
    wwe_content = soup.find_all(class_="LayoutContent")
    wwe_content = [item.text for item in wwe_content if "WWE" in item.text]

    # HTML formatında WWE içeriklerini yazdırma ve index.html dosyasına kaydetme
    if wwe_content:
        print("Bulunan WWE içeriği:")
        with open("index.html", "w", encoding="utf-8") as file:
            file.write("<html><head><title>WWE İçerikleri</title></head><body>")
            file.write("<h1>WWE İçerikleri</h1>")
            file.write("<table border='1'>")
            file.write("<tr><th>Sıra</th><th>İçerik</th></tr>")
            for i, item in enumerate(wwe_content, 1):
                file.write("<tr><td>{}</td><td>{}</td></tr>".format(i, item))
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