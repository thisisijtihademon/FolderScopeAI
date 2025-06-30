from PIL import Image
from PIL.ExifTags import TAGS

def analyze_image_file(file_path):
    try:
        image = Image.open(file_path)
        info = image._getexif()
        metadata = {}
        if info:
            for tag, value in info.items():
                decoded = TAGS.get(tag, tag)
                metadata[decoded] = value
        return metadata if metadata else {"info": "No EXIF metadata found."}
    except Exception as e:
        return {"error": str(e)}