# SONYC_CAPSTONE_VIS.py
import sys
import os
import time
import random
import pickle
from datetime import datetime
from functools import reduce
from collections import defaultdict
from math import ceil
from functools import reduce

import umap
import h5py as h5
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd
import numpy as np
from math import pi

from sklearn.decomposition import PCA
from sklearn.preprocessing import Normalizer
from sklearn.metrics import silhouette_samples, silhouette_score
from sklearn.cluster import KMeans
from sklearn import metrics
from sklearn import preprocessing
from sklearn.mixture import GaussianMixture
from sklearn.cluster import DBSCAN
from sklearn.manifold import TSNE

import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.autograd as ag
import torch.nn.init as init
from torch.nn.utils import spectral_norm
from torch.utils.data import Dataset, DataLoader

class vis:
    def create_columns(features):
        '''
        create feature column hour_minite,
        '''
        features['h_m'] = features.timestamp.apply(lambda x: datetime.fromtimestamp(x).time().strftime('%H:%M'))
        return features

    def dense_scatter(features, sample_ind, figsize=(15,15), dot_size = 2):
        '''
        this function is used for dense plot
        args: features -- pandas DataFrame
            figsize -- figure size to set
            dot_size -- the size for each dot
        out:
            matplotlib plot
        '''
        features = pd.concat([sample_ind, features], axis = 1)
        fig,ax= plt.subplots(figsize = figsize)

        # scatter
        ax.scatter(x=features["h_m"].values,
                   y=features["date"].values,
                   c=features["labels"].values,
                  s = 2)

        ax.xaxis.set_major_locator(ticker.MultipleLocator(60))
        ax.set_ylim((features["date"].min(), features["date"].max()))

    def radar_plot(features_spl, figsize=(15,15), y_ticks = [58,64,70]):
        '''
        this function is used for dense plot
        args: features -- pandas DataFrame
            figsize -- figure size to set
        out:
            matplotlib plot
        '''
        values = features_spl.mean_spl.values.tolist()
        values += values[:1]

        # number of variable
        categories=list(range(1,9))
        N = len(categories)

        # What will be the angle of each axis in the plot? (we divide the plot / number of variable)
        angles = [n / float(N) * 2 * pi for n in range(N)]
        angles += angles[:1]

        # Initialise the spider plot
        plt.figure(figsize = figsize)
        ax = plt.subplot(111, polar=True)

        # Draw one axe per variable + add labels labels yet
        plt.xticks(angles[:-1], categories, color='grey', size=16)

        # Draw ylabels
        ax.set_rlabel_position(0)
        plt.yticks(y_ticks, [str(item) for item in y_ticks], color="grey", size=14)
        plt.ylim(y_ticks[0]-2, y_ticks[-1]+2)
        plt.title('mean spl vs. clusters')
        # Plot data
        ax.plot(angles, values, linewidth=1, linestyle='solid')

        # Fill area
        ax.fill(angles, values, 'b', alpha=0.1)

    def polar_plot(features_spl, day_to_plot, figsize = (15,15)):
        '''
        this function is used for polar plot
        args: features -- pandas DataFrame
            day_to_plot -- select which day to plot
            figsize -- figure size to set
        out:
            matplotlib plot
        '''
        date_feature = features[features_spl.date == day_to_plot]
        date_feature['hour'] = date_feature.h_m.apply(lambda x: x.split(':')[0])
        # Fixing random state for reproducibility
        # np.random.seed(19680801)

        # Compute pie slices
        N = len(date_feature)
        theta, width = np.linspace(0.0, 2 * np.pi, N, endpoint=False, retstep=True)
        colors = date_feature.labels

        plt.figure(figsize = figsize)
        ax = plt.subplot(111, polar=True)
        for i in range(1,9):
            target = date_feature.apply(lambda x: x.mean_spl if x.labels == i else 0, axis = 1).values
            bars = ax.bar(
                theta, target,
                width=width-0.01,
                label = 'cluster '+str(i)
            #     bottom=50,
        #         color=i
            )
        plt.legend()

        ax.set_theta_zero_location("N")
        ax.set_theta_direction(-1)
        ax.grid(False)
        ax.spines['polar'].set_visible(False)
        ax.set_rlim(55, 75)
        ax.set_rticks(np.arange(55,75,5))

        plt.title('spl of different clusters in time slots')
        ticks = [f"{i}:00" for i in range(0, 24, 3)]
        ax.set_xticklabels(ticks)
        _ = ax

    def PCA_diel(features, sample_ind):
        features = pd.concat([sample_ind, features], axis = 1)
        emb1 = features.emb.values.tolist()
        pca = PCA(n_components=3)
        pca.fit(emb1)
        pca_out = pca.transform(emb1)

        pca_vis = pd.concat([features, pd.DataFrame(pca_out, columns=['pca1', 'pca2', 'pca3'])], axis = 1)
        for i in range(1,4):
            min_max_scaler = preprocessing.MinMaxScaler()
            scaled_array = min_max_scaler.fit_transform(pca_vis['pca'+str(i)].values.reshape(-1,1))*255
            pca_vis['scaled_pca'+str(i)] = scaled_array
        pca_vis['color_plot'] = pca_vis.apply(lambda x: '#%02x%02x%02x' % (round(x.scaled_pca1), round(x.scaled_pca2), round(x.scaled_pca3)),axis=1)
        pca_vis_h_m = pca_vis[['date','h_m','color_plot']]
        pca_vis_h_m['h_m'] = pca_vis_h_m.h_m.apply(lambda x: ':'.join(x.split(':')[:-1]))
        pca_vis_h_m = pca_vis_h_m.groupby(['date', 'h_m']).first().reset_index()

        fig,ax= plt.subplots(figsize = (20,20))

        # scatter
        ax.scatter(x=pca_vis_h_m["h_m"].values,
                   y=pca_vis_h_m["date"].values,
                   c=pca_vis_h_m["color_plot"],
                  s = 2)

        ax.xaxis.set_major_locator(ticker.MultipleLocator(60))
        ax.yaxis.set_major_locator(ticker.MultipleLocator(30))
        ax.set_ylim((pca_vis_h_m["date"].min(), pca_vis_h_m["date"].max()))

    def cluster_vis(features, use_pca=True, n_components = 64):
        print('This may take some time')

        features_X = features.emb.values.tolist()
        labels = features.labels.values.to_list()
        if use_pca:
            pca = PCA(n_components=n_components, svd_solver='randomized')
            pca.fit(features_X)
            features_X = pca.transform(features_X)
            # print('PCA components: explained_variance_ratio_:'+str(pca.explained_variance_ratio_))

        reducer = umap.UMAP()

        embedding = reducer.fit_transform(features_X)
        print('start umap plotting')
        plt.figure(figsize=(16, 16))
        plt.scatter(embedding[:, 0], embedding[:, 1], c=labels, alpha=0.3)
        plt.gca().set_aspect('equal', 'datalim')
        plt.colorbar(boundaries=np.arange(9)-0.5).set_ticks(np.arange(8))
        plt.title('UMAP projection of the Features dataset using GMM', fontsize=24)

