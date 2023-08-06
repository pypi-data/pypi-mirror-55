# SONYC_CAPSTONE_VIS.py
import os
import time
import random
import pickle
from datetime import datetime

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

        # bars = ax.bar(
        #     theta, [3000]*24,
        #     width=width-0.03,
        #     bottom=bottom,
        #     color="#f39c12", alpha=0.2
        # )

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
        # fig.set_size_inches(15, 7)

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
        print('Sample from {} sensors, taking min({}, len) data points from each sensor. \n'.format(len(sensor_list),
                                                                                                    sample_size))
        sample_ind= {}
        features = []
        row_numbers = []
        for sensor in sensor_list:
            feature_path = f'{parent_dir}/sonycnode-{sensor}.sonyc_features_openl3.h5'
            f = h5.File(feature_path,'r')
            data = f[list(f.keys())[0]]
            print(f'sampling from {sensor}, data size = {data.shape[0]}')
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
            print(f'Took {(time.time() - st)/60} mins to finish sampling from {sensor}\n')
        print('Total sampled date points = {}'.format(len(features)))
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
            print('start '+sensor)
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
        print('size = {}: {} from test and valid, {} from train'.format(len(feat_names), len(test_val), len(train_agg)))
        annotation_labels = list(truth.labels.values)
        print('number of unique labels in truth: '+str(len(truth.labels.unique())))
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
        return features, spl_mean, multi_probs

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
    def PCA(features, n_components):
        emb1 = features.emb.values.tolist()

        pca = PCA(n_components=n_components)
        pca.fit(emb1)
        pca_out = pca.transform(emb1)

        print(pca_out.shape)
        print("pca explained variance ratio: " + str(sum(pca.explained_variance_ratio_)))
#         print(sum(pca.explained_variance_ratio_[:64]))
        return pca_out
