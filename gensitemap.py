import os
import time
import re

from lxml import etree

EXTENSIONS = [".html"]
BASE_URL_PATH = "http://jedidjah.ch/"
HTML_DIR = "_build"
DEFAULT_FREQ = "never"
DEFAULT_PRIORITY = "0.5"



class UrlEntry(object):

    def __init__(self, root, filename):
        self.root = root
        self.filename = filename

    def get_loc(self):
        """Build and return the <loc> element."""
        xml = etree.Element('loc')
        url_parts = [BASE_URL_PATH, self.root[2:]]
        if self.root == '.' and self.filename == 'index.html':
            pass
        elif self.filename == 'index.html':
            url_parts.append('/')
        else:
            url_parts.append('/%s' % self.filename)
        xml.text = ''.join(url_parts)
        return xml

    def get_lastmod(self):
        """Build and return the <lastmod> element."""
        xml = etree.Element('lastmod')
        filepath = os.path.join(self.root, self.filename)
        modtime = os.path.getmtime(filepath)
        xml.text = time.strftime('%Y-%m-%d', time.localtime(modtime))
        return xml

    def get_changefreq(self):
        """Build and return the <changefreq> element."""
        xml = etree.Element('changefreq')
        xml.text = 'never'
        return xml

    def get_priority(self):
        xml = etree.Element('priority')
        if self.root in ['.', './about']:
            xml.text = '0.9'
        elif re.match(r'\.\/\d{4}\/\d{1,2}\/\d{1,2}\/.+', self.root):
            xml.text = '0.8'
        else:
            xml.text = '0.5'
        return xml

    def element(self):
        xml = etree.Element('url')
        xml.append(self.get_loc())
        xml.append(self.get_lastmod())
        xml.append(self.get_changefreq())
        xml.append(self.get_priority())
        return xml


class Sitemap(object):

    def __init__(self):
        self.root = etree.Element('urlset',
                xmlns='http://www.sitemaps.org/schemas/sitemap/0.9')

    def add_url(self, url):
        self.root.append(url)

    def to_string(self):
        return etree.tostring(self.root, xml_declaration=True,
                encoding='utf-8', pretty_print=True)


if __name__ == '__main__':
    os.chdir(HTML_DIR)
    sitemap = Sitemap()
    for root, dirs, files in os.walk('.'):
        for filename in files:
            if os.path.splitext(filename)[1] in EXTENSIONS:
                sitemap.add_url(UrlEntry(root, filename).element())
    print sitemap.to_string()
