from typing import Any
def normalize_page(page: int | None, page_size: int | None):
    p = max(1, page or 1)
    s = min(100, max(1, page_size or 20))
    return p,s 

def page_response(items: list[Any], page: int, page_size: int, total:int):
    return {"items": items, "page": page, "page_size": page_size, "total": total}

