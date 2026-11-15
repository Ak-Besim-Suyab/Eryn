from data import CONTAINERS

from discord import ui
from lib import container

from typing import TypeAlias
Container: TypeAlias = str | ui.Container

def create(*containers: Container, timeout: int = None, **kwargs):
    """
    可傳入的容器類型有兩種:
        - 字串：收到字串時，函數會查詢資料並調用 build_container() 產生對應名稱的容器並加入至視圖
        - 容器：收到容器時，會直接加入視圖
    
    以上參數皆可傳入複數，同時會將字典參數嘗試套入到所有容器中
    """

    # check if containers are empty, to avoid 400 bad request exception.
    if not containers:
        raise ValueError("containers can't be empty.")

    view = ui.LayoutView(timeout=timeout)

    for cont in containers:
        if isinstance(cont, str):
            data = CONTAINERS.get(cont)
            if data is None:
                raise ValueError(f"can't find container data: {cont}")

            cont = container.build(data, **kwargs)

        view.add_item(cont)

    return view