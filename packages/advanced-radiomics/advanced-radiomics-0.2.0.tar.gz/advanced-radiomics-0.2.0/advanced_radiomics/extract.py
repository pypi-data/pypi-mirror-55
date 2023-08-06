import numpy as np
import pandas as pd
import SimpleITK as sitk
from radiomics import firstorder, glcm, imageoperations, shape, glrlm, glszm, shape2D, ngtdm, gldm
from scipy import ndimage
import sys
import os 
import six
import logging

logging.disable(logging.CRITICAL)

sys.setrecursionlimit(30000)

# Funções de geração de dados ---------------------------------------------------------------------------

def generateRandomImage(size, lims=[0,255]):
    """
    Create random image with numpy.random.random.

    Parameters
    ----------
    size : tuple
        Shape of image.
    lims : list
        Min and Max values of the image.

    Returns
    -------
    image : SimpleITK.Image
        Random image created.

    Examples
    --------

    >>> import SimpleITK as sitk
    >>> image = generateRandomImage((2,3,4))
    >>> print(sitk.GetArrayFromImage(image))
    [[[ 10 208  58 210]
      [253 142  92 100]
      [240  12  31 244]]
     [[ 50 119 103 103]
      [225 130  85  60]
      [ 63 121 226 239]]]
    
    """
    a,b = lims
    image_array = (b-a)*np.random.random(size) + a
    image = sitk.GetImageFromArray(image_array.astype(int))
    return image


def generateRandomMask(size, p=0.5):
    """
    Create random mask with numpy.random.random.

    Parameters
    ----------
    size : tuple
        Shape of image.
    p : float
        Percentual of values equal to 0 in mask.

    Returns
    -------
    mask : SimpleITK.Image
        Random mask created.

    Examples
    --------

    >>> import SimpleITK as sitk
    >>> mask = generateRandomMask((2,3,4))
    >>> print(sitk.GetArrayFromImage(mask))
    [[[0 0 1 1]
      [0 1 0 0]
      [1 1 0 1]]
     [[1 1 1 0]
      [1 1 0 0]
      [0 1 1 0]]]
    
    """
    mask_array = (np.random.random(size) > p).astype(int)
    mask = sitk.GetImageFromArray(mask_array) 
    return mask

def generateBoth(size, lims=[0,255], p=0.5):
    """
    Create random both image and mask with numpy.random.random.

    Parameters
    ----------
    size : tuple
        Shape of image.
    p : float
        Percentual of values equal to 0 in mask.
    lims : list
        Min and Max values of the image.

    Returns
    -------
    image : SimpleITK.Image
        Random image created.
    mask : SimpleITK.Image
        Random mask created.

    Examples
    --------

    >>> import SimpleITK as sitk
    >>> image, mask = generateBoth((2,3,4))
    >>> print(sitk.GetArrayFromImage(image))
    [[[222 221  50 176]
      [186 217  82  16]
      [160 133  53   4]]
     [[ 16 162 157 206]
      [ 24 130 228 136]
      [ 24  78  50 180]]]

    >>> print(sitk.GetArrayFromImage(mask))
    [[[1 1 0 0]
      [0 0 0 1]
      [0 0 0 0]]
     [[1 1 1 1]
      [1 0 0 1]
      [0 0 0 1]]]
    
    """
    image, mask = generateRandomImage(size, lims), generateRandomMask(size, p)
    return image, mask

#Funções Abrir arquivos ----------------------------------------------------------

def openFile(path_name):
    """
    Create an image object of SimpleITK given the file/directory name.

    Parameters
    ----------
    path_name : string
        Path to file/diretory

    Returns
    -------
    image : SimpleITK.Image
        Image opened.

    Examples
    --------

    >>> image = openFile("image.nrrd")

    """
    if os.path.isdir(path_name):
        reader = sitk.ImageSeriesReader()
        dicom_names = reader.GetGDCMSeriesFileNames(path_name)
        reader.SetFileNames(dicom_names)
        image_object = reader.Execute()
    
    elif os.path.isfile(path_name):
        image_object = sitk.ReadImage(path_name)

    else:
        print("Path name wrong.")
        return None

    return image_object 

# Funções de alteração das imagens -------------------------------------------------

