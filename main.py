"""Relay — personal social media monitoring agent.

Starts the APScheduler poll loop and FastAPI web dashboard.
Run with: python main.py
"""

import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

logger = logging.getLogger(__name__)


def main():
    logger.info("Relay starting up...")
    # Scheduler and web server wired up in MLT-112
    logger.info("Nothing to run yet — scaffold complete.")


if __name__ == "__main__":
    main()
