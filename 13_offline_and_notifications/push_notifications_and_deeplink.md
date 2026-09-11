# Push Notifications & Deep Linking - সম্পূর্ণ গাইড ও ইন্টারভিউ প্রশ্নোত্তর

Firebase Cloud Messaging (FCM) দিয়ে নোটিফিকেশন হ্যান্ডলিং এবং ইউনিভার্সাল/অ্যাপ লিংক দিয়ে নির্দিষ্ট স্ক্রিনে ইউজার রিডাইরেক্ট করার প্র্যাকটিক্যাল টেকনিক।

---

## 🔔 ১. Firebase Cloud Messaging (FCM)

### প্রশ্ন ১: FCM-এ Foreground, Background, এবং Terminated স্টেটে নোটিফিকেশন হ্যান্ডলিং কীভাবে আলাদা?

**উত্তর (ডিটেইল):**

```
┌─────────────────────────────────────────────────────────────┐
│ 1. Foreground (অ্যাপ ওপেন ও ইউজারের সামনে একটিভ)            │
│    -> FirebaseMessaging.onMessage.listen(...)              │
│    -> ডিফল্ট সিস্টেম পপআপ দেখায় না, flutter_local_notifications │
│       দিয়ে ম্যানুয়ালি হেডস-আপ ব্যানার তৈরি করতে হয়।          │
├─────────────────────────────────────────────────────────────┤
│ 2. Background (অ্যাপ মিনিমাইজড হয়ে রিসেন্ট অ্যাপসে আছে)      │
│    -> FirebaseMessaging.onBackgroundMessage(...)           │
│    -> টপ-লেভেল বা static ফাংশন হতে হবে (@pragma vm-entry)   │
├─────────────────────────────────────────────────────────────┤
│ 3. Terminated / Killed (ইউজার সোয়াইপ করে অ্যাপ বন্ধ করেছে) │
│    -> FirebaseMessaging.instance.getInitialMessage()       │
│    -> নোটিফিকেশনে ট্যাপ করে অ্যাপ খুললে এই মেথডে ডেটা পাওয়া যায়│
└─────────────────────────────────────────────────────────────┘
```

**বাস্তব কোড উদাহরণ:**

```dart
import 'package:firebase_core/firebase_core.dart';
import 'package:firebase_messaging/firebase_messaging.dart';

// Background handler অবশ্যই টপ-লেভেল ফাংশন হতে হবে
@pragma('vm:entry-point')
Future<void> _firebaseMessagingBackgroundHandler(RemoteMessage message) async {
  await Firebase.initializeApp();
  print("Background Message ID: ${message.messageId}");
}

void setupPushNotifications() {
  FirebaseMessaging.onBackgroundMessage(_firebaseMessagingBackgroundHandler);

  // ১. Foreground নোটিফিকেশন
  FirebaseMessaging.onMessage.listen((RemoteMessage message) {
    print("Foreground Message: ${message.notification?.title}");
    // এখানে flutter_local_notifications দিয়ে ব্যানার দেখান
  });

  // ২. Background অবস্থায় নোটিফিকেশন ট্যাপ করলে
  FirebaseMessaging.onMessageOpenedApp.listen((RemoteMessage message) {
    _navigateToDetailScreen(message.data['product_id']);
  });

  // ৩. Terminated অবস্থায় নোটিফিকেশন ট্যাপ করে অ্যাপ ওপেন করলে
  FirebaseMessaging.instance.getInitialMessage().then((RemoteMessage? message) {
    if (message != null) {
      _navigateToDetailScreen(message.data['product_id']);
    }
  });
}

void _navigateToDetailScreen(String? id) {
  // Navigation লজিক (GoRouter বা Navigator)
}
```

---

### প্রশ্ন ২: Notification Payload বনাম Data-only Payload-এর মধ্যে পার্থক্য কী? সাইলেন্ট নোটিফিকেশন কী?

**উত্তর (ডিটেইল):**

- **Notification Payload (`"notification": {"title": "Hi", "body": "Hello"}`):**
  - ব্যাকগ্রাউন্ডে থাকলে ওএস সরাসরি সিস্টেম ট্রে-তে ব্যানার দেখিয়ে দেয়। আপনার ডার্ট কোড রান করার সুযোগ পায় না যতক্ষণ না ইউজার নোটিফিকেশনে ট্যাপ করে।
- **Data-only Payload (`"data": {"key": "value"}`):**
  - এতে কোনো ভিজ্যুয়াল নোটিফিকেশন সরাসরি তৈরি হয় না। ওএস অ্যাপের ব্যাকগ্রাউন্ড হ্যান্ডলারকে জাগিয়ে দেয় (Wake up)।
  - **Silent Notification:** অ্যাপ ব্যাকগ্রাউন্ডে গোপনে ডেটা ফেচ বা সিঙ্ক করতে পারে, এবং ডার্ট কোড নিজে সিদ্ধান্ত নিতে পারে নোটিফিকেশন দেখাবে কিনা।

---

## 🔗 ২. Deep Linking (App Links & Universal Links)

### প্রশ্ন ৩: Custom Scheme বনাম App Links / Universal Links-এর পার্থক্য কী?

**উত্তর (ডিটেইল):**

1. **Custom Scheme (`myapp://product/123`):**
   - ব্রাউজার কোনো ডোমেইন ভেরিফিকেশন করে না। যদি দুটি অ্যাপ একই স্কিম রেজিস্টার করে, তবে ইউজারের ফোনে কনফ্লিক্ট ডায়ালগ আসে (Disambiguation dialog)।
2. **App Links (Android) & Universal Links (iOS) (`https://mywebsite.com/product/123`):**
   - এটি স্ট্যান্ডার্ড HTTPS URL।
   - **ডোমেইন ভেরিফিকেশন:** আপনার সার্ভারে `.well-known/assetlinks.json` (Android) এবং `apple-app-site-association` (iOS) ফাইল রাখতে হয় যা প্রমাণ করে আপনিই ডোমেইনের মালিক।
   - ফোনে অ্যাপ ইন্সটল থাকলে সরাসরি কোনো ব্রাউজার ছাড়াই এক ক্লিকে অ্যাপের নির্দিষ্ট স্ক্রিন ওপেন হয়ে যাবে। অ্যাপ ইন্সটল না থাকলে স্বাভাবিক ব্রাউজার ওয়েবসাইটে চলে যাবে।