class fetch_data:
    def fetch_spl(sensor_ids):
        spl_root_path = '/beegfs/work/sonyc/new_indices/2017/sonycnode-'
        fix = '.sonyc_recording_index.h5'

        res = []

        for sensor_id in sensor_ids:
            print('start '+ sensor_id)
            sensor_time_dict = {}
            file_path = spl_root_path + sensor_id + fix
            sensor_table = h5.File(file_path)[list(h5.File(file_path).keys())[0]]
            for i in range(len(sensor_table)):
                res.append([np.round(float(sensor_table[i][0]), decimals = 2),sensor_table[i][1], sensor_table[i][6], sensor_id])
        spl_df = pd.DataFrame(res)
        spl_df.columns = ['time_stamp', 'path', 'mean_spl', 'sensor']
        spl_df['date'] = spl_df.time_stamp.apply(lambda x: datetime.fromtimestamp(x).strftime('%Y-%m-%d'))
        spl_df['h_m'] = spl_df.time_stamp.apply(lambda x: datetime.fromtimestamp(x).strftime('%H:%M:%S'))
        return spl_df

    def fetch_feature(df_output = False, sample_size = 43000, parent_dir = '/beegfs/work/sonyc/features/openl3/2017'):
        def time_stamp_to_datetime(sample_ind):
            res = []
            for k, v in sample_ind.items():
                for item in v:
                    res.append([item, k])
            timestamp_df = pd.DataFrame(res, columns = ['time_stamp', 'sensor_id'])
            timestamp_df['date'] = timestamp_df.time_stamp.apply(lambda x: datetime.fromtimestamp(x).strftime('%Y-%m-%d'))
            timestamp_df['h_m'] = timestamp_df.time_stamp.apply(lambda x: datetime.fromtimestamp(x).strftime('%H:%M:%S'))
            return timestamp_df
        # if filesize < 1500, empty
        sensor_list = [s.split('-')[1].split('.')[0] for s in os.listdir(parent_dir) if os.path.getsize(f'{parent_dir}/{s}') > 1500]
        # print('Sample from {} sensors, taking min({}, len) data points from each sensor. \n'.format(len(sensor_list),sample_size))

        sample_ind= {}
        features = []
        row_numbers = []
        for sensor in sensor_list:
            feature_path = f'{parent_dir}/sonycnode-{sensor}.sonyc_features_openl3.h5'
            f = h5.File(feature_path,'r')
            data = f[list(f.keys())[0]]
            # print(f'sampling from {sensor}, data size = {data.shape[0]}')
            sampled_idx = random.sample(list(range(data.shape[0])), min(sample_size-1, data.shape[0]))
            timestamps = []
            st = time.time()
            for j in sampled_idx:
                timestamps.append(data[j]['timestamp'])
                temp = data[j]['openl3']
                features.append(np.hstack([np.mean(temp, axis = 0), np.median(temp, axis = 0), temp.min(axis = 0),
                                           temp.max(axis = 0)]))
                row_numbers.append('_'.join([sensor, str(j)])) #sensor_id and row number
            sample_ind[sensor] = timestamps
            # print(f'Took {(time.time() - st)/60} mins to finish sampling from {sensor}\n')
        # print('Total sampled date points = {}'.format(len(features)))
        if df_output:
            features_df = pd.DataFrame()
            features_df['emb'] = features
            return features_df, time_stamp_to_datetime(sample_ind)
        else:
            return features, sample_ind


    def fetch_feature_spl_match(features, sample_ind):
        spl_root_path = '/beegfs/work/sonyc/new_indices/2017/sonycnode-'
        fix = '.sonyc_recording_index.h5'
        res = []
        features = pd.concat([sample_ind, features], axis = 1)
        sensors = features.sensor_id.unique()
        time_stamps = features.time_stamp.unique()

        for sensor in sensors:
            # print('start '+sensor)
            sensor_time_dict = {}
            file_path = spl_root_path + sensor + fix
            sensor_table = h5.File(file_path)[list(h5.File(file_path).keys())[0]]
            for i in range(len(sensor_table)):
                sensor_time_dict[np.round(float(sensor_table[i][0]), decimals=2)] = [sensor_table[i][1], sensor_table[i][6]]
                if i % 10000 == 0:
                    print(str(i)+' is completed!!')
            print('hash_ready')
            for time_stamp in time_stamps:
                try:
                    res.append([time_stamp, sensor_time_dict[time_stamp][0], sensor_time_dict[time_stamp][1], sensor])
                except:
                    continue
        spl_data = pd.DataFrame(res, columns= ['timestamp', 'path', 'mean_spl', 'sensor'])
        spl_and_feature = pd.merge(features, spl_data,  how='left', left_on=['sensor_id','timestamp'], right_on = ['sensor','timestamp'])
        return spl_and_feature

    def load_annotations(file_path='/beegfs/work/sonyc/ust/annotations/latest/annotations.csv'):
        data = pd.read_csv(file_path)
        keys = ['timestamp', 'sonyc_sensor_id', 'audio_filename']
        class_cols = ['1_engine_presence', '2_machinery-impact_presence', '3_non-machinery-impact_presence',
                      '4_powered-saw_presence', '5_alert-signal_presence', '6_music_presence', '7_human-voice_presence',
                      '8_dog_presence']
        selected = keys + class_cols
        train_agg = data[data.split == 'train'][selected].groupby(keys).agg(lambda x: 1*(x == 1).any())

        train_agg['labels'] = train_agg.apply(lambda x: tuple([col[0] for col in class_cols if x[col]]), axis=1)
        train_agg.reset_index(inplace = True)
        cols = ['timestamp', 'sonyc_sensor_id', 'audio_filename', 'labels']
        train_agg = train_agg[cols]
        data['labels'] = data.apply(lambda x: tuple([col[0] for col in class_cols if x[col]]), axis=1)
        test_val = data[data.annotator_id == 0][cols]
        truth = pd.concat([test_val, train_agg])
        feat_names = [i.split('.')[0]+'.npz' for i in truth.audio_filename.values]
        # print('size = {}: {} from test and valid, {} from train'.format(len(feat_names), len(test_val), len(train_agg)))
        annotation_labels = list(truth.labels.values)
        # print('number of unique labels in truth: '+str(len(truth.labels.unique())))
        return train_agg, test_val, truth

    def fetch_full_annotation(file_path='/beegfs/work/sonyc/ust/features/l3-mel256-music-512/44.1k'):
        print(' the current audio embedding is not synced with feature embedding!')
        feat_dir = file_path
        features = []
        st = time.time()

        for file_name in feat_names:
            feat_file = f'{feat_dir}/{file_name}'
            temp = np.load(feat_file)['embedding']
            features.append(np.hstack([np.median(temp, axis = 0) ,temp.std(axis = 0), temp.max(axis = 0)]))

        print(f'Took {(time.time() - st)/60} mins to finish loading features from {len(feat_names)} files.\n')
        print(features.shape)
        return features

    def fetch_emb_spl_prob(s_list = None):
        parent_dir = '/beegfs/work/sonyc/features/openl3_day_format/2017'
        sensor_list = os.listdir(parent_dir)

        date_dict = {}
        for sensor in sensor_list:
            s = sensor.split('-')[1].split('.')[0]
            date_dict[s] = [s.split('.')[0] for s in os.listdir(parent_dir + '/' + sensor) if os.path.getsize(f'{parent_dir}/{sensor}/{s}') > 10000000]
            print('{} has {} days.'.format(s, len(date_dict[s])))

        if not s_list:
            s_list = ['b827ebc6dcc6', 'b827eb815321', 'b827eb2a1bce', 'b827ebefb215', 'b827eb2c65db', 'b827ebad073b',
                  'b827eb0d8af7', 'b827eb122f0f', 'b827ebb40450', 'b827ebc7f772', 'b827eb0fedda',
                  'b827eb4e7821', 'b827eb905497', 'b827ebba613d', 'b827eb42bd4a', 'b827eb1685c7',
                  'b827eb44506f', 'b827eb132382', 'b827eb539980', 'b827eb4cc22e', 'b827ebf31214', 'b827eb29eb77',
                  'b827eb86d458']

        i = s_list[0]
        temp = set(date_dict[i])
        for j in s_list:
            temp = list(set(temp) & set(date_dict[j]))

        temp = sorted(temp)

        start = temp[0] + ' 00:00:00'
        end = temp[-1] + ' 23:59:59'
        s_time = time.mktime(datetime.strptime(start, "%Y-%m-%d %H:%M:%S").timetuple())
        e_time = time.mktime(datetime.strptime(end, "%Y-%m-%d %H:%M:%S").timetuple())
        # print(datetime.fromtimestamp(s_time))
        # print(datetime.fromtimestamp(e_time))
        s_time, e_time

        parent_dir = '/beegfs/work/sonyc/features/openl3/2017'

        features = []
        spl_mean = []
        multi_probs = []

        sensor_ids = []
        row_numbers = []
        timestamps = []

        for i, sensor in enumerate(s_list):
            print(i+1)
            st = time.time()
            # get features
            f = h5.File(f'{parent_dir}/sonycnode-{sensor}.sonyc_features_openl3.h5','r')
            data = f[list(f.keys())[0]]
            # get class predictions
            p = h5.File(f'/beegfs/work/sonyc/class_predictions/1.0.0/2017/sonycnode-{sensor}.sonyc_class_predictions.h5','r')
            preds = p['coarse']
            # get spl
            h = h5.File(f'/beegfs/work/sonyc/new_indices_validated/2017/sonycnode-{sensor}.sonyc_recording_index.h5','r')
            spl = h[list(h.keys())[0]]

            print(f'sampling from {sensor}, from {start} to {end} ...')

            for j in range(data.shape[0]):
                if data[j]['timestamp'] > e_time: break
                if data[j]['timestamp'] >= s_time:
                    temp = data[j]['openl3']
                    features.append(np.hstack([np.mean(temp, axis = 0), np.median(temp, axis = 0), temp.min(axis = 0),
                                               temp.max(axis = 0)]))
                    sensor_ids.append(sensor)
                    timestamps.append(data[j]['timestamp'])
                    row_numbers.append(j)

                    spl_mean.append(spl[j]['spl_mean'])
                    multi_probs.append(list(preds[j])[2:])

            print(f'Took {(time.time() - st)/60} mins to finish sampling from {sensor}\n')

        print('Total sampled date points = {}'.format(len(features)))
        features_df = pd.DataFrame()
        features_df['emb'] = features
        spl_mean_df = pd.DataFrame(spl_mean, columns=['spl_mean'])
        multi_probs_df = pd.DataFrame(multi_probs)
        return features_df, spl_mean_df, multi_probs_df

