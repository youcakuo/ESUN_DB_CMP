import datetime
import argparse

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

def logResult(results, more=False, logFile='result'):
    logFile = logFile + '_' + datetime.datetime.now().strftime("%Y%m%d%H%M") + '.txt'
    resultToLog = ['Not found', 'Not match']
    if more:
        resultToLog.append('pass')
    with open(logFile, 'a') as file:
        for rl in resultToLog:
            file.write(rl + ':\n')
            for r in results:
                if r[1]==rl:
                    file.write(r[0])
            file.write('\n')

def main(baseFile='DDLNBSDB_DBU1_UAT.TXT', targetFile='DDLNBSDB_DBP1.TXT', more=False):
    with open(baseFile, 'r', encoding='big5') as fb, open(targetFile, 'r', encoding='big5') as ft:
        fb_content = fb.readlines()
        ft_content = ft.readlines()

        processCmd = False
        cmdBase = []
        results = []
        for lineb in fb_content:
            baseStr = str(lineb)
            if baseStr.lstrip().startswith('CREATE TABLE '):
                processCmd = True
            elif baseStr.startswith('-') and processCmd:
                processCmd = False
                check = validateCmd(cmdBase, ft_content)
                if not check:
                    print(cmdBase[2].rstrip(), ': pass')
                    results.append((cmdBase[2], 'pass'))
                else:
                    print(cmdBase[2].rstrip(), ':', check)
                    results.append((cmdBase[2], check))
                cmdBase = []
            if processCmd:
                tmp = lineb.split(' ')
                cmdBase.extend([b for b in tmp if b])
        logResult(results, more=more)

def debugInfo(info, logLen = 50):
    rst = ''
    if not info:
        rst = '-'*logLen
    else:
        rst = info + ' '*(int(logLen)-len(info))
    return '|' + rst + '|'


if __name__ =='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-b', '--base', help='比對基礎檔案名稱')
    parser.add_argument('-t', '--target', help='比對目標檔案名稱')
    parser.add_argument('-m', '--more', help='log包含正確比對', action='store_true')
    args = parser.parse_args()

    baseFile = args.base if args.base else 'DDLNBSDB_DBU1_UAT.TXT'
    targetFile = args.target if args.target else 'DDLNBSDB_DBP1.TXT'
    print(debugInfo(''))
    print(debugInfo('baseFile   : ' + baseFile))
    print(debugInfo('targetFile : ' + targetFile))
    print(debugInfo('more       : ' + str(args.more)))
    print(debugInfo('')+'\n')
    main(baseFile, targetFile, args.more)

