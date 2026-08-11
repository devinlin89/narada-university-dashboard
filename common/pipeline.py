from abc import ABC, abstractmethod
from time import perf_counter

from common.exceptions import NaradaError
from config.logger import configure_logging


class Pipeline(ABC):
    """Base class for executable project pipelines."""

    logger = None

    @classmethod
    def run(cls, *args, **kwargs) -> None:
        """Run the pipeline with common logging, error handling, and timing.

        Args:
            *args: Positional arguments passed to the pipeline's execute method.
            **kwargs: Keyword arguments passed to the pipeline's execute method.

        Raises:
            NaradaError: If the pipeline fails with a known application error.
        """

        configure_logging()

        start_time = perf_counter()

        try:
            cls.execute(*args, **kwargs)

        except NaradaError as error:
            cls.logger.error("%s failed: %s", cls.__name__, error)
            raise

        except Exception:
            cls.logger.exception("%s failed unexpectedly.", cls.__name__)
            raise

        finally:
            elapsed = perf_counter() - start_time

            cls.logger.info(
                "Total execution time: %.3f s.",
                elapsed,
            )

    @classmethod
    @abstractmethod
    def execute(cls, *args, **kwargs) -> None:
        """Execute the pipeline-specific workflow.

        Args:
            *args: Positional arguments required by the pipeline.
            **kwargs: Keyword arguments required by the pipeline.

        Raises:
            NotImplementedError: If the method is not implemented by a subclass.
        """

        raise NotImplementedError