from typing import List, Optional, TypedDict

from fastapi import HTTPException, status


class BaseHTTPException(HTTPException):
    status_code: int
    detail: str

    def __init__(self, detail: Optional[str] = None) -> None:
        super().__init__(status_code=self.status_code, detail=detail or self.detail)


class NotFoundHTTPException(BaseHTTPException):
    status_code = status.HTTP_404_NOT_FOUND
    detail = 'Entity not found'


class AuthenticationRequiredHTTPException(BaseHTTPException):
    status_code = status.HTTP_401_UNAUTHORIZED
    detail = 'Not authenticated'


class RequestValidationDetail(TypedDict):
    location: List[str]
    message: str
    type: Optional[str]


class RequestValidationHTTPException(BaseHTTPException):
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    detail = 'Validation error'

    def __init__(self, detail: List[RequestValidationDetail]) -> None:
        super().__init__(
            detail=[  # type: ignore
                {
                    'loc': item['location'],
                    'msg': item['message'],
                    'type': item.get('type') or 'value_error.str.condition',
                }
                for item in detail
            ]
        )


class InternalServerErrorHTTPException(BaseHTTPException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = 'Internal server error'


class DatasetManagementHTTPException(BaseHTTPException):
    status_code = status.HTTP_504_GATEWAY_TIMEOUT
    detail = 'Dataset storage not available'


class RelatedObjectsExistHTTPException(BaseHTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = 'Can\'t delete: related objects exist'


class MinimumObjectsCountDoesntMatchHTTPException(BaseHTTPException):
    status_code = status.HTTP_400_BAD_REQUEST
    detail = 'Minimum objects count in annotation set doesn\'t match'
