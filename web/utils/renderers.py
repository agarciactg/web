from rest_framework.renderers import JSONRenderer


class webRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        # We check to if data already contains code_transaction, if not then is default rest
        # framework response so we add custom
        if "code_transaction" not in data:
            data = {"code_transaction": "OK", "data": data}
            # Le asignamos por default codigo 200
            if "response" in renderer_context:
                renderer_context["response"].status_code = 200

        return super().render(data, accepted_media_type, renderer_context)
