import os
import json
import time
import sys
import hashlib  # <--- [YENİ] Kriptografik işlemler için gerekli kütüphane

# --- SABİTLER ---
CONFIG_FILE = "config.json"

def load_config():
    """
    Konfigürasyon dosyasını yükler ve doğrular.
    """
    if not os.path.exists(CONFIG_FILE):
        print(f"[KRİTİK HATA] Konfigürasyon dosyası bulunamadı: {CONFIG_FILE}")
        return None

    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            config = json.load(f)
            return config
    except Exception as e:
        print(f"[HATA] Ayarlar yüklenirken hata: {e}")
        return None

def create_directories(config):
    """
    Gerekli klasörleri (logs, data) oluşturur.
    """
    log_dir = os.path.dirname(config.get("log_file", "logs/synapse.log"))
    data_dir = os.path.dirname(config.get("db_file", "data/baseline.json"))

    os.makedirs(log_dir, exist_ok=True)
    os.makedirs(data_dir, exist_ok=True)

# --- [YENİ] HASH HESAPLAMA MOTORU ---
def calculate_file_hash(filepath):
    """
    Verilen dosyanın SHA-256 hash'ini (parmak izini) hesaplar.
    
    GÜVENLİK VE PERFORMANS NOTLARI:
    1. 'Chunking' (Parçalama)
       Bu, 'Memory Overflow' hatalarını önler.
    2. 'rb' Modu, Bu, resim veya exe 
       dosyalarının bozulmadan okunmasını sağlar.
    """
    sha256_hash = hashlib.sha256() # SHA-256 motorunu başlat
    
    try:
        with open(filepath, "rb") as f: # Dosyayı binary okuma modunda aç
            # Dosyayı sonuna kadar 4096 byte'lık bloklar halinde oku
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block) # Hash motoruna bu bloğu yedir
        
        # İşlem bitince hexadecimal (onaltılık) formatta özet stringi döndür
        return sha256_hash.hexdigest()
        
    except FileNotFoundError:
        # Dosya tam işlem sırasında silinmiş olabilir
        return None
    except PermissionError:
        # Dosya yönetici izni gerektiriyor veya kilitli olabilir
        print(f"[UYARI] Erişim reddedildi: {filepath}")
        return None
    except Exception as e:
        # Beklenmedik diğer hatalar
        print(f"[HATA] Hash hesaplanırken sorun: {filepath} - {e}")
        return None

# --- ANA BLOK ---
if __name__ == "__main__":
    print("="*50)
    print("   SYNAPSE - Dosya Bütünlük İzleyicisi (v1.0)")
    print("="*50)

    # 1. Ayarları Yükle
    config = load_config()
    if config is None:
        sys.exit(1)

    # 2. Klasörleri Kontrol Et
    create_directories(config)
    
    print(f"[BİLGİ] Sistem başlatıldı. Hedef: {config['monitor_path']}")
    
    # --- [TEST ALANI] ---
    #'main.py'nin kendisinin hash'ini alalım.
    # Bu kısmı ileride sileceğiz, sadece şu anlık test için var.
    print("-" * 30)
    print("TEST: Hash Motoru Deneniyor...")
    target_file = "main.py" 
    file_hash = calculate_file_hash(target_file)
    
    if file_hash:
        print(f"BAŞARILI! '{target_file}' dosyasının SHA-256 İmzası:")
        print(f">> {file_hash}")
    else:
        print("BAŞARISIZ! Hash hesaplanamadı.")
    print("-" * 30)