# -*- coding: utf-8 -*-
class FinetuneMonitor:
    def __init__(self):
        self.jobs = []
    def track_job(self, job_id):
        # TODO
        pass
    def get_metrics(self, job_id):
        # TODO: 获取训练指标
        pass
    def should_stop(self, job_id):
        # TODO: 过拟合检测
        pass
