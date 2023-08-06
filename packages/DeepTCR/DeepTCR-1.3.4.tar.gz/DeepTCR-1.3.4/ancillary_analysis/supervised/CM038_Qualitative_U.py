"""
Figure 3f-h, Supplementary Figure 23
"""

"""This script is used to provide a descriptive analysis of the distribution of TCR sequences
within the CheckMate-038 clinical trial.
"""

import pickle
import numpy as np
import pandas as pd
import umap
from DeepTCR.DeepTCR import DeepTCR_WF,DeepTCR_U
import matplotlib.pyplot as plt
import os
import seaborn as sns
from scipy.stats import gaussian_kde
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import fisher_exact, ranksums, spearmanr
from sklearn.model_selection import StratifiedShuffleSplit
from umap import UMAP
from scipy import ndimage as ndi
from matplotlib.patches import Circle
import pickle

os.environ["CUDA DEVICE ORDER"] = 'PCI_BUS_ID'
os.environ["CUDA_VISIBLE_DEVICES"] = "6"

DTCR = DeepTCR_WF('Human_TIL',device='/device:GPU:0')
DTCR.Get_Data(directory='../../Data/CheckMate_038',Load_Prev_Data=False,
               aa_column_beta=1,count_column=2,v_beta_column=7,d_beta_column=14,j_beta_column=21,data_cut=1.0,
              hla='../../Data/CheckMate_038/HLA_Ref_sup_AB.csv')

with open('cm038_ft_pred_perc.pkl','rb') as f:
    features,predicted,perc = pickle.load(f)

win = 10
cut_bottom = np.percentile(predicted[:,0],win)
cut_top = np.percentile(predicted[:,0],100-win)

df_plot = pd.DataFrame()
df_plot['beta'] = DTCR.beta_sequences
df_plot['sample'] = DTCR.sample_id
df_plot['pred'] = predicted[:,0]
df_plot['gt'] = DTCR.class_id
df_plot['freq'] = DTCR.freq

# plt.figure()
# ax = sns.distplot(df_plot['pred'],1000,color='k',kde=False)
# N,bins= np.histogram(df_plot['pred'],1000)
# for p,b in zip(ax.patches,bins):
#     if b < cut_bottom:
#         p.set_facecolor('r')
#     elif b > cut_top:
#         p.set_facecolor('b')
# y_min,y_max = plt.ylim()
# plt.xlim([0,1])
# plt.xticks(np.arange(0.0,1.1,0.1))
# plt.yticks([])
# plt.xlabel('')
# plt.ylabel('')
# plt.show()

beta_sequences = DTCR.beta_sequences
v_beta = DTCR.v_beta
j_beta = DTCR.j_beta
d_beta = DTCR.d_beta
hla = DTCR.hla_data_seq
sample_id = DTCR.sample_id

file = 'cm038_x2_u.pkl'
featurize = False
if featurize:
    DTCR_U = DeepTCR_U('test_hum', device='/device:GPU:6')
    DTCR_U.Load_Data(beta_sequences=beta_sequences, v_beta=v_beta, d_beta=d_beta, j_beta=j_beta, hla=hla)
    DTCR_U.Train_VAE(Load_Prev_Data=False, latent_dim=64,stop_criterion=0.01)
    X_2 = umap.UMAP().fit_transform(DTCR_U.features)
    with open(file, 'wb') as f:
        pickle.dump(X_2, f, protocol=4)
else:
    with open(file,'rb') as f:
        X_2 = pickle.load(f)


df_plot['x'] = X_2[:,0]
df_plot['y'] = X_2[:,1]

