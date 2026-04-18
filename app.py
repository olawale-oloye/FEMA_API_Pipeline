"""
Application entry point.

Initializes logging and runs the FEMA ETL pipeline.
"""

from conf.conf import setup_logging
from pipelines.fema_pipeline import run_pipeline


def main() -> None:
    """
    Main application function.
    """
    setup_logging()
    run_pipeline()


if __name__ == "__main__":
    main()
