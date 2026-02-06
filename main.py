import os
import json
import time
import sys


CONFIG_FILE = "config.json"

def load_config():
    """
    Konfigürasyon dosyasını yükler ve doğrular.
    Dönüş: Config sözlüğü (dict) veya başarısız olursa None.
    """
    # 1. Dosya var mı kontrolü (Defensive Programming)
    if not os.path.exists(CONFIG_FILE):
        print(f"[KRİTİK HATA] Konfigürasyon dosyası bulunamadı: {CONFIG_FILE}")
        print("Lütfen 'config.json' dosyasının proje dizininde olduğundan emin olun.")
        return None

    # 2. Güvenli dosya okuma bloğu
    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            config = json.load(f)
            # İleride buraya konfigürasyon doğrulama (validation) ekleyebiliriz.
            # Örneğin: "monitor_path" config içinde var mı?
            return config
    except json.JSONDecodeError:
        print(f"[HATA] {CONFIG_FILE} dosyası geçerli bir JSON formatında değil.")
        return None
    except Exception as e:
        print(f"[HATA] Beklenmedik bir hata oluştu: {e}")
        return None

def create_directories(config):
    """
    Gerekli klasörlerin varlığını kontrol eder, yoksa oluşturur.
    Bu, programın ilk çalıştırılmasında hata vermesini engeller.
    """
    # config içindeki yolları al, yoksa varsayılan kullan
    log_dir = os.path.dirname(config.get("log_file", "logs/synapse.log"))
    data_dir = os.path.dirname(config.get("db_file", "data/baseline.json"))

    # Klasörleri oluştur (exist_ok=True, klasör varsa hata verme demektir)
    os.makedirs(log_dir, exist_ok=True)
    os.makedirs(data_dir, exist_ok=True)
    print("[SİSTEM] Gerekli klasör yapısı kontrol edildi/oluşturuldu.")

# --- ANA BLOK ---

if __name__ == "__main__":
    print("="*50)
    print("   SYNAPSE - Dosya Bütünlük İzleyicisi (v1.0)")
    print("="*50)

    # 1. Ayarları Yükle
    config = load_config()

    if config is None:
        # Ayarlar yoksa programı hata kodu 1 ile kapat
        sys.exit(1)

    # 2. Klasör Yapısını Doğrula
    create_directories(config)

    # 3. Başlangıç Bilgisi
    print(f"[BİLGİ] İzlenen Hedef: {os.path.abspath(config['monitor_path'])}")
    print("[BİLGİ] Sistem başlatılıyor...")
    
    # Şimdilik burada duruyoruz.