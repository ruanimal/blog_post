#coding=utf-8

with open(u'sublime快捷键.md', 'r') as f:
    old = f.readlines()
    for index, line in enumerate(old):
        if index < 27: continue
        if line.startswith('-') and '`' not in line:
            line = line.split('\t')
            line[0] = line[0][:2] + '`%s`\t' % line[0][2:]
            old[index] = ''.join(line)

    o = open(u'sublime快捷键1.md', 'w')
    o.write(''.join(old))
    o.close()