# -*- coding: utf-8 -*-
import re
text = "电话13812345678，邮箱test@example.com"
m = re.search(r'\d{11}', text)
print(m.group())

pattern = r'(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})'
m = re.search(pattern, "2024-01-15")
if m:
    print(m.groupdict())
