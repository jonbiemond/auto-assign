from cbs import CBS


class TestCBS:
    def test_init(self):
        """The events, persons and schedule instance variables are created on init."""
        scheduler = CBS(events=6, persons=["Rick", "Morty", "Summer"])
        assert isinstance(scheduler._events, range)
        assert isinstance(scheduler._persons, list)
        assert isinstance(scheduler._schedule, dict)

    def test_schedule(self):
        """The schedule is generated using just the first person."""
        scheduler = CBS(events=3, persons=["Rick", "Morty", "Summer"])
        schedule = scheduler.schedule()
        assert schedule == {"Rick": [1, 1, 1], "Morty": [0, 0, 0], "Summer": [0, 0, 0]}

    def test_persons_per_event(self):
        """The schedule assigns the requested number of persons per event."""
        scheduler = CBS(events=3, persons=["Rick", "Morty", "Summer"])
        scheduler.persons_per_event(2)
        schedule = scheduler.schedule()
        assert schedule == {"Rick": [1, 1, 1], "Morty": [1, 1, 1], "Summer": [0, 0, 0]}
