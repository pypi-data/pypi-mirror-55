from clean_architecture.exception import (
    BadRequestException,
    ConflictedException,
    ForbiddenException,
    MethodNotAllowedException,
    NotAcceptableException,
    NotFoundException,
    PaymentRequiredException,
    PreconditionFailedException,
    UnauthorizedException,
    UnProcessableEntityException,
)

from .response_object import ResponseFailure


class UseCase:
    def execute(self, request_object):
        if not request_object:
            return ResponseFailure.build_from_invalid_request_object(request_object)
        try:
            return self.process_request(request_object)
        except BadRequestException as e:
            return ResponseFailure.build_resource_error(
                status_code=e.status_code, error_code=e.error_code, message=e.message
            )
        except ConflictedException as e:
            return ResponseFailure.build_resource_error(
                status_code=e.status_code, error_code=e.error_code, message=e.message
            )
        except ForbiddenException as e:
            return ResponseFailure.build_resource_error(
                status_code=e.status_code, error_code=e.error_code, message=e.message
            )
        except MethodNotAllowedException as e:
            return ResponseFailure.build_resource_error(
                status_code=e.status_code, error_code=e.error_code, message=e.message
            )
        except NotAcceptableException as e:
            return ResponseFailure.build_resource_error(
                status_code=e.status_code, error_code=e.error_code, message=e.message
            )
        except NotFoundException as e:
            return ResponseFailure.build_resource_error(
                status_code=e.status_code, error_code=e.error_code, message=e.message
            )
        except PaymentRequiredException as e:
            return ResponseFailure.build_resource_error(
                status_code=e.status_code, error_code=e.error_code, message=e.message
            )
        except PreconditionFailedException as e:
            return ResponseFailure.build_resource_error(
                status_code=e.status_code, error_code=e.error_code, message=e.message
            )
        except UnauthorizedException as e:
            return ResponseFailure.build_resource_error(
                status_code=e.status_code, error_code=e.error_code, message=e.message
            )
        except UnProcessableEntityException as e:
            return ResponseFailure.build_resource_error(
                status_code=e.status_code, error_code=e.error_code, message=e.message
            )
        except Exception as exc:
            return ResponseFailure.build_system_error(
                message="{}: {}".format(exc.__class__.__name__, "{}".format(exc)))

    def process_request(self, request_object):
        raise NotImplementedError(
            "process_request() not implemented by UseCase class"
        )
