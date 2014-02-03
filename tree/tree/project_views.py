import django
import json
from django.http import HttpResponse
from django.shortcuts import render


def clean_node(request, node, addr, html):
    flag = 0
    # flag used to differentiate between parent node and leaf node in template
    title = node['title']
    if node['slug'] == addr:
        if node['kind'] == 'Topic':
            flag = 1
        else:
            flag = 0
        html = render(request, 'project.html', {'title': title, 'node': node, 'flag': flag})
        return html
    else:
        if node['kind'] == 'Topic':
            for child in node['children']:
                html = clean_node(request, child, addr, html)
    	return html


# load function opens the json file
def load(request, addr):
    html = " "
    json1_file = open('json1.json')
    json1_data = json.load(json1_file)
    html = clean_node(request, json1_data, addr, html)
    return HttpResponse(html)
