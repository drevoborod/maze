import signal
from unittest import TestCase

from src.app.field import Field, CellCondition
from src.app.console_output import draw_route
from src.app.route_1 import Route1


DEFAULT_TIMEOUT = 1


class ExecutionTimeoutError(Exception):
    pass


class RunTimeout:
    def __init__(self, seconds, error_message=None):
        if error_message is None:
            error_message = f'test timed out after {seconds}s.'
        self.seconds = seconds
        self.error_message = error_message

    def handle_timeout(self, signum, frame):
        raise ExecutionTimeoutError(self.error_message)

    def __enter__(self):
        signal.signal(signal.SIGALRM, self.handle_timeout)
        signal.alarm(self.seconds)

    def __exit__(self, exc_type, exc_val, exc_tb):
        signal.alarm(0)


# ToDo: replace with pytest-based realization and use its parametrization.
class TestRouteDrawTime(TestCase):
    """
    Tests how long route is being drawn.

    """
    def setUp(self):
        self.field = Field().build(20, 20)
        for x in range(3, 6):
            self.field.set_cell_state(x, 5, CellCondition.blocked)
        for y in range(7, 18):
            self.field.set_cell_state(8, y, CellCondition.blocked)
        self.field.set_cell_state((3, 4), (5, 4), (3, 3), (5, 3), CellCondition.blocked)

    def test_from_left_top_to_right_bottom(self):
        r = Route1(self.field, self.field(4, 4), self.field(16, 12))
        with RunTimeout(DEFAULT_TIMEOUT):
            draw_route(r)

    def test_from_left_top_to_right_bottom_increased_complexity_8_19_regular_route(self):
        for x in range(8, 19):
            self.field.set_cell_state(x, 6, CellCondition.blocked)
        r = Route1(self.field, self.field(4, 4), self.field(16, 12))
        with RunTimeout(DEFAULT_TIMEOUT):
            draw_route(r)

    def test_from_left_top_to_right_bottom_increased_complexity_8_21_regular_route(self):
        for x in range(8, 21):
            self.field.set_cell_state(x, 6, CellCondition.blocked)
        r = Route1(self.field, self.field(4, 4), self.field(16, 12))
        with RunTimeout(DEFAULT_TIMEOUT):
            draw_route(r)

    def test_from_right_bottom_to_left_top_reversed_route(self):
        for x in range(8, 19):
            self.field.set_cell_state(x, 6, CellCondition.blocked)
        r = Route1(self.field, self.field(16, 12), self.field(4, 4))
        with RunTimeout(DEFAULT_TIMEOUT):
            draw_route(r)

    def test_from_left_top_to_middle_increased_complexity_8_19_regular_route(self):
        for x in range(8, 19):
            self.field.set_cell_state(x, 6, CellCondition.blocked)
        r = Route1(self.field, self.field(4, 4), self.field(6, 12))
        with RunTimeout(DEFAULT_TIMEOUT):
            draw_route(r)

    def test_from_left_top_to_middle_increased_complexity_8_21_regular_route(self):
        for x in range(8, 21):
            self.field.set_cell_state(x, 6, CellCondition.blocked)
        r = Route1(self.field, self.field(4, 4), self.field(6, 12))
        with RunTimeout(DEFAULT_TIMEOUT):
            draw_route(r)


class TestRouteMisc(TestCase):
    """
    Tests different aspects of route creation.

    """
    def setUp(self):
        self.field = Field().build(20, 20)
        for x in range(3, 6):
            self.field.set_cell_state(x, 5, CellCondition.blocked)
        for y in range(7, 18):
            self.field.set_cell_state(8, y, CellCondition.blocked)
        self.field.set_cell_state((3, 4), (5, 4), (3, 3), (5, 3), CellCondition.blocked)

    def test_no_duplicates_in_route(self):
        for x in range(8, 21):
            self.field.set_cell_state(x, 6, CellCondition.blocked)
        for x in range(2, 6):
            self.field.set_cell_state(x, 12, CellCondition.blocked)
        for y in range(7, 12):
            self.field.set_cell_state(4, y, CellCondition.blocked)
        for y in range(1, 5):
            self.field.set_cell_state(13, y, CellCondition.blocked)
        r = Route1(self.field, self.field(6, 12), self.field(4, 4))
        assert len(r.path) == len(set(r.path))
