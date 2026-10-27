from rest_framework.views import exception_handler as drf_exception_handler


def api_exception_handler(exc, context):
    response = drf_exception_handler(exc, context)
    if response is None:
        return None

    detail = response.data.get("detail") if isinstance(response.data, dict) else None
    message = str(detail) if detail is not None else "Request failed."
    response.data = {
        "status": response.status_code,
        "message": message,
        "data": response.data,
    }
    return response
