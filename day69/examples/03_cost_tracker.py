# -*- coding: utf-8 -*-
class CostTracker:
    PRICING = {"gpt-4o":(2.5,10.0),"gpt-4o-mini":(0.15,0.6)}
    def __init__(self): self.records = []
    def record(self, model, in_tok, out_tok):
        p = self.PRICING.get(model,(0,0))
        c = (in_tok*p[0]+out_tok*p[1])/1_000_000
        self.records.append({"model":model,"cost":c})
        return c
    def total(self): return sum(r["cost"] for r in self.records)
if __name__ == "__main__":
    t = CostTracker()
    t.record("gpt-4o-mini",1000,500)
    print(f"Total: ${t.total():.6f}")
