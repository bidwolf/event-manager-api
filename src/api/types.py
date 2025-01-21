from dataclasses import dataclass
from http import HTTPStatus


@dataclass
class HttpRequest:
    body: dict | None
    params: dict | None = None


@dataclass
class HttpResponse:
    payload: dict
    status: HTTPStatus
