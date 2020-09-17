import numpy as np
import matplotlib.pyplot as plt

if __name__=='__main__':
    filepath = "./logging.txt"

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

    plt.figure()
    for key in seqgroup.keys():
        record = np.array(seqgroup[key])
        look_vec = np.float32(record[:,1:4])
        obj_vec = np.float32(record[:,4:7])
        timestamp = np.float32(record[:,7])
        cos_arr = np.zeros(len(look_vec))
        for i in range(len(look_vec)):
            lv = look_vec[i]
            ov = obj_vec[i]
            prod = np.dot(lv, ov.T)
            mul_mag = np.linalg.norm(lv)*np.linalg.norm(ov)
            cos_arr[i] = np.arccos(prod/mul_mag)*180/3.1415
        plt.plot(timestamp, cos_arr)

    plt.show()
    plt.close()
