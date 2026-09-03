# -*- coding: utf-8 -*-
def accuracy(predicted, expected):
    return sum(1 for p,e in zip(predicted,expected) if p==e)/len(expected) if expected else 0
def f1(predicted, expected):
    tp = sum(1 for p,e in zip(predicted,expected) if p==1 and e==1)
    fp = sum(1 for p,e in zip(predicted,expected) if p==1 and e==0)
    fn = sum(1 for p,e in zip(predicted,expected) if p==0 and e==1)
    prec = tp/(tp+fp) if (tp+fp)>0 else 0
    rec = tp/(tp+fn) if (tp+fn)>0 else 0
    return 2*prec*rec/(prec+rec) if (prec+rec)>0 else 0
if __name__ == "__main__":
    print(f"Acc: {accuracy(['A','B','C'],['A','B','D']):.2%}")
    print(f"F1: {f1([1,0,1,1],[1,1,0,1]):.2f}")
