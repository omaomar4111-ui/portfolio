# 🎬 نظام بورتفوليو محرر الفيديو + لوحة التحكم (Firebase & GitHub Pages)

نظام كامل واحترافي مصمم للعمل بدون سيرفر (Serverless) ومستضاف مجاناً بنسبة 100% على **GitHub Pages** ومربوط بقاعدة بيانات وتخزين سحابي عبر **Google Firebase**.

---

## 📁 هيكل المشروع

```text
portfolio/
├── index.html           # واجهة الموقع العامة (العرض، الكاروسيل 3D، الفيديوهات الطويلة، نبذة، تواصل)
├── admin.html           # لوحة تحكم الأدمن (تسجيل الدخول، تعديل البيانات، إضافة/تعديل/حذف الفيديوهات)
├── firebase-config.js   # ملف الإعدادات الموحد (تضع فيه مفاتيح Firebase مرة واحدة فقط)
├── firestore.rules      # قواعد أمان قاعدة البيانات (Firestore Security Rules)
├── storage.rules        # قواعد أمان التخزين السحابي (Storage Security Rules)
└── README.md            # دليل الاستخدام والتشغيل
```

---

## ⚡ الخطوة 1: إعداد Firebase (مرة واحدة فقط - 5 دقائق)

1. ادخل على [Firebase Console](https://console.firebase.google.com).
2. اضغط **Add project** وأنشئ مشروع جديد باسم (مثل: `my-portfolio`).
3. **Authentication (المصادقة):**
   - ادخل على `Build` ➔ `Authentication` ➔ اضغط `Get started`.
   - في تبويب `Sign-in method`، فعّل **Email/Password**.
   - في تبويب `Users`، اضغط `Add user` وأدخل بريدك:
     - البريد: `omaomar4111@gmail.com`
     - كلمة المرور: اختر كلمة مرور قوية (ستستخدمها للدخول للوحة التحكم).
4. **Firestore Database (قاعدة البيانات):**
   - ادخل على `Build` ➔ `Firestore Database` ➔ اضغط `Create database`.
   - اختر **Start in production mode** واختر أقرب Region (مثل `europe-west`).
   - ادخل على تبويب `Rules` في الأعلى، الصق ما بداخل ملف `firestore.rules` واضغط **Publish**.
5. **Storage (التخزين للملفات والصور):**
   - ادخل على `Build` ➔ `Storage` ➔ اضغط `Get started` واضغط Done.
   - ادخل على تبويب `Rules` في الأعلى، الصق ما بداخل ملف `storage.rules` واضغط **Publish**.
6. **الحصول على مفاتيح التطبيق:**
   - اضغط على أيقونة الترس ⚙️ بجانب Project Overview ➔ `Project settings`.
   - في تبويب `General` انزل للأسفل إلى `Your apps` واضغط على أيقونة الويب `</>`.
   - سجّل التطبيق باسم `Portfolio Web` وانسخ القيم الموجودة في `firebaseConfig`.
   - افتح ملف `firebase-config.js` في المشروع والصق القيم الخاصة بك فيه.

---

## 🚀 الخطوة 2: الرفع على GitHub Pages

1. أنشئ مستودعاً جديداً (New Repository) على GitHub باسم `portfolio` واجعله **Public**.
2. ارفع ملفات المجلد:
   - `index.html`
   - `admin.html`
   - `firebase-config.js`
3. من إعدادات المستودع (Settings) ➔ **Pages**:
   - `Source`: Deploy from a branch.
   - `Branch`: اختر `main` واجعل المجلد `/ (root)` ثم اضغط **Save**.
4. خلال دقائق سيكون موقعك متاحاً على:
   - **الموقع للجمهور:** `https://<YOUR_USERNAME>.github.io/portfolio/`
   - **لوحة التحكم:** `https://<YOUR_USERNAME>.github.io/portfolio/admin.html`

---

## 🛠️ كيفية الاستخدام

1. افتح رابط لوحة التحكم `admin.html`.
2. سجّل الدخول بالبريد `omaomar4111@gmail.com` وكلمة المرور.
3. **بيانات الموقع:** اكتب اسمك، التخصص، النبذة، روابط السوشيال ورقم الواتساب، وارفع صورتك الشخصية ثم اضغط "حفظ التغييرات".
4. **فيديوهات قصيرة:** أضف فيديوهات الريلز/الشورتس مع الصورة المصغرة ورابط يوتيوب أو ارفع ملف فيديو.
5. **فيديوهات طويلة:** أضف الأفلام أو الحلقات الطويلة مع التصنيف والمدة.
6. افتح `index.html` لتشاهد كل المحتوى يتحدث مباشرة وتلقائياً!
