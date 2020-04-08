# LIDC-IDRI-Extract-64x64x16-nodules
This is a Python script to extract all nodules of the LIDC-IDRI dataset, in 64x64 size. It extracts 16 slices for every nodule to achieve 3D representation

I am not good at writing tutorials and big read me files.

The process is simple:

a. put the config file in your user folder.
b. download everything from LIDC-IDRI.
c. Tune the parameters of the script to obtain more or less slices, to obtain all annotations rather than relying on only one, and more.
d. I forgot to say, you have to install the pylidc library: pip install pylidc

After the execution, you will have all the nodules cropped, with a specific file name, in your directory of choice.

You may improve the script of course, but please refer to this repository if you used it.