def filterStatistical(image_object, filter_type="prewitt", sigma=1):
    """
    Filter the image input. Supports 4 types of filters.

    Parameters
    ----------
    image_object : SimpleITK.Image
        Image to filter.
    filter_type : str, optional (default="prewitt")
        Type of filter. The filters are "prewitt", "sobel", "laplace", "LoG".
    sigma : int, optional (default=1)
        Sigma of LoG. Only works if filter_type is equal to "LoG".

    Returns
    -------
    image_filt_object : SimplITK.Image
        Image filtered.

    """
    image_array = sitk.GetArrayFromImage(image_object)

    filters = {"prewitt": ndimage.prewitt, "sobel": ndimage.sobel, 
               "laplace": ndimage.laplace, "LoG": ndimage.gaussian_laplace}

    filter_func = filters[filter_type]
    if filter_type == "LoG":
        image_filt_object = sitk.GetImageFromArray(filter_func(image_array, sigma))
    else:    
        image_filt_object = sitk.GetImageFromArray(filter_func(image_array))
    return image_filt_object

def reduceSize(image_object, mask_object):
    """
    Reduce the size of both image and mask, where is the VOI.

    Parameters
    ----------
    image_object : SimpleITK.Image
        Image Object with the original image.
    mask_object : SimpleITK.Image
        Image Object with the mask.

    Returns
    -------
    red_image_object : SimpleITK.Image
        Image Object with the image reduced.
    red_mask_object : SimpleITK.Image
        Image Object with the mask reduced.

    Examples
    --------

    >>> image = openFile("image.nrrd")
    >>> mask = openFile("mask.nrrd")
    >>> im, mk = reduceSize(image, mask)

    """
    mask_np = sitk.GetArrayFromImage(mask_object)
    image_np = sitk.GetArrayFromImage(image_object)
    d,l,c = mask_np.shape
    dim = [[],[],[]]
    for k in range(d):
        if mask_np[k,:,:].max() == 0:
            continue
        else:
            dim[0].append(k)
        for i in range(l):
            if mask_np[k,i,:].max() == 0:
                continue
            else:
                dim[1].append(i)
            for j in range(c):
                if mask_np[k,i,j] == 1:
                    dim[2].append(j)
                    
    mask = mask_np[min(dim[0]):max(dim[0])+1, min(dim[1]):max(dim[1])+1, min(dim[2]):max(dim[2])+1]
    image = image_np[min(dim[0]):max(dim[0])+1, min(dim[1]):max(dim[1])+1, min(dim[2]):max(dim[2])+1]

    red_image_object = sitk.GetImageFromArray(image)
    red_mask_object = sitk.GetImageFromArray(mask)

    return red_image_object, red_mask_object

def createBin(image_object, num=8):
    """
    Create image with 'num' bins.

    Parameters
    ----------
    image_object : SimpleITK.Image
        Original image.
    num : int
        Number of bins, default = 8.

    Returns
    -------
    image_object_bin : SimpleITK.Image
        Image with 'num' bins.

    """
    image_array = sitk.GetArrayFromImage(image_object)
    _, bin_edges = np.histogram(image_array.flatten(), bins=num)
    bin_edges[-1] += 1
    for i in range(num):
        image_array[(image_array >= bin_edges[i]) & (image_array < bin_edges[i+1])] = i+1
    image_object_bin = sitk.GetImageFromArray(image_array)
    return image_object_bin


# Função de extração -----------------------------------------------------------------

def extractFeatures(image, mask, name, binCount=8, features="all"):
    """
    Extract the features by type.

    Parameters
    ----------
    image : SimpleITK.Image
        Original image.
    mask : SimpleITK.Image
        Image's mask.
    name : str
        Identifier.
    binCount : int, optional (default=8)
        Number of bins.
    features : str or list, optional (default="all")
        If "all", calculate all features. If list, must contain at least one of these strings:
        * "FO" -> First Order
        * "S3D" -> Shap
        * "GLCM" -> GLCM
        * "GLSZM" -> GLSZM
        * "GLRLM" -> GLRLM
        * "NGTDM" -> NGTDM
        * "GLDM" -> GLDM

    Returns
    -------
    df -> pandas.DataFrame
        Dataframe with features calculated.

    """
    def extractType(func, type_name):
        name = []
        values = []
        feat = func(image,mask, binCount=binCount)
        feat.enableAllFeatures()  
        feat.execute()
        for (key,val) in six.iteritems(feat.featureValues):
            name.append(key+f'_{type_name}')
            values.append(val)
        return pd.DataFrame([values], columns=name)

    features_array = np.array(["FO", "S3D", "GLCM", "GLSZM", "GLRLM", "NGTDM", "GLDM"])
    features_func = np.array([firstorder.RadiomicsFirstOrder, shape.RadiomicsShape, glcm.RadiomicsGLCM,
                              glszm.RadiomicsGLSZM, glrlm.RadiomicsGLRLM, ngtdm.RadiomicsNGTDM, 
                              gldm.RadiomicsGLDM])
    if features != "all":
        if features is str:
            print("Type wrong. Returning None.")
            return None
        index = pd.Index(features_array).isin(features)
        features_array = features_array[index]
        features_func = features_func[index]

    list_feat = list(map(lambda i: extractType(features_func[i], features_array[i]), np.arange(len(features_array))))
    df = pd.concat([pd.DataFrame([name], columns=["Caso"])] + list_feat, axis=1)
    return df

