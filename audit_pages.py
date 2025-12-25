"""
LABBAIK AI - Page Audit Script
===============================
Run this locally to verify all pages are working.

Usage: python audit_pages.py
"""

import sys
import os

# Colors for terminal output
class Colors:
    OK = '\033[92m'      # Green
    WARN = '\033[93m'    # Yellow
    FAIL = '\033[91m'    # Red
    END = '\033[0m'      # Reset

def check_mark(status):
    if status == "ok":
        return f"{Colors.OK}✅ OK{Colors.END}"
    elif status == "warn":
        return f"{Colors.WARN}⚠️ WARN{Colors.END}"
    else:
        return f"{Colors.FAIL}❌ FAIL{Colors.END}"

def audit_pages():
    """Audit all page files and imports."""
    
    print("\n" + "="*60)
    print("🔍 LABBAIK AI - PAGE AUDIT REPORT")
    print("="*60 + "\n")
    
    # Define expected pages
    pages = {
        "home": {
            "file": "ui/pages/home.py",
            "function": "render_home_page",
            "critical": True
        },
        "chat": {
            "file": "ui/pages/chat.py", 
            "function": "render_chat_page",
            "critical": True
        },
        "simulator": {
            "file": "ui/pages/simulator.py",
            "function": "render_simulator_page", 
            "critical": True
        },
        "umrah_mandiri": {
            "file": "ui/pages/umrah_mandiri.py",
            "function": "render_umrah_mandiri_page",
            "critical": True
        },
        "umrah_bareng": {
            "file": "ui/pages/umrah_bareng.py",
            "function": "render_umrah_bareng_page",
            "critical": True
        },
        "booking": {
            "file": "ui/pages/booking.py",
            "function": "render_booking_page",
            "critical": True
        },
    }
    
    results = []
    
    for page_name, config in pages.items():
        print(f"📄 Checking: {page_name}")
        print(f"   File: {config['file']}")
        
        # Check 1: File exists
        file_exists = os.path.exists(config['file'])
        print(f"   - File exists: {check_mark('ok' if file_exists else 'fail')}")
        
        if not file_exists:
            results.append((page_name, "fail", "File not found"))
            print()
            continue
        
        # Check 2: File is not empty
        file_size = os.path.getsize(config['file'])
        print(f"   - File size: {file_size} bytes {check_mark('ok' if file_size > 100 else 'warn')}")
        
        # Check 3: Function can be imported
        try:
            module_path = config['file'].replace('/', '.').replace('.py', '')
            module = __import__(module_path, fromlist=[config['function']])
            func = getattr(module, config['function'], None)
            
            if func and callable(func):
                print(f"   - Import {config['function']}: {check_mark('ok')}")
                results.append((page_name, "ok", "All checks passed"))
            else:
                print(f"   - Import {config['function']}: {check_mark('fail')} (not callable)")
                results.append((page_name, "fail", "Function not found"))
                
        except ImportError as e:
            print(f"   - Import: {check_mark('fail')} - {str(e)[:50]}")
            results.append((page_name, "fail", f"Import error: {e}"))
        except Exception as e:
            print(f"   - Import: {check_mark('warn')} - {str(e)[:50]}")
            results.append((page_name, "warn", f"Warning: {e}"))
        
        print()
    
    # Summary
    print("="*60)
    print("📊 SUMMARY")
    print("="*60)
    
    ok_count = sum(1 for _, status, _ in results if status == "ok")
    warn_count = sum(1 for _, status, _ in results if status == "warn")
    fail_count = sum(1 for _, status, _ in results if status == "fail")
    
    print(f"   ✅ OK:   {ok_count}/{len(results)}")
    print(f"   ⚠️ WARN: {warn_count}/{len(results)}")
    print(f"   ❌ FAIL: {fail_count}/{len(results)}")
    
    if fail_count == 0:
        print(f"\n{Colors.OK}🎉 All pages are ready!{Colors.END}")
    else:
        print(f"\n{Colors.FAIL}⚠️ {fail_count} page(s) need attention{Colors.END}")
        for name, status, msg in results:
            if status == "fail":
                print(f"   - {name}: {msg}")
    
    print("\n" + "="*60 + "\n")
    
    return fail_count == 0


def audit_services():
    """Audit critical services."""
    
    print("🔧 SERVICES AUDIT")
    print("-"*40)
    
    services = [
        ("Database", "services.database.repository", "get_db"),
        ("AI Chat", "services.ai.chat_service", "UnifiedChatService"),
        ("RAG", "services.ai.rag_service", "RAGService"),
        ("Cost Calculator", "services.cost.calculator", "calculate_umrah_cost"),
        ("Price Repo", "services.price.repository", "get_price_repo"),
        ("Price Monitor", "services.price.monitoring", "get_cached_health_status"),
    ]
    
    for name, module_path, attr in services:
        try:
            module = __import__(module_path, fromlist=[attr])
            obj = getattr(module, attr, None)
            status = "ok" if obj else "warn"
            print(f"   {name}: {check_mark(status)}")
        except ImportError:
            print(f"   {name}: {check_mark('fail')} (module not found)")
        except Exception as e:
            print(f"   {name}: {check_mark('warn')} ({str(e)[:30]})")
    
    print()


def audit_env():
    """Check environment variables."""
    
    print("🔐 ENVIRONMENT CHECK")
    print("-"*40)
    
    env_vars = [
        ("DATABASE_URL", True),       # Critical
        ("GROQ_API_KEY", True),        # Critical for AI
        ("OPENAI_API_KEY", False),     # Optional fallback
        ("CHROMA_PATH", False),        # Optional
    ]
    
    for var, critical in env_vars:
        value = os.getenv(var)
        if value:
            # Mask sensitive values
            masked = value[:8] + "..." if len(value) > 8 else "***"
            print(f"   {var}: {check_mark('ok')} ({masked})")
        else:
            status = "fail" if critical else "warn"
            label = "REQUIRED" if critical else "optional"
            print(f"   {var}: {check_mark(status)} ({label})")
    
    print()


if __name__ == "__main__":
    print("\n🕋 LABBAIK AI v6.0 - System Audit\n")
    
    # Check if running from project root
    if not os.path.exists("app.py"):
        print(f"{Colors.FAIL}❌ Error: Run this script from project root directory{Colors.END}")
        print("   cd /path/to/labbaik-ai")
        print("   python audit_pages.py")
        sys.exit(1)
    
    # Run audits
    audit_env()
    audit_services()
    pages_ok = audit_pages()
    
    # Exit code
    sys.exit(0 if pages_ok else 1)