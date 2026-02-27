# Force unbuffered output for immediate logging in Docker - must be first!
import os
import sys
sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', buffering=1)
sys.stderr = os.fdopen(sys.stderr.fileno(), 'w', buffering=1)

print("Starting AI News Generator cron scheduler...", flush=True)

try:
    import schedule
    import time
    import threading
    import subprocess
    from datetime import datetime
    print("✅ All imports successful", flush=True)
except ImportError as e:
    print(f"❌ IMPORT ERROR: {e}", flush=True, file=sys.stderr)
    sys.exit(1)
except Exception as e:
    print(f"❌ ERROR during imports: {e}", flush=True, file=sys.stderr)
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("=" * 50, flush=True)
print("🚀 AI News Generator — Cron Scheduler", flush=True)

try:
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    WORKDIR = SCRIPT_DIR
    os.chdir(WORKDIR)
    sys.path.append(WORKDIR)

    print(f"📁 Working directory: {WORKDIR}", flush=True)
    print(f"🐍 Python executable: {sys.executable}", flush=True)

    # ── Create required result directories on startup ──
    for d in ["result/img_match", "result/json"]:
        os.makedirs(os.path.join(WORKDIR, d), exist_ok=True)
    print("📂 Result directories verified", flush=True)

    print("=" * 50, flush=True)
except Exception as e:
    print(f"❌ ERROR during initialization: {e}", flush=True, file=sys.stderr)
    sys.exit(1)

# ── Thread-safe run lock (prevents overlapping runs) ──
_social_media_lock = threading.Lock()

def run_script(script_path):
    """Run a Python script using subprocess for proper isolation."""
    script_full_path = os.path.join(WORKDIR, script_path)
    print(f"\n{'='*50}", flush=True)
    print(f"🔄 Running {script_path}... {datetime.now()}", flush=True)
    
    if not os.path.exists(script_full_path):
        print(f"❌ Script not found: {script_full_path}", flush=True, file=sys.stderr)
        return
    
    try:
        result = subprocess.run(
            [sys.executable, script_full_path],
            cwd=WORKDIR,
            capture_output=True,
            text=True,
            timeout=3600  # 1 hour timeout
        )
        if result.stdout:
            print(f"✅ STDOUT:\n{result.stdout}", flush=True)
        if result.stderr:
            print(f"⚠️ STDERR:\n{result.stderr}", flush=True)
        if result.returncode != 0:
            print(f"❌ {script_path} exited with code {result.returncode}", flush=True)
        else:
            print(f"✅ {script_path} completed successfully", flush=True)
        print(f"{'='*50}\n", flush=True)
    except subprocess.TimeoutExpired:
        print(f"❌ {script_path} timed out after 1 hour", flush=True, file=sys.stderr)
    except Exception as e:
        print(f"❌ ERROR running {script_path}: {str(e)}", flush=True, file=sys.stderr)

def run_social_media():
    """Thread-safe wrapper — prevents overlapping pipeline runs."""
    if not _social_media_lock.acquire(blocking=False):
        print("⏭️ Social media pipeline already running, skipping this cycle.", flush=True)
        return
    try:
        run_script('social_media/main_social_media.py')
    finally:
        _social_media_lock.release()

# Run immediately on startup
print("\n📋 Running social media pipeline on startup...", flush=True)
threading.Thread(target=run_social_media, daemon=True).start()

# Schedule social media scraping every hour at :30
schedule.every().hour.at(":30").do(lambda: threading.Thread(target=run_social_media, daemon=True).start())

# Also run every 3 hours for deeper scrape
schedule.every(3).hours.do(lambda: threading.Thread(target=run_social_media, daemon=True).start())

print("\n✅ Cron scheduler initialized!", flush=True)
print("⏰ Schedule:", flush=True)
for job in schedule.jobs:
    print(f"   - {job}", flush=True)
print("=" * 50, flush=True)

try:
    while True:
        schedule.run_pending()
        time.sleep(1)
except KeyboardInterrupt:
    print("\n🛑 Cron scheduler stopped by user", flush=True)
except Exception as e:
    print(f"\n❌ FATAL ERROR: {e}", flush=True, file=sys.stderr)
    import traceback
    traceback.print_exc()
    sys.exit(1)
