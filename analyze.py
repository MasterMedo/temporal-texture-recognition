from collections import defaultdict
d = defaultdict(lambda: [0, 0])
files = defaultdict(int)
with open('results.txt') as f:
    for l in f.read().split('\n')[:-1]:
        a, b = l.split(', ')
        files[a] += 1
        c = a[:a.index('/')]
        d[c][c == b] += 1 if '1' not in a else 0

print(f"{'file':25} number of frames")
for f in files:
    print(f'{f:25} {files[f]}')

print()
print(f"{'file':10}{'percentage':11}{'correct':8}{'wrong':6}")
for f in d:
    w, c = d[f]
    p = f'{c/(c+w):.1%}'
    print(f'{f:{10}}{p:6}{c:8}{w:6}')
