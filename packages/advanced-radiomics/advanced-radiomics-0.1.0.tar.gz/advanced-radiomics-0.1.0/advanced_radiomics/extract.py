import numpy as np
import pandas as pd
import SimpleITK as sitk
from radiomics import firstorder, glcm, imageoperations, shape, glrlm, glszm, shape2D, ngtdm, gldm
import sys
import os 
import six
import logging

logging.disable(logging.CRITICAL)

sys.setrecursionlimit(30000)

# Funções de geração de dados ---------------------------------------------------------------------------

def generateRandomImageObject(size, lims=[0,255]):
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
    >>> image = generateRandomImageObject((2,3,4))
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


def generateRandomMaskObject(size, p=0.5):
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
    >>> mask = generateRandomMaskObject((2,3,4))
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
    image, mask = generateRandomImageObject(size, lims), generateRandomMaskObject(size, p)
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

def extractFeatures(image, mask, name, binCount=8):
    """
    Extract all radiomics features from a image with it's mask.

    Parameters
    ----------
    image : SimpleITK.Image
        Original image.
    mask : SimpleITK.Image
        Image's mask.
    name : string
        String with the identifier of image (name, ID or other).
    binCount : int
        Number of bins, default = 8.

    Returns
    -------
    data : pandas.DataFrame
        DataFrame with the features

    Examples
    --------

    >>> image = openFile("image.nrrd")
    >>> mask = openFile("mask.nrrd")
    >>> df = extractFeatures(image, mask, "John")

    """
    firstOrderFeatures = firstorder.RadiomicsFirstOrder(image,mask, binCount=binCount)
    firstOrderFeatures.enableAllFeatures()  # On the feature class level, all features are disabled by default.
    firstOrderFeatures.execute()
    names = ['Caso']
    values = [name]
    for (key,val) in six.iteritems(firstOrderFeatures.featureValues):
        names.append(key+'_FO')
        values.append(val)

    shape_3D = shape.RadiomicsShape(image,mask, binCount=binCount)
    shape_3D.enableAllFeatures()  # On the feature class level, all features are disabled by default.
    shape_3D.execute()
    for (key,val) in six.iteritems(shape_3D.featureValues):
        names.append(key+'_S3D')
        values.append(val)

    GLCM = glcm.RadiomicsGLCM(image,mask, binCount=binCount)
    GLCM.enableAllFeatures()  # On the feature class level, all features are disabled by default.
    GLCM.execute()
    for (key,val) in six.iteritems(GLCM.featureValues):
        names.append(key+'_GLCM')
        values.append(val)

    GLSZM = glszm.RadiomicsGLSZM(image,mask, binCount=binCount)
    GLSZM.enableAllFeatures()  # On the feature class level, all features are disabled by default.
    GLSZM.execute()
    for (key,val) in six.iteritems(GLSZM.featureValues):
        names.append(key+'_GLSZM')
        values.append(val)

    GLRLM = glrlm.RadiomicsGLRLM(image,mask, binCount=binCount)
    GLRLM.enableAllFeatures()  # On the feature class level, all features are disabled by default.
    GLRLM.execute()
    for (key,val) in six.iteritems(GLRLM.featureValues):
        names.append(key+'_GLRLM')
        values.append(val)


    NGTDM = ngtdm.RadiomicsNGTDM(image,mask, binCount=binCount)
    NGTDM.enableAllFeatures()  # On the feature class level, all features are disabled by default.
    NGTDM.execute()
    for (key,val) in six.iteritems(NGTDM.featureValues):
        names.append(key+'_NGTDM')
        values.append(val)


    GLDM = gldm.RadiomicsGLDM(image, mask, binCount=binCount)
    GLDM.enableAllFeatures()
    GLDM.execute()
    for (key,val) in six.iteritems(GLDM.featureValues):
        names.append(key+'_GLDM')
        values.append(val)


    values = np.array(values)
    values = values.reshape((1,values.size))

    data = pd.DataFrame(values, columns = names)

    return data


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