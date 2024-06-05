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
    wwe_content = soup.select(".TableContents > .TBase.TableBorderColor")
    wwe_content = [item.text.strip() for item in wwe_content if "WWE" in item.text]

    # İçeriği sıralama ve numaralandırma
    wwe_content = sorted(wwe_content)
    wwe_content_with_numbers = [f"{i}. {content}" for i, content in enumerate(wwe_content, 1)]

    # HTML formatında WWE içeriklerini yazdırma ve index.html dosyasına kaydetme
    if wwe_content_with_numbers:
        print("Bulunan WWE içeriği:")
        with open("index.html", "w", encoding="utf-8") as file:
            file.write("<html><head><title>WWE İçerikleri</title>")
            file.write("<style>")
            file.write("body { background-color: black; color: white; font-family: Arial, sans-serif; }")
            file.write(".event { margin-bottom: 20px; }")
            file.write("</style>")
            file.write("</head><body>")
            file.write("<h1 style='text-align: center;'>WWE İçerikleri</h1>")
            for i, item in enumerate(wwe_content_with_numbers, 1):
                file.write(f"<div class='event'>{i}. {item}</div>")
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