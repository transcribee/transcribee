#!/usr/bin/env python

import argparse
import asyncio
import logging

from transcribee_proto.api import TaskType
from transcribee_worker.worker import Worker

logging.basicConfig(level=logging.INFO)


async def main():
    parser = argparse.ArgumentParser(description="Worker")
    parser.add_argument(
        "--coordinator",
        help="url to the task coordinator (aka the transcribee backend)",
        default="http://localhost:8000",
    )
    parser.add_argument("--token", help="Worker token", required=True)
    args = parser.parse_args()

    worker = Worker(
        base_url=f"{args.coordinator}/api/v1/tasks",
        token=args.token,
        task_types=[TaskType.TRANSCRIBE],
    )
    await worker.run_task()


if __name__ == "__main__":
    asyncio.run(main())
