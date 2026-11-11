"""按稳定任务 ID 执行安全删除，避免旧 UI 回调导致 ValueError。"""
from __future__ import annotations

from typing import TypeVar

T = TypeVar("T")


def pop_task_by_id(tasks: list[T], task_id: str) -> tuple[int, T] | None:
    """移除匹配 ID 的任务，返回原索引与任务供失败回滚。

    重复调用或过期回调安全地返回 None，不修改列表。
    """
    for index, task in enumerate(tasks):
        if task.id == task_id:
            return index, tasks.pop(index)
    return None
