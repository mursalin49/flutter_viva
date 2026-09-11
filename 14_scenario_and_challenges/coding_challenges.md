# Senior Live Coding & Scenario-Based Challenges - সম্পূর্ণ গাইড ও ইন্টারভিউ প্রশ্নোত্তর

টেকনিক্যাল ইন্টারভিউয়ের লাইভ কোডিং রাউন্ডে এবং মেশিন টেস্টে প্রায়ই যেসব প্র্যাকটিক্যাল কোডিং প্রবলেম সমাধান করতে দেওয়া হয়।

---

## 🔍 ১. সার্চ বারে Debounce & Throttle প্যাটার্ন

### প্রশ্ন ১: Debounce কী? সার্চ বারে প্রতি ক্যারেক্টার টাইপ করার সাথে সাথে API কল রোধ করার জন্য এটি কীভাবে লিখবেন?

**উত্তর ও লাইভ কোডিং সলিউশন:**

- **Debounce:** ইউজার যখন দ্রুত টাইপ করতে থাকে, তখন কোনো রিকোয়েস্ট পাঠানো হবে না। ইউজার টাইপিং থামিয়ে একটি নির্দিষ্ট সময় (যেমন ৫০০ মিলিসেকেন্ড) অপেক্ষা করলেই কেবলমাত্র ফাইনাল কি-ওয়ার্ড দিয়ে API কল হবে।

**Timer দিয়ে কাস্টম Debouncer ক্লাস:**

```dart
import 'dart:async';
import 'package:flutter/material.dart';

class Debouncer {
  final int milliseconds;
  Timer? _timer;

  Debouncer({this.milliseconds = 500});

  void run(VoidCallback action) {
    _timer?.cancel(); // আগের চলমান টাইমার বাতিল করুন
    _timer = Timer(Duration(milliseconds: milliseconds), action);
  }

  void dispose() {
    _timer?.cancel();
  }
}

// UI-তে ব্যবহার:
class ProductSearchScreen extends StatefulWidget {
  const ProductSearchScreen({super.key});

  @override
  State<ProductSearchScreen> createState() => _ProductSearchScreenState();
}

class _ProductSearchScreenState extends State<ProductSearchScreen> {
  final _debouncer = Debouncer(milliseconds: 500);

  void _onSearchChanged(String query) {
    if (query.trim().isEmpty) return;

    _debouncer.run(() {
      print("🔍 API Call Triggered for: $query");
      // apiService.searchProducts(query);
    });
  }

  @override
  void dispose() {
    _debouncer.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Search Products')),
      body: Padding(
        padding: const EdgeInsets.all(16.0),
        child: TextField(
          decoration: const InputDecoration(
            hintText: 'Search...',
            prefixIcon: Icon(Icons.search),
          ),
          onChanged: _onSearchChanged,
        ),
      ),
    );
  }
}
```

---

## 📜 ২. Infinite Scroll Pagination (লোড মোর)

### প্রশ্ন ২: `ScrollController` দিয়ে অফিশিয়াল উপায়ে এন্ডলেস স্ক্রলিং বা ইনফিনিট পেজিনেশন কীভাবে কোড করবেন?

**উত্তর ও লাইভ কোডিং সলিউশন:**

```dart
import 'package:flutter/material.dart';

class PaginatedUserList extends StatefulWidget {
  const PaginatedUserList({super.key});

  @override
  State<PaginatedUserList> createState() => _PaginatedUserListState();
}

class _PaginatedUserListState extends State<PaginatedUserList> {
  final ScrollController _scrollController = ScrollController();
  final List<String> _items = [];
  int _page = 1;
  bool _isLoading = false;
  bool _hasMore = true;

  @override
  void initState() {
    super.initState();
    _fetchNextPage();
    _scrollController.addListener(_onScroll);
  }

  void _onScroll() {
    // ইউজার স্ক্রলের ৮০% পার হলেই পরবর্তী পেজ লোড ট্রিগার করুন
    if (_scrollController.position.pixels >=
        _scrollController.position.maxScrollExtent * 0.8) {
      if (!_isLoading && _hasMore) {
        _fetchNextPage();
      }
    }
  }

  Future<void> _fetchNextPage() async {
    setState(() => _isLoading = true);

    // ফেক নেটওয়ার্ক লেটেন্সি
    await Future.delayed(const Duration(seconds: 2));

    if (_page > 3) {
      setState(() {
        _hasMore = false;
        _isLoading = false;
      });
      return;
    }

    final newItems = List.generate(15, (index) => "Item #Page $_page - Index $index");
    setState(() {
      _page++;
      _items.addAll(newItems);
      _isLoading = false;
    });
  }

  @override
  void dispose() {
    _scrollController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Infinite Scroll')),
      body: ListView.builder(
        controller: _scrollController,
        itemCount: _items.length + (_hasMore ? 1 : 0),
        itemBuilder: (context, index) {
          if (index == _items.length) {
            return const Padding(
              padding: EdgeInsets.all(16.0),
              child: Center(child: CircularProgressIndicator()),
            );
          }
          return ListTile(title: Text(_items[index]));
        },
      ),
    );
  }
}
```

---

## 🖼️ ৩. মেমোরি-দক্ষ ইমেজ লোডিং ও স্ক্রলিং অপ্টিমাইজেশন

### প্রশ্ন ৩: `ListView.builder`-এ অনেক বেশি বড় রেজোলিউশনের ইমেজ স্ক্রল করার সময় OOM (Out of Memory) বা ল্যাগিং রোধ করতে কী করবেন?

**উত্তর (ডিটেইল):**

1. **`memCacheWidth` ও `memCacheHeight` ব্যবহার করা:**
   - অরিজিনাল ইমেজ ৪০০০x৩০০০ হলেও মোবাইল স্ক্রিনের থাম্বনেইল হয়তো মাত্র ৩০০x৩০০। 
   - মেমোরিতে পুরো ইমেজ ডিকোড না করে সাইজ স্পেসিফাই করুন:
   ```dart
   Image.network(
     'https://example.com/image.jpg',
     cacheWidth: 300,
     cacheHeight: 300,
   );
   ```
2. **`cached_network_image` প্যাকেজ:** ডিস্ক ক্যাশিং এবং অটোমেটিক মেমোরি ইভিকশন (LRU Cache) হ্যান্ডেল করে।
3. **`ListView` অপ্টিমাইজেশন ফ্ল্যাগ:**
   - `addAutomaticKeepAlives: false` (স্ক্রিন থেকে সরে গেলে উইজেট মেমোরি ক্লিয়ার করে দেওয়া)।
   - `addRepaintBoundaries: true` (প্রতিটি আইটেমের ড্রয়িং যাতে পাশের আইটেমের উপর প্রভাব না ফেলে)।
