import os
import re
import sys
from pathlib import Path
from PIL import Image, ExifTags, ImageOps
import piexif
from typing import Tuple

def convert_to_webp(img_dir):
  for root, _, files in os.walk(img_dir):
    for f in files:
      if f.endswith(".jpg") or f.endswith(".jpeg") or f.endswith(".png"):

        img_path = os.path.join(root, f)
        image = Image.open(img_path)

        # Find orientation tag 
        orientation = None
        for key in ExifTags.TAGS.keys():
          if ExifTags.TAGS[key] == 'Orientation':
            orientation = key
            break

        exif = image.getexif()

        if orientation and orientation in exif:
          if exif[orientation] == 3:
            image = image.rotate(180, expand=True)
          elif exif[orientation] == 6:
            image = image.rotate(270, expand=True)  
          elif exif[orientation] == 8:
            image = image.rotate(90, expand=True)

        webp_img = image.convert("RGBA")  

        webp_path = f"{img_path.rsplit('.', 1)[0]}.webp"
        webp_img.save(webp_path)

def update_references(directory=".", exclude_exts=[]):
  for root, dirs, files in os.walk(directory):
    for file in files:
      if file.lower().endswith((".js", ".jsx", ".ts", ".tsx")):
        file_path = os.path.join(root, file)

        try:
          with open(file_path, 'r') as f:
            content = f.read()

          # Search for image references
          patterns = [
            re.compile(r'"\s*(.+)(.jpg)"'), 
            re.compile(r'"\s*(.+)(.png)"'),
            re.compile(r'"\s*(.+)(.jpeg)"'),
            re.compile(r'src="(.+)(.jpg|jpeg|png)"')
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