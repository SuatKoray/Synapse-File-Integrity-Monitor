import os
import json
import time
import sys
import hashlib
import urllib.request  # Discord'a HTTP isteği atmak için (Harici kütüphane gerektirmez)

# ---  SABİTLER  ---
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

# --- KRİPTOGRAFİK İŞLEMLER ---
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
        return None

# --- TARAMA MOTORU ---
def scan_directory(path, extensions, silent=False):
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

# --- BİLDİRİM SİSTEMİ ---
def send_discord_alert(message, webhook_url):
    """
    Harici kütüphane (requests) yerine yerleşik 'urllib' kullanıldı.
    Bu sayede kod her ortamda çalışır ve bağımlılık yaratmaz.
    """
    if not webhook_url:
        return # URL yoksa sessiz kal

    data = {
        "content": message,
        "username": "Synapse Security"
    }
    
    # JSON verisini hazırla ve byte'a çevir
    json_data = json.dumps(data).encode('utf-8')
    
    # İsteği oluştur
    req = urllib.request.Request(
        webhook_url, 
        data=json_data, 
        headers={
            'Content-Type': 'application/json',
            'User-Agent': 'Mozilla/5.0' # Bazı sunucular User-Agent olmadan reddeder
        }
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            # Başarılı olursa (200 OK) sessizce devam et
            pass
    except Exception as e:
        print(f"[UYARI] Discord bildirimi gönderilemedi: {e}")

# --- CANLI İZLEME DÖNGÜSÜ ---
def start_monitoring(config):
    db_path = config.get("db_file", "data/baseline.json")
    webhook_url = config.get("webhook_url", "")
    
    # Başlangıç kontrolü
    if not os.path.exists(db_path):
        print("[UYARI] Referans veritabanı bulunamadı. İlk tarama yapılıyor...")
        initial_snapshot = scan_directory(config['monitor_path'], config['file_extensions'])
        save_baseline(initial_snapshot, db_path)
    
    # Veritabanını yükle
    with open(db_path, 'r') as f:
        baseline = json.load(f)
        
    print(f"\n[SİSTEM] CANLI İZLEME AKTİF. ({config['monitoring_interval']} sn aralık)")
    if webhook_url:
        print("[SİSTEM] Discord Entegrasyonu: AÇIK")
        send_discord_alert("✅ **Synapse Güvenlik Sistemi Başlatıldı!**", webhook_url)
    else:
        print("[SİSTEM] Discord Entegrasyonu: KAPALI (URL Girilmedi)")
        
    print("[BİLGİ] Çıkmak için 'Ctrl + C' tuşlarına basın.\n")

    try:
        while True:
            time.sleep(config['monitoring_interval'])
            
            # Sessiz tarama
            current_snapshot = scan_directory(config['monitor_path'], config['file_extensions'], silent=True)
            
            changes_detected = False
            alert_messages = []

            # A. SİLİNENLER
            for filepath in list(baseline.keys()):
                if filepath not in current_snapshot:
                    msg = f"🚨 **ALARM: DOSYA SİLİNDİ!**\n`{filepath}`"
                    print(msg.replace("*", "").replace("`", "")) 
                    alert_messages.append(msg)
                    changes_detected = True

            # B. YENİ ve DEĞİŞENLER
            for filepath, current_hash in current_snapshot.items():
                if filepath not in baseline:
                    msg = f"⚠️ **ALARM: YENİ DOSYA TESPİT EDİLDİ!**\n`{filepath}`"
                    print(msg.replace("*", "").replace("`", ""))
                    alert_messages.append(msg)
                    changes_detected = True
                elif baseline[filepath] != current_hash:
                    msg = f"🔥 **KRİTİK ALARM: DOSYA DEĞİŞTİRİLDİ!**\n`{filepath}`"
                    print(msg.replace("*", "").replace("`", ""))
                    alert_messages.append(msg)
                    changes_detected = True
            
            # C. EĞER DEĞİŞİKLİK VARSA BİLDİR VE KAYDET
            if changes_detected:

                for msg in alert_messages:
                    send_discord_alert(msg, webhook_url)
                
                
                baseline = current_snapshot
                save_baseline(baseline, db_path)
                print("[SİSTEM] Veritabanı güncellendi.\n")

    except KeyboardInterrupt:
        print("\n[SİSTEM] İzleme kullanıcı tarafından durduruldu.")
        send_discord_alert("🛑 **Synapse Sistemi Kapatıldı.**", webhook_url)

# ---  ANA GİRİŞ  ---
if __name__ == "__main__":
    print("="*50)
    print("   SYNAPSE - Dosya Bütünlük İzleyicisi (v1.0)")
    print("="*50)

    config = load_config()
    if config:
        create_directories(config)
        start_monitoring(config)