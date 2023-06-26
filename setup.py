from setuptools import setup, find_packages

setup(
    name='image_info_tool',
    version='1.0',
    description='A tool to extract EXIF information from images',
    author='Harris Munahar',
    author_email='zimibot@email.com',
    packages=find_packages(),
    install_requires=[
        'exifread',
        'Pillow',
        'piexif',
        'opencv-python',
        'json'
    ],
)
