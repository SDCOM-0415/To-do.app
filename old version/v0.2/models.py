"""
数据模型
定义任务和相关数据结构
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional
import uuid

@dataclass
class Task:
    """任务数据模型"""
    id: str
    title: str
    description: str = ""
    priority: str = "MEDIUM"  # LOW, MEDIUM, HIGH
    status: str = "PENDING"   # PENDING, COMPLETED
    created_at: str = ""
    completed_at: Optional[str] = None
    due_date: Optional[str] = None
    
    def __post_init__(self):
        """初始化后处理"""
        if not self.id:
            self.id = str(uuid.uuid4())
        if not self.created_at:
            self.created_at = datetime.now().isoformat()
    
    def mark_completed(self):
        """标记任务为已完成"""
        self.status = "COMPLETED"
        self.completed_at = datetime.now().isoformat()
    
    def mark_pending(self):
        """标记任务为待完成"""
        self.status = "PENDING"
        self.completed_at = None
    
    def to_dict(self):
        """转换为字典"""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'priority': self.priority,
            'status': self.status,
            'created_at': self.created_at,
            'completed_at': self.completed_at,
            'due_date': self.due_date
        }
    
    @classmethod
    def from_dict(cls, data):
        """从字典创建任务对象"""
        return cls(
            id=data.get('id', ''),
            title=data.get('title', ''),
            description=data.get('description', ''),
            priority=data.get('priority', 'MEDIUM'),
            status=data.get('status', 'PENDING'),
            created_at=data.get('created_at', ''),
            completed_at=data.get('completed_at'),
            due_date=data.get('due_date')
        )
    
    def is_overdue(self):
        """检查任务是否过期"""
        if not self.due_date or self.status == "COMPLETED":
            return False
        
        try:
            due_date = datetime.fromisoformat(self.due_date.replace('Z', '+00:00'))
            return datetime.now() > due_date
        except (ValueError, AttributeError):
            return False
    
    def days_until_due(self):
        """计算距离截止日期的天数"""
        if not self.due_date:
            return None
        
        try:
            due_date = datetime.fromisoformat(self.due_date.replace('Z', '+00:00'))
            delta = due_date - datetime.now()
            return delta.days
        except (ValueError, AttributeError):
            return None