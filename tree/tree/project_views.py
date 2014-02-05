import json

import django
from django.conf import settings
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render


def load(request, addr):

    slug_list = [slug for slug in addr.strip('/').split("/") if slug]

    with open('json1.json', 'r') as json1_file:

        node = {"children": [json.load(json1_file)], "kind": "Topic", "title": "Content"}

        for slug in slug_list:
            for child in node.get("children", []):
                if child["slug"] == slug:
                    node = child
                    break

            if node["slug"] != slug:
                return HttpResponseNotFound("Path not found")

        return render(request, '%s.html' % node['kind'].lower(), {'node': node})
