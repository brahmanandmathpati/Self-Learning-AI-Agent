import argparse
import json
import os
import platform
import shutil
import sys

def bytes_to_gb(num_bytes):
    return round(num_bytes / (1024**3), 1)

def total_ram_gb():
    try:
        import psutil
    except ImportError:
        return None
    return bytes_to_gb(psutil.virtual_memory().total)

def collect_info():
    disk = shutil.disk_usage(os.path.abspath(os.sep))
    return {
        "os": f"{platform.system()} {platform.release()}",
        "python_version": platform.python_version(),
        "python_64bit": sys.maxsize > 2**32,
        "cpu_cores": os.cpu_count(),
        "ram_gb": total_ram_gb(),
        "free_disk_gb": bytes_to_gb(disk.free),
        "nvidia_gpu_tool_found": shutil.which("nvidia-smi") is not None,
    }

def check_minimum(info):
    warnings = []
    if info["cpu_cores"] is not None and info["cpu_cores"] < 4:
        warnings.append("Fewer than 4 CPU cores: training will be slower.")
    if info["ram_gb"] is not None and info["ram_gb"] < 8:
        warnings.append("Less than 8 GB RAM: skip the optional Ollama model.")
    if info["free_disk_gb"] < 5:
        warnings.append("Less than 5 GB free disk: free some space before installing.")
    if not info["python_64bit"]:
        warnings.append("Python is 32-bit: install 64-bit Python 3.10+.")
    return warnings

def main():
    parser = argparse.ArgumentParser(description="Print and save laptop details")
    parser.add_argument("--name", required=True, help="your first name, e.g. somesh")
    args = parser.parse_args()

    info = collect_info()
    info["warnings"] = check_minimum(info)

    for key, value in info.items():
        print(f"{key:>22}: {value}")

    file_name = f"hardware_{args.name.lower()}.json"
    with open(file_name, "w", encoding="utf-8") as f:
        json.dump(info, f, indent=2)

    print(f"\nSaved to {file_name}")

if __name__ == "__main__":
    main()
