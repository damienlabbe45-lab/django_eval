from logging import Formatter
from typing import Self


class FormatDate(Formatter):
    """Formatter personalyze to use function date() for the timestamp."""
    # update : override formatTime not format

    def formatTime(self: Self, record, datefmt=None):
        """
        Retourne la chaîne de date/heure personnalisée.
        """
        from datetime import datetime
        now = datetime.now()
        return now.strftime("%d %B %Y à %H heure %M minutes %S secondes %f microsecondes").replace(
            m := now.strftime("%B"), {'January': 'janvier', 'February': 'février', 'March': 'mars', 'April': 'avril', 
                                             'May': 'mai', 'June': 'juin','July': 'juillet', 'August': 'août', 
                                             'September': 'septembre', 'October': 'octobre', 'November': 'novembre', 'December': 'décembre'}[m])


class LogError(object):
    """Mixin for initializing the logging system (WARNING and errors only)."""

    def loggingperso(self: Self):
        """Configure logging to display only warnings and errors in the console and in a file."""
        from logging import getLogger,  WARNING
        import sys
        from sys import stdout
        from pathlib import Path
        stdout.reconfigure(line_buffering=True) # type: ignore[union-attr]
        sys.stderr.reconfigure(line_buffering=True) # type: ignore[union-attr]
        LOG_FILENAME = Path(__file__).resolve().parents[1] / 'log_bot.log'
        # use FORMETTER
        CUSTOM_FORMETTER = FormatDate(
            fmt='%(asctime)s | %(levelname)s | %(name)s | %(message)s')
        root_logger = getLogger()
        # Check whether the configuration has already been done
        for handler in root_logger.handlers[:]:
            root_logger.removeHandler(handler)
        if not root_logger.handlers:
            from logging import StreamHandler, FileHandler

            class UnbufferedStreamHandler(StreamHandler):
                """Console handler that forces immediate display for every line."""

                def emit(self, record):
                    super().emit(record)
                    self.flush()

            class UnbufferedFileHandler(FileHandler):
                """File handler that forces a write to disk after every line."""

                def emit(self, record):
                    super().emit(record)
                    self.flush()
            # Handler for the console (StreamHandler)
            console_handler = UnbufferedStreamHandler(stdout)
            console_handler.setLevel(WARNING)
            console_handler.setFormatter(CUSTOM_FORMETTER)
            # Handler for the file
            file_handler = UnbufferedFileHandler(
                LOG_FILENAME, encoding='utf-8')
            file_handler.setLevel(WARNING)
            file_handler.setFormatter(CUSTOM_FORMETTER)

            root_logger.setLevel(WARNING)
            root_logger.addHandler(console_handler)
            root_logger.addHandler(file_handler)

        def handle_unhandled_exception(exc_type, exc_value, exc_traceback):
            import sys
            # Allows Ctrl+C to shut down the bot normally without creating clutter
            if issubclass(exc_type, KeyboardInterrupt):
                sys.__excepthook__(exc_type, exc_value, exc_traceback)
                # Send the crash directly to the root_logger (i.e., to both the screen and the log file).
                return
            root_logger.error("Crash fatal détecté (Hors-Log) :",
                              exc_info=(exc_type, exc_value, exc_traceback))
            # We replace Python's default interceptor with our own.
        sys.excepthook = handle_unhandled_exception