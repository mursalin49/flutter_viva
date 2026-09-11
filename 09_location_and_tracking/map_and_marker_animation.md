# Google Maps & Smooth Marker Animation

ম্যাপে গাড়ির আইকন মসৃণভাবে মুভ করানো, দিক পরিবর্তন (Bearing) এবং রুট পলিলাইন আঁকা।

---

## 🚗 ১. স্মুথ মার্কার অ্যানিমেশন (Marker Interpolation)

### প্রশ্ন ১: Uber বা Pathao অ্যাপে গাড়িটি এক পয়েন্ট থেকে অন্য পয়েন্টে যাওয়ার সময় লাফিয়ে (Jump) না গিয়ে স্মুথলি কীভাবে গড়ায়?

**উত্তর (ডিটেইল):**
জিপিএস থেকে ডেটা আসে প্রতি ২-৫ সেকেন্ড পর পর বিচ্ছিন্ন কো-অর্ডিনেট (Discrete Points) হিসেবে। যদি সরাসরি মার্কারের পজিশন আপডেট করে দেন, তবে গাড়িটি হঠাৎ হঠাৎ লাফিয়ে নতুন জায়গায় চলে যাবে।

**সমাধান: Linear Interpolation (`lerp`) & `AnimationController`:**
পুরোনো পয়েন্ট `A` থেকে নতুন পয়েন্ট `B`-এর মাঝখানের পথটিকে একটি `Tween` অ্যানিমেশনের মাধ্যমে ৫০-১০০টি ছোট ছোট পয়েন্টে বিভক্ত করে প্রতি ফ্রেমে মার্কারের পজিশন আপডেট করা হয়:

```dart
// দুটি ল্যাটিচ্যুড/লংগিচ্যুডের মধ্যে মসৃণ মান বের করার গণিত
double lerp(double start, double end, double fraction) {
  return start + (end - start) * fraction;
}

LatLng interpolateLatLng(LatLng start, LatLng end, double fraction) {
  return LatLng(
    lerp(start.latitude, end.latitude, fraction),
    lerp(start.longitude, end.longitude, fraction),
  );
}
```

---

### প্রশ্ন ২: গাড়ি ঘোরার সময় গাড়ির মুখ (Bearing / Rotation Angle) কীভাবে ঠিক রাখবেন?

**উত্তর (ডিটেইল):**
গাড়ি যেদিকে যাচ্ছে, মার্কার আইকনটির মুখও সেদিকে ঘোরানো দরকার। এর জন্য পূর্বের পয়েন্ট এবং বর্তমান পয়েন্টের মধ্যে কোণ (Bearing/Heading) হিসাব করা হয়:

```dart
import 'dart:math' as math;

double calculateBearing(LatLng start, LatLng end) {
  double startLat = start.latitude * (math.pi / 180);
  double startLng = start.longitude * (math.pi / 180);
  double endLat = end.latitude * (math.pi / 180);
  double endLng = end.longitude * (math.pi / 180);

  double dLng = endLng - startLng;

  double y = math.sin(dLng) * math.cos(endLat);
  double x = math.cos(startLat) * math.sin(endLat) -
      math.sin(startLat) * math.cos(endLat) * math.cos(dLng);

  double heading = math.atan2(y, x);
  return (heading * (180 / math.pi) + 360) % 360; // 0 to 360 degrees
}
```

---

## 🗺️ ২. রুট পলিলাইন (Route Polylines)

### প্রশ্ন ৩: পিকআপ লোকেশন থেকে ড্রপ-অফ লোকেশন পর্যন্ত রাস্তার রুট (Polyline) কীভাবে আঁকা হয়?

**উত্তর (ডিটেইল):**
1. ব্যবহারকারীর পিকআপ এবং ড্রপ-অফ কো-অর্ডিনেট দিয়ে **Google Directions API**-তে কল করা হয়।
2. API রেসপন্সে একটি এনকোডেড স্ট্রিং (`overview_polyline.points`) ফেরত আসে।
3. প্যাকেজ `flutter_polyline_points` ব্যবহার করে সেই স্ট্রিংটিকে ডিকোড করে `List<LatLng>` তৈরি করা হয়।
4. `GoogleMap` উইজেটের `polylines` প্রোপার্টিতে একটি `Polyline` সেট করে দিলে ম্যাপের রাস্তার উপর নীল দাগ দিয়ে রুট প্রদর্শিত হয়।
