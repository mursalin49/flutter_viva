# Popular Gateways - Stripe, bKash, SSLCommerz & In-App Purchase

আন্তর্জাতিক ও স্থানীয় পেমেন্ট গেটওয়ে এবং অ্যাপল/গুগল ইন-অ্যাপ পারচেস গাইড।

---

## 💳 ১. Stripe Payment Gateway (`flutter_stripe`)

### প্রশ্ন ১: Stripe Payment Sheet কীভাবে কাজ করে?

**উত্তর (ডিটেইল):**
Stripe কার্ডের তথ্য সরাসরি মার্চেন্ট অ্যাপের সার্ভারে যেতে দেয় না (PCI Compliance)। এর বদলে **PaymentSheet** ব্যবহার করা হয়:

```dart
import 'package:flutter_stripe/flutter_stripe.dart';

Future<void> makePayment() async {
  try {
    // ১. ব্যাকএন্ড থেকে পেমেন্ট ইনটেন্ট এবং ক্লায়েন্ট সিক্রেট আনুন
    final paymentIntentData = await myBackendService.createPaymentIntent(amount: 5000); // 50.00 USD

    // ২. স্ট্রাইপ পেমেন্ট শিট ইনিশিয়ালাইজ করুন
    await Stripe.instance.initPaymentSheet(
      paymentSheetParameters: SetupPaymentSheetParameters(
        paymentIntentClientSecret: paymentIntentData['client_secret'],
        merchantDisplayName: 'My Shop Ltd',
        style: ThemeMode.system,
      ),
    );

    // ৩. ইউজারের সামনে নেটিভ কার্ড ডায়ালগ ওপেন করুন
    await Stripe.instance.presentPaymentSheet();
    print('পেমেন্ট সফলভাবে সম্পন্ন হয়েছে!');
  } catch (e) {
    print('পেমেন্ট ব্যর্থ হয়েছে: $e');
  }
}
```

---

## 🇧🇩 ২. বাংলাদেশি পেমেন্ট গেটওয়ে (bKash & SSLCommerz)

### প্রশ্ন ২: bKash Tokenized Checkout কীভাবে কাজ করে?

**উত্তর (ডিটেইল):**
bKash-এর আধুনিক ইন্টিগ্রেশন ৩টি ধাপে ঘটে:
1. **Grant Token:** আপনার ব্যাকএন্ড bKash সার্ভার থেকে একটি টেম্পোরারি টোকেন নেয়।
2. **Create Payment:** অর্ডারের মূল্য দিয়ে একটি পেমেন্ট URL এবং `paymentID` তৈরি করা হয়।
3. **Webview / SDK Launch:** মোবাইল অ্যাপের ভেতরে সুরক্ষিত Webview ওপেন করা হয় যেখানে ইউজার bKash পিন ও ওটিপি দেয়।
4. **Execute Payment:** ব্যবহারকারী পিন দেওয়ার পর ব্যাকএন্ড থেকে `executePayment` API কল করে ট্রানজেকশন সফল করতে হয়।

---

## 📱 ৩. In-App Purchase (IAP) বনাম সাধারণ পেমেন্ট গেটওয়ে

### প্রশ্ন ৩: কখন Stripe/bKash ব্যবহার করবেন এবং কখন বাধ্যতামূলকভাবে Google Play Billing / Apple In-App Purchase ব্যবহার করতে হবে? (খুব জনপ্রিয় পলিসি প্রশ্ন)

| পণ্যের ধরন | অনুমোদিত পেমেন্ট গেটওয়ে | উদাহরণ |
| :--- | :--- | :--- |
| **Physical Goods (বাস্তব পণ্য/সেবা)** | নিজস্ব পেমেন্ট গেটওয়ে (Stripe, bKash, SSLCommerz, Cards)। | দারাজ থেকে কাপড় কেনা, পাঠাও রাইড বুকিং, ফুডপান্ডা খাবার ডেলিভারি। |
| **Digital Goods (ডিজিটাল কনটেন্ট/সাবস্ক্রিপশন)** | **বাধ্যতামূলকভাবে** Google Play Billing ও Apple In-App Purchase ব্যবহার করতে হবে! | Netflix/Spotify সাবস্ক্রিপশন, গেমিং কয়েন, ই-বুক আনলক করা, Tinder গোল্ড। |

> **সতর্কতা:** ডিজিটাল কনটেন্টের জন্য যদি আপনি অ্যাপের ভেতর Stripe বা বিকাশ দিয়ে ক্রেডিট কার্ডের অপশন দেন, তবে Google ও Apple আপনার অ্যাপ **তৎক্ষণাৎ রিজেক্ট বা প্লে স্টোর থেকে রিমুভ** করে দেবে (যেমনটা Epic Games / Fortnite-এর ক্ষেত্রে হয়েছিল)!
