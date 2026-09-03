# -*- coding: utf-8 -*-
class HallucinationDetector:
    def check(self, answer, context):
        ctx = set(context.lower().split())
        ans = set(answer.lower().split())
        overlap = len(ctx & ans)
        return {"score": overlap / max(len(ans),1), "overlap": overlap}
if __name__ == "__main__":
    d = HallucinationDetector()
    print(d.check("Python由Guido创建","Python由Guido van Rossum于1991年创建"))
