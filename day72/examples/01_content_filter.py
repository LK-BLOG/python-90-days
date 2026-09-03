# -*- coding: utf-8 -*-
class ContentFilter:
    BLOCKED = ["暴力","色情","赌博"]
    WARNING = ["政治","宗教"]
    def check(self, text):
        r = {"safe":True,"blocked":[],"warning":[]}
        for w in self.BLOCKED:
            if w in text: r["safe"]=False; r["blocked"].append(w)
        for w in self.WARNING:
            if w in text: r["warning"].append(w)
        return r
if __name__ == "__main__":
    f = ContentFilter()
    print(f.check("天气不错"))
    print(f.check("暴力内容"))
