import hashlib
import shutil
from pathlib import Path

def hash_file(path: Path, block_size: int = 65536):
    hashes = {
        'MD5': hashlib.md5(),
        'SHA1': hashlib.sha1(),
        'SHA256': hashlib.sha256(),
        'SHA512': hashlib.sha512()
    }
    with path.open('rb') as f:
        while chunk := f.read(block_size):
            for h in hashes.values():
                h.update(chunk)
    return {k: v.hexdigest() for k, v in hashes.items()}

def write_hash_report(path: Path):
    results = hash_file(path)
    with open("hash_report.txt", "w") as rpt:
        rpt.write(f"Hash report for file: {path.name}\n")
        rpt.write("="*60 + "\n")
        for name, digest in results.items():
            rpt.write(f"{name}: {digest}\n")
    print("[+] hash_report.txt created")

def create_sha256_checksum(path: Path):
    sha256 = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(65536), b''):
            sha256.update(chunk)
    line = f"{sha256.hexdigest()}  {path.name}\n"
    with open(path.name + ".sha256", "w") as cf:
        cf.write(line)
    print("[+] checksum file created:", path.name + ".sha256")

def verify_checksum(path: Path, checksum_file: Path):
    with open(checksum_file, "r") as cf:
        expected_hash = cf.readline().split()[0]
    actual_hash = hashlib.sha256(path.read_bytes()).hexdigest()
    if expected_hash == actual_hash:
        print("Checksum OK (Authentic)")
    else:
        print("Checksum FAILED (Tampered)")
        print("Expected:", expected_hash)
        print("Actual:  ", actual_hash)

def tamper_file(path: Path):
    shutil.copy2(path, "backup_" + path.name)
    with open(path, "a") as f:
        f.write("\nTampered line!!\n")
    print("[!] File tampered")

# Use a local file, e.g., example.txt
file_path = Path("example.txt")

write_hash_report(file_path)
create_sha256_checksum(file_path)
verify_checksum(file_path, Path("example.txt.sha256"))

tamper_file(file_path)
verify_checksum(file_path, Path("example.txt.sha256"))
