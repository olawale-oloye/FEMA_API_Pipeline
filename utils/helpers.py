from collections.abc import Generator
from typing import Any


def chunk_list(
    data: list[dict[str, Any]], size: int
) -> Generator[list[dict[str, Any]], None, None]:
    for i in range(0, len(data), size):
        yield data[i : i + size]
