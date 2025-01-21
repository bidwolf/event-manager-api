from src.api.composer.event import event_service_composer
from src.api.controllers.attendee import AttendeeController, AttendeeControllerInterface
from src.drivers.database.connection import connection
from src.modules.events.dao.attendee import AttendeeDAO
from src.modules.events.repositories.attendee import AttendeeRepository
from src.modules.events.services.attendee import (
    AttendeeService,
    AttendeeServiceInterface,
)


def attendee_service_composer() -> AttendeeServiceInterface:
    attendee_dao = AttendeeDAO(connection=connection)
    attendee_repository = AttendeeRepository(dao=attendee_dao)
    event_service = event_service_composer()
    attendee_service = AttendeeService(
        event_service=event_service, repository=attendee_repository
    )
    return attendee_service


def attendee_composer() -> AttendeeControllerInterface:
    attendee_service = attendee_service_composer()
    controller = AttendeeController(service=attendee_service)
    return controller
