# Mocking, Bloc Testing & Golden Tests - সম্পূর্ণ গাইড

API ডিপেন্ডেন্সি মক করা, Bloc/Cubit-এর স্টেট ট্রানজিশন টেস্ট এবং গোল্ডেন UI টেস্ট।

---

## 🎭 ১. Mocking Dependencies (`mocktail`)

### প্রশ্ন ১: টেস্ট চালানোর সময় Mocking কেন করা হয়? `mocktail` বনাম `mockito`-এর সুবিধা কী?

**উত্তর (ডিটেইল):**
- **কেন Mocking করা হয়:** টেস্ট চালানোর সময় যদি আসল API কল বা ডেটাবেস কোয়েরি চলে, তবে ইন্টারনেট চলে গেলে টেস্ট ফেইল করবে, সার্ভারে ফেক ডেটা জমা হবে এবং টেস্ট অনেক ধীরগতির হবে। তাই ফেক বা নকল অবজেক্ট দিয়ে রেসপন্স সিমুলেট করা হয়।
- **`mocktail` এর সুবিধা:** `mockito`-তে কোড জেনারেশনের জন্য `build_runner` চালাতে হয়। `mocktail` এ কোনো `build_runner` লাগে না, সরাসরি Dart-এ মক অবজেক্ট লেখা যায়।

**Mocktail কোড উদাহরণ:**

```dart
import 'package:flutter_test/flutter_test.dart';
import 'package:mocktail/mocktail.dart';

// আসল ক্লাসের নকল মক ক্লাস তৈরি করুন
class MockUserRepository extends Mock implements UserRepository {}

void main() {
  late MockUserRepository mockRepo;

  setUp(() {
    mockRepo = MockUserRepository();
  });

  test('সফল ইউজার ফেচিং টেস্ট', () async {
    // যখন fetchUser কল হবে, তখন নকল ডেটা রিটার্ন করো
    when(() => mockRepo.getUser(1)).thenAnswer(
      (_) async => User(id: 1, name: 'Rahim'),
    );

    final user = await mockRepo.getUser(1);

    expect(user.name, 'Rahim');
    verify(() => mockRepo.getUser(1)).called(1); // মেথডটি ঠিক একবার কল হয়েছে কিনা
  });
}
```

---

## 🧱 ২. State Management Testing (`bloc_test`)

### প্রশ্ন ২: Bloc বা Cubit কীভাবে টেস্ট করতে হয়?

**উত্তর (ডিটেইল):**
`bloc_test` প্যাকেজ ব্যবহার করে একটি অ্যাকশনের ফলে কোন কোন স্টেট ক্রমানুসারে নির্গত (emit) হচ্ছে তা যাচাই করা হয়:

```dart
import 'package:bloc_test/bloc_test.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  group('CounterCubit Test', () {
    late CounterCubit cubit;

    setUp(() {
      cubit = CounterCubit();
    });

    tearDown(() {
      cubit.close();
    });

    test('প্রাথমিক স্টেট ০ হতে হবে', () {
      expect(cubit.state, 0);
    });

    blocTest<CounterCubit, int>(
      'increment কল করলে 1 নির্গত (emit) করবে',
      build: () => cubit,
      act: (cubit) => cubit.increment(),
      expect: () => [1],
    );
  });
}
```

---

## 🖼️ ৩. Golden Tests (গোল্ডেন টেস্ট)

### প্রশ্ন ৩: Golden Test কী এবং এটি কখন ব্যবহার করা হয়?

**উত্তর (ডিটেইল):**
- **Golden Test:** এটি একটি পিক্সেল-বাই-পিক্সেল ভিজ্যুয়াল রিগ্রেশন টেস্ট। 
- Flutter ফ্রেমওয়ার্ক একটি উইজেটকে মেমোরিতে রেন্ডার করে একটি রেফারেন্স ইমেজ (`.png`) ফাইলের সাথে তুলনা করে।
- যদি কোনো ডিজাইনার বা ডেভেলপার অসাবধানতাবশত বাটনের কালার, প্যাডিং বা ফন্ট সাইজ ১ পিক্সেলও পরিবর্তন করে ফেলে, তবে গোল্ডেন টেস্ট সাথে সাথে ফেইল করে আপনাকে ডিফ (Diff) ইমেজ দেখিয়ে দেবে!
