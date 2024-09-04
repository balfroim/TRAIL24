"""Module to access product metadata from the disk."""

import pathlib

POSTERS_ROOT = pathlib.Path("./results/posters")
ABSTRACTS_ROOT = pathlib.Path("./results/abstracts")


def get_poster_path_from_pid(pid: int, quality: str = "1x") -> pathlib.Path:
    """Get the path to the poster image of a product with a given PID."""

    poster_path = POSTERS_ROOT / f"{pid}_{quality}.jpg"

    # Check if the poster exists
    if not poster_path.exists():
        return POSTERS_ROOT / f"default-poster-{quality}.jpg"
        # raise FileNotFoundError(f"Poster not found for PID {pid}")

    return poster_path


def get_abstract_from_pid(pid: int, language: str = "en") -> str:
    """Get the abstract of a product with a given PID."""

    abstract_path = ABSTRACTS_ROOT / f"{language}" / f"{pid}.txt"

    # Check if the abstract exists
    if not abstract_path.exists():
        raise FileNotFoundError(f"Abstract not found for PID {pid}")

    with open(abstract_path, "r", encoding="UTF-8") as file:
        return file.read()
