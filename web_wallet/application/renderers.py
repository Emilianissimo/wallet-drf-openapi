from rest_framework import renderers


class JSONOpenAPIRenderer(renderers.OpenAPIRenderer):
    media_type = 'application/json'
