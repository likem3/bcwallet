import json
import logging


logger = logging.getLogger('observer')


class RequestObserverMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        body = request.body.decode('utf-8')
        response_obj = self.get_response(request)

        if response_obj.status_code not in [200, 201]:
            request_info = {
                'method': request.method,
                'body': json.loads(body) if body else {},
            }

            if 'application/json' in response_obj.headers.get('Content-Type', None):
                response_content = response_obj.content.decode('utf-8')
            else:
                response_content = ""

            response_info = {
                'status_code': response_obj.status_code,
                'content': json.loads(response_content) if response_content else {},
            }
            url = request.build_absolute_uri()

            logger.info(
                msg=f'request: {url}',
                extra={
                    'request': request_info,
                    'response': response_info
                }
            )

        return response_obj