class clustering:
    def k_means_pp(features, num_clusters):
        X_embedded = features.emb.values.tolist()
        kmeans = KMeans(n_clusters=num_clusters, random_state=0, init='k-means++', ).fit(X_embedded)
        features['labels'] = kmeans.labels_
        return features

    def dbscan(features):
        X_embedded = features.emb.values.tolist()
        clustering = DBSCAN().fit(X_embedded)
        features['labels'] = clustering.labels_
        return features

    def hdbscan():
        pass

    def GMM(features, n_components):
        X_embedded = features.emb.values.tolist()
        gmm = GaussianMixture(n_components=n_components)
        labels = gmm.fit_predict(X_embedded)
        features['labels'] = labels
        return features

class dim_reduction:
    def umap(features):
        reducer = umap.UMAP()
        embedding = reducer.fit_transform(features.emb.values.tolist())
        return embedding

    def tsne(features, n_components=2):
        embedding = TSNE(n_components=n_components).fit_transform(features)
        return embedding

    def PCA(features, n_components):
        emb1 = features.emb.values.tolist()

        pca = PCA(n_components=n_components)
        pca.fit(emb1)
        pca_out = pca.transform(emb1)

        print(pca_out.shape)
        print("pca explained variance ratio: " + str(sum(pca.explained_variance_ratio_)))