def histplot_2d(d, w, labels=None, ax=None, colors=None, cmap=None, circle_mask=False, grid_size=50, log_scale=False, n_pad=5, lw=None, gaussian_sigma=0.5, vmin=None, vmax=0.01):
    # set line width
    if lw is None:
        lw = n_pad

    # center of data
    d_center = np.mean(np.concatenate(d, axis=0), axis=0)
    # largest radius
    d_radius = np.max(np.sum((d_center[np.newaxis, :] - np.concatenate(d, axis=0)) ** 2, axis=1) ** (1 / 2))
    # padding factors
    d_pad = 1.20
    c_pad = 0.90

    # set step and edges of bins for 2d hist
    x_edges = np.linspace(d_center[0] - (d_radius * d_pad), d_center[0] + (d_radius + d_pad), grid_size + 1)
    y_edges = np.linspace(d_center[1] - (d_radius * d_pad), d_center[1] + (d_radius + d_pad), grid_size + 1)
    X, Y = np.meshgrid(x_edges[:-1] + (np.diff(x_edges) / 2), y_edges[:-1] + (np.diff(y_edges) / 2))

    # construct 2d smoothed histograms for each sample
    # counts
    h = np.stack([np.histogramdd(_d, bins=[x_edges, y_edges], weights=_w)[0] for _d, _w in zip(d, w)], axis=2)
    # log scale counts option
    if log_scale:
        h = np.log(h + 1)
    # smooth counts and normalized
    s = np.stack([ndi.gaussian_filter(h[:, :, i], sigma=gaussian_sigma) for i in range(h.shape[-1])], axis=2)
    s = np.stack([s[:, :, i] / np.sum(s[:, :, i]) for i in range(s.shape[-1])], axis=2)

    # set color map
    if cmap is None:
        cmap = plt.get_cmap('viridis')
    # cmap.set_under(color='white', alpha=0)

    # set circle mask
    c_mask = None
    if circle_mask:
        r_bins = c_pad * (grid_size / 2)
        c_mask = np.meshgrid(np.arange(grid_size), np.arange(grid_size))
        c_mask = np.sqrt(((c_mask[0] - (grid_size / 2)) ** 2) + ((c_mask[1] - (grid_size / 2)) ** 2)) >= r_bins

        # define ellipse
        # e_c = np.array([np.mean(X[0, [0, -1]]) + (x_step / 2), np.mean(Y[[0, -1], 0]) + (y_step / 2)])
        # e_w = np.array([2 * (r_bins + 0.) * x_step, 2 * (r_bins + 0.) * y_step])

    # plot
    if ax is not None:
        # xlim = [X[0, 0] - (y_step * 2), X[0, -1] + (y_step * 2)]
        # ylim = [Y[0, 0] - (x_step * 2), Y[-1, 0] + (x_step * 2)]
        for i in range(s.shape[-1]):
            ax[i].cla()
            if circle_mask:
                ax[i].pcolormesh(X, Y, np.ma.masked_array(s[:, :, i], c_mask), cmap=cmap[0] if len(cmap) == 1 else cmap[i], shading='gouraud', vmin=0, vmax=vmax)
                ax[i].add_artist(Circle(d_center, d_radius * (d_pad * c_pad), color=cmap.colors[0] if colors is None else colors[i], fill=False, lw=lw))
            else:
                ax[i].pcolormesh(X, Y, h[:, :, i], cmap=cmap, shading='gouraud', vmin=vmin, vmax=vmax)
            ax[i].set(xticks=[], yticks=[], frame_on=False)
            if labels is not None:
                ax[i].set(title=labels[i])

    return s, h, X, Y, [d_center, d_radius * (d_pad * c_pad)], c_mask


d = df_plot
d['file'] = d['sample']
d['sample'] = d['sample'].str.replace('_TCRB.tsv', '')
d['counts'] = d.groupby('sample')['freq'].transform(lambda x: x / x.min())
grid_size = 500
gaussian_sigma = 0.5
vmax = 0.00001

s = pd.read_csv('CM038_BM.csv')
s.rename(columns={'DeepTCR':'preds'},inplace=True)
s = s.sort_values('preds')
c_dict = dict(crpr='blue', sdpd='red')
color_labels = [c_dict[_] for _ in s['Response_cat'].values]

cmap_blue = plt.get_cmap('Blues')
cmap_blue(0)
cmap_blue._lut[0] = np.ones(4)
cmap_blue._lut[256] = np.ones(4)
cmap_red = plt.get_cmap('Reds')
cmap_red(0)
cmap_red._lut[0] = np.ones(4)
cmap_red._lut[256] = np.ones(4)
map_dict = dict(crpr=cmap_blue, sdpd=cmap_red)
map_labels = [map_dict[_] for _ in s['Response_cat'].values]

#supplemental Figure
_, ax = plt.subplots(nrows=4, ncols=11)
ax_supp_density = ax.flatten()
# cmap = plt.get_cmap('viridis')
# cmap = plt.get_cmap('YlGnBu')
# cmap(0)
# cmap._lut = cmap._lut[np.concatenate([np.flip(np.arange(256)), [257, 256, 258]])]
# cmap._lut[[0, 256]] = np.ones(4)

H = histplot_2d([d.loc[d['sample'] == i, ['y', 'x']].values for i in s['sample'].values],
                [d.loc[d['sample'] == i, 'counts'].values for i in s['sample'].values],
                ax=ax_supp_density, log_scale=True, vmax=vmax, gaussian_sigma=gaussian_sigma,
                circle_mask=True, cmap=map_labels, lw=2, colors=color_labels,grid_size=grid_size)
[ax_supp_density[i].set_title('%.3f' % s['preds'].iloc[i], fontsize=18) for i in range(H[0].shape[-1])]
[ax_supp_density[i].set(xticks=[], yticks=[], frame_on=False) for i in range(H[0].shape[-1], len(ax_supp_density))]
plt.gcf().set_size_inches(13, 5.5)
plt.tight_layout()

