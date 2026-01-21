import sys
import os
import subprocess

def run_diagnosis():
    print("🔍 DIAGNOSING LIVEKIT IMPORT ISSUE")
    print("=" * 50)
    
    # 1. Check Python environment
    print("1. Python Environment:")
    print(f"   Executable: {sys.executable}")
    print(f"   Version: {sys.version}")
    print(f"   Prefix: {sys.prefix}")
    
    # 2. Check if we're in a virtual environment
    print(f"   Virtual Env: {hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix)}")
    
    # 3. Check livekit package info
    print("\n2. LiveKit Package:")
    try:
        result = subprocess.run([
            sys.executable, '-m', 'pip', 'show', 'livekit-agents'
        ], capture_output=True, text=True, check=True)
        print("   " + result.stdout.replace('\n', '\n   '))
    except subprocess.CalledProcessError:
        print("   ❌ livekit-agents not found via pip")
    
    # 4. Try imports in current context
    print("\n3. Import Tests:")
    try:
        from livekit import agents
        print("   ✅ from livekit import agents - SUCCESS")
        print(f"   Agents module: {agents.__file__}")
    except ImportError as e:
        print(f"   ❌ from livekit import agents - FAILED: {e}")
    
    try:
        import livekit
        print("   ✅ import livekit - SUCCESS")
        print(f"   LiveKit module: {livekit.__file__}")
    except ImportError as e:
        print(f"   ❌ import livekit - FAILED: {e}")
    
    # 5. Check for file conflicts
    print("\n4. File Conflicts:")
    current_dir = os.path.dirname(os.path.abspath(__file__))
    suspicious_files = [f for f in os.listdir(current_dir) if 'livekit' in f.lower()]
    if suspicious_files:
        print(f"   ⚠️  Suspicious files: {suspicious_files}")
    else:
        print("   ✅ No obvious file conflicts")
    
    print("\n" + "=" * 50)

if __name__ == "__main__":
    run_diagnosis()