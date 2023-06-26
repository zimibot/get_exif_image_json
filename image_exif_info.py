import os
import exifread
from PIL import Image
from PIL.ExifTags import TAGS
import piexif
import cv2
import json
from collections import defaultdict

patterns = ["\\x00", "\\x01", "\\x02", "\\x03", "b'", "'", "\u0000"]

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bytes):
            return obj.decode('utf-8', errors='replace')
        return super().default(obj)

def get_geotagging(tags):
    geotagging = {}
    for tag in tags.keys():
        if tag.startswith('GPS'):
            geotagging[tag] = tags[tag]
    return geotagging

def get_decimal_from_dms(dms, ref):
    degrees = dms[0].num / dms[0].den
    minutes = dms[1].num / dms[1].den
    seconds = dms[2].num / dms[2].den

    decimal_degrees = degrees + (minutes / 60.0) + (seconds / 3600.0)
    if ref in ['S', 'W']:
        decimal_degrees = -decimal_degrees

    return decimal_degrees

def get_coordinates(geotags):
    lat = None
    lon = None

    if 'GPS GPSLatitude' in geotags and 'GPS GPSLatitudeRef' in geotags and 'GPS GPSLongitude' in geotags and 'GPS GPSLongitudeRef' in geotags:
        lat = get_decimal_from_dms(geotags['GPS GPSLatitude'].values, geotags['GPS GPSLatitudeRef'].values)
        lon = get_decimal_from_dms(geotags['GPS GPSLongitude'].values, geotags['GPS GPSLongitudeRef'].values)

    return lat, lon

def get_image_info_exifread(image_path):
    with open(image_path, 'rb') as f:
        tags = exifread.process_file(f, strict=True)

    image_info = {
        'Name Method': 'exifread',
        'File Name': os.path.basename(image_path),
        'File Size': os.path.getsize(image_path),
        'Extension': os.path.splitext(image_path)[1].lower()
    }

    if tags:
        geotags = get_geotagging(tags)
        if geotags:
            lat, lon = get_coordinates(geotags)
            image_info['Coordinates'] = (lat, lon)

        for tag, value in tags.items():
            tag_name = TAGS.get(tag, tag)
            if tag_name != 'JPEGThumbnail':
                image_info[tag_name] = str(value)

    return image_info

def get_image_info_piexif(image_path):
    image = Image.open(image_path)
    exif_data = image.info.get('exif')
    image_info = {
        'Name Method': 'piexif',
        'File Name': os.path.basename(image_path),
        'File Size': os.path.getsize(image_path),
        'Extension': os.path.splitext(image_path)[1].lower()
    }

    if exif_data:
        exif_dict = piexif.load(exif_data)
        if 'GPS' in exif_dict:
            gps_dict = exif_dict['GPS']
            if 'GPSLatitude' in gps_dict and 'GPSLatitudeRef' in gps_dict and 'GPSLongitude' in gps_dict and 'GPSLongitudeRef' in gps_dict:
                lat = get_decimal_from_dms(gps_dict['GPSLatitude'], gps_dict['GPSLatitudeRef'])
                lon = get_decimal_from_dms(gps_dict['GPSLongitude'], gps_dict['GPSLongitudeRef'])
                image_info['Coordinates'] = (lat, lon)

        for ifd_name in exif_dict:
            if ifd_name != 'GPS' and exif_dict[ifd_name] is not None:
                if isinstance(exif_dict[ifd_name], dict):
                    for key, value in exif_dict[ifd_name].items():
                        tag_name = TAGS.get(key, key)
                        cleaned_value = str(value).strip().replace("\\x00", "").replace("\\x01", "").replace("\\x02", "").replace("\\x03", "").replace("b'", "").replace("'", "").replace("\u0000", "")
                        image_info[tag_name] = cleaned_value
                elif isinstance(exif_dict[ifd_name], list):
                    cleaned_value = [str(val) for val in exif_dict[ifd_name]]
                    image_info[ifd_name] = cleaned_value

    return image_info

def get_image_info_pillow(image_path):
    image = Image.open(image_path)
    exif_data = image._getexif()
    image_info = {
        'Name Method': 'pillow',
        'File Name': os.path.basename(image_path),
        'File Size': os.path.getsize(image_path),
        'Image Size': image.size,
        'Image Mode': image.mode,
        'Extension': os.path.splitext(image_path)[1].lower()
    }

    if exif_data:
        for tag_id, value in exif_data.items():
            tag_name = TAGS.get(tag_id, tag_id)
            cleaned_value = str(value).strip().replace("\\x00", "").replace("\\x01", "").replace("\\x02", "").replace("\\x03", "").replace("b'", "").replace("'", "").replace("\u0000", "")
            image_info[tag_name] = cleaned_value

    return image_info

def get_image_info_opencv(image_path):
    image = cv2.imread(image_path)
    image_info = {
        'Name Method': 'openCv',
        'File Name': os.path.basename(image_path),
        'File Size': os.path.getsize(image_path),
        'Image Size': (image.shape[1], image.shape[0]),
        'Extension': os.path.splitext(image_path)[1].lower()
    }

    return image_info

def print_image_info(image_info):
    if image_info:
        for key, value in image_info.items():
            print("{}: {}".format(key, value))
    else:
        print("Tidak ada data EXIF dalam gambar.")

# Mendapatkan direktori saat ini
current_directory = os.getcwd() + "/gambar"
# Mendapatkan direktori output
output_directory = os.path.join(current_directory, "output")
# Membuat daftar file gambar dengan ekstensi yang valid
image_files = [file for file in os.listdir(current_directory) if file.endswith(('.jpg', '.jpeg', '.png', '.webp'))]

if len(image_files) > 0:
    print("Gambar yang ditemukan dalam direktori saat ini:")
    for file in image_files:
        print(file)
    print()

    grouped_info = defaultdict(lambda: defaultdict(list))

    for image_file in image_files:
        image_path = os.path.join(current_directory, image_file)
        image_info = {}

        print("Informasi untuk file {} menggunakan exifread:".format(image_file))
        image_info = get_image_info_exifread(image_path)
        print("------------------------------")
        print_image_info(image_info)
        print("==============================")
        grouped_info[image_info['Extension']][image_info['Name Method']].append(image_info)

        print("Informasi untuk file {} menggunakan piexif:".format(image_file))
        image_info = get_image_info_piexif(image_path)
        print("------------------------------")
        print_image_info(image_info)
        print("==============================")
        grouped_info[image_info['Extension']][image_info['Name Method']].append(image_info)

        print("Informasi untuk file {} menggunakan Pillow:".format(image_file))
        image_info = get_image_info_pillow(image_path)
        print("------------------------------")
        print_image_info(image_info)
        print("==============================")
        grouped_info[image_info['Extension']][image_info['Name Method']].append(image_info)

        print("Informasi untuk file {} menggunakan OpenCV:".format(image_file))
        image_info = get_image_info_opencv(image_path)
        print("------------------------------")
        print_image_info(image_info)
        print("==============================")
        grouped_info[image_info['Extension']][image_info['Name Method']].append(image_info)

    # Menyimpan informasi gambar yang dikelompokkan ke dalam file JSON
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
    json_filename = os.path.join(output_directory, "example_result.json")
    with open(json_filename, 'w') as f:
        json.dump(grouped_info, f, indent=4, cls=CustomJSONEncoder)
    print("Informasi gambar disimpan dalam file: {}".format(json_filename))

else:
    print("Tidak ada file gambar (.jpg, .jpeg, .png) dalam direktori saat ini.")