_, ax_crpr = plt.subplots()
ax_crpr.cla()
D = H[1][:, :, s['Response_cat'] == 'crpr']
D /= D.sum(axis=0).sum(axis=0)[np.newaxis, np.newaxis, :]
D = ndi.gaussian_filter(np.mean(D, axis=2), sigma=gaussian_sigma)
# ax_crpr.pcolormesh(H[2], H[3], np.ma.masked_array(D, H[-1]), shading='gouraud', cmap=cmap, vmin=0, vmax=0.005)
ax_crpr.pcolormesh(H[2], H[3], D, shading='gouraud', cmap=cmap_blue, vmin=0, vmax=vmax)
ax_crpr.set(xticks=[], yticks=[], frame_on=False)
ax_crpr.add_artist(Circle(H[4][0], H[4][1], color='blue', lw=2, fill=False))
# ax_crpr.set_title('CR/PR')
plt.gcf().set_size_inches(5, 5)
plt.tight_layout()

_, ax_sdpd = plt.subplots()
ax_sdpd.cla()
cmap = plt.get_cmap('Reds')
cmap._lut[0] = np.ones(4)
cmap._lut[256] = np.ones(4)
D = H[1][:, :, s['Response_cat'] == 'sdpd']
D /= D.sum(axis=0).sum(axis=0)[np.newaxis, np.newaxis, :]
D = ndi.gaussian_filter(np.mean(D, axis=2), sigma=gaussian_sigma)
# ax_sdpd.pcolormesh(H[2], H[3], np.ma.masked_array(D, H[-1]), shading='gouraud', cmap=cmap, vmin=0, vmax=0.005)
ax_sdpd.pcolormesh(H[2], H[3], D, shading='gouraud', cmap=cmap_red, vmin=0, vmax=vmax)
ax_sdpd.set(xticks=[], yticks=[], frame_on=False)
ax_sdpd.add_artist(Circle(H[4][0], H[4][1], color='red', lw=2, fill=False))
# ax_sdpd.set_title('SD/PD')
plt.gcf().set_size_inches(5, 5)
plt.tight_layout()


_, ax = plt.subplots(nrows=4, ncols=11)
ax_diff_sample = ax.flatten()

qs = np.quantile(d['pred'].values, [0.1, 0.9])
Ha = histplot_2d([d.loc[d['sample'] == i, ['y', 'x']].values for i in s['sample'].values],
                 [d.loc[d['sample'] == i, 'counts'].values * (d.loc[d['sample'] == i, 'pred'].values > qs[1]) for i in s['sample'].values],
                 log_scale=True,grid_size=grid_size)

Hb = histplot_2d([d.loc[d['sample'] == i, ['y', 'x']].values for i in s['sample'].values],
                 [d.loc[d['sample'] == i, 'counts'].values * (d.loc[d['sample'] == i, 'pred'].values < qs[0]) for i in s['sample'].values],
                 log_scale=True,grid_size=grid_size)

h_sums = (Ha[1].sum(axis=0).sum(axis=0) + Hb[1].sum(axis=0).sum(axis=0))[np.newaxis, np.newaxis, :]
d_maps = (Hb[1] / h_sums) - (Ha[1] / h_sums)
d_maps = np.stack([ndi.gaussian_filter(d_maps[:, :, i], sigma=gaussian_sigma) for i in range(d_maps.shape[2])], axis=2)

for i in range(43):
    ax_diff_sample[i].cla()
    ax_diff_sample[i].pcolormesh(H[2], H[3], d_maps[:, :, i], shading='gouraud', cmap='bwr', vmin=-0.005, vmax=vmax)
    ax_diff_sample[i].set(xticks=[], yticks=[], frame_on=False)
    ax_diff_sample[i].set_title('%.3f' % s['preds'].iloc[i], fontsize=18)
    ax_diff_sample[i].add_artist(Circle(H[4][0], H[4][1], color=color_labels[i], lw=2, fill=False))
[ax_diff_sample[i].set(xticks=[], yticks=[], frame_on=False) for i in range(H[0].shape[-1], len(ax_diff_sample))]
plt.gcf().set_size_inches(13, 5.5)
plt.tight_layout()

_, ax_diff_overall = plt.subplots()
ax_diff_overall.cla()
ax_diff_overall.pcolormesh(H[2], H[3], np.mean(d_maps, axis=2), shading='gouraud', cmap='bwr', vmin=-0.005, vmax=vmax)
ax_diff_overall.set(xticks=[], yticks=[], frame_on=False)
ax_diff_overall.add_artist(Circle(H[4][0], H[4][1], color='grey', lw=2, fill=False))
# ax_diff_overall.set_title('CR/PR vs SD/PD')
plt.gcf().set_size_inches(5, 5)
plt.tight_layout()

