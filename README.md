# make3DRecordThumbnail

Make a thumbnail for 3D data csv records.

## Dependencies
To install dependencis with conda:
```
conda create -n 3dtb numpy matplotlib pandas
```
To activate enviroment
```
conda activate 3dtb
```

## Test

To test script

```
python -m doctest make3dthumbnail.py
```

To test script in verbose mode
```
python -m doctest -v make3dthumbnail.py
```

## Run 

To make jpg preview of 3D paths and put preview in same folder,
```
python make3dthumbnail.py --path path/to/group/folder
```
To make png preview of 3D paths and put in different output folder
```
python make3dthumbnail.py --path path/to/group/folder --opath path/to/group