from collections import defaultdict
keys = ['1','2','5']
tb1info = defaultdict(list)
tb2info = {}
for key in keys:
    tb2info[key] = []

tb2info['1'].append('1')
if tb2info.get('1') == []:
    tb2info['1'].append('123')
else:
    tb2info['1'].append('45')

print(tb1info.keys())
print(tb1info)
print(tb2info.keys())
print(tb2info)