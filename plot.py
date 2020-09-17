import numpy as np
import matplotlib.pyplot as plt
import sys

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


if __name__=='__main__':
    filepath = "./logging.txt"
    if len(sys.argv) > 1:
        filepath = sys.argv[1]

    seqgroup = {}
    data = []
    f = open(filepath, "r")
    lines = f.readlines()
    for line in lines:
        row = line.split(",")
        group = int(row[0])
        if group in seqgroup.keys():
            seqgroup[group].append(row)
        else:
            seqgroup[group] = []
    f.close()

    for key in seqgroup.keys():
        record = np.array(seqgroup[key])
        timestamp, cos_arr, err_arr = get_cos_score(record)
        plt.figure("Cosine Score")
        plt.plot(timestamp, cos_arr)
        plt.figure("Error Score")
        plt.plot(timestamp, err_arr)

        size = cos_arr.shape[0]
        err_diff_arr = err_arr[1:size] - err_arr[0:size-1]
        plt.figure("Error Score Diff")
        plt.plot(timestamp[0:size-1], err_diff_arr)

        error_desc_range = np.where(err_diff_arr < -0.1)
        print(error_desc_range)
        error_desc_start_point = np.min(error_desc_range)
        response_time = timestamp[error_desc_start_point]

        plt.figure("Error Score")
        #plt.axvline(x=response_time, color='r', linestyle='-', linewidth=1)
        plt.scatter(response_time, err_arr[error_desc_start_point])

    plt.show()
    plt.close()
