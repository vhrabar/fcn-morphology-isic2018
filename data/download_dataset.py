#!/usr/bin/env python3
import zipfile
import requests
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

from rich.progress import (
    Progress,
    BarColumn,
    TextColumn,
    DownloadColumn,
    TransferSpeedColumn,
    TimeRemainingColumn,
)


BASE_URLS = {
    "training-data": "https://isic-archive.s3.amazonaws.com/challenges/2018/ISIC2018_Task1-2_Training_Input.zip",
    "training-ground-truth": "https://isic-archive.s3.amazonaws.com/challenges/2018/ISIC2018_Task1_Training_GroundTruth.zip",
    "validation-data": "https://isic-archive.s3.amazonaws.com/challenges/2018/ISIC2018_Task1-2_Validation_Input.zip",
    "validation-ground-truth": "https://isic-archive.s3.amazonaws.com/challenges/2018/ISIC2018_Task1_Validation_GroundTruth.zip",
    "test-data": "https://isic-archive.s3.amazonaws.com/challenges/2018/ISIC2018_Task1-2_Test_Input.zip",
    "test-ground-truth": "https://isic-archive.s3.amazonaws.com/challenges/2018/ISIC2018_Task1_Test_GroundTruth.zip",
}

ZIP_FILENAMES = {k: f"{k}.zip" for k in BASE_URLS}


def base_dir()-> Path:
    return Path(__file__).resolve().parent

def ensure_dir(p: Path)->None:
    p.mkdir(parents=True, exist_ok=True)


def download_file(url: str, dest: Path, progress: Progress, task_id)-> None:
    if dest.exists():
        progress.update(task_id, completed=1, total=1)
        progress.advance(task_id)
        return

    with requests.get(url, stream=True) as r:
        r.raise_for_status()

        total = int(r.headers.get("content-length", 0))
        progress.update(task_id, total=total)

        with open(dest, "wb") as f:
            for chunk in r.iter_content(chunk_size=1024 * 1024):
                if not chunk:
                    continue
                f.write(chunk)
                progress.update(task_id, advance=len(chunk))


def extract_zip(zip_path: Path, extract_to: Path) -> None:
    if not zip_path.exists():
        return

    with zipfile.ZipFile(zip_path, "r") as z:
        members = z.namelist()

        top_levels = set()
        for m in members:
            parts = m.split("/")
            if len(parts) > 1:
                top_levels.add(parts[0])

        strip_root = len(top_levels) == 1

        for member in members:
            if member.endswith("/"):
                continue

            path = Path(member)
            parts = path.parts[1:] if strip_root else path.parts

            if not parts:
                continue

            out_path = extract_to.joinpath(*parts)
            out_path.parent.mkdir(parents=True, exist_ok=True)

            with z.open(member) as src, open(out_path, "wb") as dst:
                dst.write(src.read())


def process_item(progress: Progress, base: Path, key: str, url: str) -> None:
    target_dir = base / key
    zip_path = base / ZIP_FILENAMES[key]

    ensure_dir(target_dir)

    task = progress.add_task(f"[cyan]{key}", start=False)

    if target_dir.exists() and any(target_dir.iterdir()):
        progress.update(task, completed=1, total=1)
        return

    progress.start_task(task)

    download_file(url, zip_path, progress, task)

    progress.update(task, description=f"[yellow]extracting {key}")
    extract_zip(zip_path, target_dir)

    try:
        zip_path.unlink()
    except FileNotFoundError:
        pass

    progress.update(task, description=f"[green]done {key}")
    progress.advance(task)


def main() -> None:
    base = base_dir() / "ISIC2018"
    ensure_dir(base)

    progress = Progress(
        TextColumn("[bold blue]{task.description}"),
        BarColumn(),
        DownloadColumn(),
        TransferSpeedColumn(),
        TimeRemainingColumn(),
    )

    with progress:
        with ThreadPoolExecutor(max_workers=6) as executor:
            futures = [
                executor.submit(process_item, progress, base, k, url)
                for k, url in BASE_URLS.items()
            ]

            for f in as_completed(futures):
                f.result()

    print("DONE")

if __name__ == "__main__":
    main()
