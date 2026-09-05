# -*- coding: utf-8 -*-
"""Day 71：微调任务进度与指标监控。"""
from datetime import datetime
class MonitorPractice:
    def __init__(self): self.jobs={}
    def track(self, job_id: str, status: str, loss: float | None = None) -> dict:
        """记录任务状态、损失和更新时间。"""
        # TODO：持久化指标并处理重复任务ID
        item={"job_id":job_id,"status":status,"loss":loss,"updated_at":datetime.now().isoformat()}
        self.jobs[job_id]=item
        return item
    def metrics(self, job_id: str) -> dict:
        """返回任务指标；未知任务应抛出KeyError。"""
        # TODO：补充耗时、吞吐量、token和费用指标
        if job_id not in self.jobs: raise KeyError(job_id)
        return self.jobs[job_id]
if __name__ == "__main__": print("请记录训练任务")
