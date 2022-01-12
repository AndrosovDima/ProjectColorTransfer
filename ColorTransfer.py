import ot
import numpy as np
import matplotlib.pyplot as plt
# from matplotlib.pyplot import imread
# from mpl_toolkits.mplot3d import Axes3D
from sklearn.cluster import MiniBatchKMeans
# import os
import cv2



class ColorTranseferer():
    def __init__(self, photo_1, photo_2):
        self.I1 = cv2.imdecode(np.frombuffer(photo_1, np.uint8), -1) / 256
        self.I2 = cv2.imdecode(np.frombuffer(photo_2, np.uint8), -1) / 256

    def im2mat(self, I):
        '''Преобразует картинку I в матрицу'''
        return I.reshape(-1, 3)

    def mat2im(self, X, shape):
        '''Преобразует матрицу X в картинку размерами 'shape'.'''
        return X.reshape(shape)

    def showImageAsPointCloud(self, X, Y):
        '''Показывает цветовую палитру для картинок X и Y.'''
        fig = plt.figure(figsize=(17, 8))
        ax = fig.add_subplot(121, projection='3d')
        ax.set_xlim(0, 1)
        ax.scatter(X[:, 0], X[:, 1], X[:, 2], c=X, s=10, marker='o', alpha=0.6)
        ax.set_xlabel('R', fontsize=22)
        ax.set_xticklabels([])
        ax.set_ylim(0, 1)
        ax.set_ylabel('G', fontsize=22)
        ax.set_yticklabels([])
        ax.set_zlim(0, 1)
        ax.set_zlabel('B', fontsize=22)
        ax.set_zticklabels([])
        ax.set_title('Initial Color Palette', fontsize=20)
        ax.grid('off')

        ax = fig.add_subplot(122, projection='3d')
        ax.set_xlim(0, 1)
        ax.scatter(Y[:, 0], Y[:, 1], Y[:, 2], c=Y, s=10, marker='o', alpha=0.6)
        ax.set_xlabel('R', fontsize=22)
        ax.set_xticklabels([])
        ax.set_ylim(0, 1)
        ax.set_ylabel('G', fontsize=22)
        ax.set_yticklabels([])
        ax.set_zlim(0, 1)
        ax.set_zlabel('B', fontsize=22)
        ax.set_zticklabels([])
        ax.set_title('Target Color Palette', fontsize=20)
        ax.grid('off')
        plt.show()

    def colorTransfer(self, OT_plan, kmeans1, kmeans2, shape):
        '''Возвращает картинку с перенесенным цветом размерами "shape".'''
        samples_transformed = OT_plan.dot(kmeans2.cluster_centers_)
        X1_transformed = samples_transformed[kmeans1.labels_]
        return self.mat2im(X1_transformed, shape)

    def transfer_color(self, method='C_1'):
        '''Главная функция переноса цвета'''
        # plotting input pictures
        # fig = plt.figure(figsize=(17, 30))
        # ax = fig.add_subplot(1, 2, 1)
        # ax.imshow(self.I1)
        # ax.set_title('photo', fontsize=25)
        # ax.axis('off')
        # ax = fig.add_subplot(1, 2, 2)
        # ax.imshow(self.I2)
        # ax.set_title('photo with color to transfer', fontsize=25)
        # ax.axis('off')
        # plt.show()

        X1 = self.im2mat(self.I1)
        X2 = self.im2mat(self.I2)

        nbsamples = 1000

        kmeans1 = MiniBatchKMeans(n_clusters=nbsamples, init_size=nbsamples).fit(X1)
        X1_sampled = kmeans1.cluster_centers_

        kmeans2 = MiniBatchKMeans(n_clusters=nbsamples, init_size=nbsamples).fit(X2)
        X2_sampled = kmeans2.cluster_centers_

        # self.showImageAsPointCloud(X1_sampled, X2_sampled)

        C_1 = np.ones((nbsamples, nbsamples))
        C_2 = np.ones((nbsamples, nbsamples))
        for i in range(nbsamples):
            for j in range(nbsamples):
                C_1[i, j] = np.linalg.norm(X1_sampled[i] - X2_sampled[j])
                C_2[i, j] = C_1[i, j] ** 2

        if method == 'C_1':
            metric = C_1
        else:
            metric = C_2

        OT_plan = ot.emd(np.ones(nbsamples), np.ones(nbsamples), metric)

        I = self.colorTransfer(OT_plan, kmeans1, kmeans2, self.I1.shape)
        I = cv2.convertScaleAbs(I, alpha=(255.0))

        return cv2.imencode('.jpeg', I)[1].tostring()
