# -*- coding: utf-8 -*-
import re
from .pipe import Pipe
import newsman.utils.decoding as decoder

RE_META_PROP = re.compile(r'<meta property="(.+?)" content="(.+?)"', re.MULTILINE|re.DOTALL)

class Html2meta(Pipe):
    """Class for extracting information from open graph meta tags.

    Attributes:
        urlfilter: UrlFilter object for link validation.
    """

    name = 'html2meta'

    def __init__(self, config):
        """Object initialization.

        Args:
            config: Dict with configuration parameters.
        """
        pass

    def set_annotations(self, page, **kwargs):
        """Extracts image info from html code in asynchronous mode.

        Args:
            page: <Page> object.

        Returns:
            page: <Page> object.
        """

        html = page.html

        if html:

            metadata = {}
            for match in RE_META_PROP.finditer(html):

                metadata[match.group(1)] = decoder.decode(match.group(2))

            page.metadata = metadata

        return page
