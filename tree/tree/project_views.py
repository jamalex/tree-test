import json

import django
from django.conf import settings
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render


def load(request, addr):

    # break up the path into a list of individual slugs
    slug_list = [slug for slug in addr.strip('/').split("/") if slug]

    with open('json1.json', 'r') as json_file:

        # load the JSON data, and embed it in a dummy root node to make later logic easier
        node = {"children": [json.load(json_file)], "kind": "Topic", "title": "Content"}

        # work our way through the slugs in the path, to find the desired node in the tree
        for slug in slug_list:

            # check each of the current node's children for a matching slug
            for child in node.get("children", []):
                if child["slug"] == slug:
                    node = child
                    break

            # if we looked through all the children and didn't find a match, it's a 404
            if node["slug"] != slug:
                return HttpResponseNotFound("Path not found")

        # render the template appropriate to the selected node's kind
        return render(request, '%s.html' % node['kind'].lower(), {'node': node})
