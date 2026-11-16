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

# Bucket name matching firebase-config.js
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
    "09 - جيم": ("Fitness", "جيم ولياقة"),
    "10 - موشن": ("Motion", "موشن جرافيك"),
    "11 - ملابس": ("Fashion", "أزياء وملابس"),
    "12 - ايجنسي": ("Agency", "أعمال الأيچنسي"),
    "AI": ("AI", "ذكاء اصطناعي"),
    "ايفنت": ("Event", "فعاليات وتغطيات"),
    "بلح": ("Dates", "تمور وأغذية"),
    "سعودي": ("Saudi", "مشاريع سعودية"),
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
    print("      Omar Mostafa Portfolio - Video Migrator")
    print("=====================================================")

    if not os.path.exists(KEY_PATH):
        print("\n[!] ملف مفتاح الخدمة غير موجود!")
        print(f"يرجى التأكد من وضع الملف باسم: serviceAccountKey.json داخل المجلد:")
        print(f"-> {CURRENT_DIR}")
        input("\nاضغط Enter للخروج...")
        sys.exit(1)

    if not os.path.exists(DRIVE_FILES_PATH):
        print(f"\n[!] ملف فهرس الفيديوهات drive_files.json غير موجود في: {CURRENT_DIR}")
        sys.exit(1)

    print("\n[1/4] جاري الاتصال بـ Firebase Admin SDK...")
    cred = credentials.Certificate(KEY_PATH)
    try:
        firebase_admin.initialize_app(cred, {'storageBucket': BUCKET_NAME})
        bucket = storage.bucket()
    except Exception:
        firebase_admin.initialize_app(cred, {'storageBucket': FALLBACK_BUCKET})
        bucket = storage.bucket()

    db = firestore.client()
    print("      تم الاتصال بـ Firestore و Storage بنجاح!")

    os.makedirs(TEMP_DIR, exist_ok=True)

    with open(DRIVE_FILES_PATH, 'r', encoding='utf-8') as f:
        files = json.load(f)

    # Resume capability
    processed_ids = set()
    if os.path.exists(PROGRESS_FILE):
        try:
            with open(PROGRESS_FILE, 'r', encoding='utf-8') as pf:
                processed_ids = set(json.load(pf))
            print(f"[2/4] استئناف الترحيل: {len(processed_ids)} فيديو تم رفعهم مسبقاً.")
        except Exception:
            processed_ids = set()

    total = len(files)
    print(f"[3/4] إجمالي الفيديوهات المطلوب ترحيلها: {total}")

    success_count = len(processed_ids)

    for idx, item in enumerate(files, 1):
        file_id = item['id']
        rel_path = item['path']

        if file_id in processed_ids:
            continue

        raw_folder = rel_path.split('\\')[0] if '\\' in rel_path else rel_path.split('/')[0]
        cat_en, cat_ar = CATEGORY_MAP.get(raw_folder, (raw_folder, raw_folder))
        title = clean_title(rel_path)

        print(f"\n--- [{idx}/{total}] جاري معالجة: {title} ({raw_folder}) ---")

        safe_name = re.sub(r'[^a-zA-Z0-9_\-\.]', '_', os.path.basename(rel_path))
        temp_video_path = os.path.join(TEMP_DIR, f"{file_id}_{safe_name}")
        if not temp_video_path.endswith('.mp4'):
            temp_video_path += '.mp4'

        try:
            # 1. Download via gdown
            print("  -> جاري التنزيل من Google Drive...")
            gdown.download(id=file_id, output=temp_video_path, quiet=True)

            if not os.path.exists(temp_video_path) or os.path.getsize(temp_video_path) == 0:
                print("  [!] فشل التحميل أو الملف فارغ. تخطي.")
                continue

            size_mb = os.path.getsize(temp_video_path) / (1024 * 1024)
            print(f"  -> تم التنزيل بنجاح ({size_mb:.2f} MB)")

            # 2. Upload to Firebase Storage
            storage_dest = f"videos/{file_id}_{safe_name}"
            blob = bucket.blob(storage_dest)
            blob.content_type = 'video/mp4'

            print("  -> جاري الرفع إلى Firebase Storage...")
            blob.upload_from_filename(temp_video_path)

            try:
                blob.make_public()
                direct_url = blob.public_url
            except Exception:
                # Standard Firebase media token URL format
                direct_url = f"https://firebasestorage.googleapis.com/v0/b/{bucket.name}/o/{storage_dest.replace('/', '%2F')}?alt=media"

            print(f"  -> تم الرفع والرابط المباشر: {direct_url}")

            # 3. Add to Firestore shortVideos
            doc_data = {
                'title': title,
                'category': cat_en,
                'categoryAr': cat_ar,
                'videoUrl': direct_url,
                'thumbnail': f"https://lh3.googleusercontent.com/d/{file_id}=w600",
                'order': idx,
                'fileId': file_id,
                'createdAt': firestore.SERVER_TIMESTAMP
            }

            db.collection('shortVideos').add(doc_data)
            print("  -> تم الحفظ في قاعدة بيانات Firestore بنجاح!")

            # 4. Save progress
            processed_ids.add(file_id)
            success_count += 1
            with open(PROGRESS_FILE, 'w', encoding='utf-8') as pf:
                json.dump(list(processed_ids), pf, ensure_ascii=False)

        except Exception as err:
            print(f"  [X] حدث خطأ أثناء المعالجة: {err}")
        finally:
            if os.path.exists(temp_video_path):
                try:
                    os.remove(temp_video_path)
                except Exception:
                    pass

    print("\n=====================================================")
    print(f" اكتملت العملية بنجاح! تم رفع {success_count} من أصل {total} فيديو.")
    print("=====================================================")

if __name__ == '__main__':
    main()
