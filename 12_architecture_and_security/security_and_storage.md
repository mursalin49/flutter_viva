# App Security & Reverse Engineering Protection - সম্পূর্ণ গাইড ও ইন্টারভিউ প্রশ্নোত্তর

Flutter মোবাইল অ্যাপ্লিকেশনে ডেটা সিকিউরিটি, নেটওয়ার্ক স্নিফিং প্রতিরোধ, টোকেন স্টোরেজ এবং রিভার্স ইঞ্জিনিয়ারিং প্রটেকশন।

---

## 🛡️ ১. SSL Pinning (Certificate Pinning)

### প্রশ্ন ১: SSL Pinning কী এবং ম্যান-ইন-দ্য-মিডল (MITM) অ্যাটাক কীভাবে রোধ করে?

**উত্তর (ডিটেইল):**
- **স্বাভাবিক HTTPS কানেকশন:** মোবাইল ফোন অপারেটিং সিস্টেমের (Android/iOS) ট্রাস্টেড CA (Certificate Authority)-র উপর নির্ভর করে এনক্রিপশন যাচাই করে। কোনো হ্যাকার যদি ইউজারের ফোনে নিজের একটি ফেইক রুট সার্টিফিকেট ইন্সটল করিয়ে প্রক্সি (যেমন: Charles Proxy, Burp Suite, Fiddler) চালু করে, তবে অ্যাপের সকল পাসওয়ার্ড ও API রিকোয়েস্ট/রেসপন্স পরিষ্কার টেক্সটে দেখতে পারে (MITM Attack)।
- **SSL Pinning:** অ্যাপের ভেতরেই সার্ভারের নির্দিষ্ট পাবলিক কি (Public Key Hash) অথবা সার্টিফিকেট হার্ডকোড করে দেওয়া হয়। ফলে হ্যান্ডশেক করার সময় সার্ভার সার্টিফিকেট হুবহু ম্যাচ না করলে অ্যাপ কোনো কানেকশন এলাও করে না—এমনকি ফোনে ফেইক রুট সার্টিফিকেট থাকলেও রিকোয়েস্ট ব্লক হয়ে যায়।

**Dio দিয়ে SHA-256 Public Key Pinning-এর উদাহরণ:**
```dart
import 'dart:io';
import 'package:dio/dio.dart';
import 'package:dio/io.dart';

void setupSslPinning(Dio dio) {
  // সার্ভার পাবলিক কি হ্যাশ (SPKI Fingerprint)
  const expectedFingerprint = "9a73d9e840...b4f17c";

  (dio.httpClientAdapter as DefaultHttpClientAdapter).onHttpClientCreate =
      (HttpClient client) {
    SecurityContext sc = SecurityContext(withTrustedRoots: false);
    // আপনি চাইলে কাস্টম .pem সার্টিফিকেট লোড করতে পারেন
    // sc.setTrustedCertificatesBytes(certBytes);

    HttpClient httpClient = HttpClient(context: sc);
    httpClient.badCertificateCallback =
        (X509Certificate cert, String host, int port) {
      // যদি সার্টিফিকেট ফিঙ্গারপ্রিন্ট মিলে যায় তবেই true, অন্যথায় false
      final sha256 = cert.sha256;
      return sha256 == expectedFingerprint;
    };
    return httpClient;
  };
}
```

---

## 🔐 ২. Secure Storage বনাম SharedPreferences

### প্রশ্ন ২: SharedPreferences-এ সেনসিটিভ ডেটা রাখা কেন অনিরাপদ? `flutter_secure_storage` কীভাবে কাজ করে?

**উত্তর (ডিটেইল):**

