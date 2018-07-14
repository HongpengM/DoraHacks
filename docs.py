import os
import os.path as osp


def folderFilter(flist, root='.'):
    if root:
        return [i for i in flist if ((not '.' in i) and (not '_' in i) and osp.isdir(osp.join(root, i)))]
    else:
        return [i for i in flist if ((not '.' in i) and (not '_' in i) and osp.isdir(i))]


def pyFilter(flist):
    return [i for i in flist if '.py' in i]


def folderRunner(root):
    currentRoot = osp.abspath(root)
    docdict = {}
    currentDir = folderFilter(os.listdir(root), currentRoot)
    currentPy = pyFilter(os.listdir(root))

    isModule = '__init__.py' in currentPy
    name = osp.abspath(currentRoot).split('\\')[-1]
    dirdict = {}
    for i in currentDir:
        dirdict[i] = folderRunner(osp.join(root, i))
    docdict['name'] = name
    docdict['dir'] = dirdict
    docdict['py'] = currentPy
    docdict['isModule'] = isModule
    return docdict


def docsOutput(docdict, level=0):
    indent = ' ' * level * 4
    fileindent = ' ' * ((level + 1) * 4 + 1)
    if docdict['isModule']:
        output = indent + docdict['name'] + '/' + ' ' * 10
        print(output + (40 - len(output)) * '-' + 'Module')
    else:
        output = indent + docdict['name'] + '/'
        print(output)
    for i in docdict['py']:
        if i == '__init__.py':
            continue
        print(fileindent + i)
    for i in docdict['dir'].keys():
        docsOutput(docdict['dir'][i], level=level + 1)


def docsOut(docdict, level=0):
    out = ''
    indent = ' ' * level * 4
    fileindent = ' ' * ((level + 1) * 4 + 1)
    if docdict['isModule']:
        output = indent + docdict['name'] + '/' + ' ' * 10
        out += (output + (60 - len(output)) * '-' + 'Module') + '\n'
    else:
        output = indent + docdict['name'] + '/'
        out += (output) + '\n'
    for i in docdict['py']:
        if i == '__init__.py':
            continue
        out += fileindent + i + '\n'
    for i in docdict['dir'].keys():
        if docsOut(docdict['dir'][i], level=level + 1):
            out += docsOut(docdict['dir'][i], level=level + 1)
        out += '\n'

    return out


docs = folderRunner(osp.abspath('.'))
# print(docs)
# docsOutput(docs, 0)
print(docsOut(docs))
# print(docsOut(docs))
with open('readme_draft.md', 'w') as f:
    out = '```python\n' + docsOut(docs) + '\n```'
    header = '''# PyMotionCorr
A python version of motion correction software tools for cyro-EM

## Hierarchy Structure\n'''
    f.writelines(header + out)
