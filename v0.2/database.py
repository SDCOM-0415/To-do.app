"""
数据库操作模块
处理任务数据的存储和读取
"""

import json
import os
from typing import List, Optional
from models import Task
from config import DATABASE_FILE

class TaskDatabase:
    """任务数据库管理类"""
    
    def __init__(self, db_file: str = DATABASE_FILE):
        self.db_file = db_file
        self.tasks = []
        self.load_tasks()
    
    def load_tasks(self) -> bool:
        """从文件加载任务数据"""
        try:
            if os.path.exists(self.db_file):
                with open(self.db_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.tasks = [Task.from_dict(task_data) for task_data in data]
                return True
            else:
                self.tasks = []
                return True
        except Exception as e:
            print(f"加载任务失败: {e}")
            self.tasks = []
            return False
    
    def save_tasks(self) -> bool:
        """保存任务数据到文件"""
        try:
            data = [task.to_dict() for task in self.tasks]
            with open(self.db_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"保存任务失败: {e}")
            return False
    
    def add_task(self, task: Task) -> bool:
        """添加新任务"""
        try:
            self.tasks.append(task)
            return self.save_tasks()
        except Exception as e:
            print(f"添加任务失败: {e}")
            return False
    
    def update_task(self, task_id: str, **kwargs) -> bool:
        """更新任务"""
        try:
            task = self.get_task_by_id(task_id)
            if task:
                for key, value in kwargs.items():
                    if hasattr(task, key):
                        setattr(task, key, value)
                return self.save_tasks()
            return False
        except Exception as e:
            print(f"更新任务失败: {e}")
            return False
    
    def delete_task(self, task_id: str) -> bool:
        """删除任务"""
        try:
            self.tasks = [task for task in self.tasks if task.id != task_id]
            return self.save_tasks()
        except Exception as e:
            print(f"删除任务失败: {e}")
            return False
    
    def get_task_by_id(self, task_id: str) -> Optional[Task]:
        """根据ID获取任务"""
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None
    
    def get_all_tasks(self) -> List[Task]:
        """获取所有任务"""
        return self.tasks.copy()
    
    def get_tasks_by_status(self, status: str) -> List[Task]:
        """根据状态获取任务"""
        return [task for task in self.tasks if task.status == status]
    
    def get_tasks_by_priority(self, priority: str) -> List[Task]:
        """根据优先级获取任务"""
        return [task for task in self.tasks if task.priority == priority]
    
    def clear_all_tasks(self) -> bool:
        """清空所有任务"""
        try:
            self.tasks = []
            return self.save_tasks()
        except Exception as e:
            print(f"清空任务失败: {e}")
            return False
    
    def get_overdue_tasks(self) -> List[Task]:
        """获取过期任务"""
        return [task for task in self.tasks if task.is_overdue()]
    
    def get_tasks_due_soon(self, days: int = 3) -> List[Task]:
        """获取即将到期的任务"""
        soon_tasks = []
        for task in self.tasks:
            if task.status == "PENDING":
                days_left = task.days_until_due()
                if days_left is not None and 0 <= days_left <= days:
                    soon_tasks.append(task)
        return soon_tasks
    
    def sort_tasks_by_priority(self) -> List[Task]:
        """按优先级排序任务"""
        priority_order = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}
        return sorted(self.tasks, key=lambda x: (
            x.status == "COMPLETED",  # 未完成的任务排在前面
            priority_order.get(x.priority, 1)
        ))
    
    def sort_tasks_by_due_date(self) -> List[Task]:
        """按截止日期排序任务"""
        def sort_key(task):
            if task.status == "COMPLETED":
                return (1, task.due_date or "9999-12-31")
            return (0, task.due_date or "9999-12-31")
        
        return sorted(self.tasks, key=sort_key)
    
    def get_task_statistics(self) -> dict:
        """获取任务统计信息"""
        total = len(self.tasks)
        completed = len([t for t in self.tasks if t.status == "COMPLETED"])
        pending = total - completed
        overdue = len(self.get_overdue_tasks())
        due_soon = len(self.get_tasks_due_soon())
        
        return {
            'total': total,
            'completed': completed,
            'pending': pending,
            'overdue': overdue,
            'due_soon': due_soon
        }