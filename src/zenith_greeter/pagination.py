"""In-memory pagination for finite sequences and iterables."""
from dataclasses import dataclass
from typing import Any, List

@dataclass(frozen=True)
class Page:
    items: List[Any]
    current_page: int
    per_page: int
    total_items: int
    total_pages: int
    has_next: bool
    has_previous: bool

    @property
    def next_page(self):
        return self.current_page + 1 if self.has_next else None

    @property
    def previous_page(self):
        return self.current_page - 1 if self.has_previous else None

def paginate(items, page=1, per_page=10):
    """Return one page of an iterable; materializes the iterable in memory."""
    if not isinstance(page, int) or isinstance(page, bool) or page < 1:
        raise ValueError("page must be a positive integer")
    if not isinstance(per_page, int) or isinstance(per_page, bool) or per_page < 1:
        raise ValueError("per_page must be a positive integer")
    sequence = list(items)
    total = len(sequence)
    pages = (total + per_page - 1) // per_page
    start = (page - 1) * per_page
    return Page(sequence[start:start + per_page], page, per_page, total, pages,
                page < pages, 1 < page <= pages)
