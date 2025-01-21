from src.api.composer.attendee import attendee_service_composer
from src.api.controllers.check_in import CheckInController, CheckInControllerInterface
from src.drivers.database.connection import connection
from src.modules.events.dao.check_in import CheckInDAO
from src.modules.events.repositories.check_in import CheckInRepository
from src.modules.events.services.check_in import CheckInService, CheckInServiceInterface


def check_in_service_composer() -> CheckInServiceInterface:
    check_in_dao = CheckInDAO(connection=connection)
    check_in_repository = CheckInRepository(dao=check_in_dao)
    attendee_service = attendee_service_composer()
    check_in_service = CheckInService(
        repository=check_in_repository, attendee_service=attendee_service
    )
    return check_in_service


def check_in_composer() -> CheckInControllerInterface:
    check_in_service = check_in_service_composer()
    controller = CheckInController(service=check_in_service)
    return controller
