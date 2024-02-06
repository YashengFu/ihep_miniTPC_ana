import numpy as np

import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("AGG")
import os
os.environ["OMP_NUM_THREADS"] = "100"
plt.style.use("/afs/ihep.ac.cn/users/f/fuys/.config/matplotlib/Paper.mplstyle")

arr = np.load('./data/data_array_0927_10MHZ_comb.npy')
# arr = np.load('./data/data_array_0927_10MHZ_divide.npy')
# data_label="10MHZ_divide"
data_label="10MHZ_comb"
# print(arr)
# print(arr.shape)

# for index in range(len(arr)):
#     if arr[index][0]==32858:
#         print(index)

# print(len(arr)/6146)



chan_dict={}
for chan in range(33):
    chan_dict[str(chan)] = np.array([])


package_len = 514*8
sam_points = 100
all_useful_data = np.array([])

package_num =3000
package_num_list = [10,100,200,500,1000,2000,3000,5000]
package_num_list = [10,100,200,500,1000,2000]

for index in range(package_num_list[-1]):
# for index in range(int(len(arr)/package_len)):
    
    # if index !=3:
    if 1>0:
        package_data = arr[index*package_len:(index+1)*package_len]
        print(package_data[0][0],"head info")
        print(package_data[0][2],"length info")
        """remove head and tail"""
        select_data = package_data[1:-1].flatten()*75/(1e6)*1000
        cut_point = 32
        cut_data = select_data[0+cut_point:33*sam_points+cut_point]
        all_useful_data = np.append(all_useful_data, cut_data)

        """strange method"""
        for chann in range(32):
            data = cut_data[chann*sam_points:(chann+1)*sam_points] 
            # data = np.array(cut_data[(chann+1)*sam_points:(chann+2)*sam_points])  - np.array(cut_data[chann*sam_points:(chann+1)*sam_points])
            result = data[60:70]
            array_index = chann % 33
            chan_dict[str(array_index)] = np.append(chan_dict[str(array_index)], result)

fig, ax = plt.subplots(nrows=2, ncols=1,figsize=(30, 15))
dis_chan_range = [0,5]
for n in range(10):
    ax[0].plot(all_useful_data[dis_chan_range[0]*sam_points+(33*sam_points)*n:dis_chan_range[1]*sam_points+(33*sam_points)*n],\
               '.',label="data package %s"%n)

# for index in range(1,33):
index_list = [1,2,3,28,29,30,31,32]
for index in index_list:
    ax[1].plot(chan_dict[str(index)][-100:],label='chan %s'%index)
    

ax[1].set_xlabel("Sample points")
ax[0].set_ylabel("mV")
ax[1].set_ylabel("mV")
# ax[1].set_ylim(-20,20)
ax[0].legend(frameon=True, edgecolor='red',fontsize=15,loc=[0.0,1.1],ncol=11)
ax[1].legend(frameon=True, edgecolor='red',fontsize=18,loc=[0.0,1.1],ncol=11)
ax[0].set_title("package num %s"%package_num)
plt.tight_layout()
plt.savefig("./plots/waveform_display_%s.pdf"%data_label)

# fig, ax = plt.subplots(nrows=7,ncols=5,figsize=(28,24))
# # for index in range(33):
# index=0
# for row in range(7):
#     for col in range(5):
#         if index > 32:
#             break
#         ax[row, col].hist(chan_dict[str(index)])
#         ax[row, col].set_title('chan %s'%index)
#         index+=1
# plt.tight_layout()
# plt.savefig("./plots/waveform_hist.pdf")



sel_point =10
result_list=[]

for index_p in package_num_list:
    sel_sam = sel_point*index_p
    chan_index=[]
    ENC_value=[]
    Vstd_value=[]

    for index, value in chan_dict.items():
        value = value[0: sel_sam]
        chan_index.append(index)
        enc = np.round(np.std(value)/14*6250,2)

        ENC_value.append(enc)
        Vstd_value.append(np.std(value))

    result_list.append(ENC_value)

np.savez('./enc_data_comb.npz',a=np.array(result_list),b =np.array(package_num_list) )

    # fig, ax = plt.subplots(figsize=(12, 7))
    # ax2 = ax.twinx()
    # ax.plot(chan_index, ENC_value,'.r--',markersize=15)
    # ax2.plot(chan_index, Vstd_value,'.b--',markersize=15)
    # ax.set_xlabel("Channel ID")
    # ax.set_ylabel("ENC")
    # ax2.set_ylabel("RMS[mV]")
    # ax.set_xticklabels(labels=chan_index,rotation=60,size=15)
    # plt.tight_layout()
    # plt.savefig("./plots/ENC_results_%s.pdf"%data_label)


# print(chan_index[1:])
# print(ENC_value[1:])