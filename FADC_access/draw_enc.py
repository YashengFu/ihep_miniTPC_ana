import numpy as np

import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("AGG")

plt.style.use("/afs/ihep.ac.cn/users/f/fuys/.config/matplotlib/Paper.mplstyle")

# data = np.load('./enc_data.npz')
# data = np.load('./enc_data_baseline.npz')
data = np.load('./enc_data_comb.npz')

enc_list = data['a']
package_num_list = data['b']

fig, ax = plt.subplots(figsize=(12, 7))
ax2 = ax.twinx()
for index in range(len(package_num_list)):
    ax.plot(range(len(enc_list[index])),enc_list[index],'.--',fillstyle='none',markersize=15,label=package_num_list[index])
    ax2.plot(range(len(enc_list[index])),enc_list[index]*14/6250,'.--',fillstyle='none',markersize=15)
ax.legend()
ax.set_xlabel("Channel ID")
ax2.set_ylabel("RMS [mV]")
ax.set_ylabel("ENC")
# ax.set_xticklabels(labels=enc_list,rotation=60,size=15)
plt.tight_layout()
plt.savefig("./plots/ENC_results_package_comb.pdf")