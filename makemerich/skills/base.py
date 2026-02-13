"""Base class for all MakeMeRich skills."""

from abc import ABC, abstractmethod


class BaseSkill(ABC):
    """Base class for all trading skills (exchange adapters, analysis tools)."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Unique name for this skill."""
        ...

    @property
    @abstractmethod
    def description(self) -> str:
        """Description of what this skill does."""
        ...
