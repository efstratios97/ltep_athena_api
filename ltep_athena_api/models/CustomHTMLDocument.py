from dataclasses import dataclass
from typing import List, Optional


@dataclass
class CustomHTMLDocument:
    '''This Object represents your Custom HTML that you wish to render in your LTEP Athena Platform.
    :param str html: your html document as a string representation
    :param Optional[str] script: your optional custom script you want to execute inside your html document as a string representation
    :param Optional[str] css: your optional custom css for styling your custom html as atring representation
    :param Optional[List[str]] stylesheet_ref: your custom css ref/link to import in your custom html
    :param Optional[List[str]] javascript_library_ref: your custom javascript library import link'''
    html: str
    script: Optional[str] = None
    css: Optional[str] = None
    stylesheet_ref: Optional[List[str]] = None
    javascript_library_ref: Optional[List[str]] = None
