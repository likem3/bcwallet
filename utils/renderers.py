from rest_framework.renderers import JSONRenderer


class DefaultJSONRenderer(JSONRenderer):
    def render(
        self,
        data,
        code=200,
        status=True,
        accepted_media_type=None,
        renderer_context=None,
    ):
        data = {"code": code, "status": status, "data": data}
        return super(DefaultJSONRenderer, self).render(
            data, code, status, accepted_media_type, renderer_context
        )
