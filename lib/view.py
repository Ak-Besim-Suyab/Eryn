import data as register

from discord import ui
from lib.builder import build_container

from typing import TypeAlias
Container: TypeAlias = str | ui.Container

def create_view(*containers: Container, timeout: int = None, **kwargs):
    """
    container has two data types:
        - `str`: when `str` is provided, it will get the data from register.container and build a `Container` from container builder.
        - `ui.Container`: when `ui.Container` is provided, it will be added directly.
    """

    # check if containers are empty, to avoid 400 bad request exception.
    if not containers:
        raise ValueError("containers can't be empty.")

    view = ui.LayoutView(timeout=timeout)

    for container in containers:
        if isinstance(container, str):
            data = register.container.get(container)
            if data is None:
                raise ValueError(f"can't find container data: {container}")

            container = build_container(data, **kwargs)
        
        view.add_item(container)

    return view