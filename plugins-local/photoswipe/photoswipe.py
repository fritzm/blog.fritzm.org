import logging
import os
import re
import yaml

from PIL import Image
from pelican import signals

logger = logging.getLogger(__name__)

pswipe_regex = re.compile(r'(\[pswipe:([^,]+),([^.,]+)(\.[^,]+),([^\]]+)\])')
pswipe_template = """<img src='/images/{{album}}/{{image_root}}_thumbnail_tall{{image_ext}}' title='{{caption}}' onclick='pswipe("{{album}}",{{image_index}});'/>"""

def initialized(pelican):
    pelican.settings['GALLERIES'] = {}

def article_generator_finalized(generator):
    galleries = generator.context.get('GALLERIES')
    from jinja2 import Template
    template = Template(pswipe_template)
    for article in reversed(generator.articles):
        for match in pswipe_regex.findall(article._content):
            album = match[1]
            image_root = match[2]
            image_ext = match[3]
            caption = match[4]
            if album not in galleries: galleries[album] = []
            gallery = galleries[album]
            image_id = len(gallery)
            image_uri = '/images/' + album + '/' + image_root + image_ext
            image_path = os.path.join('content/images', album, image_root + image_ext)
            image = Image.open(image_path)
            image_index = next((i for (i,e) in enumerate(gallery) if e[0] == image_uri), len(gallery))
            if image_index == len(gallery): gallery.append([])
            gallery[image_index] = [image_uri, image.size, caption]
            context = generator.context.copy()
            context.update({
                'album': album,
                'image_root': image_root,
                'image_ext': image_ext,
                'caption': caption,
                'image_index': image_index
            })
            replacement = template.render(context)
            article._content = article._content.replace(match[0], replacement)

def register():
    signals.initialized.connect(initialized)
    signals.article_generator_finalized.connect(article_generator_finalized)
