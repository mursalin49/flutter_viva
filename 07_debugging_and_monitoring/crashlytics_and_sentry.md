# Production Crash Reporting - Firebase Crashlytics & Sentry

প্রোডাকশনে ব্যবহারকারীর ফোনে কোনো ক্র্যাশ বা অপ্রত্যাশিত এরর ঘটলে তা স্বয়ংক্রিয়ভাবে ট্র্যাক এবং সমাধান করার গাইড।

---

## 💥 ১. গ্লোবাল এরর ক্যাচিং (Global Error Handling)

### প্রশ্ন ১: Flutter-এ গ্লোবাল এরর এবং রানটাইম ক্র্যাশ কীভাবে ক্যাচ করতে হয়?

**উত্তর (ডিটেইল):**
Flutter 3+ এ সব ধরণের ক্র্যাশ ধরার জন্য দুটি প্রধান হুক রয়েছে:
1. `FlutterError.onError`: Flutter ফ্রেমওয়ার্কের ভেতরের সব UI ও উইজেট লেভেল এরর ধরে।
2. `PlatformDispatcher.instance.onError`: কোনো অ্যাসিঙ্ক (Async) ফাংশন বা ফ্রেমওয়ার্কের বাইরের এরর ধরে।

**প্রোডাকশন-গ্রেড সেটআপ (`main.dart`):**

```dart
import 'dart:ui';
import 'package:flutter/material.dart';
import 'package:firebase_core/firebase_core.dart';
import 'package:firebase_crashlytics/firebase_crashlytics.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Firebase.initializeApp();

  // ১. Flutter ফ্রেমওয়ার্কের ভেতরের এরর ক্যাচ করুন
  FlutterError.onError = (FlutterErrorDetails details) {
    FirebaseCrashlytics.instance.recordFlutterFatalError(details);
  };

  // ২. ফ্রেমওয়ার্কের বাইরের সকল Asynchronous এরর ক্যাচ করুন
  PlatformDispatcher.instance.onError = (error, stack) {
    FirebaseCrashlytics.instance.recordError(error, stack, fatal: true);
    return true;
  };

  runApp(const MyApp());
}
```

---

## 📊 ২. Crashlytics ও Sentry-র মূল ফিচার

### প্রশ্ন ২: Fatal Error বনাম Non-Fatal Error-এর মধ্যে পার্থক্য কী?

- **Fatal Error (অ্যাপ ক্র্যাশ):** অ্যাপটি সাথে সাথে বন্ধ হয়ে যায় বা ব্ল্যাক/রেড স্ক্রিন চলে আসে। ব্যবহারকারী অ্যাপ চালানো চালিয়ে যেতে পারে না।
- **Non-Fatal Error (হ্যান্ডলড এরর):** কোডে `try-catch` দিয়ে এরর ধরা হয়েছে, ফলে অ্যাপ ক্র্যাশ করেনি কিন্তু ব্যাকএন্ড কল ফেইল করেছে বা ডেটা পার্সিং ভুল হয়েছে। এটিকেও ট্র্যাকিং ড্যাশবোর্ডে লগ করে রাখা যায়:

```dart
try {
  await apiService.fetchData();
} catch (e, stackTrace) {
  // অ্যাপ ক্র্যাশ করেনি, কিন্তু ডেভ টিমের কাছে নোটিফিকেশন পাঠাতে চান
  FirebaseCrashlytics.instance.recordError(
    e, 
    stackTrace, 
    reason: 'Failed fetching home data',
    fatal: false, // Non-fatal
  );
}
```

---

### প্রশ্ন ৩: Breadcrumbs এবং User Identifier কেন যোগ করা জরুরি?

- **User Identifier:** কোন ইউজারের ফোনে এরর হয়েছে তা ড্যাশবোর্ডে দেখতে `setCustomKey` বা `setUserIdentifier` দেওয়া হয় (যেমন: `userId: 4892`—কখনোই পাসওয়ার্ড বা ক্রেডিট কার্ডের মতো গোপন তথ্য দেবেন না)।
- **Breadcrumbs:** ইউজার ক্র্যাশ করার আগের ৫টি ধাপে কী কী বাটনে চাপ দিয়েছিল (Action History) তা দেখতে Breadcrumb ব্যবহার করা হয়। এর মাধ্যমে বাগটি নিখুঁতভাবে রিপ্রডিউস করা যায়।

---

### প্রশ্ন ৪: প্রোডাকশন কোডে `print()` ব্যবহার করা কেন কঠোরভাবে নিষিদ্ধ? এর বিকল্প কী?

**উত্তর (ডিটেইল):**
1. `print()` আউটপুট অ্যান্ড্রয়েডের `logcat` এবং আইওএস সিস্টেম লগে সরাসরি চলে যায়। ফলে সংবেদনশীল তথ্য (API Token, User Data) অন্য কোনো ম্যালিসিয়াস অ্যাপ পড়তে পারে।
2. `print()` এর কোনো লেভেল ফিল্টারিং থাকে না (যেমন: Debug, Info, Warning, Error)।
3. এটি synchronous হওয়ায় অতিরিক্ত প্রিন্ট করলে অ্যাপের FPS কমে যেতে পারে।

**বিকল্প:**
`logger` অথবা `talker_flutter` প্যাকেজ ব্যবহার করা, অথবা `kDebugMode` চেক করে শুধুমাত্র ডিবাগ মোডে লগ দেওয়া:

```dart
import 'package:flutter/foundation.dart';

void safeLog(String message) {
  if (kDebugMode) {
    debugPrint('[APP_LOG]: $message');
  }
}
```
