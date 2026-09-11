# Clean Architecture ও Design Patterns - সম্পূর্ণ গাইড ও ইন্টারভিউ প্রশ্নোত্তর

Flutter এন্টারপ্রাইজ অ্যাপ্লিকেশনে কোডবেস বড় হওয়ার সাথে সাথে কোডের স্কেলাবিলিটি, টেস্টেবিলিটি ও রক্ষণাবেক্ষণ নিশ্চিত করার আর্কিটেকচার।

---

## 🏛️ ১. Clean Architecture Overview

Uncle Bob-এর Clean Architecture-এর মূল উদ্দেশ্য হলো: **বিজনেস লজিককে কোনো ফ্রেমওয়ার্ক বা এক্সটার্নাল লাইব্রেরির ওপর নির্ভরশীল না রাখা (Separation of Concerns)।**

```
┌─────────────────────────────────────────────────────────────┐
│ 1. Presentation Layer (UI, Pages, Widgets, Bloc / Riverpod) │
└──────────────────────────────┬──────────────────────────────┘
                               ▼ (ডিপেন্ড করে)
┌─────────────────────────────────────────────────────────────┐
│ 2. Domain Layer (Entities, UseCases, Repository Interface)  │  <-- পিউর Dart, Flutter-স্বাধীন
└──────────────────────────────▲──────────────────────────────┘
                               │ (ইমপ্লিমেন্ট করে)
┌──────────────────────────────┴──────────────────────────────┐
│ 3. Data Layer (DataSources, Models, Repository Impl)        │
└─────────────────────────────────────────────────────────────┘
```

---

### প্রশ্ন ১: Clean Architecture-এর ৩টি লেয়ারের দায়িত্ব কী এবং Domain Layer কেন সবচেয়ে গুরুত্বপূর্ণ?

**উত্তর (ডিটেইল):**

1. **Domain Layer (The Core):**
   - এটি অ্যাপের মূল বিজনেস লজিক বহন করে।
   - **সবচেয়ে গুরুত্বপূর্ণ বৈশিষ্ট্য:** এতে কোনো Flutter বা বাহ্যিক প্যাকেজের ইম্পোর্ট থাকে না (পিউর Dart)। ফলে Flutter ফ্রেমওয়ার্ক পরিবর্তন হলেও বিজনেস লজিকে কোনো হাত দিতে হয় না।
   - উপাদান:
     - **Entity:** অ্যাপের ডেটা মডেলের কোর রূপ (যেমন: `User` ক্লাস)।
     - **UseCase:** নির্দিষ্ট একক কাজ (যেমন: `GetUserProfileUseCase`, `LoginUseCase`)।
     - **Repository Interface:** ডেটা পাওয়ার চুক্তি বা অ্যাবস্ট্রাকশন (যেমন: `abstract class AuthRepository`)।

2. **Data Layer:**
   - ডেটা কোথা থেকে আসবে এবং কীভাবে রূপান্তর হবে তা নির্ধারণ করে।
   - উপাদান:
     - **Model:** Entity-কে এক্সটেন্ড করে এবং JSON Serialization (`fromJson`, `toJson`) হ্যান্ডেল করে।
     - **DataSource:**
       - *RemoteDataSource:* REST API (Dio/Http) বা Firebase কল করে।
       - *LocalDataSource:* Shared Preferences, Hive বা SQLite থেকে ডেটা আনে/রাখে।
     - **Repository Implementation:** Domain-এর অ্যাবস্ট্রাক্ট রিপোজিটরিকে বাস্তবায়ন করে এবং নেটওয়ার্ক চেক করে ক্যাশ বনাম রিমোট ডেটা রিটার্ন করে।

3. **Presentation Layer:**
   - ব্যবহারকারীর সাথে ইন্টারঅ্যাকশন ও স্ক্রিনে ডেটা দেখানো।
   - উপাদান: UI Screens, Widgets, এবং State Management (Bloc/Cubit, Riverpod, বা ViewModel)।

**Interview Tips:** ভাইভায় মনে রাখবেন—"Dependency Rule: বাইরের লেয়ারগুলো ভেতরের লেয়ারকে চেনে, কিন্তু ভেতরের লেয়ার (Domain) বাইরের কোনো লেয়ারকে চেনে না।"

---

### প্রশ্ন ২: Entity বনাম Model-এর পার্থক্য কী? কেন একই ক্লাসে সব রাখা হয় না?

**উত্তর (ডিটেইল):**

