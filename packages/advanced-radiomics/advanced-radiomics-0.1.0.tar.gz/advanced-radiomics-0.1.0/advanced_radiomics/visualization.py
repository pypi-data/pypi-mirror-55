import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
import scipy.stats as stats
import SimpleITK as sitk
import cv2


# Visualization Data ---------------------------------------------------------------------------------------

def showImageMask(image_object, mask_object):
	"""
	Show image and mask side by side.

	Parameters
	----------
	image_object : SimpleITK.Image
		Image object of original image.
	mask_object : SimpleITK.Image
		Image object of the mask.

	"""
	image_array = sitk.GetArrayFromImage(image_object)
	image_array_scale = (((image_array - image_array.min())/(image_array.max() - image_array.min())) * 255).astype('uint8') 
	mask_array = sitk.GetArrayFromImage(mask_object)
	mask_array_scale = (((mask_array - mask_array.min())/(mask_array.max() - mask_array.min())) * 255).astype('uint8') 
	d,l,c = image_array.shape
	both_image = np.zeros((d,l,2*c), dtype=np.uint8)
	both_image[:,:,:c] = image_array_scale.copy()
	both_image[:,:,c:] = mask_array_scale.copy()
	print("To change frames, use < and >. To quit, use 'Esc'.")
	f = 0
	while True:
		cv2.imshow('Visualization', both_image[f,:,:])
		key = cv2.waitKey(0)
		if key == 27:
			break
		elif key == 44:
			f = max(0, f-1)
		elif key == 46:
			f = min(f+1, d-1)


# Information Visualization --------------------------------------------------------------------------------

def plotPCA(data, target, normalize=False):
    """
	Plot the first and second Principal Components of PCA and Separate Points by a class.

	Parameters
	----------
	data : numpy.array or pandas.DataFrame
		Data with values.
	target : numpy.array, pandas.Series or str
		If the class is in the data, target must be the Column's name of the class.

    """    
    if type(target) is str:
        if type(data) is not pd.DataFrame:
            print("Data is not a Dataframe, class must be array.")
            return None
        Y = data[target].values.reshape((-1,1))
        data = data.drop([target], axis=1).values
        if normalize:
            data = stats.zscore(data)
        pca = PCA(n_components=2).fit(data)
        evr = pca.explained_variance_ratio_
        data_pca = pca.fit_transform(data)
        df = pd.DataFrame(np.concatenate([data_pca, Y],axis=1), 
                          columns=[f"PC1 ({round(evr[0]*100,1)}%)", f"PC2 ({round(evr[1]*100,1)}%)", "Y"])
    else:
    	if type(target) is pd.Series:
    		target = target.values.reshape((-1,1))
    	else:
    		target = target.reshape((-1,1))
    	if type(data) is pd.DataFrame:
    		data = data.values
    	if normalize:
    		data = stats.zscore(data)
    	pca = PCA(n_components=2).fit(data)
    	evr = pca.explained_variance_ratio_
    	data_pca = pca.fit_transform(data)
    	df = pd.DataFrame(np.concatenate([data_pca, target],axis=1), 
                          columns=[f"PC1 ({round(evr[0]*100,1)}%)", f"PC2 ({round(evr[1]*100,1)}%)", "Y"])
    
    sns.relplot(x=df.columns[0], y=df.columns[1], hue=df.columns[2], data=df)
    plt.show()