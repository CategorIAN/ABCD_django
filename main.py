# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import os

def find_null_bytes(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"):
                file_path = os.path.join(root, file)
                try:
                    with open(file_path, "rb") as f:
                        content = f.read()
                        if b'\x00' in content:
                            print(f"Null byte found in: {file_path}")
                except Exception as e:
                    print(f"Error reading {file_path}: {e}")

# Replace this with the path to your app directory




# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    find_null_bytes("C:/Users/ianho/PycharmProjects/ABCD_django/mysite")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
