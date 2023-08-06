Used
----

To use, simple do::

>>> from zalopaysupport import prepareResourceBeforeUpload, uploadImagesToZPSVN
>>> input = './images'
>>> output = './output'
>>> subFolderOnSVN = 'subfolder'
>>> prepareResourceBeforeUpload(input, target)
>>> uploadImagesToZPSVN(output, subFolderOnSVN)

Functions
---------
>>> prepareResourceBeforeUpload

>>> uploadImagesToZPSVN

>>> renameAllFolderAndFile

>>> renameToRemoveResolutionSuffix

>>> yes_no

>>> choose_environment

>>> choose_multi_environment


Public python package
---------------------

>>> python3 setup.py sdist
>>> twine check dist/*
>>> twine upload dist/*