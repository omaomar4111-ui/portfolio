// إعدادات Firebase الخاصة بك
// استبدل القيم هنا بالقيم التي نسختها من Firebase Console -> Project Settings -> Your apps -> Web app
const firebaseConfig = {
  apiKey: "YOUR_API_KEY",
  authDomain: "YOUR_PROJECT_ID.firebaseapp.com",
  projectId: "YOUR_PROJECT_ID",
  storageBucket: "YOUR_PROJECT_ID.appspot.com",
  messagingSenderId: "YOUR_MESSAGING_SENDER_ID",
  appId: "YOUR_APP_ID"
};

// تصدير للاستخدام في index.html و admin.html
window.firebaseConfig = firebaseConfig;
