# Force unbuffered output for immediate logging in Docker - must be first!
import os
import sys
sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', buffering=1)
sys.stderr = os.fdopen(sys.stderr.fileno(), 'w', buffering=1)

print("Starting cron scheduler...", flush=True)

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
print("🚀 Cron scheduler starting...", flush=True)

try:
    # Get the working directory - should be /app when running in Docker
    SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
    WORKDIR = SCRIPT_DIR  # cron_all.py is in the same directory as the sub-scripts
    os.chdir(WORKDIR)  # Ensure we're in the correct directory
    sys.path.append(WORKDIR)

    print(f"📁 Working directory: {WORKDIR}", flush=True)
    print(f"🐍 Python executable: {sys.executable}", flush=True)
    print(f"📝 Script directory: {SCRIPT_DIR}", flush=True)
    print(f"📂 Current directory: {os.getcwd()}", flush=True)
    print("=" * 50, flush=True)
except Exception as e:
    print(f"❌ ERROR during initialization: {e}", flush=True, file=sys.stderr)
    sys.exit(1)

def run_script(script_path):
    """Run a Python script using subprocess for proper isolation and error handling."""
    script_full_path = os.path.join(WORKDIR, script_path)
    print(f"\n{'='*50}", flush=True)
    print(f"🔄 Running {script_path}... {datetime.now()}", flush=True)
    print(f"📄 Full path: {script_full_path}", flush=True)
    
    # Check if script exists
    if not os.path.exists(script_full_path):
        print(f"❌ ERROR: Script not found: {script_full_path}", flush=True, file=sys.stderr)
        return
    
    try:
        result = subprocess.run(
            [sys.executable, script_full_path],
            cwd=WORKDIR,
            capture_output=True,
            text=True,
            timeout=3600  # 1 hour timeout per script
        )
        if result.stdout:
            print(f"✅ STDOUT from {script_path}:\n{result.stdout}", flush=True)
        if result.stderr:
            print(f"⚠️ STDERR from {script_path}:\n{result.stderr}", flush=True)
        if result.returncode != 0:
            print(f"❌ ERROR: {script_path} exited with code {result.returncode}", flush=True, file=sys.stderr)
        else:
            print(f"✅ {script_path} completed successfully", flush=True)
        print(f"{'='*50}\n", flush=True)
    except subprocess.TimeoutExpired:
        print(f"❌ ERROR: {script_path} timed out after 1 hour", flush=True, file=sys.stderr)
    except Exception as e:
        print(f"❌ ERROR running {script_path}: {str(e)}", flush=True, file=sys.stderr)
        import traceback
        traceback.print_exc()

def run_transfer():
    run_script('transfer/main_transfer.py')

def run_rumour():
    run_script('rumour/main_rumour.py')

def run_abroad_player():
    run_script('player_abroad/main_player_abroad.py')

def run_preview():
    run_script('preview/main_preview.py')

def run_review():
    run_script('review/main_review.py')

def run_social_media():
    run_script('social_media/main_social_media.py')

def run_where_to_watch():
    run_script('where_to_watch/main_where_to_watch.py')

# Lock to prevent concurrent authentication requests
auth_lock = threading.Lock()

def run_all_jobs():
    """Run all jobs with 1-minute delays between each to avoid rate limiting on Strapi API"""
    jobs = [
        ('transfer', run_transfer),
        ('rumour', run_rumour),
        ('player_abroad', run_abroad_player),
        ('preview', run_preview),
        ('review', run_review),
        # ('social_media', run_social_media),
        ('where_to_watch', run_where_to_watch),
    ]
    
    # Start jobs with 1-minute delays between each (60 seconds = 1 minute)
    for index, (name, job_func) in enumerate(jobs):
        delay_seconds = index * 60  # 0, 60, 120, 180, 240, 300 seconds (0, 1, 2, 3, 4, 5 minutes)
        delay_minutes = index
        
        if delay_seconds > 0:
            print(f"⏳ Scheduling {name} to start in {delay_minutes} minute(s) ({delay_seconds} seconds)...", flush=True)
        
        def start_job(delay_seconds, name, func):
            if delay_seconds > 0:
                print(f"⏳ Waiting {delay_seconds} seconds before starting {name}...", flush=True)
                time.sleep(delay_seconds)
            print(f"🚀 Starting {name} job...", flush=True)
            func()
        
        thread = threading.Thread(target=start_job, args=(delay_seconds, name, job_func))
        thread.start()

# Run all jobs with 1-minute delay between each to prevent API rate limiting
print("\n📋 Starting all jobs with 1-minute delays between each job...", flush=True)
run_all_jobs()

# Schedule transfer and rumour every 30 minutes
schedule.every().hour.at(":55").do(lambda: threading.Thread(target=run_transfer).start())
schedule.every().hour.at(":55").do(lambda: threading.Thread(target=run_rumour).start())

# Schedule abroad player every 1.5 hours (90 minutes)
schedule.every().hour.at(":25").do(lambda: threading.Thread(target=run_abroad_player).start())

# Schedule preview and review every hour (unchanged, or adjust as needed)
# schedule.every().hour.do(lambda: threading.Thread(target=run_preview).start())
schedule.every(10).minutes.do(lambda: threading.Thread(target=run_review).start())

schedule.every().hour.at(":55").do(lambda: threading.Thread(target=run_preview).start())
schedule.every().day.do(lambda: threading.Thread(target=run_where_to_watch).start())
# schedule.every().hour.at(":55").do(lambda: threading.Thread(target=run_social_media).start())


# Schedule the job every hour
# schedule.every().hour.do(run_all_jobs)

print("\n✅ Cron scheduler initialized successfully!", flush=True)
print("⏰ Waiting for scheduled jobs to run...", flush=True)
print(f"📅 Next scheduled jobs:", flush=True)
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
    print(f"\n❌ FATAL ERROR in scheduler loop: {e}", flush=True, file=sys.stderr)
    import traceback
    traceback.print_exc()
    sys.exit(1)
