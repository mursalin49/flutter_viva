# Google Play Store Deployment - সম্পূর্ণ গাইড ও ইন্টারভিউ প্রশ্নোত্তর

একটি Flutter অ্যাপকে প্রোডাকশনের জন্য প্রস্তুত করা এবং Google Play Console-এ সফলভাবে প্রকাশ করার সম্পূর্ণ প্রক্রিয়া।

---

## 🎯 ১. প্রোডাকশন রিলিজের পূর্বপ্রস্তুতি (Pre-Release Checklist)

### প্রশ্ন ১: Debug APK বনাম Release App Bundle (.aab)-এর মধ্যে পার্থক্য কী? Google Play Store-এ কোনটি আপলোড করতে হয়?

**উত্তর (ডিটেইল):**
- **Debug APK:** এতে Dart VM এবং Hot Reload কোড থাকে। ফাইল সাইজ অনেক বড় (৪০-৮০ MB+) হয় এবং পারফরম্যান্স অপ্টিমাইজ করা থাকে না।
- **Release APK:** AOT (Ahead-of-Time) কম্পাইল করা মেশিন কোড। কোনো ডিবাগিং প্রতীক থাকে না, সাইজ ছোট এবং ফাস্ট।
- **Release App Bundle (.aab):** Google Play Store-এ আপলোড করার জন্য **AAB বাধ্যতামূলক**। 
  - AAB আপলোড করলে Google Play Store ইউজারের ডিভাইসের CPU আর্কিটেকচার (arm64-v8a, armeabi-v7a) এবং স্ক্রিন রেজোলিউশন অনুযায়ী অপ্টিমাইজড ছোট সাইজের APK তৈরি করে দেয় (Dynamic Delivery)। ফলে ইউজারের ডাউনলোড সাইজ প্রায় ৩০-৫০% কমে যায়।

```bash
# Release App Bundle তৈরির কমান্ড:
flutter build appbundle --release
```

---

### প্রশ্ন ২: Android Keystore কী এবং এটি কেন অত্যন্ত গুরুত্বপূর্ণ? হারিয়ে গেলে কী ক্ষতি হবে?

**উত্তর (ডিটেইল):**
- **Keystore (`.jks` ফাইল):** এটি একটি ক্রিপ্টোগ্রাফিক সিকিউরিটি কি (Key) যা প্রমাণ করে অ্যাপটির আসল মালিক বা ডেভেলপার আপনি।
- **কেন গুরুত্বপূর্ণ:** আপনি যখন পরবর্তীতে অ্যাপের নতুন ভার্সন বা আপডেট পাঠাবেন, সেই আপডেটটিকে অবশ্যই একই Keystore দিয়ে সাইন করতে হবে।
- **হারিয়ে গেলে কী হবে:** যদি আপনি এই Keystore ফাইল বা এর পাসওয়ার্ড হারিয়ে ফেলেন, তবে আপনি আর কখনোই আপনার অ্যাপে কোনো আপডেট দিতে পারবেন না! 
  *(তবে আপনি যদি Google Play App Signing অপশনটি এনাবল রাখেন, তবে Google Support-এ রিকোয়েস্ট পাঠিয়ে নতুন কি রিসেট করা সম্ভব।)*

**Keystore তৈরির কমান্ড (Terminal):**
```bash
keytool -genkey -v -keystore my-upload-key.jks -keyalg RSA -keysize 2048 -validity 10000 -alias my-key-alias
```

---

### প্রশ্ন ৩: `key.properties` ফাইল কীভাবে কনফিগার করবেন এবং এটি কেন Git-এ পুশ করা নিষেধ?

**উত্তর (ডিটেইল):**
`android/key.properties` ফাইলে আপনার কীস্টোরের লোকেশন এবং পাসওয়ার্ড রাখা হয়:

```properties
storePassword=yourStorePassword
keyPassword=yourKeyPassword
keyAlias=my-key-alias
storeFile=../my-upload-key.jks
```

**`android/app/build.gradle` কনফিগারেশন:**
```groovy
def keystoreProperties = new Properties()
def keystorePropertiesFile = rootProject.file('key.properties')
if (keystorePropertiesFile.exists()) {
    keystoreProperties.load(new FileInputStream(keystorePropertiesFile))
}

android {
    ...
    signingConfigs {
        release {
            keyAlias = keystoreProperties['keyAlias']
            keyPassword = keystoreProperties['keyPassword']
            storeFile = keystoreProperties['storeFile'] ? file(keystoreProperties['storeFile']) : null
            storePassword = keystoreProperties['storePassword']
        }
    }
    buildTypes {
        release {
            signingConfig = signingConfigs.release
            minifyEnabled true
            shrinkResources true
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
        }
    }
}
```

