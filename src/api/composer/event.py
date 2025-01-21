from src.api.controllers.event import EventController, EventControllerInterface
from src.drivers.database.connection import connection
from src.modules.events.dao.event import EventDAO
from src.modules.events.repositories.event import EventRepository
from src.modules.events.services.event import EventService, EventServiceInterface


def event_service_composer() -> EventServiceInterface:
    event_dao = EventDAO(connection=connection)
    event_repository = EventRepository(dao=event_dao)
    event_service = EventService(repository=event_repository)
    return event_service


def event_composer() -> EventControllerInterface:
    event_service = event_service_composer()
    controller = EventController(service=event_service)
    return controller
