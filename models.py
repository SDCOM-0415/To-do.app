"""
数据模型 - Todo App v0.3
定义任务数据结构
"""
from dataclasses import dataclass, asdict
from datetime import datetime, date
from typing import Optional, Dict, Any
import uuid

@dataclass
class Task:
    """任务数据模型"""
    id: str
    title: str
    description: str = ""
    priority: str = "中"  # 高、中、低
    completed: bool = False
    created_at: str = ""
    updated_at: str = ""
    due_date: Optional[str] = None
    tags: list = None
    
    def __post_init__(self):
        """初始化后处理"""
        if not self.id:
            self.id = str(uuid.uuid4())
        
        if not self.created_at:
            self.created_at = datetime.now().isoformat()
        
        if not self.updated_at:
            self.updated_at = self.created_at
            
        if self.tags is None:
            self.tags = []
    
    def update(self, **kwargs):
        """更新任务信息"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = datetime.now().isoformat()
    
    def toggle_completed(self):
        """切换完成状态"""
        self.completed = not self.completed
        self.updated_at = datetime.now().isoformat()
    
    def is_overdue(self) -> bool:
        """检查是否过期"""
        if not self.due_date:
            return False
        try:
            due = datetime.fromisoformat(self.due_date).date()
            return due < date.today() and not self.completed
        except:
            return False
    
    def days_until_due(self) -> Optional[int]:
        """距离截止日期的天数"""
        if not self.due_date:
            return None
        try:
            due = datetime.fromisoformat(self.due_date).date()
            delta = due - date.today()
            return delta.days
        except:
            return None
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Task':
        """从字典创建任务"""
        # 处理旧版本数据兼容性
        if 'text' in data and 'title' not in data:
            data['title'] = data.pop('text')
        
        # 移除不支持的字段
        unsupported_fields = ['status']
        for field in unsupported_fields:
            if field in data:
                data.pop(field)
        
        # 确保必需字段存在
        if 'id' not in data:
            data['id'] = str(uuid.uuid4())
        
        # 只保留Task类支持的字段
        valid_fields = {
            'id', 'title', 'description', 'priority', 'completed', 
            'created_at', 'updated_at', 'due_date', 'tags'
        }
        filtered_data = {k: v for k, v in data.items() if k in valid_fields}
        
        return cls(**filtered_data)
    
    def get_priority_weight(self) -> int:
        """获取优先级权重（用于排序）"""
        priority_weights = {"高": 3, "中": 2, "低": 1}
        return priority_weights.get(self.priority, 2)
    
    def __str__(self) -> str:
        status = "✓" if self.completed else "○"
        return f"{status} [{self.priority}] {self.title}"