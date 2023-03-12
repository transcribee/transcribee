#!/usr/bin/env python
"""
A script for manually transcribing audio and outputting it in the transcribee datastructure
This might be handy for testing or other debugging work.
"""

import argparse
import asyncio
import logging
import shutil
import tempfile
import urllib.parse
from pathlib import Path
from typing import Optional

import requests
from pydantic import parse_raw_as
from transcribee_proto.api import AlignTask, AssignedTask, DiarizeTask
from transcribee_proto.api import Document as ApiDocument
from transcribee_proto.api import TaskType, TranscribeTask
from transcribee_worker.util import load_audio
from transcribee_worker.whisper_transcribe import transcribe

logging.basicConfig(level=logging.INFO)


class Worker:
    base_url: str
    token: str
    tmpdir: Path
    task_types: list[TaskType]

    def __init__(
        self,
        base_url: str,
        token: str,
        tmpdir: Path,
        task_types: Optional[list[TaskType]] = None,
    ):
        self.base_url = base_url
        self.token = token
        self.tmpdir = tmpdir
        if task_types is not None:
            self.task_types = task_types
        else:
            self.task_types = [TaskType.DIARIZE, TaskType.ALIGN, TaskType.TRANSCRIBE]

    def _get_headers(self):
        return {"Authorization": f"Worker {self.token}"}

    def claim_task(self) -> Optional[AssignedTask]:
        logging.info("Asking backend for new task")
        req = requests.post(
            f"{self.base_url}/claim_unassigned_task/",
            params={"task_type": ",".join(self.task_types)},
            headers=self._get_headers(),
        )
        req.raise_for_status()
        return parse_raw_as(Optional[AssignedTask], req.text)

    def get_document_file(self, document: ApiDocument) -> Optional[Path]:
        logging.debug(f"Getting file. {document=}")
        if document.audio_file is None:
            return
        file_url = urllib.parse.urljoin(self.base_url, document.audio_file)
        outfile = self.tmpdir / "audiofile"
        logging.debug(f"Downloading {file_url=} to {outfile=}")
        with open(outfile, "wb") as f:
            response = requests.get(file_url, stream=True)
            for data in response.iter_content(chunk_size=1024 * 1024):
                f.write(data)
        return outfile

    def keepalive(self, task_id: str, progress: Optional[float]):
        body = {}
        if progress is not None:
            body["progress"] = progress
        logging.debug(f"Sending keepalive for {task_id=}: {body=}")
        req = requests.post(
            f"{self.base_url}/{task_id}/keepalive/",
            json=body,
            headers=self._get_headers(),
        )
        req.raise_for_status()

    async def run_task(self, task: AssignedTask):
        logging.info(f"Running task: {task=}")

        if task.task_type == TaskType.DIARIZE:
            await self.diarize(task)
        elif task.task_type == TaskType.TRANSCRIBE:
            await self.transcribe(task)
        elif task.task_type == TaskType.ALIGN:
            await self.align(task)
        else:
            raise ValueError(f"Invalid task type: '{task.task_type}'")

    async def transcribe(self, task: TranscribeTask):
        if task.task_type != TaskType.TRANSCRIBE:
            return

        document_file = self.get_document_file(task.document)
        audio = load_audio(str(document_file))

        def progress_callback(_ctx, progress, _data):
            self.keepalive(task.id, progress=progress / 100)

        paragraphs = []
        async for paragraph in transcribe(
            audio,
            task.task_parameters.model,
            task.task_parameters.lang,
            progress_callback,
        ):
            paragraphs.append(paragraph)

        raise NotImplementedError("Transcription is not fully implemented yet")

    async def diarize(self, task: DiarizeTask):
        raise NotImplementedError("Diarization is not yet implemented")

    async def align(self, task: AlignTask):
        # document = Document(lang=args.lang, paragraphs=paragraphs)
        # aligned_document = align(document, audio)
        raise NotImplementedError("Alignment is not yet implemented")

    def mark_completed(self, task: AssignedTask):
        raise NotImplementedError("Marking tasks as completed in not yet implemented")


async def main():
    parser = argparse.ArgumentParser(description="Worker")
    parser.add_argument(
        "--coordinator",
        help="url to the task coordinator (aka the transcribee backend)",
        default="http://localhost:8000",
    )
    parser.add_argument("--token", help="Worker token", required=True)
    args = parser.parse_args()
    tmpdir = tempfile.mkdtemp()

    worker = Worker(
        base_url=f"{args.coordinator}/api/v1/tasks",
        token=args.token,
        tmpdir=Path(tmpdir),
        task_types=[TaskType.TRANSCRIBE],
    )
    task = worker.claim_task()

    try:
        if task is not None:
            task_result = await worker.run_task(task)
            logging.info(f"Worker returned: {task_result=}")
            worker.mark_completed(task)
        else:
            logging.info("Got empty task, not running worker")
    except Exception as exc:
        logging.warning("Worked failed with exception", exc_info=exc)

    logging.debug(f"Cleaning tmpdir '{tmpdir}'")
    shutil.rmtree(tmpdir)
    logging.info("Done :)")


if __name__ == "__main__":
    asyncio.run(main())