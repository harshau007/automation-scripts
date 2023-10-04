import os
import re
import sys
import shutil
from pathlib import Path

from PIL import Image, UnidentifiedImageError


def convert_to_webp(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file.lower().endswith((".png", ".jpg", ".jpeg")):
                input_path = os.path.join(root, file)
                output_path = os.path.join(root, Path(file).stem + ".webp")

                try:
                    img = Image.open(input_path)
                    img.save(output_path, "WEBP")
                    print(f"Converted {input_path} to {output_path}")
                except (OSError, UnidentifiedImageError) as err:
                    print(f"Error converting {input_path}: {err}")


def update_references(directory=".", exclude_exts=[]):
  image_extensions = [".png", ".jpg", ".jpeg"]


  for root, dirs, files in os.walk(directory):
    for file in files:
      if file.lower().endswith((".js", ".jsx", ".ts", ".tsx", ".py", ".html")):
        file_path = os.path.join(root, file)

        try:
          with open(file_path, 'r') as f:
            content = f.read()

          # Search for image references
          patterns = [
            re.compile(r'"\s*(.+)(.jpg)"'), 
            re.compile(r'"\s*(.+)(.png)"'),
            re.compile(r'"\s*(.+)(.jpeg)"')
          ]

          for pattern in patterns:
            matches = pattern.findall(content)

            if matches:
              for match in matches:
                old_path = match[0] + match[1]
                filename = os.path.basename(old_path)

                if not any(filename.endswith(ext) for ext in exclude_exts):
                  filename = os.path.splitext(filename)[0] + ".webp"

                new_path = os.path.join(os.path.dirname(old_path), filename)  
                content = content.replace(old_path, new_path)
          with open(file_path, 'w') as f:
            f.write(content)

        except OSError as err:
          print(f"Error updating {file_path}: {err}")

def delete_images_by_ext(repo_path):
  for root, dirs, files in os.walk(repo_path):
    for file in files:
      if file.endswith('.png') or file.endswith('.jpg') or file.endswith('.jpeg'):
        os.remove(os.path.join(root, file))

def main():
  dir_path = "." if len(sys.argv) == 1 else sys.argv[1]

  convert_to_webp(dir_path)
  exclude_exts = ['.svg']
  update_references(dir_path) 
  delete_images_by_ext(dir_path)
    
if __name__ == "__main__":
    main()