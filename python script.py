#this is a python scripet

import sys
import os
import hashlib

def calculate_hash(file_path):
    # Calculate the hash of a file
    hash_algorithm = hashlib.md5()
    with open(file_path, "rb") as f:
        while chunk := f.read(8192):
            hash_algorithm.update(chunk)
    return hash_algorithm.hexdigest()

def create_record(directory, record_file):
    with open(record_file, "w") as f:
        f.write(f"Directory: {directory}\n")
        for root, _, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                file_hash = calculate_hash(file_path)
                f.write(f"{file_path}: {file_hash}\n")

def compare_record(record_file):
    report = {"modified": [], "added": [], "missing": []}
    with open(record_file, "r") as f:
        lines = f.readlines()
        directory = lines[0].split(": ")[1].strip()
        for line in lines[1:]:
            file_path, file_hash = line.strip().split(": ")
            if os.path.exists(file_path):
                if calculate_hash(file_path) != file_hash:
                    report["modified"].append(file_path)
            else:
                report["missing"].append(file_path)
    
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            if file_path not in report["modified"] and file_path not in report["missing"]:
                with open(record_file, "r") as f:
                    if file_path not in f.read():
                        report["added"].append(file_path)

    return reportededed

def main():
    if len(sys.argv) == 4 and sys.argv[3] == "c":
        create_record(sys.argv[1], sys.argv[2])
        print("Tripwire record created successfully.")
    elif len(sys.argv) == 3:
        report = compare_record(sys.argv[1])
        print("Tripwire Report:")
        print("Modified Files:")
        for file in report["modified"]:
            print(file)
        print("\nAdded Files:")
        for file in report["added"]:
            print(file)
        print("\nMissing Files:")
        for file in report["missing"]:
            print(file)
    else:
        print("Invalid arguments. Usage:")
        print("To create a tripwire record: python tripwire.py tripwireDir tripwireRecord c")
        print("To compare with a tripwire record: python tripwire.py tripwireRecord")

if __name__ == "__main__":
    main()
print("hello world")