def extractFilterStatistics(image, mask, name, filter_type="prewitt", sigma=1, binCount=8):
    """
    Extract First Order feature's of the filtered image.

    Parameters
    ----------
    image : SimpleITK.Image
        Original image.
    mask : SimpleITK.Image
        Image's mask.
    name : str
        Identifier.
    filter_type : str, optional (default="prewitt")
        Type of filter. The filters are "prewitt", "sobel", "laplace", "LoG".
    binCount : int, optional (default=8)
        Number of bins.
    sigma : int, optional (default=1)
        Sigma of LoG. Only works if filter_type is equal to "LoG".

    Returns
    -------
    features : pandas.DataFrame
        Dataframe with features.

    """
    image_filt = filterStatistical(image, filter_type, sigma)
    features = extractFeatures(image_filt, mask, name, binCount=binCount, features=["FO"])
    return features


def multiVOI(image_object, mask_object, name, binCount=8):
    """
    Separate VOI's.

    Parameters
    ----------
    image_object : SimpleITK.Image
        Original image.
    mask_object : SimpleITK.Image
        Mask image.
    name : string
        Identifier.
    binCount : int
        Number of bins.

    Returns
    -------
    dados : pandas.DataFrame
        DataFrame with features per VOI.

    """

    # Auxiliar functions -------------------------------

    def remove(matrix, old, new):
        matrix[matrix==old] = new
        return matrix
    
    def findElement(matrix, element):
        l,c = matrix.shape
        matrix_f = matrix.flatten()*element
        arg_max = np.argmax(matrix_f)
        i = arg_max//c
        j = arg_max%c
        return i,j

    def searchVOI(matrix, p):
        l,c = matrix.shape
        i,j = p
        matrix[i,j] = -1
        actions = (i!=0)*[[-1,0]] + (j!=c-1)*[[0,1]] + (i!=l-1)*[[1,0]] + (j!=0)*[[0,-1]]  + (i!=0 and j!=0)*[[-1,-1]] + (i!=0 and j!=c-1)*[[-1,1]] + (i!=l-1 and j!=0)*[[1,-1]] + (i!=l-1 and j!=c-1)*[[1,1]]

        for a in actions:
            di, dj = a
            if matrix[i+di,j+dj] == 1:

                matrix = searchVOI(matrix, (i+di,j+dj))
                
        return matrix

    # --------------------------------------------------

    seg = sitk.GetArrayFromImage(mask_object)
    seg = seg.astype(np.int8)
    d,l,c = seg.shape
    dados = None
    
    cont = 1
    while True:
        find = False
        seg_copy = seg.copy()
        seg_copy = seg_copy.astype(np.int8)
        seg_i = np.zeros(seg.shape, dtype = np.int8)
        for k in range(d):
            if find: # Já encontrou uma segmentação
                if seg_copy[k,:,:].min() != -1: # Prox layer não possui mais continuação da mesma
                    break
                i,j = findElement(seg_copy[k,:,:].copy(), -1)
                seg_i[k,:,:] = remove(searchVOI(seg[k,:,:].copy(),(i,j)),1,0)
                if k < d-1:
                    seg_copy[k+1,:,:] *= remove(seg_i[k,:,:].copy(),0,1)
                continue


            if seg_copy[k,:,:].max() == seg_copy[k,:,:].min(): # Não possui nenhuma segmentação na layer selecionada
                continue


            i,j = findElement(seg_copy[k,:,:].copy(), 1) # Inicio da segmentação 
            seg_i[k,:,:] = remove(searchVOI(seg[k,:,:].copy(),(i,j)),1,0)
            find = True
            if k < d-1:
                seg_copy[k+1,:,:] *= remove(seg_i[k,:,:].copy(),0,1)

        if np.sum(seg_i) == 0:
            break

        print(f"Segmentação {cont} concluída!")

        mask = sitk.GetImageFromArray(seg_i*(-1))

        if dados is None:
            dados = extractFeatures(image_object, mask, name+f"_{cont}", binCount)
        else:
            dados = pd.concat([dados, extractFeatures(image_object, mask, name+f"_{cont}", binCount)], axis=0)
        cont += 1
        seg += np.array(seg_i)

    return dados