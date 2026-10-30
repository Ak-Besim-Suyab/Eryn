import data

from discord import ui
from lib.builder import build_container

from typing import TypeAlias

Container: TypeAlias = str | ui.Container

def create_view(*containers: Container, timeout: int = None, **kwargs):
    """
    傳入的參數種類:
        - `str`: 傳入資料名稱, 函式會自動從 data.container 取得, 並透過 builder 建構為 `Container`
        - `ui.Container`: 直接傳入 `Container`
    """

    view = ui.LayoutView(timeout=timeout)

    for container in containers:
        match container:
            case str():
                view.add_item(build_container(data.container.get(container), **kwargs))
            case ui.Container():
                view.add_item(container)
            case _:
                raise ValueError(f"不支援的元件類型: {type(container)}")

    return view