idx_crpr = predicted[:,0] >= cut_top
idx_sdpd = predicted[:,0] <= cut_bottom
df_plot['label'] = None
df_plot['label'].iloc[idx_crpr] = 'crpr'
df_plot['label'].iloc[idx_sdpd] = 'sdpd'
df_plot['label'] = df_plot['label'].fillna(value='out')
label_dict = {'crpr':'b','sdpd':'r','out':'darkgrey'}
df_plot['c'] = df_plot['label'].map(label_dict)

#Plot crpr sequences
df_plot_crpr = df_plot[df_plot['label']!='sdpd']
plt.figure()
df_plot_crpr.sort_values(by='pred',ascending=True,inplace=True)
plt.scatter(df_plot_crpr['x'],df_plot_crpr['y'],c=df_plot_crpr['c'],s=1)
plt.xticks([])
plt.yticks([])
x_min,x_max = plt.xlim()
y_min,y_max = plt.ylim()

#Plot sdpd sequences
df_plot_sdpd = df_plot[df_plot['label']!='crpr']
plt.figure()
df_plot_sdpd.sort_values(by='pred',ascending=False,inplace=True)
plt.scatter(df_plot_sdpd['x'],df_plot_sdpd['y'],c=df_plot_sdpd['c'],s=1)
plt.xticks([])
plt.yticks([])
plt.xlim([x_min,x_max])
plt.ylim([y_min,y_max])

ref = df_plot.groupby(['sample']).agg({'gt':'first'}).reset_index()
ref.sort_values(by='gt',ascending=False,inplace=True)
ref_pred = pd.read_csv('sample_tcr_hla.csv')
ref_pred = ref_pred.groupby(['Samples']).agg({'y_pred':'mean'}).reset_index()
ref_dict = dict(zip(ref_pred['Samples'],ref_pred['y_pred']))
ref['pred'] = ref['sample'].map(ref_dict)
ref.sort_values(by='pred',inplace=True)

n_rows = 4
n_cols = 11
fig,ax = plt.subplots(n_rows,n_cols,figsize=(13,5))
ax = np.ndarray.flatten(ax)
for s,l,r,a in zip(ref['sample'],ref['gt'],ref['pred'],ax):
    df_temp =df_plot[df_plot['sample']==s]
    df_temp = df_temp[df_temp['label']!='out']
    a.scatter(df_temp['x'], df_temp['y'], c=df_temp['c'], s=0.1)
    a.set_xticks([])
    a.set_yticks([])
    a.set_xlim([x_min,x_max])
    a.set_ylim([y_min,y_max])
    a.set_title(np.round(r,3))
    if l == 'crpr':
        c = 'b'
    else:
        c = 'r'
    for axis in ['top', 'bottom', 'left', 'right']:
        a.spines[axis].set_linewidth(3)

    for axis in ['top', 'bottom', 'left', 'right']:
        a.spines[axis].set_color(c)

lef = n_cols*n_rows-43
for ii in range(43,43+lef):
    ax[ii].remove()
plt.subplots_adjust(top = 0.9, bottom=0.1, hspace=0.5)

#Plot unfiltered sample repertoires
def gaussian_density(x,y,w=None):
    xy = np.vstack([x,y])
    z = gaussian_kde(xy,weights=w)(xy)
    r = np.argsort(z)
    x ,y, z = x[r], y[r], z[r]
    return x,y,z

n_rows = 4
n_cols = 11
fig,ax = plt.subplots(n_rows,n_cols,figsize=(13,5))
ax = np.ndarray.flatten(ax)
for s,l,r,a in zip(ref['sample'],ref['gt'],ref['pred'],ax):
    df_temp =df_plot[df_plot['sample']==s]
    x = np.array(df_temp['x'])
    y = np.array(df_temp['y'])
    x,y,z = gaussian_density(x,y,df_temp['freq'])
    a.scatter(x, y, s=0.1,c=z,cmap=plt.cm.jet)
    a.set_xticks([])
    a.set_yticks([])
    a.set_xlim([x_min,x_max])
    a.set_ylim([y_min,y_max])
    a.set_title(np.round(r,3))
    if l == 'crpr':
        c = 'b'
    else:
        c = 'r'
    for axis in ['top', 'bottom', 'left', 'right']:
        a.spines[axis].set_linewidth(3)

    for axis in ['top', 'bottom', 'left', 'right']:
        a.spines[axis].set_color(c)

lef = n_cols*n_rows-43
for ii in range(43,43+lef):
    ax[ii].remove()
plt.subplots_adjust(top = 0.9, bottom=0.1, hspace=0.5)

# df_out = pd.DataFrame(DTCR_U.features)
# df_out['pred'] = predicted[:,0]
# df_out['label'] = DTCR.class_id
# df_out['sample'] = DTCR.sample_id
# df_out['freq'] = DTCR.freq
# df_out['counts'] = DTCR.counts
# df_out.to_csv('cm038_ft_u.csv',index=False)