"""Flet 删除任务回归测试。"""
import unittest

from models import Task
from task_operations import pop_task_by_id


class DeleteTaskTests(unittest.TestCase):
    def test_delete_and_repeat_delete_are_safe(self):
        first = Task(id="first", title="任务 A")
        second = Task(id="second", title="任务 B")
        tasks = [first, second]
        self.assertEqual(pop_task_by_id(tasks, "first"), (0, first))
        self.assertEqual([task.id for task in tasks], ["second"])
        self.assertIsNone(pop_task_by_id(tasks, "first"))
        self.assertEqual([task.id for task in tasks], ["second"])

    def test_delete_by_id_even_when_callback_holds_old_object(self):
        original = Task(id="same-id", title="已重新加载的任务")
        tasks = [original]
        self.assertEqual(pop_task_by_id(tasks, "same-id"), (0, original))
        self.assertEqual(tasks, [])

    def test_missing_task_keeps_list_unchanged(self):
        task = Task(id="one", title="任务")
        tasks = [task]
        self.assertIsNone(pop_task_by_id(tasks, "missing"))
        self.assertEqual(tasks, [task])

    def test_rollback_restores_original_position(self):
        tasks = [Task(id=str(i), title=str(i)) for i in range(3)]
        result = pop_task_by_id(tasks, "1")
        self.assertIsNotNone(result)
        index, removed = result
        tasks.insert(index, removed)
        self.assertEqual([item.id for item in tasks], ["0", "1", "2"])


if __name__ == "__main__":
    unittest.main()
