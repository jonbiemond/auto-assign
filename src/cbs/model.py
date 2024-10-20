"""The scheduler model."""

from dataclasses import dataclass
from typing import Iterable, Hashable

import cpmpy as cp
from cpmpy.expressions.core import Expression


@dataclass
class Constraint:
    name: str
    description: str | None
    expressions: Iterable[Expression | bool]


class CBS:
    """Constraint-Based Scheduler"""

    def __init__(self, events: int, persons: Iterable[Hashable]):
        """Return a CBS model instance.

        Args:
            events (int): The number of events.
            persons (Iterable[Hashable]): Iterable of key-compliant person objects.
        """
        self._events = range(0, events)
        self._persons = persons
        self._schedule = {m: cp.boolvar(shape=events) for m in persons}
        self._constraints = {}

        # set initial constraint
        self.persons_per_event(1)

    def set_constraint(
        self,
        name: str,
        description: str | None,
        expressions: Iterable[Expression | bool],
    ) -> None:
        """Add or replace a constraint.

        Args:
            name (str): The name of the constraint to add or replace.
            description (str): A reader friendly of the description.
            expressions (Iterable[Expression]): Collection of cpmpy expressions.
        """
        self._constraints[name] = Constraint(name, description, expressions)

    def persons_per_event(self, n: int) -> None:
        """Set the number of persons required per event.

        Args:
            n (int): The number of persons required.
        """
        expressions = (
            cp.sum(self._schedule[j][i] for j in self._persons) == n
            for i in self._events
        )
        self.set_constraint(
            "persons_per_event",
            f"The total number of persons required for each event is {n}.",
            expressions,
        )

    def solve(self) -> None:
        """Apply constraints to cpmpy model and solve.

        Raises
            ValueError: If the model is not solvable.
        """
        model = cp.Model()
        for constraint in self._constraints.values():
            for expression in constraint.expressions:
                model += expression
        if not model.solve():
            raise ValueError()

    def schedule(self) -> dict[Hashable : list[int]]:
        """Solve for constraints and generate schedule as a dictionary.

        Returns
            dict: The schedule as a dictionary.
        """
        self.solve()
        return {i: [int(j) for j in self._schedule[i].value()] for i in self._persons}
