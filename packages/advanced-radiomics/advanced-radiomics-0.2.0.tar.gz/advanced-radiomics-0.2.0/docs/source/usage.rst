=====
Usage
=====

Start by importing Advanced Radiomics.

.. code-block:: python

    import advanced_radiomics


Module Extract
--------------

This module is used to generate random images/mask (for research), open files, 
transform images (reduce the size, create image with bins) and extract features for
one segmentation or multiples segmentations (multiVOI).

.. autofunction:: advanced_radiomics.extract.generateRandomImage
.. autofunction:: advanced_radiomics.extract.generateRandomMask
.. autofunction:: advanced_radiomics.extract.generateBoth
.. autofunction:: advanced_radiomics.extract.openFile
.. autofunction:: advanced_radiomics.extract.filterStatistical
.. autofunction:: advanced_radiomics.extract.reduceSize
.. autofunction:: advanced_radiomics.extract.createBin
.. autofunction:: advanced_radiomics.extract.extractFeatures
.. autofunction:: advanced_radiomics.extract.extractFilterStatistics
.. autofunction:: advanced_radiomics.extract.multiVOI

Module Analysis
---------------

This module is for calculate statistics and other informations about the data.

.. autofunction:: advanced_radiomics.analysis.separateFeatures

Module Visualization
--------------------

This module is used to visualizate the data and to visualizate some informations, like PCA.

.. autofunction:: advanced_radiomics.visualization.showImageMask
.. autofunction:: advanced_radiomics.visualization.plotPCA