1. **`shared_preferences` কেন অনিরাপদ:**
   - অ্যান্ড্রয়েডে এটি প্লেইন XML ফাইল হিসেবে (`/data/data/com.example.app/shared_prefs/`) আন-এনক্রিপ্টেড অবস্থায় স্টোর হয়।
   - রুট করা ফোন বা ব্যাকআপ এক্সপ্লোরার দিয়ে যে কেউ এই ফাইল ওপেন করে ইউজার টোকেন ও পাসওয়ার্ড চুরি করতে পারে।

2. **`flutter_secure_storage` কীভাবে ডেটা সুরক্ষিত রাখে:**
   - **Android:** এটি **Android Keystore** সিস্টেম ব্যবহার করে ডেটা AES এনক্রিপ্ট করে এবং এনক্রিপশন কিগুলো হার্ডওয়্যার সিকিউরিটি মডিউলে (TEE/StrongBox) সুরক্ষিত থাকে।
   - **iOS:** এটি অ্যাপলের মিলিটারি-গ্রেড **Keychain Services** ব্যবহার করে, যা ডিভাইস লক থাকা অবস্থায় সম্পূর্ণ সুরক্ষিত থাকে।

```dart
import 'package:flutter_secure_storage/flutter_secure_storage.dart';

class SecureStorageService {
  static const _storage = FlutterSecureStorage(
    aOptions: AndroidOptions(encryptedSharedPreferences: true),
  );

  static Future<void> saveToken(String token) async {
    await _storage.write(key: 'auth_token', value: token);
  }

  static Future<String?> getToken() async {
    return await _storage.read(key: 'auth_token');
  }
}
```

---

## 🚫 ৩. Root / Jailbreak Detection & API Keys

### প্রশ্ন ৩: Jailbroken / Rooted ডিভাইসে ব্যাংকিং বা ফিনটেক অ্যাপ কেন রান করা ঝুঁকিপূর্ণ? কীভাবে এটি ডিটেক্ট করবেন?

**উত্তর (ডিটেইল):**
- রুটেড বা জেলব্রোকেন ডিভাইসে ওএস-এর স্যান্ডবক্সিং সিকিউরিটি ভেঙে যায়। ফ্রাইডা (Frida) বা এক্সপোজড (Xposed) ফ্রেমওয়ার্ক দিয়ে অ্যাপ মেমোরি ম্যানিপুলেট করা, বায়োমেট্রিক বাইপাস করা বা রানটাইমে কোড ইনজেকশন দেওয়া যায়।
- ব্যাংকিং ও ওয়ালেট অ্যাপে `flutter_jailbreak_flag` বা `freerasp` প্যাকেজ ব্যবহার করে ডিভাইস রুট চেক করা হয় এবং রুট পাওয়া গেলে ব্যবহারকারীকে সতর্ক করে অ্যাপ ক্লোজ করে দেওয়া হয়।

### প্রশ্ন ৪: Google Maps বা থার্ড-পার্টি API Secret Key কীভাবে সোর্স কোডে সুরক্ষিত রাখবেন?

**উত্তর (ডিটেইল):**
1. **ভুল পদ্ধতি:** সরাসরি Dart ফাইলের ভেতরে `static const apiKey = "AIzaSy..."` লেখা। কারণ APK ডিকম্পাইল করলেই স্ট্রিং হিসেবে কীটি পেয়ে যায়।
2. **সঠিক পদ্ধতি:**
   - **`--dart-define` ব্যবহার করা:**
     ```bash
     flutter run --dart-define=API_KEY=my_secret_key_123
     ```
     কোডে কল করা:
     ```dart
     const apiKey = String.fromEnvironment('API_KEY');
     ```
   - **প্রক্সি ব্যাকএন্ড আর্কিটেকচার:** সেনসিটিভ API যেমন OpenAI, Payment Secret Keys কখনো মোবাইল অ্যাপে রাখবেন না। মোবাইল ক্লায়েন্ট আপনার নিজস্ব সুরক্ষিত ব্যাকএন্ডে রিকোয়েস্ট পাঠাবে এবং ব্যাকএন্ড থার্ড-পার্টি API কল করবে।
