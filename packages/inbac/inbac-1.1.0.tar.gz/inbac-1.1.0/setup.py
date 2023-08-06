# -*- coding: utf-8 -*-
from distutils.core import setup

packages = \
['inbac']

package_data = \
{'': ['*']}

install_requires = \
['pillow>=6.2,<7.0']

entry_points = \
{'console_scripts': ['inbac = inbac.inbac:main',
                     'test = tests.test_inbac:main']}

setup_kwargs = {
    'name': 'inbac',
    'version': '1.1.0',
    'description': 'Interactive batch cropper made for quick cropping of images.',
    'long_description': '# inbac\n\n![](https://raw.githubusercontent.com/weclaw1/inbac/master/resources/demo.gif)\n\n## Description\n\ninbac is an **in**teractive **ba**tch **c**ropper made for quick cropping of images.  \nI made this program because cropping thousands of images with image viewers or image manipulation programs was too slow.\n\n## Requirements\n- [poetry](https://github.com/sdispater/poetry)\n- tkinter\n\nAfter installing above dependencies run `poetry install` in project directory to install remaining dependencies.\n\n## Examples\n\n`poetry run inbac /home/user/pictures/`  \nOpens images in /home/user/pictures/ and saves cropped images to /home/user/pictures/crops\n\n`poetry run inbac -a 1 1 -r 256 256 /home/user/pictures/ /home/user/crops/`  \nOpens images in /home/user/pictures/ in 1:1 ratio selection mode and saves images resized to 256x256px in /home/user/crops/ \n\n## Usage\n\n```\nusage: inbac [-h] [-a ASPECT_RATIO ASPECT_RATIO] [-r RESIZE RESIZE]\n             [-s SELECTION_BOX_COLOR] [-w WINDOW_SIZE WINDOW_SIZE]\n             [-f IMAGE_FORMAT] [-q IMAGE_QUALITY]\n             [input_dir] [output_dir]\n\ninbac - interactive batch cropper\n\nLeft Mouse Button                 - select part of image\n\nZ                                 - save selection and go to the next picture\n\nX                                 - save selection and stay on the same picture\n\nRight Arrow or Right Mouse Button - go to next picture\n\nLeft Arrow or Left Mouse Button   - go to previous picture\n\npositional arguments:\n  input_dir             input directory (defaults to current working\n                        directory)\n  output_dir            output directory (defaults to folder crops in input\n                        directory)\n\noptional arguments:\n  -h, --help            show this help message and exit\n  -a ASPECT_RATIO ASPECT_RATIO, --aspect_ratio ASPECT_RATIO ASPECT_RATIO\n                        selection should have specified aspect ratio\n  -r RESIZE RESIZE, --resize RESIZE RESIZE\n                        cropped image will be resized to specified width and\n                        height\n  -s SELECTION_BOX_COLOR, --selection_box_color SELECTION_BOX_COLOR\n                        color of the selection box (default is black)\n  -w WINDOW_SIZE WINDOW_SIZE, --window_size WINDOW_SIZE WINDOW_SIZE\n                        initial window size (default is 800x600)\n  -f IMAGE_FORMAT, --image_format IMAGE_FORMAT\n                        define the croped image format\n  -q IMAGE_QUALITY, --image_quality IMAGE_QUALITY\n                        define the croped image quality\n ```\n',
    'author': 'Robert Węcławski',
    'author_email': 'r.weclawski@gmail.com',
    'url': 'https://github.com/weclaw1/inbac',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
