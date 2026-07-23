from abc import ABC, abstractmethod
from time import perf_counter

from config.logger import configure_logging


class Pipeline(ABC):
    # Base class for executable project pipelines

    logger = None

    @classmethod
    def run(cls) -> None:
        # Execute the pipeline with common logging and timing

        configure_logging()

        start_time = perf_counter()

        try:
            cls.execute()

        except Exception:
            cls.logger.exception("%s failed.", cls.__name__)
            raise

        finally:
            elapsed = perf_counter() - start_time

            cls.logger.info(
                "Total execution time: %.3f s.",
                elapsed,
            )

    @classmethod
    @abstractmethod
    def execute(cls) -> None:
        # Execute the pipeline-specific workflow

        raise NotImplementedError