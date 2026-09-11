#!/usr/bin/env python3
"""
Flutter Interview Questions & Answers - Guide Generator
Compiles 74 files across 6 categories into:
1. FLUTTER_INTERVIEW_COMPLETE_GUIDE.md (Master Markdown)
2. Flutter_Interview_Guide_Offline.html (Interactive & Printable HTML Book)
3. Flutter_Interview_Complete_Guide.pdf (Direct Offline PDF Book via Chrome Headless)
"""

import os
import re
import sys
import subprocess
import html
import markdown
from pygments.formatters import HtmlFormatter

BASE_DIR = os.path.abspath(os.path.dirname(__file__) + "/..")
OUTPUT_MD = os.path.join(BASE_DIR, "FLUTTER_INTERVIEW_COMPLETE_GUIDE.md")
OUTPUT_HTML = os.path.join(BASE_DIR, "Flutter_Interview_Guide_Offline.html")
OUTPUT_PDF = os.path.join(BASE_DIR, "Flutter_Interview_Complete_Guide.pdf")

# Structure definition with category metadata and ordered files
CHAPTERS = [
    {
        "id": "chap-01-basics",
        "title": "অধ্যায় ১: Flutter Basics (মৌলিক ধারণা)",
        "english_title": "Chapter 1: Flutter Basics",
        "badge": "Flutter Basics",
        "dir": "01_flutter_basics",
        "files": [
            ("what_is_flutter.md", "Flutter কী এবং কেন? (Introduction)"),
            ("dart_vs_flutter.md", "Dart বনাম Flutter এর সম্পর্ক"),
            ("flutter_architecture.md", "Flutter আর্কিটেকচার ও ইঞ্জিন কাঠামো"),
            ("basics_qna_01.md", "Flutter Basics - প্রশ্নোত্তর সেট ০১ (প্রশ্ন ১–১০)"),
            ("basics_qna_02.md", "Flutter Basics - প্রশ্নোত্তর সেট ০২ (প্রশ্ন ১১–২০)"),
            ("basics_qna_03.md", "Flutter Basics - প্রশ্নোত্তর সেট ০৩ (প্রশ্ন ২১–৩০)"),
            ("basics_qna_04.md", "Flutter Basics - প্রশ্নোত্তর সেট ০৪ (প্রশ্ন ৩১–৪০)"),
            ("basics_qna_05.md", "Flutter Basics - প্রশ্নোত্তর সেট ০৫ (প্রশ্ন ৪১–৫০)"),
            ("basics_qna_06.md", "Flutter Basics - প্রশ্নোত্তর সেট ০৬ (প্রশ্ন ৫১–৬০)"),
            ("basics_qna_07.md", "Flutter Basics - প্রশ্নোত্তর সেট ০৭ (প্রশ্ন ৬১–৭০)"),
            ("basics_qna_08.md", "Flutter Basics - প্রশ্নোত্তর সেট ০৮ (প্রশ্ন ৭১–৮০)"),
            ("basics_qna_09.md", "Flutter Basics - প্রশ্নোত্তর সেট ০৯ (প্রশ্ন ৮১–৯০)"),
            ("basics_qna_10.md", "Flutter Basics - প্রশ্নোত্তর সেট ১০ (প্রশ্ন ৯১–১০০)"),
        ]
    },
    {
        "id": "chap-02-state-management",
        "title": "অধ্যায় ২: State Management (স্টেট ম্যানেজমেন্ট)",
        "english_title": "Chapter 2: State Management",
        "badge": "State Management",
        "dir": "02_state_management",
        "files": [
            ("when_to_use_what.md", "কোন স্টেট ম্যানেজমেন্ট কখন ব্যবহার করবেন?"),
            ("provider_vs_bloc.md", "Provider বনাম Bloc গভীর তুলনা"),
            ("riverpod_overview.md", "Riverpod সম্পূর্ণ গাইড ও ফিচার"),
            ("sm_qna_01.md", "State Management - প্রশ্নোত্তর সেট ০১ (প্রশ্ন ১–১০)"),
            ("sm_qna_02.md", "State Management - প্রশ্নোত্তর সেট ০২ (প্রশ্ন ১১–২০)"),
            ("sm_qna_03.md", "State Management - প্রশ্নোত্তর সেট ০৩ (প্রশ্ন ২১–৩০)"),
            ("sm_qna_04.md", "State Management - প্রশ্নোত্তর সেট ০৪ (প্রশ্ন ৩১–৪০)"),
            ("sm_qna_05.md", "State Management - প্রশ্নোত্তর সেট ০৫ (প্রশ্ন ৪১–৫০)"),
            ("sm_qna_06.md", "State Management - প্রশ্নোত্তর সেট ০৬ (প্রশ্ন ৫১–৬০)"),
            ("sm_qna_07.md", "State Management - প্রশ্নোত্তর সেট ০৭ (প্রশ্ন ৬১–৭০)"),
            ("sm_qna_08.md", "State Management - প্রশ্নোত্তর সেট ০৮ (প্রশ্ন ৭১–৮০)"),
            ("sm_qna_09.md", "State Management - প্রশ্নোত্তর সেট ০৯ (প্রশ্ন ৮১–৯০)"),
            ("sm_qna_10.md", "State Management - প্রশ্নোত্তর সেট ১০ (প্রশ্ন ৯১–১০০)"),
        ]
    },
    {
        "id": "chap-03-widgets",
        "title": "অধ্যায় ৩: Widgets & UI সিস্টেম",
        "english_title": "Chapter 3: Widgets & UI System",
        "badge": "Widgets & UI",
        "dir": "03_widgets",
        "files": [
            ("stateless_vs_stateful.md", "Stateless বনাম Stateful Widget গভীর বিশ্লেষণ"),
            ("build_context_explained.md", "BuildContext কীভাবে কাজ করে?"),
            ("custom_widgets.md", "Custom Widgets তৈরি এবং অপ্টিমাইজেশন"),
            ("widgets_qna_01.md", "Widgets Q&A - সেট ০১ (প্রশ্ন ১–১৩)"),
            ("widgets_qna_02.md", "Widgets Q&A - সেট ০২ (প্রশ্ন ১৪–২৬)"),
            ("widgets_qna_03.md", "Widgets Q&A - সেট ০৩ (প্রশ্ন ২৭–৩৯)"),
            ("widgets_qna_04_bn.md", "Widgets Q&A - সেট ০৪ (প্রশ্ন ৪০–৫২)"),
            ("widgets_qna_05_bn.md", "Widgets Q&A - সেট ০৫ (প্রশ্ন ৫৩–৬৫)"),
            ("widgets_qna_06_bn.md", "Widgets Q&A - সেট ০৬ (প্রশ্ন ৬৬–৭৮)"),
            ("widgets_qna_07_bn.md", "Widgets Q&A - সেট ০৭ (প্রশ্ন ৭৯–৯১)"),
            ("widgets_qna_08_bn.md", "Widgets Q&A - সেট ০৮ (প্রশ্ন ৯২–১০৪)"),
            ("widgets_qna_09_bn.md", "Widgets Q&A - সেট ০৯ (প্রশ্ন ১০৫–১১৭)"),
            ("widgets_qna_10_bn.md", "Widgets Q&A - সেট ১০ (প্রশ্ন ১১৮–১৩০)"),
            ("widgets_qna_11_bn.md", "Widgets Q&A - সেট ১১ (প্রশ্ন ১৩১–১৪৩)"),
            ("widgets_qna_12_bn.md", "Widgets Q&A - সেট ১২ (প্রশ্ন ১৪৪–১৫৬)"),
            ("widgets_qna_13_bn.md", "Widgets Q&A - সেট ১৩ (প্রশ্ন ১৫৭–১৬৯)"),
        ]
    },
    {
        "id": "chap-04-advanced",
        "title": "অধ্যায় ৪: Advanced Flutter & Performance",
        "english_title": "Chapter 4: Advanced Flutter & Performance",
        "badge": "Advanced Flutter",
        "dir": "04_advanced",
        "files": [
            ("isolate_vs_future.md", "Isolate বনাম Future: মাল্টিথ্রেডিং ও কনকারেন্সি"),
            ("memory_leak_flutter.md", "Memory Leak শনাক্তকরণ এবং প্রতিরোধ"),
            ("performance_tips.md", "Flutter অ্যাপ পারফরম্যান্স অপ্টিমাইজেশন টিপস"),
            ("advanced_qna_01_bn.md", "Advanced Q&A - সেট ০১ (রেন্ডারিং পাইপলাইন বাংলা)"),
            ("advanced_qna_01.md", "Advanced Q&A - Rendering Pipeline (English Deep Dive)"),
            ("advanced_qna_02_bn.md", "Advanced Q&A - সেট ০২ (প্রশ্ন ৮–১৪)"),
            ("advanced_qna_03_bn.md", "Advanced Q&A - সেট ০৩ (প্রশ্ন ১৫–২১)"),
            ("advanced_qna_04_bn.md", "Advanced Q&A - সেট ০৪ (প্রশ্ন ২২–২৮)"),
            ("advanced_qna_05_bn.md", "Advanced Q&A - সেট ০৫ (প্রশ্ন ২৯–৩৫)"),
            ("advanced_qna_06_bn.md", "Advanced Q&A - সেট ০৬ (প্রশ্ন ৩৬–৪২)"),
            ("advanced_qna_07_bn.md", "Advanced Q&A - সেট ০৭ (প্রশ্ন ৪৩–৪৯)"),
        ]
    },
    {
        "id": "chap-05-dart",
        "title": "অধ্যায় ৫: Dart Language (মাস্টারিং ডার্ট)",
        "english_title": "Chapter 5: Dart Language",
        "badge": "Dart Language",
        "dir": "05_dart_questions",
        "files": [
            ("null_safety.md", "Dart Sound Null Safety পূর্ণাঙ্গ নির্দেশিকা"),
            ("async_await.md", "Asynchronous Programming: Async & Await"),
            ("future_vs_stream.md", "Future বনাম Stream এর তুলনা ও ব্যবহার"),
            ("dart_qna_01.md", "Dart Language Q&A - সেট ০১ (প্রশ্ন ১–১৩)"),
            ("dart_qna_02.md", "Dart Language Q&A - সেট ০২ (প্রশ্ন ১৪–২৬)"),
            ("dart_qna_03.md", "Dart Language Q&A - সেট ০৩ (প্রশ্ন ২৭–৩৯)"),
            ("dart_qna_04.md", "Dart Language Q&A - সেট ০৪ (প্রশ্ন ৪০–৫২)"),
            ("dart_qna_05.md", "Dart Language Q&A - সেট ০৫ (প্রশ্ন ৫৩–৬৫)"),
            ("dart_qna_06.md", "Dart Language Q&A - সেট ০৬ (প্রশ্ন ৬৬–৭৮)"),
            ("dart_qna_07.md", "Dart Language Q&A - সেট ০৭ (প্রশ্ন ৭৯–৯১)"),
            ("dart_qna_08.md", "Dart Language Q&A - সেট ০৮ (প্রশ্ন ৯২–১০৪)"),
            ("dart_qna_09.md", "Dart Language Q&A - সেট ০৯ (প্রশ্ন ১০৫–১১৭)"),
            ("dart_qna_10.md", "Dart Language Q&A - সেট ১০ (প্রশ্ন ১১৮–১৩০)"),
            ("dart_qna_11.md", "Dart Language Q&A - সেট ১১ (প্রশ্ন ১৩১–১৪৩)"),
            ("dart_qna_12.md", "Dart Language Q&A - সেট ১২ (প্রশ্ন ১৪৪–১৫৬)"),
            ("dart_qna_13.md", "Dart Language Q&A - সেট ১৩ (প্রশ্ন ১৫৭–১৬৯)"),
            ("dart_qna_14.md", "Dart Language Q&A - সেট ১৪ (প্রশ্ন ১৭০–১৮২)"),
        ]
    },
    {
        "id": "chap-06-mock-interviews",
        "title": "অধ্যায় ৬: Mock Interviews (বাস্তব ইন্টারভিউ সেশন)",
        "english_title": "Chapter 6: Real Mock Interviews",
        "badge": "Mock Interviews",
        "dir": "mock_interview",
        "files": [
            ("mock_interview_1.md", "Mock Interview ১: Junior / Mid-Level Flutter Developer"),
            ("mock_interview_2.md", "Mock Interview ২: Architecture & State Management Focus"),
            ("mock_interview_3.md", "Mock Interview ৩: Performance, Memory & Advanced Concepts"),
            ("mock_interview_4.md", "Mock Interview ৪: Real-world Scenario & Problem Solving"),
        ]
    },
    {
        "id": "chap-07-deployment",
        "title": "অধ্যায় ৭: App Deployment & Store Release (প্লে স্টোর ও অ্যাপ স্টোর)",
        "english_title": "Chapter 7: App Deployment & Store Release",
        "badge": "Deployment & Release",
        "dir": "06_deployment_and_release",
        "files": [
            ("playstore_deployment.md", "Google Play Store ডিপ্লয়মেন্ট, Keystore ও রিলিজ গাইড"),
            ("appstore_deployment.md", "Apple App Store ডিপ্লয়মেন্ট, Certificates ও TestFlight"),
            ("in_app_updates.md", "In-App Updates ও Force Update মেকানিজম"),
        ]
    },
    {
        "id": "chap-08-debugging",
        "title": "অধ্যায় ৮: Debugging, Profiling & Crash Monitoring",
        "english_title": "Chapter 8: Debugging, Profiling & Crash Monitoring",
        "badge": "Debugging & Monitoring",
        "dir": "07_debugging_and_monitoring",
        "files": [
            ("flutter_devtools.md", "Flutter DevTools - পারফরম্যান্স, মেমোরি ও CPU প্রোফাইলিং"),
            ("crashlytics_and_sentry.md", "Production Crash Reporting - Firebase Crashlytics & Sentry"),
        ]
    },
    {
        "id": "chap-09-realtime",
        "title": "অধ্যায় ৯: Real-Time Chat & Media Calling (চ্যাট ও কলিং)",
        "english_title": "Chapter 9: Real-Time Chat & Media Calling",
        "badge": "Chat & Calling",
        "dir": "08_realtime_chat_and_media",
        "files": [
            ("realtime_chat.md", "Real-Time Chatting Architecture (WebSocket, Socket.io, Firebase)"),
            ("audio_video_calling.md", "Audio & Video Calling (WebRTC, Agora, CallKit Incoming Calls)"),
        ]
    },
    {
        "id": "chap-10-location",
        "title": "অধ্যায় ১০: Background Location & Live Tracking (লাইভ ট্র্যাকিং)",
        "english_title": "Chapter 10: Background Location & Live Tracking",
        "badge": "Location & Tracking",
        "dir": "09_location_and_tracking",
        "files": [
            ("live_location_background.md", "Background Live Location Tracking ও ব্যাটারি অপ্টিমাইজেশন"),
            ("map_and_marker_animation.md", "Google Maps, Smooth Marker Animation ও রুট পলিলাইন"),
        ]
    },
    {
        "id": "chap-11-payments",
        "title": "অধ্যায় ১১: Payment Gateways & In-App Purchase (পেমেন্ট গেটওয়ে)",
        "english_title": "Chapter 11: Payment Gateways & In-App Purchase",
        "badge": "Payment Gateways",
        "dir": "10_payment_gateways",
        "files": [
            ("payment_architecture.md", "Payment Gateway Security Architecture ও Webhook ফ্লো"),
            ("popular_gateways.md", "Popular Gateways: Stripe, bKash, SSLCommerz ও In-App Purchase"),
        ]
    },
    {
        "id": "chap-12-testing",
        "title": "অধ্যায় ১২: Testing in Flutter (ইউনিট, উইজেট ও ইন্টিগ্রেশন টেস্ট)",
        "english_title": "Chapter 12: Testing in Flutter",
        "badge": "Flutter Testing",
        "dir": "11_testing_in_flutter",
        "files": [
            ("testing_overview.md", "Flutter Testing Overview - পিরামিড, উইজেট টেস্ট ও pump"),
            ("mocking_and_bloc_test.md", "Mocktail দিয়ে API মক করা, Bloc Testing ও Golden Tests"),
        ]
    }
]

