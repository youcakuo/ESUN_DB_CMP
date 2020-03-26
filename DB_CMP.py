baseFile = 'DDLNBSDB_DBU1_UAT.TXT'
targetFile = 'DDLNBSDB_DBP1.TXT'

def validateCmd(cmd, target):
    isFind = False
    cmdTarget = []
    rst = 'Not found'
    for linet in target:
        targetStr = str(linet)
        if targetStr.lstrip().startswith('CREATE TABLE') and cmd[2] in targetStr:
            isFind = True
            rst = ''
        if isFind:
            if targetStr.startswith('-'):
                if cmd != cmdTarget:
                    rst = 'Not match'
                    #print('check error:', cmd[2])
                else:
                    pass
                    #print('check pass:', cmd[2])
                break
            else:
                tmp = linet.split(' ')
                cmdTarget.extend([t for t in tmp if t])
    return rst


def main():
    with open(baseFile, 'r', encoding='utf-8') as fb, open(targetFile, 'r', encoding='utf-8') as ft:
        fb_content = fb.readlines()
        ft_content = ft.readlines()

        processCmd = False
        cmdBase = []
        for lineb in fb_content:
            baseStr = str(lineb)
            if baseStr.lstrip().startswith('CREATE TABLE '):
                processCmd = True
            elif baseStr.startswith('-') and processCmd:
                processCmd = False
                check = validateCmd(cmdBase, ft_content)
                if not check:
                    print(cmdBase[2], 'pass')
                else:
                    print(cmdBase[2], check)
                cmdBase = []
            if processCmd:
                tmp = lineb.split(' ')
                cmdBase.extend([b for b in tmp if b])

if __name__ =='__main__':
    main()

