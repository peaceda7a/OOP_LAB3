import os
import time
from datetime import datetime

class File:
    def __init__(self, filepath):
        self.filepath = filepath
        self.filename = os.path.basename(filepath)
        self.extension = os.path.splitext(filepath)[1]
        self.creation_date = datetime.fromtimestamp(os.path.getctime(filepath))
        self.last_updated = datetime.fromtimestamp(os.path.getmtime(filepath))
        self.status = "unchanged"

    def update_status(self, snapshot_time):
        if os.path.getmtime(self.filepath) > snapshot_time:
            self.status = "changed"
        else:
            self.status = "unchanged"

    def get_info(self):
        return {
            "filename": self.filename,
            "extension": self.extension,
            "creation_date": self.creation_date,
            "last_updated": self.last_updated,
        }

class TextFile(File):
    def get_info(self):
        info = super().get_info()
        with open(self.filepath, 'r', encoding='utf-8') as file:
            content = file.read()
            lines = content.splitlines()
            words = content.split()
            info.update({
                "line_count": len(lines),
                "word_count": len(words),
                "character_count": len(content),
            })
        return info

class ImageFile(File):
    def get_info(self):
        info = super().get_info()
        info.update({"dimensions": "800x600"})
        return info

class CodeFile(File):
    def get_info(self):
        info = super().get_info()
        with open(self.filepath, 'r', encoding='utf-8') as file:
            content = file.read()
            lines = content.splitlines()
            class_count = content.count("class ")
            method_count = content.count("def ")
            info.update({
                "line_count": len(lines),
                "class_count": class_count,
                "method_count": method_count,
            })
        return info

class ChangeDetectionSystem:
    def __init__(self, folder_path):
        self.folder_path = folder_path
        self.files = {}
        self.snapshot_time = time.time()
        self.scan_folder()

    def scan_folder(self):
        for filename in os.listdir(self.folder_path):
            filepath = os.path.join(self.folder_path, filename)
            if os.path.isfile(filepath):
                extension = os.path.splitext(filename)[1]
                if extension == ".txt":
                    file_obj = TextFile(filepath)
                elif extension in [".png", ".jpg"]:
                    file_obj = ImageFile(filepath)
                elif extension in [".py", ".java"]:
                    file_obj = CodeFile(filepath)
                else:
                    file_obj = File(filepath)
                self.files[filename] = file_obj

    def commit(self):
        self.snapshot_time = time.time()
        for file_obj in self.files.values():
            file_obj.status = "unchanged"
        print("Snapshot updated. All files are now 'unchanged'.")

    def info(self, filename):
        file_obj = self.files.get(filename)
        if file_obj:
            info = file_obj.get_info()
            for key, value in info.items():
                print(f"{key}: {value}")
        else:
            print(f"File '{filename}' not found.")

    def status(self):
        for file_obj in self.files.values():
            file_obj.update_status(self.snapshot_time)
            print(f"{file_obj.filename}: {file_obj.status}")

    def interactive_mode(self):
        print("Change Detection System Initialized.")
        while True:
            command = input("Enter a command (commit, info <filename>, status, exit): ").strip()
            if command == "commit":
                self.commit()
            elif command.startswith("info"):
                _, filename = command.split(maxsplit=1)
                self.info(filename)
            elif command == "status":
                self.status()
            elif command == "exit":
                print("Exiting the system.")
                break
            else:
                print("Unknown command. Please try again.")

folder_to_monitor = "./monitor_folder"
os.makedirs(folder_to_monitor, exist_ok=True)
system = ChangeDetectionSystem(folder_to_monitor)
system.interactive_mode()