| বৈশিষ্ট্য | Entity | Model |
| :--- | :--- | :--- |
| **লেয়ার** | Domain Layer | Data Layer |
| **লাইব্রেরি নির্ভরতা** | কোনো থার্ড পার্টি প্যাকেজ থাকে না (পিউর ডার্ট)। | `json_serializable`, `freezed` বা `equatable` থাকতে পারে। |
| **ফাংশনালিটি** | শুধুমাত্র ফিল্ডস ও বিজনেস লজিক। | `fromJson()`, `toJson()`, `toEntity()` মেথড থাকে। |
| **পরিবর্তনশীলতা** | ব্যাকএন্ডের API রেসপন্স পরিবর্তন হলেও Entity অপরিবর্তিত থাকে। | API-এর রেসপন্স কী বদলালে শুধু Model বদলায়। |

**উদাহরণ:**
```dart
// Domain Layer: Entity
class UserEntity {
  final String id;
  final String fullName;
  final String email;

  const UserEntity({required this.id, required this.fullName, required this.email});
}

// Data Layer: Model
class UserModel extends UserEntity {
  const UserModel({required super.id, required super.fullName, required super.email});

  factory UserModel.fromJson(Map<String, dynamic> json) {
    return UserModel(
      id: json['_id'] ?? '',
      fullName: json['name'] ?? '',
      email: json['email_address'] ?? '',
    );
  }

  Map<String, dynamic> toJson() => {
    '_id': id,
    'name': fullName,
    'email_address': email,
  };
}
```

---

## 🧩 ২. Design Patterns & Dependency Injection

### প্রশ্ন ৩: Repository Pattern কী এবং এটি ব্যবহারের সুবিধা কী?

**উত্তর (ডিটেইল):**
Repository Pattern হলো ডেটা সোর্স (API, Database, Cache) এবং বিজনেস লজিকের মধ্যে একটি মধ্যস্থতাকারী (Mediator) লেয়ার।

**সুবিধা:**
1. **ডিকাপলিং:** আপনার UI বা UseCase জানে না ডেটা কি সরাসরি সার্ভার থেকে এলো নাকি লোকাল SQLite থেকে।
2. **টেস্টিং সুবিধা:** রিপোজিটরি অ্যাবস্ট্রাক্ট হওয়ার কারণে সহজেই Unit Test-এ Fake বা Mock Repository ইনজেক্ট করা যায়।
3. **ক্যাশিং ম্যানেজমেন্ট:** অফলাইন সাপোর্ট দেওয়ার জন্য রিপোজিটরির ভেতরেই ডিসিশন নেওয়া যায়: নেটওয়ার্ক থাকলে API কল করে লোকাল ডিবি আপডেট করো, না থাকলে লোকাল ডেটা দাও।

---

### প্রশ্ন ৪: Dependency Injection (DI) কী এবং `get_it` কীভাবে কাজ করে?

**উত্তর (ডিটেইল):**
Dependency Injection হলো এমন একটি কৌশল যেখানে একটি অবজেক্ট তার প্রয়োজনীয় অন্যান্য ডিপেনডেন্সি নিজে তৈরি (instantiate) না করে বাইরে থেকে গ্রহণ করে (Inversion of Control)।

`get_it` হলো ডার্টের একটি অত্যন্ত জনপ্রিয় **Service Locator**।

**কেন সরাসরি `new ApiClient()` করব না?**
যদি কোনো ক্লাসের ভেতরে হার্ডকোড করে ডিপেনডেন্সি তৈরি করা হয়, তবে ওই ক্লাসকে আলাদা করে ইউনিট টেস্ট করা অসম্ভব হয়ে যায়।

**`get_it` ব্যবহারের বাস্তব উদাহরণ:**
```dart
import 'package:get_it/get_it.dart';

final sl = GetIt.instance; // sl = Service Locator

void initLocator() {
  // ১. External / Network Clients (Singleton)
  sl.registerLazySingleton<Dio>(() => Dio());

  // ২. DataSources
  sl.registerLazySingleton<AuthRemoteDataSource>(
    () => AuthRemoteDataSourceImpl(dio: sl()),
  );

  // ৩. Repositories
  sl.registerLazySingleton<AuthRepository>(
    () => AuthRepositoryImpl(remoteDataSource: sl()),
  );

  // ৪. UseCases
  sl.registerLazySingleton(() => LoginUseCase(sl()));

  // ৫. Blocs / Cubits (Factory - প্রতিবার নতুন ইন্সট্যান্স)
  sl.registerFactory(() => AuthBloc(loginUseCase: sl()));
}
```

> **Interview Tips:** `registerLazySingleton` কেবল তখনই ইন্সট্যান্স তৈরি করে যখন প্রথমবার এটিকে কল করা হয়। আর `registerFactory` প্রতিবার কল করার সময় একটি নতুন ফ্রেশ অবজেক্ট রিটার্ন করে (Bloc/Controller-এর জন্য উপযুক্ত)।
