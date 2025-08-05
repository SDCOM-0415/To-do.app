"""
数据库管理 - Todo App v0.3
处理任务数据的存储和检索
"""
import json
from typing import List, Optional, Dict, Any
from pathlib import Path
from models import Task
from config import app_config

class TaskDatabase:
    """任务数据库管理类"""
    
    def __init__(self):
        self.tasks_file = app_config.tasks_file
        self._tasks: List[Task] = []
        self.load_tasks()
    
    def load_tasks(self) -> bool:
        """从文件加载任务"""
        try:
            if self.tasks_file.exists():
                with open(self.tasks_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self._tasks = [Task.from_dict(task_data) for task_data in data]
                print(f"已加载 {len(self._tasks)} 个任务")
                return True
            else:
                self._tasks = []
                return True
        except Exception as e:
            print(f"加载任务失败: {e}")
            self._tasks = []
            return False
    
    def save_tasks(self) -> bool:
        """保存任务到文件"""
        try:
            data = [task.to_dict() for task in self._tasks]
            with open(self.tasks_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"保存任务失败: {e}")
            return False
    
    def add_task(self, task: Task) -> bool:
        """添加新任务"""
        try:
            self._tasks.append(task)
            return self.save_tasks()
        except Exception as e:
            print(f"添加任务失败: {e}")
            return False
    
    def update_task(self, task_id: str, **kwargs) -> bool:
        """更新任务"""
        try:
            task = self.get_task_by_id(task_id)
            if task:
                task.update(**kwargs)
                return self.save_tasks()
            return False
        except Exception as e:
            print(f"更新任务失败: {e}")
            return False
    
    def delete_task(self, task_id: str) -> bool:
        """删除任务"""
        try:
            self._tasks = [task for task in self._tasks if task.id != task_id]
            return self.save_tasks()
        except Exception as e:
            print(f"删除任务失败: {e}")
            return False
    
    def get_task_by_id(self, task_id: str) -> Optional[Task]:
        """根据ID获取任务"""
        for task in self._tasks:
            if task.id == task_id:
                return task
        return None
    
    def get_all_tasks(self) -> List[Task]:
        """获取所有任务"""
        return self._tasks.copy()
    
    def get_tasks_by_status(self, completed: bool) -> List[Task]:
        """根据完成状态获取任务"""
        return [task for task in self._tasks if task.completed == completed]
    
    def get_tasks_by_priority(self, priority: str) -> List[Task]:
        """根据优先级获取任务"""
        return [task for task in self._tasks if task.priority == priority]
    
    def get_overdue_tasks(self) -> List[Task]:
        """获取过期任务"""
        return [task for task in self._tasks if task.is_overdue()]
    
    def search_tasks(self, query: str) -> List[Task]:
        """搜索任务"""
        query = query.lower()
        return [
            task for task in self._tasks 
            if query in task.title.lower() or query in task.description.lower()
        ]
    
    def sort_tasks(self, sort_by: str = "created_at", reverse: bool = False) -> List[Task]:
        """排序任务"""
        if sort_by == "priority":
            return sorted(self._tasks, key=lambda x: x.get_priority_weight(), reverse=not reverse)
        elif sort_by == "due_date":
            # 将没有截止日期的任务放在最后
            def sort_key(task):
                if not task.due_date:
                    return "9999-12-31" if not reverse else "0000-01-01"
                return task.due_date
            return sorted(self._tasks, key=sort_key, reverse=reverse)
        elif sort_by == "title":
            return sorted(self._tasks, key=lambda x: x.title.lower(), reverse=reverse)
        elif sort_by == "completed":
            return sorted(self._tasks, key=lambda x: x.completed, reverse=reverse)
        else:  # created_at
            return sorted(self._tasks, key=lambda x: x.created_at, reverse=reverse)
    
    def get_statistics(self) -> Dict[str, Any]:
        """获取任务统计信息"""
        total = len(self._tasks)
        completed = len([task for task in self._tasks if task.completed])
        pending = total - completed
        overdue = len(self.get_overdue_tasks())
        
        priority_stats = {}
        for priority in ["高", "中", "低"]:
            priority_stats[priority] = len(self.get_tasks_by_priority(priority))
        
        return {
            "total": total,
            "completed": completed,
            "pending": pending,
            "overdue": overdue,
            "completion_rate": (completed / total * 100) if total > 0 else 0,
            "priority_stats": priority_stats
        }
    
    def clear_completed_tasks(self) -> bool:
        """清除已完成的任务"""
        try:
            self._tasks = [task for task in self._tasks if not task.completed]
            return self.save_tasks()
        except Exception as e:
            print(f"清除已完成任务失败: {e}")
            return False
    
    def clear_all_tasks(self) -> bool:
        """清除所有任务"""
        try:
            self._tasks = []
            return self.save_tasks()
        except Exception as e:
            print(f"清除所有任务失败: {e}")
            return False

# 全局数据库实例
task_db = TaskDatabase()