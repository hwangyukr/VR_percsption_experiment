import numpy as np
import os
import sys
import matplotlib.pyplot as plt
from collections import defaultdict
from matplotlib import font_manager, rc
import seaborn as sns
import pandas as pd

font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
rc('font', family=font_name)

def load(dirname):
    filenames = os.listdir(dirname)
    filenames = list(reversed(filenames))
    fileinfo = list()
    data = dict()
    for filename in filenames:
        full_path = os.path.join(dirname, filename)
        filename = filename.split('.')[0]
        name = filename[0] + filename[1]
        type = filename[2] + filename[3]
        f = open(full_path, "r")
        lines = f.readlines()
        seqgroup = defaultdict(list)
        for line in lines:
            row = line.split(",")
            group = int(row[0])
            seqgroup[group].append(row)
        f.close()
        data[full_path] = seqgroup
        fileinfo.append(dict({ 'full_path': full_path, 'name': name, 'type': type }))
    return fileinfo, data

def make_groups(meta):
    group_by_name = defaultdict(list)
    group_by_type = defaultdict(list)
    for log in meta:
        group_by_name[log['name']].append(log)
        group_by_type[log['type']].append(log)
    return group_by_type, group_by_name

def get_cos_score(record):
    look_vec = np.float32(record[:,1:3])
    obj_vec = np.float32(record[:,4:6])
    timestamp = np.float32(record[:,7])-np.float32(record[0,7])
    cos_arr = np.zeros(len(look_vec))
    err_arr = np.zeros(len(look_vec))
    for i in range(len(look_vec)):
        lv = look_vec[i]
        ov = obj_vec[i]
        prod = np.dot(lv, ov.T)
        mul_mag = np.linalg.norm(lv)*np.linalg.norm(ov)
        cos_arr[i] = prod/mul_mag
        err_arr[i] = np.arccos(cos_arr[i])*180/3.1415
    return timestamp, cos_arr, err_arr

def measure(timestamp, cos_arr, err_arr):
    size = err_arr.shape[0]
    err_diff_arr = err_arr[1:size] - err_arr[0:size-1]
    move_range = np.where(err_diff_arr <= -0.1)[0]
    resTime = 0
    turnaTime = timestamp.max()
    if move_range.shape[0] <= 0:
        resTime = -1
    else:
        resTime = min(timestamp[move_range])

    return resTime, turnaTime, cos_arr[cos_arr.shape[0]-1]

def analysis_log_list(data, log_list, tag, axes):
    cnt = 0
    meanResTimes = list()
    meanTurnaTimes = list()
    meanAccuarcies = list()

    for log in log_list:
        log_seq = data[log['full_path']]

        resTimes = list()
        turnaTimes = list()
        accuarcies = list()

        for seq in log_seq.keys():
            record = np.array(log_seq[seq])
            timestamp, cos_arr, err_arr = get_cos_score(record)
            axes[cnt].plot(timestamp, cos_arr)

            resTime, turnaTime, accuarcy = measure(timestamp, cos_arr, err_arr)
            if resTime > 0:
                resTimes.append(resTime)
            turnaTimes.append(turnaTime)
            accuarcies.append(accuarcy)

            #axes[cnt][1].set_title("Error : " + tag)
            #axes[cnt][1].plot(timestamp, err_arr)
        avg_resTime = np.float32(resTimes).sum() / len(resTimes)
        turnaTime = np.float32(turnaTimes).sum() / len(turnaTimes)
        accuarcies = np.float32(accuarcies).sum() / len(accuarcies)

        #print(avg_resTime, turnaTime, accuarcies)
        meanResTimes.append(avg_resTime)
        meanTurnaTimes.append(turnaTime)
        meanAccuarcies.append(accuarcies)

        axes[cnt].set_title("Accuarcy : " + tag + log['type'])
        axes[cnt].set_xlabel('반응시간 : ' + str(avg_resTime)
            + ' / 수행시간 : ' + str(turnaTime)
            + ' / 정확도 : ' + str(accuarcies))
        cnt = cnt + 1

    meanResTimes = np.float32(meanResTimes).sum() / len(meanResTimes)
    meanTurnaTimes = np.float32(meanTurnaTimes).sum() / len(meanTurnaTimes)
    meanAccuarcies = np.float32(meanAccuarcies).sum() / len(meanAccuarcies)

    return meanResTimes, meanTurnaTimes, meanAccuarcies

def get_total_values(meta, data):
    total_values = list()
    for test in meta:
        ttype = test['type']
        if ttype == '11': ttype = 'a.청각&시각 사용'
        if ttype == '01': ttype = 'c.청각만 사용';continue
        if ttype == '10': ttype = 'b.시각만 사용';continue
        name = test['name']
        seqgroup = data[test['full_path']]
        for seq in seqgroup.keys():
            one_try = seqgroup[seq]
            timestamp, cos_arr, err_arr = get_cos_score(np.array(one_try))
            resTime, turnaTime, accuarcy = measure(timestamp, cos_arr, err_arr)
            if resTime<=0: continue
            total_values.append(dict({ 'name':name, 'resTime':resTime, 'turnaTime':turnaTime, 'accuarcy':accuarcy, 'type':ttype }))
    return total_values

if __name__=='__main__':
    dirname = './data'
    meta, data = load(dirname)
    total_values = get_total_values(meta, data)

    df = pd.DataFrame(total_values)
    print(df.groupby(["type"])["turnaTime"].std()) #표준편차
    print(df.groupby(["type"])["turnaTime"].median())
    print(df.groupby(["type"])["turnaTime"].mean())


    plt.figure()
    plt.ylim(0.8, 1.0)
    plt.title('상황별 정확도')
    sns.boxplot(x = "type", y="accuarcy", data = df)
    plt.figure()
    plt.title('상황별 반응시간')
    sns.boxplot(x = "type", y="resTime", data = df)
    plt.figure()
    plt.title('상황별 수행시간')
    sns.boxplot(x = "type", y="turnaTime", data = df)
    #plt.show()

    plt.figure()
    plt.title('사람별 정확도 (시각 & 청각 사용)')
    sns.boxplot(x = "name", y="accuarcy", data = df)
    plt.figure()
    plt.title('사람별 반응시간 (시각 & 청각 사용)')
    sns.boxplot(x = "name", y="resTime", data = df)
    plt.figure()
    plt.title('사람별 수행시간 (시각 & 청각 사용)')
    sns.boxplot(x = "name", y="turnaTime", data = df)
    plt.show()

    '''
    group_by_type, group_by_name = make_groups(meta)

    f, axes = plt.subplots(15, 1, sharex=True, sharey=False)
    for key in group_by_type.keys():
        res, tur, acc = analysis_log_list(data, group_by_type[key], key, axes)
        print(res, tur, acc)
    #plt.show()

    for key in group_by_name.keys():
        f, axes = plt.subplots(3, 1, sharex=True, sharey=False)
        analysis_log_list(data, group_by_name[key], key, axes)

    plt.show()
    '''