#         print(sum(pca.explained_variance_ratio_[:64]))
        return pca_out

############## Functions and Classes Prepared for AE #################
class DummyEncoder(object):
    def __init__(self, encoder):
        self.encoder = encoder

    def load(self, target_network):
        self.encoder.load_state_dict(target_network.state_dict())

    def __call__(self, x):
        return self.encoder(x)
class MLP(nn.Module):
    def __init__(self, c_in, c_h, n_blocks, act, sn):
        super(MLP, self).__init__()
        self.act = get_act(act)
        self.n_blocks = n_blocks
        f = spectral_norm if sn else lambda x: x
        self.in_dense_layer = f(nn.Linear(c_in, c_h))
        self.first_dense_layers = nn.ModuleList([f(nn.Linear(c_h, c_h)) for _ in range(n_blocks)])
        self.second_dense_layers = nn.ModuleList([f(nn.Linear(c_h, c_h)) for _ in range(n_blocks)])

    def forward(self, x):
        h = self.in_dense_layer(x)
        for l in range(self.n_blocks):
            y = self.first_dense_layers[l](h)
            y = self.act(y)
            y = self.second_dense_layers[l](y)
            y = self.act(y)
            h = h + y
        return h
class Prenet(nn.Module):
    def __init__(self, c_in, c_h, c_out,
            kernel_size, n_conv_blocks,
            subsample, act, dropout_rate):
        super(Prenet, self).__init__()
        self.act = get_act(act)
        self.subsample = subsample
        self.n_conv_blocks = n_conv_blocks
        self.in_conv_layer = nn.Conv2d(1, c_h, kernel_size=kernel_size)
        self.first_conv_layers = nn.ModuleList([nn.Conv2d(c_h, c_h, kernel_size=kernel_size) for _ \
                in range(n_conv_blocks)])
        self.second_conv_layers = nn.ModuleList([nn.Conv2d(c_h, c_h, kernel_size=kernel_size, stride=sub)
            for sub, _ in zip(subsample, range(n_conv_blocks))])
        output_size = c_in
        for l, sub in zip(range(n_conv_blocks), self.subsample):
            output_size = ceil(output_size / sub)
        self.out_conv_layer = nn.Conv1d(c_h * output_size, c_out, kernel_size=1)
        self.dropout_layer = nn.Dropout(p=dropout_rate)
        self.norm_layer = nn.InstanceNorm2d(c_h, affine=False)

    def forward(self, x):
        # reshape x to 4D
        x = x.contiguous().view(x.size(0), 1, x.size(1), x.size(2))
        out = pad_layer_2d(x, self.in_conv_layer)
        out = self.act(out)
        out = self.norm_layer(out)
        for l in range(self.n_conv_blocks):
            y = pad_layer_2d(out, self.first_conv_layers[l])
            y = self.act(y)
            y = self.norm_layer(y)
            y = self.dropout_layer(y)
            y = pad_layer_2d(y, self.second_conv_layers[l])
            y = self.act(y)
            y = self.norm_layer(y)
            y = self.dropout_layer(y)
            if self.subsample[l] > 1:
                out = F.avg_pool2d(out, kernel_size=self.subsample[l], ceil_mode=True)
            out = y + out
        out = out.contiguous().view(out.size(0), out.size(1) * out.size(2), out.size(3))
        out = pad_layer(out, self.out_conv_layer)
        out = self.act(out)
        return out
