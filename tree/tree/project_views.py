import json

import django
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render


def generate(request, node, addr, html):
    if node['slug'] == addr:
	link = settings.MEDIA_URL + "styles.css"
        if node['kind'] == 'Topic':
            html = render(request, 'parent.html', {'node': node , 'link' : link })
        else:
            html = render(request, 'child.html', {'node': node , 'link' : link })
        return html
    else:
        if node['kind'] == 'Topic':
            for child in node['children']:
                html = generate(request, child, addr, html)
    	return html



# load function opens the json file
def load(request, addr):
    html = " "
    with open('json1.json', 'r') as json1_file:
        json1_data = json.load(json1_file)
        html = generate(request, json1_data, addr, html)
        return html

