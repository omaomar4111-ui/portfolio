import os
import sys
import json
import re
import gdown
import firebase_admin
from firebase_admin import credentials, firestore, storage

# Ensure UTF-8 terminal output
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
KEY_PATH = os.path.join(CURRENT_DIR, "serviceAccountKey.json")
DRIVE_FILES_PATH = os.path.join(CURRENT_DIR, "drive_files.json")
PROGRESS_FILE = os.path.join(CURRENT_DIR, "migration_progress.json")
TEMP_DIR = os.path.join(CURRENT_DIR, "temp_downloads")

BUCKET_NAME = "portfolio-35032.firebasestorage.app"
FALLBACK_BUCKET = "portfolio-35032.appspot.com"

CATEGORY_MAP = {
    "01 - طبي": ("Medical", "طبي"),
    "02 - تشطيب عقاري": ("Finishing", "تشطيب عقاري"),
    "03 - عقارات": ("Real Estate", "عقارات"),
    "04 - نجف": ("Lighting", "نجف وإضاءة"),
    "05 - اثاث مطابخ": ("Kitchens", "أثاث ومطابخ"),
    "06 - كافيه": ("Cafe", "كافيهات"),
    "07 - تجميل": ("Beauty", "تجميل وعناية"),
    "08 - عربيات": ("Automotive", "سيارات"),
    "09 - جيم": ("Gym & Fitness", "جيم ولياقة"),
    "10 - موشن": ("Motion Graphics", "موشن جرافيك"),
    "11 - ملابس": ("Fashion", "أزياء وملابس"),
    "12 - ايجنسي": ("Agency", "أعمال الأيچنسي"),
    "AI": ("AI", "ذكاء اصطناعي"),
    "ايفنت": ("Events", "فعاليات وتغطيات"),
    "بلح": ("Dates", "تمور وأغذية"),
    "سعودي": ("Saudi Projects", "مشاريع سعودية"),
    "مطعم": ("Restaurant", "مطاعم وأغذية")
}

def clean_title(path_str):
    filename = os.path.basename(path_str)
    name, _ = os.path.splitext(filename)
    folder = path_str.split(os.sep)[0] if os.sep in path_str else path_str.split('/')[0]
    kind_info = CATEGORY_MAP.get(folder, (folder, folder))
    if name.isdigit():
        return f"{kind_info[0]} #{int(name):02d}"
    return f"{kind_info[0]} - {name}"

def main():
    print("=====================================================")
    print("  Omar Mostafa Portfolio - Idempotent Video Migrator")
    print("=====================================================")

    if not os.path.exists(KEY_PATH):
        print(f"\n[!] serviceAccountKey.json not found in: {CURRENT_DIR}")
        print("Please place your Firebase serviceAccountKey.json in the project root.")
        sys.exit(1)

    if not os.path.exists(DRIVE_FILES_PATH):
        print(f"\n[!] drive_files.json not found in: {CURRENT_DIR}")
        sys.exit(1)

    print("\n[1/4] Connecting to Firebase Admin SDK...")
    cred = credentials.Certificate(KEY_PATH)
    try:
        firebase_admin.initialize_app(cred, {'storageBucket': BUCKET_NAME})
        bucket = storage.bucket()
    except Exception:
        firebase_admin.initialize_app(cred, {'storageBucket': FALLBACK_BUCKET})
        bucket = storage.bucket()

    db = firestore.client()
    print("      Connected successfully to Firestore and Storage!")

    os.makedirs(TEMP_DIR, exist_ok=True)

    with open(DRIVE_FILES_PATH, 'r', encoding='utf-8') as f:
        files = json.load(f)

    # 1. Load progress
    processed_ids = set()
    if os.path.exists(PROGRESS_FILE):
        try:
            with open(PROGRESS_FILE, 'r', encoding='utf-8') as pf:
                processed_ids = set(json.load(pf))
            print(f"[2/4] Resuming: {len(processed_ids)} videos already uploaded.")
        except Exception:
            processed_ids = set()

    total = len(files)
    print(f"[3/4] Total videos in catalog: {total}")

    success_count = len(processed_ids)

    for idx, item in enumerate(files, 1):
        file_id = item['id']
        rel_path = item['path']

        if file_id in processed_ids:
            continue

        raw_folder = rel_path.split('\\')[0] if '\\' in rel_path else rel_path.split('/')[0]
        cat_en, cat_ar = CATEGORY_MAP.get(raw_folder, (raw_folder, raw_folder))
        title = clean_title(rel_path)

        print(f"\n--- [{idx}/{total}] Processing: {title} ({raw_folder}) ---")

        safe_name = re.sub(r'[^a-zA-Z0-9_\-\.]', '_', os.path.basename(rel_path))
        temp_video_path = os.path.join(TEMP_DIR, f"{file_id}_{safe_name}")
        if not temp_video_path.endswith('.mp4'):
            temp_video_path += '.mp4'

        try:
            # Step A: Download
            print("  -> Downloading from Google Drive...")
            gdown.download(id=file_id, output=temp_video_path, quiet=True)

            if not os.path.exists(temp_video_path) or os.path.getsize(temp_video_path) == 0:
                print("  [!] Download failed or empty file. Skipping.")
                continue

            size_mb = os.path.getsize(temp_video_path) / (1024 * 1024)
            print(f"  -> Downloaded: {size_mb:.2f} MB")

            # Step B: Upload to Firebase Storage
            storage_dest = f"videos/{file_id}_{safe_name}"
            blob = bucket.blob(storage_dest)
            blob.content_type = 'video/mp4'

            print("  -> Uploading to Firebase Storage...")
            blob.upload_from_filename(temp_video_path)

            try:
                blob.make_public()
                direct_url = blob.public_url
            except Exception:
                direct_url = f"https://firebasestorage.googleapis.com/v0/b/{bucket.name}/o/{storage_dest.replace('/', '%2F')}?alt=media"

            print(f"  -> Direct public URL: {direct_url}")

            # Step C: Deterministic Idempotent Document Write
            # Use fixed doc ID = file_id so re-runs never duplicate documents!
            # Provide both 'genre' and 'category' so all frontend consumers resolve correctly
            doc_data = {
                'id': file_id,
                'fileId': file_id,
                'title': title,
                'genre': cat_en,
                'category': cat_en,
                'categoryAr': cat_ar,
                'videoUrl': direct_url,
                'thumbnail': f"https://lh3.googleusercontent.com/d/{file_id}=w600",
                'order': idx,
                'source': 'Firebase Storage',
                'updatedAt': firestore.SERVER_TIMESTAMP
            }

            db.collection('shortVideos').document(file_id).set(doc_data, merge=True)
            print(f"  -> Firestore doc shortVideos/{file_id} saved/updated successfully!")

            processed_ids.add(file_id)
            success_count += 1
            with open(PROGRESS_FILE, 'w', encoding='utf-8') as pf:
                json.dump(list(processed_ids), pf, ensure_ascii=False)

        except Exception as err:
            print(f"  [X] Error on {file_id}: {err}")
        finally:
            if os.path.exists(temp_video_path):
                try:
                    os.remove(temp_video_path)
                except Exception:
                    pass

    print("\n=====================================================")
    print(f" Migration finished! {success_count}/{total} files in Firebase Storage & Firestore.")
    print("=====================================================")

if __name__ == '__main__':
    main()
