# In-App Updates & Force Update মেকানিজম

অ্যাপ স্টোর বা প্লে স্টোরে নতুন ভার্সন আসার পর ব্যবহারকারীকে অ্যাপের ভেতর থেকেই আপডেট দেওয়ার প্র্যাকটিক্যাল টেকনিক।

---

## 🔄 ১. Google Play In-App Updates

### প্রশ্ন ১: Flexible Update বনাম Immediate Update-এর পার্থক্য কী?

**উত্তর (ডিটেইল):**
Google Play Core লাইব্রেরি ব্যবহার করে অ্যাপের ভেতর দুইভাবে আপডেট করানো যায়:

| ফিচার | Flexible Update | Immediate Update |
| :--- | :--- | :--- |
| **ব্যবহারের সময়** | ছোটখাটো বাগ ফিক্স বা অপশনাল নতুন ফিচার আসলে। | কোনো ক্রিটিক্যাল সিকিউরিটি বাগ বা মেজর ব্রেকিং চেঞ্জ আসলে। |
| **ইউজার এক্সপেরিয়েন্স** | ইউজার অ্যাপ ব্যবহার করতে থাকবে, ব্যাকগ্রাউন্ডে আপডেট ডাউনলোড হবে। ডাউনলোড শেষে ইনস্টল করার রিকোয়েস্ট আসবে। | পুরো স্ক্রিন ব্লক করে আপডেট ডাউনলোড ও ইনস্টল করতে বাধ্য করবে। আপডেট না হওয়া পর্যন্ত অ্যাপ চালানো যাবে না। |
| **বাধ্যতামূলক কি?** | না, ইউজার চাইলে বাতিল করতে পারে। | হ্যাঁ, ইউজার অ্যাপ চালাতে চাইলে আপডেট করতেই হবে। |

**Flutter-এ কোড উদাহরণ (`in_app_update` প্যাকেজ):**

```dart
import 'package:in_app_update/in_app_update.dart';

Future<void> checkForUpdate() async {
  try {
    final info = await InAppUpdate.checkForUpdate();
    
    if (info.updateAvailability == UpdateAvailability.updateAvailable) {
      if (info.immediateUpdateAllowed) {
        // Immediate / Force Update শুরু করুন
        await InAppUpdate.performImmediateUpdate();
      } else if (info.flexibleUpdateAllowed) {
        // Flexible Update ব্যাকগ্রাউন্ডে ডাউনলোড করুন
        await InAppUpdate.startFlexibleUpdate();
        await InAppUpdate.completeFlexibleUpdate();
      }
    }
  } catch (e) {
    print('In-App update failed: $e');
  }
}
```

---

## 🛡️ ২. Custom Force Update (Remote Config / Backend API)

### প্রশ্ন ২: iOS এবং Android উভয়ের জন্য কীভাবে একটি নির্ভরযোগ্য Force Update সিস্টেম তৈরি করবেন?

**উত্তর (ডিটেইল):**
কারণ Apple-এর নিজস্ব কোনো ইন-অ্যাপ আপডেট ডায়ালগ নেই, তাই ইন্ডাস্ট্রি স্ট্যান্ডার্ড সমাধান হলো **Firebase Remote Config** অথবা **Backend Version API** ব্যবহার করা।

**আর্কিটেকচার ফ্লো:**
```
App Launch ➔ Fetch Min Required Version from Server ➔ Compare with Local App Version
     │
     ├── Local Version < Min Version ➔ Show Non-dismissible Dialog ("Please Update App") ➔ Redirect to Store
     └── Local Version >= Min Version ➔ Allow User to Continue
```

**বাস্তব কোড উদাহরণ (`package_info_plus` সহ):**

```dart
import 'package:flutter/material.dart';
import 'package:package_info_plus/package_info_plus.dart';
import 'package:url_launcher/url_launcher.dart';

Future<void> verifyAppVersion(BuildContext context) async {
  final packageInfo = await PackageInfo.fromPlatform();
  final currentVersionCode = int.tryParse(packageInfo.buildNumber) ?? 1;

  // সার্ভার বা Firebase Remote Config থেকে পাওয়া মিনিমাম দরকারি ভার্সন
  const minRequiredVersionCode = 12; 

  if (currentVersionCode < minRequiredVersionCode) {
    if (!context.mounted) return;
    
    // ব্যকগ্রাউন্ড বন্ধ করে আন-ডিসমিসেবল পপআপ দেখান
    showDialog(
      context: context,
      barrierDismissible: false,
      builder: (ctx) => WillPopScope(
        onWillPop: () async => false, // ব্যাক বাটন বন্ধ
        child: AlertDialog(
          title: const Text('গুরুত্বপূর্ণ আপডেট প্রয়োজন!'),
          content: const Text(
            'অ্যাপটির একটি নতুন সংস্করণ উপলব্ধ রয়েছে। অনুগ্রহ করে আপডেট করে অ্যাপটি ব্যবহার করুন।'
          ),
          actions: [
            ElevatedButton(
              onPressed: () {
                final storeUrl = Theme.of(context).platform == TargetPlatform.iOS
                    ? 'https://apps.apple.com/app/idYOUR_APP_ID'
                    : 'https://play.google.com/store/apps/details?id=YOUR_PACKAGE_NAME';
                launchUrl(Uri.parse(storeUrl), mode: LaunchMode.externalApplication);
              },
              child: const Text('এখনই আপডেট করুন'),
            ),
          ],
        ),
      ),
    );
  }
}
```
