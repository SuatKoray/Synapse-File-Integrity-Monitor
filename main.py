import os
import json
import time
import sys
import hashlib

# --- SABİTLER ---
CONFIG_FILE = "config.json"

def load_config():
    if not os.path.exists(CONFIG_FILE):
        print(f"[KRİTİK HATA] {CONFIG_FILE} bulunamadı!")
        return None
    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"[HATA] Ayarlar yüklenirken hata: {e}")
        return None

def create_directories(config):
    log_dir = os.path.dirname(config.get("log_file", "logs/synapse.log"))
    data_dir = os.path.dirname(config.get("db_file", "data/baseline.json"))
    os.makedirs(log_dir, exist_ok=True)
    os.makedirs(data_dir, exist_ok=True)

def calculate_file_hash(filepath):
    sha256_hash = hashlib.sha256()
    try:
        with open(filepath, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except (FileNotFoundError, PermissionError):
        return None
    except Exception as e:
        # Sessizce geç, loglama ileride eklenecek
        return None

def scan_directory(path, extensions, silent=False):
    """
    Belirtilen klasörü tarar.
    silent=True ise ekrana bilgi basmaz (Döngüde kirlilik olmasın diye).
    """
    snapshot = {}
    if not silent:
        print(f"[TARAMA] {path} dizini haritalanıyor...", end="\r")
    
    ignored_dirs = {"logs", "data", ".git", "__pycache__", ".venv", "venv", ".idea", ".vscode"}

    for root, dirs, files in os.walk(path):
        dirs[:] = [d for d in dirs if d not in ignored_dirs]
        
        for file in files:
            if any(file.endswith(ext) for ext in extensions):
                filepath = os.path.join(root, file)
                file_hash = calculate_file_hash(filepath)
                if file_hash:
                    normalized_path = os.path.normpath(filepath)
                    snapshot[normalized_path] = file_hash

    if not silent:
        print(f"[TARAMA] Tamamlandı. {len(snapshot)} dosya indekslendi.      ")
    return snapshot

def save_baseline(baseline_data, db_path):
    try:
        with open(db_path, 'w', encoding='utf-8') as f:
            json.dump(baseline_data, f, indent=4)
        return True
    except Exception as e:
        print(f"[HATA] Veritabanı kaydedilemedi: {e}")
        return False

# --- CANLI İZLEME MOTORU ---
def start_monitoring(config):
    db_path = config.get("db_file", "data/baseline.json")
    
    # 1. Başlangıçta veritabanı var mı kontrol et
    if not os.path.exists(db_path):
        print("[UYARI] Referans veritabanı bulunamadı. İlk tarama yapılıyor...")
        initial_snapshot = scan_directory(config['monitor_path'], config['file_extensions'])
        save_baseline(initial_snapshot, db_path)
    
    # 2. Mevcut veritabanını hafızaya yükle
    with open(db_path, 'r') as f:
        baseline = json.load(f)
        
    print(f"\n[SİSTEM] CANLI İZLEME BAŞLATILDI. ({config['monitoring_interval']} sn aralık)")
    print("[BİLGİ] Çıkmak için 'Ctrl + C' tuşlarına basın.\n")

    try:
        while True:
            # Belirlenen süre kadar uyu (CPU Tasarrufu)
            time.sleep(config['monitoring_interval'])
            
            # Anlık durumu çek (Sessiz modda)
            current_snapshot = scan_directory(config['monitor_path'], config['file_extensions'], silent=True)
            
            changes_detected = False
            
            # A. SİLİNENLERİ KONTROL ET (Baseline'da var, Current'ta yok)
            for filepath in list(baseline.keys()):
                if filepath not in current_snapshot:
                    print(f"!!! [ALARM] DOSYA SİLİNDİ: {filepath}")
                    changes_detected = True

            # B. YENİ ve DEĞİŞENLERİ KONTROL ET
            for filepath, current_hash in current_snapshot.items():
                if filepath not in baseline:
                    print(f"!!! [ALARM] YENİ DOSYA: {filepath}")
                    changes_detected = True
                elif baseline[filepath] != current_hash:
                    print(f"!!! [ALARM] DEĞİŞİKLİK TESPİT EDİLDİ: {filepath}")
                    changes_detected = True
            
            # C. EĞER DEĞİŞİKLİK VARSA VERİTABANINI GÜNCELLE
            if changes_detected:
                baseline = current_snapshot
                save_baseline(baseline, db_path)
                print("[SİSTEM] Veritabanı yeni duruma göre güncellendi.\n")

    except KeyboardInterrupt:
        print("\n[SİSTEM] İzleme kullanıcı tarafından durduruldu.")

# --- ANA BLOK ---
if __name__ == "__main__":
    print("="*50)
    print("   SYNAPSE - Dosya Bütünlük İzleyicisi (v1.0)")
    print("="*50)

    config = load_config()
    if config:
        create_directories(config)
        # Doğrudan izlemeyi başlatıyoruz
        start_monitoring(config)