def make_slug(text):
    clean = re.sub(r'[^a-zA-Z0-9\u0980-\u09FF]+', '-', text.strip().lower())
    return clean.strip('-')

def clean_file_content(content):
    lines = content.splitlines()
    return "\n".join(lines).strip()

def build():
    print(f"[*] Starting compilation from {BASE_DIR}...")
    
    total_files = 0
    for ch in CHAPTERS:
        total_files += len(ch["files"])
    print(f"[*] Total planned files: {total_files}")
    
    missing = []
    for ch in CHAPTERS:
        for fname, _ in ch["files"]:
            path = os.path.join(BASE_DIR, ch["dir"], fname)
            if not os.path.exists(path):
                missing.append(f"{ch['dir']}/{fname}")
    if missing:
        print(f"[!] Warning: Missing files: {missing}")
    else:
        print(f"[+] All {total_files} files verified and present on disk.")

    # 1. GENERATE MASTER MARKDOWN
    md_parts = []
    md_parts.append("# 📱 Complete Flutter Developer Interview Preparation Guide\n")
    md_parts.append("### 🎯 সম্পূর্ণ ফ্লাটার ও ডার্ট ইন্টারভিউ প্রস্তুতি নোট (বাংলা ও টেকনিক্যাল টার্ম)\n")
    md_parts.append("> এই মাস্টারনোটটিতে Flutter Basics, State Management, Widgets & UI, Advanced Concepts, Dart Language এবং Mock Interviews সহ সর্বমোট ৭৪টি ফাইলের ৫০০+ প্রশ্নোত্তর ও উদাহরণ সুবিন্যস্তভাবে সংকলন করা হয়েছে।\n\n---\n")
    
    # Table of Contents
    md_parts.append("## 📑 সূচিপত্র (Table of Contents)\n")
    for idx, ch in enumerate(CHAPTERS, 1):
        ch_slug = ch["id"]
        md_parts.append(f"\n### [{ch['title']}](#{ch_slug})\n")
        for fname, ftitle in ch["files"]:
            sec_slug = f"{ch['id']}-{make_slug(fname)}"
            md_parts.append(f"- [{ftitle}](#{sec_slug})")
    
    md_parts.append("\n\n---\n\n")

    # Content compilation
    html_sections = []
    
    for ch_idx, ch in enumerate(CHAPTERS, 1):
        ch_id = ch["id"]
        md_parts.append(f"\n\n# {ch['title']}\n<a id=\"{ch_id}\"></a>\n\n")
        
        ch_html = [f"<div class=\"chapter-block\" id=\"{ch_id}\">"]
        ch_html.append(f"<div class=\"chapter-header\">")
        ch_html.append(f"<span class=\"chapter-badge\">{ch['badge']}</span>")
        ch_html.append(f"<h1 class=\"chapter-title\">{html.escape(ch['title'])}</h1>")
        ch_html.append(f"<p class=\"chapter-subtitle\">{html.escape(ch['english_title'])}</p>")
        ch_html.append(f"</div>")
        
        for fname, ftitle in ch["files"]:
            fpath = os.path.join(BASE_DIR, ch["dir"], fname)
            sec_id = f"{ch['id']}-{make_slug(fname)}"
            
            with open(fpath, "r", encoding="utf-8") as f:
                content = f.read()
            
            cleaned = clean_file_content(content)
            
            # Master markdown entry
            md_parts.append(f"\n\n---\n\n## {ftitle}\n<a id=\"{sec_id}\"></a>\n\n")
            md_parts.append(cleaned)
            md_parts.append("\n\n")
            
            # HTML generation
            ch_html.append(f"<div class=\"file-section\" id=\"{sec_id}\">")
            ch_html.append(f"<div class=\"section-header-tag\"><span class=\"file-badge\">{ch['dir']}/{fname}</span></div>")
            ch_html.append(f"<h2 class=\"section-title\">{html.escape(ftitle)}</h2>")
            
            # Convert this markdown snippet to HTML
            md_exts = ['fenced_code', 'codehilite', 'tables', 'toc', 'nl2br', 'sane_lists']
            section_html = markdown.markdown(cleaned, extensions=md_exts, output_format='html5')
            
            ch_html.append(section_html)
            ch_html.append("</div>\n")
        
        ch_html.append("</div>\n")
        html_sections.append("\n".join(ch_html))

    # Write Master Markdown
    full_md = "\n".join(md_parts)
    with open(OUTPUT_MD, "w", encoding="utf-8") as f:
        f.write(full_md)
    print(f"[+] Master Markdown written to: {OUTPUT_MD} ({len(full_md.splitlines())} lines)")

    # 2. GENERATE OFFLINE PRINTABLE HTML
    pygments_css = HtmlFormatter(style='friendly').get_style_defs('.codehilite')
    
    # Build Sidebar TOC
    sidebar_links = []
    for ch in CHAPTERS:
        sidebar_links.append(f"<div class=\"toc-chapter\">")
        sidebar_links.append(f"<a href=\"#{ch['id']}\" class=\"toc-chap-link\"><strong>{html.escape(ch['title'])}</strong></a>")
        sidebar_links.append(f"<ul class=\"toc-file-list\">")
        for fname, ftitle in ch["files"]:
            sec_id = f"{ch['id']}-{make_slug(fname)}"
            sidebar_links.append(f"<li><a href=\"#{sec_id}\" class=\"toc-file-link\">{html.escape(ftitle)}</a></li>")
        sidebar_links.append(f"</ul>")
        sidebar_links.append(f"</div>")
    
    sidebar_html = "\n".join(sidebar_links)
    all_body_content = "\n".join(html_sections)
    
    full_html = f"""<!DOCTYPE html>
<html lang="bn">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Flutter Interview Complete Guide & Notes</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500&family=Hind+Siliguri:wght@400;500;600;700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
/* CSS Reset & Variables */
:root {{
  --bg-primary: #f8fafc;
  --bg-surface: #ffffff;
  --bg-sidebar: #0f172a;
  --text-primary: #1e293b;
  --text-secondary: #475569;
  --text-muted: #64748b;
  --accent-color: #0284c7;
  --accent-hover: #0369a1;
  --accent-light: #e0f2fe;
  --border-color: #e2e8f0;
  --code-bg: #1e293b;
  --code-text: #f1f5f9;
  --card-bg: #ffffff;
  --card-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.07), 0 2px 4px -2px rgb(0 0 0 / 0.05);
  --sidebar-width: 320px;
  --font-main: 'Hind Siliguri', 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  --font-mono: 'Fira Code', Consolas, Monaco, monospace;
}}

[data-theme="dark"] {{
  --bg-primary: #0b1120;
  --bg-surface: #111827;
  --bg-sidebar: #030712;
  --text-primary: #f3f4f6;
  --text-secondary: #cbd5e1;
  --text-muted: #94a3b8;
  --accent-color: #38bdf8;
  --accent-hover: #0ea5e9;
  --accent-light: #1e293b;
  --border-color: #1f2937;
  --code-bg: #030712;
  --code-text: #f9fafb;
  --card-bg: #111827;
  --card-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.3);
}}

* {{
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}}

body {{
  font-family: var(--font-main);
  background-color: var(--bg-primary);
  color: var(--text-primary);
  line-height: 1.8;
  font-size: 16px;
  -webkit-font-smoothing: antialiased;
}}

/* Top Navbar */
.topbar {{
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 64px;
  background-color: var(--bg-surface);
  border-bottom: 1px solid var(--border-color);
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 24px;
  z-index: 1000;
  box-shadow: 0 1px 3px 0 rgb(0 0 0 / 0.05);
}}

.topbar-left {{
  display: flex;
  align-items: center;
  gap: 16px;
}}

.menu-btn {{
  background: none;
  border: none;
  font-size: 20px;
  cursor: pointer;
  color: var(--text-primary);
  padding: 8px;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
}}

.logo-text {{
  font-weight: 700;
  font-size: 1.15rem;
  color: var(--accent-color);
  display: flex;
  align-items: center;
  gap: 8px;
}}

.topbar-right {{
  display: flex;
  align-items: center;
  gap: 12px;
}}

.search-input {{
  background: var(--bg-primary);
  border: 1px solid var(--border-color);
  color: var(--text-primary);
  padding: 8px 16px;
  border-radius: 8px;
  font-family: var(--font-main);
  font-size: 14px;
  width: 220px;
  transition: all 0.2s;
}}

.search-input:focus {{
  outline: none;
  border-color: var(--accent-color);
  width: 300px;
}}

.btn {{
  padding: 8px 16px;
  border-radius: 8px;
  font-family: var(--font-main);
  font-size: 14px;
  font-weight: 600;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  border: none;
  transition: background 0.2s;
}}

.btn-primary {{
  background-color: var(--accent-color);
  color: #ffffff;
}}

.btn-primary:hover {{
  background-color: var(--accent-hover);
}}

.btn-outline {{
  background-color: transparent;
  color: var(--text-primary);
  border: 1px solid var(--border-color);
}}

.btn-outline:hover {{
  background-color: var(--bg-primary);
}}

/* Layout */
.app-container {{
  display: flex;
  margin-top: 64px;
  min-height: calc(100vh - 64px);
}}

/* Sidebar */
.sidebar {{
  width: var(--sidebar-width);
  background-color: var(--bg-sidebar);
  color: #f8fafc;
  height: calc(100vh - 64px);
  position: fixed;
  top: 64px;
  left: 0;
  overflow-y: auto;
  padding: 20px 16px 40px;
  transition: transform 0.3s ease;
  z-index: 900;
}}

.sidebar::-webkit-scrollbar {{
  width: 6px;
}}
.sidebar::-webkit-scrollbar-thumb {{
  background: #334155;
  border-radius: 4px;
}}

.sidebar-title {{
  font-size: 12px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: #94a3b8;
  margin-bottom: 16px;
  padding-left: 8px;
}}

.toc-chapter {{
  margin-bottom: 20px;
}}

.toc-chap-link {{
  display: block;
  color: #f1f5f9;
  text-decoration: none;
  padding: 8px 10px;
  border-radius: 6px;
  font-size: 14px;
  line-height: 1.5;
  background: #1e293b;
  margin-bottom: 6px;
  border-left: 3px solid #38bdf8;
}}

.toc-chap-link:hover {{
  background: #334155;
}}

.toc-file-list {{
  list-style: none;
  padding-left: 12px;
}}

.toc-file-link {{
  display: block;
  color: #cbd5e1;
  text-decoration: none;
  padding: 5px 8px;
  border-radius: 4px;
  font-size: 13px;
  line-height: 1.4;
  transition: all 0.15s;
}}

.toc-file-link:hover {{
  color: #38bdf8;
  background: rgba(255, 255, 255, 0.05);
}}

/* Main Content Area */
.content-wrapper {{
  margin-left: var(--sidebar-width);
  flex: 1;
  padding: 40px 48px 100px;
  max-width: 1050px;
}}

/* Book Cover Hero */
.hero-cover {{
  background: linear-gradient(135deg, #0284c7 0%, #0369a1 50%, #075985 100%);
  color: #ffffff;
  padding: 60px 40px;
  border-radius: 16px;
  margin-bottom: 48px;
  box-shadow: 0 10px 25px -5px rgba(2, 132, 199, 0.3);
  text-align: center;
}}

.hero-cover h1 {{
  font-size: 2.4rem;
  font-weight: 800;
  line-height: 1.3;
  margin-bottom: 16px;
}}

.hero-cover p {{
  font-size: 1.2rem;
  opacity: 0.92;
  max-width: 800px;
  margin: 0 auto 24px;
}}

.hero-meta {{
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 12px;
  font-size: 14px;
}}

.meta-pill {{
  background: rgba(255, 255, 255, 0.2);
  padding: 6px 14px;
  border-radius: 20px;
  backdrop-filter: blur(4px);
}}

/* Chapter Styling */
.chapter-block {{
  margin-bottom: 60px;
}}

.chapter-header {{
  border-bottom: 3px solid var(--accent-color);
  padding-bottom: 16px;
  margin-bottom: 32px;
  padding-top: 24px;
}}

.chapter-badge {{
  display: inline-block;
  background-color: var(--accent-light);
  color: var(--accent-color);
  font-size: 13px;
  font-weight: 700;
  text-transform: uppercase;
  padding: 4px 12px;
  border-radius: 6px;
  margin-bottom: 8px;
}}

.chapter-title {{
  font-size: 2rem;
  font-weight: 700;
  color: var(--text-primary);
  line-height: 1.3;
}}

.chapter-subtitle {{
  font-size: 1rem;
  color: var(--text-muted);
  margin-top: 4px;
}}

/* File Sections */
.file-section {{
  background: var(--card-bg);
  border: 1px solid var(--border-color);
  border-radius: 12px;
  padding: 32px 36px;
  margin-bottom: 40px;
  box-shadow: var(--card-shadow);
}}

.section-header-tag {{
  margin-bottom: 12px;
}}

.file-badge {{
  font-family: var(--font-mono);
  font-size: 12px;
  color: var(--text-muted);
  background: var(--bg-primary);
  padding: 4px 8px;
  border-radius: 4px;
  border: 1px solid var(--border-color);
}}

.section-title {{
  font-size: 1.6rem;
  font-weight: 700;
  color: var(--accent-color);
  margin-bottom: 24px;
  padding-bottom: 10px;
  border-bottom: 1px solid var(--border-color);
}}

/* Markdown Headings inside sections */
.file-section h1, .file-section h2, .file-section h3, .file-section h4 {{
  color: var(--text-primary);
  margin-top: 28px;
  margin-bottom: 12px;
  line-height: 1.4;
}}

.file-section h3 {{
  font-size: 1.25rem;
  color: #0284c7;
  border-left: 4px solid var(--accent-color);
  padding-left: 12px;
  margin-top: 32px;
}}

[data-theme="dark"] .file-section h3 {{
  color: #38bdf8;
}}

.file-section p {{
  margin-bottom: 14px;
}}

.file-section ul, .file-section ol {{
  margin-bottom: 16px;
  padding-left: 24px;
}}

.file-section li {{
  margin-bottom: 6px;
}}

.file-section strong {{
  font-weight: 600;
  color: var(--text-primary);
}}

.file-section blockquote {{
  border-left: 4px solid #f59e0b;
  background: rgba(245, 158, 11, 0.08);
  padding: 14px 18px;
  border-radius: 0 8px 8px 0;
  margin: 18px 0;
  font-style: italic;
}}

.file-section hr {{
  border: none;
  border-top: 1px solid var(--border-color);
  margin: 28px 0;
}}

/* Tables */
.file-section table {{
  width: 100%;
  border-collapse: collapse;
  margin: 20px 0;
  font-size: 15px;
}}

.file-section th, .file-section td {{
  border: 1px solid var(--border-color);
  padding: 10px 14px;
  text-align: left;
}}

.file-section th {{
  background-color: var(--bg-primary);
  font-weight: 600;
}}

.file-section tr:nth-child(even) {{
  background-color: rgba(0, 0, 0, 0.02);
}}

/* Code Blocks */
.file-section pre, .codehilite pre {{
  background-color: var(--code-bg);
  color: var(--code-text);
  font-family: var(--font-mono);
  font-size: 13.5px;
  padding: 18px;
  border-radius: 8px;
  overflow-x: auto;
  line-height: 1.55;
  margin: 16px 0 20px;
  position: relative;
}}

.file-section code {{
  font-family: var(--font-mono);
  font-size: 13.5px;
  background: var(--bg-primary);
  color: #e11d48;
  padding: 2px 6px;
  border-radius: 4px;
  border: 1px solid var(--border-color);
}}

[data-theme="dark"] .file-section code {{
  color: #fb7185;
}}

.file-section pre code {{
  background: transparent;
  color: inherit;
  padding: 0;
  border: none;
}}

/* Pygments Syntax Highlighting Overrides */
{pygments_css}

/* Back to Top Floating Button */
.back-to-top {{
  position: fixed;
  bottom: 24px;
  right: 24px;
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background-color: var(--accent-color);
  color: white;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
  font-size: 18px;
  z-index: 800;
  opacity: 0.85;
  transition: all 0.2s;
}}

.back-to-top:hover {{
  opacity: 1;
  transform: translateY(-2px);
}}

/* PRINT STYLES FOR PDF */
@media print {{
  body {{
    background: #ffffff !important;
    color: #000000 !important;
    font-size: 11pt;
    line-height: 1.5;
  }}
  
  .topbar, .sidebar, .back-to-top, .search-box, .btn {{
    display: none !important;
  }}
  
  .app-container {{
    margin-top: 0 !important;
  }}
  
  .content-wrapper {{
    margin-left: 0 !important;
    padding: 0 !important;
    max-width: 100% !important;
  }}
  
  .hero-cover {{
    background: none !important;
    color: #000000 !important;
    box-shadow: none !important;
    border-bottom: 2pt solid #0284c7;
    page-break-after: always;
    padding: 40pt 0 !important;
  }}
  
  .hero-cover h1 {{
    color: #0284c7 !important;
  }}
  
  .meta-pill {{
    border: 1px solid #999;
    color: #333;
  }}
  
  .chapter-block {{
    page-break-before: always;
    margin-bottom: 30pt;
  }}
  
  .file-section {{
    border: none !important;
    box-shadow: none !important;
    padding: 10pt 0 !important;
    margin-bottom: 25pt !important;
    background: transparent !important;
  }}
  
  .section-title {{
    color: #0284c7 !important;
    border-bottom: 1pt solid #ccc;
    page-break-after: avoid;
  }}
  
  .file-section h3 {{
    color: #0369a1 !important;
    border-left: 3pt solid #0284c7 !important;
    page-break-after: avoid;
    break-after: avoid;
  }}
  
  pre, .codehilite pre {{
    background-color: #f1f5f9 !important;
    color: #0f172a !important;
    border: 1px solid #cbd5e1 !important;
    page-break-inside: avoid;
    break-inside: avoid;
  }}
  
  code {{
    color: #be123c !important;
  }}
  
  blockquote {{
    border-left: 3pt solid #d97706 !important;
    background: #fffbeb !important;
    color: #000000 !important;
  }}
  
  @page {{
    size: A4;
    margin: 18mm 15mm 18mm 15mm;
  }}
}}

@media (max-width: 900px) {{
  .sidebar {{
    transform: translateX(-100%);
  }}
  .sidebar.open {{
    transform: translateX(0);
  }}
  .content-wrapper {{
    margin-left: 0;
    padding: 24px 16px 80px;
  }}
  .search-input {{
    width: 140px;
  }}
  .search-input:focus {{
    width: 180px;
  }}
}}
</style>
</head>
<body>

<!-- Top Navigation -->
<header class="topbar">
  <div class="topbar-left">
    <button class="menu-btn" onclick="toggleSidebar()" title="সূচিপত্র টগল করুন">☰</button>
    <div class="logo-text">
      <span>🚀</span>
      <span>Flutter Interview Guide</span>
    </div>
  </div>
  <div class="topbar-right">
    <input type="text" id="searchInput" class="search-input" placeholder="টপিক বা প্রশ্ন খুঁজুন..." oninput="handleSearch()">
    <button class="btn btn-outline" onclick="toggleTheme()" title="ডার্ক / লাইট মোড টগল করুন">🌓 মোড</button>
    <button class="btn btn-primary" onclick="window.print()" title="PDF হিসেবে সেভ বা প্রিন্ট করুন">🖨️ PDF প্রিন্ট</button>
  </div>
</header>

<div class="app-container">
  <!-- Sidebar Navigation -->
  <aside class="sidebar" id="sidebar">
    <div class="sidebar-title">সূচিপত্র (Table of Contents)</div>
    {sidebar_html}
  </aside>

  <!-- Main Content -->
  <main class="content-wrapper">
    <!-- Hero Cover -->
    <div class="hero-cover">
      <h1>🚀 Flutter Developer Interview Preparation Guide</h1>
      <p>সম্পূর্ণ বাংলা গাইড ও টেকনিক্যাল প্রশ্নোত্তর সংকলন — ফ্রেশার থেকে শুরু করে অভিজ্ঞ Flutter ডেভেলপারদের জন্য এক নজরে রিভিশন নোট</p>
      <div class="hero-meta">
        <span class="meta-pill">📚 মোট ৬টি প্রধান ক্যাটাগরি</span>
        <span class="meta-pill">📑 ৭৪টি অধ্যায় ও ফাইল</span>
        <span class="meta-pill">🎯 ৫০০+ বিস্তারিত প্রশ্নোত্তর</span>
        <span class="meta-pill">💻 কোড উদাহরণ ও Interview Tips</span>
      </div>
    </div>

    <!-- All Chapters -->
    {all_body_content}
  </main>
</div>

<button class="back-to-top" onclick="window.scrollTo({{top: 0, behavior: 'smooth'}})" title="উপরে যান">↑</button>

<script>
function toggleSidebar() {{
  const sb = document.getElementById('sidebar');
  sb.classList.toggle('open');
}}

function toggleTheme() {{
  const current = document.documentElement.getAttribute('data-theme');
  const next = current === 'dark' ? 'light' : 'dark';
  document.documentElement.setAttribute('data-theme', next);
  localStorage.setItem('theme', next);
}}

// Load stored theme
const savedTheme = localStorage.getItem('theme');
if (savedTheme) {{
  document.documentElement.setAttribute('data-theme', savedTheme);
}} else if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {{
  document.documentElement.setAttribute('data-theme', 'dark');
}}

function handleSearch() {{
  const query = document.getElementById('searchInput').value.toLowerCase().trim();
  const sections = document.querySelectorAll('.file-section');
  
  sections.forEach(sec => {{
    if (!query) {{
      sec.style.display = '';
      return;
    }}
    const text = sec.innerText.toLowerCase();
    if (text.includes(query)) {{
      sec.style.display = '';
    }} else {{
      sec.style.display = 'none';
    }}
  }});
}}
</script>
</body>
</html>
"""

    with open(OUTPUT_HTML, "w", encoding="utf-8") as f:
        f.write(full_html)
    print(f"[+] Offline HTML written to: {OUTPUT_HTML}")

    # 3. GENERATE PDF DIRECTLY VIA CHROME HEADLESS
    chrome_paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"
    ]
    browser_bin = None
    for p in chrome_paths:
        if os.path.exists(p):
            browser_bin = p
            break
            
    if browser_bin:
        print(f"[*] Generating PDF using {browser_bin}...")
        cmd = [
            browser_bin,
            "--headless=new",
            "--disable-gpu",
            "--no-pdf-header-footer",
            f"--print-to-pdf={OUTPUT_PDF}",
            OUTPUT_HTML
        ]
        try:
            res = subprocess.run(cmd, capture_output=True, text=True, timeout=180)
            if os.path.exists(OUTPUT_PDF) and os.path.getsize(OUTPUT_PDF) > 1000:
                print(f"[+] PDF generated successfully: {OUTPUT_PDF} ({os.path.getsize(OUTPUT_PDF) / (1024*1024):.2f} MB)")
            else:
                print(f"[!] PDF generation completed, checking file. stderr: {res.stderr}")
        except Exception as e:
            print(f"[!] PDF generation error: {e}")
    else:
        print("[!] No Chrome or Edge executable found to generate PDF directly.")

if __name__ == "__main__":
    build()