class Postnet(nn.Module):
    def __init__(self, c_in, c_h, c_out, c_cond,
            kernel_size, n_conv_blocks,
            upsample, act, sn):
        super(Postnet, self).__init__()
        self.act = get_act(act)
        self.upsample = upsample
        self.c_h = c_h
        self.n_conv_blocks = n_conv_blocks
        f = spectral_norm if sn else lambda x: x
        total_upsample = reduce(lambda x, y: x*y, upsample)
        self.in_conv_layer = f(nn.Conv1d(c_in, c_h * c_out // total_upsample, kernel_size=1))
        self.first_conv_layers = nn.ModuleList([f(nn.Conv2d(c_h, c_h, kernel_size=kernel_size)) for _ \
                in range(n_conv_blocks)])
        self.second_conv_layers = nn.ModuleList([f(nn.Conv2d(c_h, c_h*up*up, kernel_size=kernel_size))
            for up, _ in zip(upsample, range(n_conv_blocks))])
        self.out_conv_layer = f(nn.Conv2d(c_h, 1, kernel_size=1))
        self.conv_affine_layers = nn.ModuleList(
                [f(nn.Linear(c_cond, c_h * 2)) for _ in range(n_conv_blocks*2)])
        self.norm_layer = nn.InstanceNorm2d(c_h, affine=False)
        self.ps = nn.PixelShuffle(max(upsample))

    def forward(self, x, cond):
        out = pad_layer(x, self.in_conv_layer)
        out = out.contiguous().view(out.size(0), self.c_h, out.size(1) // self.c_h, out.size(2))
        for l in range(self.n_conv_blocks):
            y = pad_layer_2d(out, self.first_conv_layers[l])
            y = self.act(y)
            y = self.norm_layer(y)
            y = append_cond_2d(y, self.conv_affine_layers[l*2](cond))
            y = pad_layer_2d(y, self.second_conv_layers[l])
            y = self.act(y)
            if self.upsample[l] > 1:
                y = self.ps(y)
                y = self.norm_layer(y)
                y = append_cond_2d(y, self.conv_affine_layers[l*2+1](cond))
                out = y + upsample(out, scale_factor=(self.upsample[l], self.upsample[l]))
            else:
                y = self.norm_layer(y)
                y = append_cond(y, self.conv_affine_layers[l*2+1](cond))
                out = y + out
        out = self.out_conv_layer(out)
        out = out.squeeze(dim=1)
        return out
class SpeakerEncoder(nn.Module):
    def __init__(self, c_in, c_h, c_out, kernel_size,
            bank_size, bank_scale, c_bank,
            n_conv_blocks, n_dense_blocks,
            subsample, act, dropout_rate):
        super(SpeakerEncoder, self).__init__()
        self.c_in = c_in
        self.c_h = c_h
        self.c_out = c_out
        self.kernel_size = kernel_size
        self.n_conv_blocks = n_conv_blocks
        self.n_dense_blocks = n_dense_blocks
        self.subsample = subsample
        self.act = get_act(act)
        self.conv_bank = nn.ModuleList(
                [nn.Conv1d(c_in, c_bank, kernel_size=k) for k in range(bank_scale, bank_size + 1, bank_scale)])
        in_channels = c_bank * (bank_size // bank_scale) + c_in
        self.in_conv_layer = nn.Conv1d(in_channels, c_h, kernel_size=1)
        self.first_conv_layers = nn.ModuleList([nn.Conv1d(c_h, c_h, kernel_size=kernel_size) for _ \
                in range(n_conv_blocks)])
        self.second_conv_layers = nn.ModuleList([nn.Conv1d(c_h, c_h, kernel_size=kernel_size, stride=sub)
            for sub, _ in zip(subsample, range(n_conv_blocks))])
        self.pooling_layer = nn.AdaptiveAvgPool1d(1)
        self.first_dense_layers = nn.ModuleList([nn.Linear(c_h, c_h) for _ in range(n_dense_blocks)])
        self.second_dense_layers = nn.ModuleList([nn.Linear(c_h, c_h) for _ in range(n_dense_blocks)])
        self.output_layer = nn.Linear(c_h, c_out)
        self.dropout_layer = nn.Dropout(p=dropout_rate)

    def conv_blocks(self, inp):
        out = inp
        # convolution blocks
        for l in range(self.n_conv_blocks):
            y = pad_layer(out, self.first_conv_layers[l])
            y = self.act(y)
            y = self.dropout_layer(y)
            y = pad_layer(y, self.second_conv_layers[l])
            y = self.act(y)
            y = self.dropout_layer(y)
            if self.subsample[l] > 1:
                out = F.avg_pool1d(out, kernel_size=self.subsample[l], ceil_mode=True)
            out = y + out
        return out

    def dense_blocks(self, inp):
        out = inp
        # dense layers
        for l in range(self.n_dense_blocks):
            y = self.first_dense_layers[l](out)
            y = self.act(y)
            y = self.dropout_layer(y)
            y = self.second_dense_layers[l](y)
            y = self.act(y)
            y = self.dropout_layer(y)
            out = y + out
        return out

    def forward(self, x):
        out = conv_bank(x, self.conv_bank, act=self.act)
        # dimension reduction layer
        out = pad_layer(out, self.in_conv_layer)
        out = self.act(out)
        # conv blocks
        out = self.conv_blocks(out)
        # avg pooling
        out = self.pooling_layer(out).squeeze(2)
        # dense blocks
        out = self.dense_blocks(out)
        out = self.output_layer(out)
        return out
class ContentEncoder(nn.Module):
    def __init__(self, c_in, c_h, c_out, kernel_size,
            bank_size, bank_scale, c_bank,
            n_conv_blocks, subsample,
            act, dropout_rate):
        super(ContentEncoder, self).__init__()
        self.n_conv_blocks = n_conv_blocks
        self.subsample = subsample
        self.act = get_act(act)
        self.conv_bank = nn.ModuleList(
                [nn.Conv1d(c_in, c_bank, kernel_size=k) for k in range(bank_scale, bank_size + 1, bank_scale)])
        in_channels = c_bank * (bank_size // bank_scale) + c_in
        self.in_conv_layer = nn.Conv1d(in_channels, c_h, kernel_size=1)
        self.first_conv_layers = nn.ModuleList([nn.Conv1d(c_h, c_h, kernel_size=kernel_size) for _ \
                in range(n_conv_blocks)])
        self.second_conv_layers = nn.ModuleList([nn.Conv1d(c_h, c_h, kernel_size=kernel_size, stride=sub)
            for sub, _ in zip(subsample, range(n_conv_blocks))])
        self.norm_layer = nn.InstanceNorm1d(c_h, affine=False)
        self.mean_layer = nn.Conv1d(c_h, c_out, kernel_size=1)
        self.std_layer = nn.Conv1d(c_h, c_out, kernel_size=1)
        self.dropout_layer = nn.Dropout(p=dropout_rate)

    def forward(self, x):
        out = conv_bank(x, self.conv_bank, act=self.act)
        # dimension reduction layer
        out = pad_layer(out, self.in_conv_layer)
        out = self.norm_layer(out)
        out = self.act(out)
        out = self.dropout_layer(out)
        # convolution blocks
        for l in range(self.n_conv_blocks):
            y = pad_layer(out, self.first_conv_layers[l])
            y = self.norm_layer(y)
            y = self.act(y)
            y = self.dropout_layer(y)
            y = pad_layer(y, self.second_conv_layers[l])
            y = self.norm_layer(y)
            y = self.act(y)
            y = self.dropout_layer(y)
            if self.subsample[l] > 1:
                out = F.avg_pool1d(out, kernel_size=self.subsample[l], ceil_mode=True)
            out = y + out
        mu = pad_layer(out, self.mean_layer)
        log_sigma = pad_layer(out, self.std_layer)
        return mu, log_sigma
class Decoder(nn.Module):
    def __init__(self,
            c_in, c_cond, c_h, c_out,
            kernel_size,
            n_conv_blocks, upsample, act, sn, dropout_rate):
        super(Decoder, self).__init__()
        self.n_conv_blocks = n_conv_blocks
        self.upsample = upsample
        self.act = get_act(act)
        f = spectral_norm if sn else lambda x: x
        self.in_conv_layer = f(nn.Conv1d(c_in, c_h, kernel_size=1))
        self.first_conv_layers = nn.ModuleList([f(nn.Conv1d(c_h, c_h, kernel_size=kernel_size)) for _ \
                in range(n_conv_blocks)])
        self.second_conv_layers = nn.ModuleList(\
                [f(nn.Conv1d(c_h, c_h * up, kernel_size=kernel_size)) \
                for _, up in zip(range(n_conv_blocks), self.upsample)])
        self.norm_layer = nn.InstanceNorm1d(c_h, affine=False)
        self.conv_affine_layers = nn.ModuleList(
                [f(nn.Linear(c_cond, c_h * 2)) for _ in range(n_conv_blocks*2)])
        self.out_conv_layer = f(nn.Conv1d(c_h, c_out, kernel_size=1))
        self.dropout_layer = nn.Dropout(p=dropout_rate)

    def forward(self, z, cond):
        out = pad_layer(z, self.in_conv_layer)
        out = self.norm_layer(out)
        out = self.act(out)
        out = self.dropout_layer(out)
        # convolution blocks
        for l in range(self.n_conv_blocks):
            y = pad_layer(out, self.first_conv_layers[l])
            y = self.norm_layer(y)
            y = append_cond(y, self.conv_affine_layers[l*2](cond))
            y = self.act(y)
            y = self.dropout_layer(y)
            y = pad_layer(y, self.second_conv_layers[l])
            if self.upsample[l] > 1:
                y = pixel_shuffle_1d(y, scale_factor=self.upsample[l])
            y = self.norm_layer(y)
            y = append_cond(y, self.conv_affine_layers[l*2+1](cond))
            y = self.act(y)
            y = self.dropout_layer(y)
            if self.upsample[l] > 1:
                out = y + upsample(out, scale_factor=self.upsample[l])
            else:
                out = y + out
        out = pad_layer(out, self.out_conv_layer)
        return out
class AE(nn.Module):
    def __init__(self, config):
        super(AE, self).__init__()
        self.speaker_encoder = SpeakerEncoder(**config['SPLEncoder'])
        self.content_encoder = ContentEncoder(**config['EmbEncoder'])
        self.decoder = Decoder(**config['Decoder'])

    def forward(self, x):
        emb = self.speaker_encoder(x)
        mu, log_sigma = self.content_encoder(x)
        eps = log_sigma.new(*log_sigma.size()).normal_(0, 1)
        dec = self.decoder(mu + torch.exp(log_sigma / 2) * eps, emb)
        return mu, log_sigma, emb, dec

    def inference(self, x, x_cond):
        emb = self.speaker_encoder(x_cond)
        mu, _ = self.content_encoder(x)
        dec = self.decoder(mu, emb)
        return dec

    def get_speaker_embeddings(self, x):
        emb = self.speaker_encoder(x)
        return emb
    def get_content_embeddings(self, x):
        emb = self.content_encoder(x)
        return emb
############ END Functions and Classes Prepared for AE END ##############

class debiasing:
    def global_local_deb(features, config=None, batch_size=64, n_iterations=2000):
        def cc(net):
            device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
            return net.to(device)

        def infinite_iter(iterable):
            it = iter(iterable)
            while True:
                try:
                    ret = next(it)
                    yield ret
                except StopIteration:
                    it = iter(iterable)
        def pad_layer(inp, layer, pad_type='constant'):
            kernel_size = layer.kernel_size[0]
            if kernel_size % 2 == 0:
                pad = (kernel_size//2, kernel_size//2 - 1)
            else:
                pad = (kernel_size//2, kernel_size//2)
            # padding
            inp = F.pad(inp,
                    pad=pad,
                    mode=pad_type)
            out = layer(inp)
            return out

        def pad_layer_2d(inp, layer, pad_type='constant'):
            kernel_size = layer.kernel_size
            if kernel_size[0] % 2 == 0:
                pad_lr = [kernel_size[0]//2, kernel_size[0]//2 - 1]
            else:
                pad_lr = [kernel_size[0]//2, kernel_size[0]//2]
            if kernel_size[1] % 2 == 0:
                pad_ud = [kernel_size[1]//2, kernel_size[1]//2 - 1]
            else:
                pad_ud = [kernel_size[1]//2, kernel_size[1]//2]
            pad = tuple(pad_lr + pad_ud)
            # padding
            inp = F.pad(inp,
                    pad=pad,
                    mode=pad_type)
            out = layer(inp)
            return out

        def pixel_shuffle_1d(inp, scale_factor=2):
            batch_size, channels, in_width = inp.size()
            channels //= scale_factor
            out_width = in_width * scale_factor
            inp_view = inp.contiguous().view(batch_size, channels, scale_factor, in_width)
            shuffle_out = inp_view.permute(0, 1, 3, 2).contiguous()
            shuffle_out = shuffle_out.view(batch_size, channels, out_width)
            return shuffle_out

        def upsample(x, scale_factor=2):
            x_up = F.interpolate(x, scale_factor=scale_factor, mode='nearest')
            return x_up

        def flatten(x):
            out = x.contiguous().view(x.size(0), x.size(1) * x.size(2))
            return out

        def concat_cond(x, cond):
            # x = [batch_size, x_channels, length]
            # cond = [batch_size, c_channels]
            cond = cond.unsqueeze(dim=2)
            cond = cond.expand(*cond.size()[:-1], x.size(-1))
            out = torch.cat([x, cond], dim=1)
            return out

        def append_cond(x, cond):
            # x = [batch_size, x_channels, length]
            # cond = [batch_size, x_channels * 2]
            p = cond.size(1) // 2
            mean, std = cond[:, :p], cond[:, p:]
            out = x * std.unsqueeze(dim=2) + mean.unsqueeze(dim=2)
            return out

        def conv_bank(x, module_list, act, pad_type='constant'):
            outs = []
            for layer in module_list:
                out = act(pad_layer(x, layer, pad_type))
                outs.append(out)
            out = torch.cat(outs + [x], dim=1)
            return out

        def get_act(act):
            if act == 'relu':
                return nn.ReLU()
            elif act == 'lrelu':
                return nn.LeakyReLU()
            else:
                return nn.ReLU()
        def ae_step(data, lambda_kl):
            x = cc(data['emb'].unsqueeze(-1))
            mu, log_sigma, emb, dec = model(x)
            criterion = nn.L1Loss()
            loss_rec = criterion(dec, x)
            loss_kl = 0.5 * torch.mean(torch.exp(log_sigma) + mu ** 2 - 1 - log_sigma)
            loss = config['lambda']['lambda_rec'] * loss_rec + \
                    lambda_kl * loss_kl
            opt.zero_grad()
            loss.backward()
            grad_norm = torch.nn.utils.clip_grad_norm_(model.parameters(),
                    max_norm=config['optimizer']['grad_norm'])
            opt.step()
            meta = {'loss_rec': loss_rec.item(),
                    'loss_kl': loss_kl.item(),
                    'grad_norm': grad_norm}
            return meta

        def save_model(iteration):
            # save model and discriminator and their optimizer
            store_model_path = './AE_model_dict'
            torch.save(model.state_dict(), f'{store_model_path}.ckpt')
            torch.save(opt.state_dict(), f'{store_model_path}.opt')
        def batchify(batch):
            inputs = batch

            return {
                'emb': torch.from_numpy(np.array(batch), )
            }
        features_ndarray = np.array([emb.tolist()[0] for emb in features.values])
        train_loader = DataLoader(train_dataset, shuffle=True, collate_fn=batchify, batch_size=64)
        if not config:
            config = {
                'SPLEncoder':{
                'c_in': 2048,
                'c_h': 512,
                'c_out': 256,
                'kernel_size': 2,
                'bank_size': 8,
                'bank_scale': 1,
                'c_bank': 128,
                'n_conv_blocks': 6,
                'n_dense_blocks': 6,
                'subsample': [1, 2, 1, 2, 1, 2],
                'act': 'relu',
                'dropout_rate': 0},
            'EmbEncoder':{
                'c_in': 2048,
                'c_h': 512,
                'c_out': 256,
                'kernel_size': 2,
                'bank_size': 8,
                'bank_scale': 1,
                'c_bank': 128,
                'n_conv_blocks': 6,
                'subsample': [1, 2, 1, 2, 1, 2],
                'act': 'relu',
                'dropout_rate': 0},
            'Decoder':{
                'c_in': 256,
                'c_cond': 256,
                'c_h': 512,
                'c_out': 2048,
                'kernel_size': 2,
                'n_conv_blocks': 6,
                'upsample': [2, 1, 2, 1, 2, 1],
                'act': 'relu',
                'sn': False,
                'dropout_rate': 0},
            'optimizer':{
                'lr': 0.0005,
                'beta1': 0.9,
                'beta2': 0.999,
                'amsgrad': True,
                'weight_decay': 0.0001,
                'grad_norm': 5},
            'lambda':{
                'lambda_rec': 10,
                'lambda_kl': 1},
            'annealing_iters': 20000,
            }
        model = cc(AE(config))
        optimizer = config['optimizer']
        opt = torch.optim.Adam(model.parameters(),
        lr=optimizer['lr'], betas=(optimizer['beta1'], optimizer['beta2']),
        amsgrad=optimizer['amsgrad'], weight_decay=optimizer['weight_decay'])
        for iteration in range(n_iterations):
            if iteration >= config['annealing_iters']:
                lambda_kl = config['lambda']['lambda_kl']
            else:
                lambda_kl = config['lambda']['lambda_kl'] * (iteration + 1) / config['annealing_iters']
            data = next(iter(train_loader))
            meta = ae_step(data, lambda_kl)
            # add to logger
            loss_rec = meta['loss_rec']
            loss_kl = meta['loss_kl']

            print(f'AE:[{iteration + 1}/{n_iterations}], loss_rec={loss_rec:.2f}, '
                    f'loss_kl={loss_kl:.2f}, lambda={lambda_kl:.1e}     ', end='\r')
            if (iteration + 1) % 100 == 0 or iteration + 1 == n_iterations:
                save_model(iteration=iteration)
                print()
        emb_res = []
        for batch in train_loader:
            without_spl = model.get_content_embeddings(cc(batch['emb'].unsqueeze(-1)))
            emb_res.append(without_spl.cpu().data.numpy())
        no_spl_emb = np.concatenate(emb_res, axis = 0)
        return no_spl_emb
