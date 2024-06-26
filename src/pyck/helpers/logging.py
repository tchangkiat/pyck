import logging
from logging.handlers import RotatingFileHandler
import traceback

from pyck.utils.styles import red, grey, bold


class Logging(object):
    _instance = None

    _formatter = logging.Formatter(
        "[%(asctime)s %(levelname)s] %(message)s", "%Y-%m-%d %H:%M:%S"
    )
    _logger = logging.getLogger("default")
    _logger.setLevel(logging.INFO)
    _fh = RotatingFileHandler("app.log", maxBytes=1024 * 1024 * 1, backupCount=3)
    _fh.setLevel(logging.INFO)
    _fh.setFormatter(_formatter)
    _logger.addHandler(_fh)

    @classmethod
    def get_instance(cls):
        """Get the instance of the logging object, or create one if not created yet"""
        if cls._instance is None:
            cls._instance = cls.__new__(cls)
        return cls._instance

    def info(self, message: str):
        """Logs an INFO message."""
        print(message)
        self._logger.info(message)

    def debug(self, message: str):
        """Logs a debug message."""
        print(grey(message))
        self._logger.info(message)

    def error(
        self,
        message: str,
        resources: list[str] = [],
        show_traceback: bool = False,
        traceback_detail: str = "",
    ):
        """Logs an ERROR message."""
        print(
            bold(red("\n-------------------- Error --------------------\n"))
            + bold(message)
        )
        self._logger.error(message)
        if traceback_detail:
            if show_traceback:
                print("\n" + grey(traceback_detail))
            self._logger.error(traceback_detail)
        if len(resources) != 0:
            resources_str = "\nResources:"
            resource_count = 0
            for resource in resources:
                resource_count += 1
                resources_str += "\n[" + str(resource_count) + "] " + resource
            print(resources_str)
        print(bold(red("-------------------- ----- --------------------\n")))

    def exception(
        self, exception: Exception, resources: list[str] = [], show_traceback=False
    ):
        """Logs an ERROR message based on an exception"""
        self.error(
            exception,
            resources=resources,
            show_traceback=show_traceback,
            traceback_detail="".join(
                traceback.format_exception(
                    type(exception),
                    value=exception,
                    tb=exception.__traceback__,
                )
            ),
        )