> **Security Warning:** `key.properties` এবং `.jks` ফাইল কখনোই গিটহাবে পুশ করবেন না। এগুলোকে অবশ্যই `.gitignore`-এ যুক্ত রাখবেন।

---

### প্রশ্ন ৪: Version Code বনাম Version Name-এর পার্থক্য কী?

**উত্তর (ডিটেইল):**
`pubspec.yaml` ফাইলে ভার্সনিং এভাবে লেখা হয়:
```yaml
version: 1.2.0+5
```
- **Version Name (`1.2.0`):** এটি ব্যবহারকারীদের দেখানোর জন্য (Semantic Versioning: Major.Minor.Patch)।
- **Version Code (`5`):** এটি একটি পূর্ণসংখ্যা (Integer) যা Google Play Store ইন্টারনালি ট্র্যাক করে। প্রতিবার নতুন আপডেট দেওয়ার সময় এই সংখ্যাটি অবশ্যই আগের চেয়ে বড় হতে হবে (যেমন: ৫ এর পর ৬)।

---

### প্রশ্ন ৫: ProGuard / R8 এবং কোড Obfuscation কী? কেন প্রোডাকশনে এটি জরুরি?

**উত্তর (ডিটেইল):**
1. **Minification & Dead Code Elimination:** আপনার প্রোজেক্ট এবং প্যাকেজগুলোর মধ্যে যেসব কোড/মেথড বাস্তবে ব্যবহৃত হয়নি সেগুলোকে মুছে ফেলে অ্যাপের সাইজ উল্লেখযোগ্যভাবে কমিয়ে দেয়।
2. **Obfuscation (কোড দুর্বোধ্য করা):** ক্লাস, ভেরিয়েবল ও মেথডের নাম পরিবর্তন করে অপ্রাসঙ্গিক অক্ষর (যেমন: `a`, `b`, `c`) দিয়ে রিপ্লেস করে দেয়। ফলে কেউ আপনার APK রিভার্স ইঞ্জিনিয়ারিং বা ডিকম্পাইল করলেও ভেতরের বিজনেস লজিক সহজে বুঝতে পারে না।

**Flutter-এ কোড অবফাসকেট করার কমান্ড:**
```bash
flutter build appbundle --obfuscate --split-debug-info=./build/debug-info
```

---

## ⚠️ ২. Play Store রিজেকশনের শীর্ষ কারণ ও ইন্টারভিউ টিপস

### প্রশ্ন ৬: Play Store-এ সাধারণত কোন কোন কারণে অ্যাপ রিজেক্ট বা সাসপেন্ড হয়?

1. **Privacy Policy (গোপনীয়তা নীতি) না থাকা বা অসম্পূর্ণ হওয়া:** অ্যাপ যদি ইন্টারনেট, লোকেশন, ক্যামেরা বা ফোন মেমোরি পারমিশন নেয়, তবে একটি পাবলিক Privacy Policy URL দেওয়া বাধ্যতামূলক।
2. **Sensitive Permissions (যেমন: SMS, Background Location):** আপনি যদি ব্যাকগ্রাউন্ড লোকেশন বা কল লগ চান, তবে Google-কে ভিডিও প্রুফ দিয়ে বোঝাতে হবে যে এই পারমিশন ছাড়া অ্যাপের মূল ফিচার অচল।
3. **Data Safety Form ভুল পূরণ করা:** অ্যাপে কোনো অ্যানালিটিক্স (Firebase, Facebook SDK) বা থার্ড-পার্টি লাইব্রেরি ডেটা সংগ্রহ করলে তা Play Console-এর Data Safety সেকশনে সঠিকভাবে উল্লেখ না করলে রিজেক্ট হয়।
4. **টেস্টিং ক্রেডেনশিয়াল না দেওয়া:** লগইন সিস্টেম থাকলে গুগল রিভিয়্যুয়ারদের জন্য টেস্ট ইমেইল ও পাসওয়ার্ড দিতে হয়। না দিলে তারা অ্যাপ পরীক্ষা করতে না পেরে রিজেক্ট করে দেয়।
5. **ক্র্যাশ বা ব্রোকেন ফাংশনালিটি:** রিভিয়্যুয়ারের ডিভাইসে অ্যাপ ওপেন করার সাথে সাথে ক্র্যাশ করলে অ্যাপ রিজেক্ট হবে।
