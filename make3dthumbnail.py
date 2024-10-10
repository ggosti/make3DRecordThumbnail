import argparse
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pathlib

def dir_path(string):
    if os.path.isdir(string):
        return string
    else:
        raise NotADirectoryError(string)

def setAxLim2BBox(ax,BBox,yup=True):
    """Sets axis limits to match bounding box.

    Parameters:
    --------
    pathDir -- directory path string    

    Usage examples:
    >>> BBox = {'x0':-1.,'x1':+1.}
    >>> fig = plt.figure()
    >>> ax = fig.add_subplot()
    >>> setAxLim2BBox(ax,BBox)
    >>> ax.get_xlim()
    (-1.0, 1.0)
    """
    if yup:
        if 'x0' in BBox: ax.set_xlim((BBox['x0'],BBox['x1']))
        if 'y0' in BBox: ax.set_zlim((BBox['y0'],BBox['y1']))
        if 'z0' in BBox:
            if hasattr(ax, 'get_zlim'):
                ax.set_ylim((BBox['z0'],BBox['z1']))
    else:
        if 'x0' in BBox: ax.set_xlim((BBox['x0'],BBox['x1']))
        if 'y0' in BBox: ax.set_ylim((BBox['y0'],BBox['y1']))
        if 'z0' in BBox: 
            if hasattr(ax, 'get_zlim'):
                ax.set_zlim((BBox['z0'],BBox['z1']))    

# Read data from csv in folder
def readData(pathDir):
    """Read data from csv in folder.

    Parameters:
    --------
    pathDir -- directory path string

    Examples:
    --------
    >>> ids, fileNames, dfUs, df = readData('./csv-Test/')
    >>> ids
    [0, 1, 2, 3]
    >>> fileNames
    ['U0', 'U1', 'U2', 'U3']
    >>> dfUs[1].index
    RangeIndex(start=0, stop=3, step=1)
    >>> 'time' in df.columns
    True
    >>> 'posx' in df.columns
    True
    >>> 'fx' in df.columns
    True
    >>> 'dirx' in df.columns
    True
    """
    dfUs = [] 
    ids = []
    fileNames = []

    listCSVs = [f for f in os.listdir(pathDir) if f.split('.')[-1] == 'csv']
    listCSVs.sort()

    for uId,f in enumerate(listCSVs):
        # add users ids
        ids.append(uId) 
        fileNames.append(f.split('.')[0])
        print('uId', uId,'f',f)
        dfU = pd.read_csv(pathDir+'/'+f,index_col=False)
        print('columns',dfU.columns,len(dfU))
        dfU.columns = dfU.columns.str.lstrip()
        #print('columns',dfU.columns)
        dfU['ID'] = uId
        dfU['filename'] =f.split('.')[0]
        dfUs.append(dfU)
    return ids, fileNames, dfUs, pd.concat(dfUs,ignore_index=True)

def getVR(dfS):  
    """Gets VR state navigation modality from a session data frames.
    
    Parameters:
    --------
    dfS -- session dataframe

    Return variables:
    --------
    nav --  ndarray 
        Array with true values when navigation modality is VR
    """

    assert (('Time' in dfS.columns) or ('time' in dfS.columns) or ('t' in dfS.columns))  , "neither Time or time or t in csv columns: "+dfS.columns
    
    if 'Time' in dfS.columns:
        timeCol = 'Time'
    elif 'time' in dfS.columns:
        timeCol = 'time'    
    elif 't' in dfS.columns:
        timeCol = 't'  

    t =  dfS[timeCol].values
    nav = np.zeros((len(t),2))
    nav[:,0] = t
    #print(dfU['nav'] )
    boolVR = (dfS['nav'] == 'VR') 
    #print(boolVR )
    nav[:,1] = boolVR.values    
    return nav
    

def getAR(dfS):  
    """Gets AR state navigation modality from a session data frames.
    
    Parameters:
    --------
    dfS -- session dataframe

    Return variables:
    --------
    navs --  ndarray 
        Array with true values when navigation modality is AR
    """

    assert (('Time' in dfS.columns) or ('time' in dfS.columns) or ('t' in dfS.columns))  , "neither Time or time or t in csv columns: "+dfS.columns
    
    if 'Time' in dfS.columns:
        timeCol = 'Time'
    elif 'time' in dfS.columns:
        timeCol = 'time'    
    elif 't' in dfS.columns:
        timeCol = 't'
    

    t =  dfS[timeCol].values
    nav = np.zeros((len(t),2))
    nav[:,0] = t
    #print(dfU['nav'] )
    boolVR = (dfS['nav'] == 'AR') 
    #print(boolVR )
    nav[:,1] = boolVR.values    
    return nav

def getVRs(ids,dfSs):
    """Gets a navigation modality from a list of session data frames.
    
    Parameters:
    --------
    ids -- sessions ids 
    dfUs -- sessions dataframe

    Return variables:
    --------
    navs --  list of ndarray 
        list of Array of navigation modality
    """

    navs = [getVR(dfS) for uId,dfS in zip(ids,dfSs)]

    return navs

def getPath(dfS,listCols = ['posx','posy','posz']):
    """Gets a paths extracting equal length colums from a session data frames.

    Parameters:
    --------
    ids -- session ids 
    dfS -- session dataframe
    listCols -- list of columns keys for the columns to be extracted

    Return variables:
    --------
    navs --  ndarray 
        Array of navigation
    """

    assert (('Time' in dfS.columns) or ('time' in dfS.columns) or ('t' in dfS.columns))  , "neither Time or time or t in csv columns: "+dfS.columns
    
    if 'Time' in dfS.columns:
        timeCol = 'Time'
    elif 'time' in dfS.columns:
        timeCol = 'time'    
    elif 't' in dfS.columns:
        timeCol = 't'

    t =  dfS[timeCol].values
    path = np.zeros((len(t),len(listCols)+1))
    path[:,0] = t 
    for c,colName in enumerate(listCols):
        path[:,c+1] = dfS[colName].values 

    return path

def getPaths(ids,dfSs,listCols = ['posx','posy','posz']):
    """Gets a paths extracting equal length colums from a list of sessions data frames.

    Parameters:
    --------
    ids -- session ids 
    dfUs -- session dataframe
    listCols -- list of columns keys for the columns to be extracted

    Examples:
    --------
    >>> ids, fileNames, dfSs, df = readData('csv-Test/')
    >>> paths = getPaths(ids,dfSs)
    >>> len(paths)
    4
    >>> paths[0]
    array([[ 1.   , -0.57 ,  1.57 ,  3.5  ],
           [ 2.   , -0.569,  1.6  ,  3.49 ],
           [ 3.   , -0.566,  1.63 ,  3.48 ]])
    >>> dpaths = getPaths(ids,dfSs,['dirx','diry','dirz'])
    >>> len(dpaths)
    4
    >>> dpaths[0]
    array([[ 1.   ,  0.2  , -0.919, -0.341],
           [ 2.   ,  0.222, -0.779, -0.586],
           [ 3.   ,  0.254, -0.648, -0.718]])
    """

    paths = [getPath(dfS,listCols) for uId,dfS in zip(ids,dfSs)]  

    return paths


def getVarsFromSession(path,varsName):
    """Gets variables from a sessions folder.

    Parameters:
    --------
    path -- path to sessions .csv 

    Examples:
    --------
    >>> ids, fileNames,paths = getVarsFromSession('csv-Test/','pos')
    >>> len(fileNames)
    4
    >>> len(paths)
    4
    >>> paths[0]
    array([[ 1.   , -0.57 ,  1.57 ,  3.5  ],
           [ 2.   , -0.569,  1.6  ,  3.49 ],
           [ 3.   , -0.566,  1.63 ,  3.48 ]])
    >>> ids, fileNames,dpaths = getVarsFromSession('csv-Test/','dir')
    >>> len(dpaths)
    4
    >>> dpaths[0]
    array([[ 1.   ,  0.2  , -0.919, -0.341],
           [ 2.   ,  0.222, -0.779, -0.586],
           [ 3.   ,  0.254, -0.648, -0.718]])
    """
    ids, fileNames, dfSs, df = readData(path)

    #print('varN',varN)
    if varsName == 'nav':
        data = getVRs(ids,dfSs)
    elif varsName == 'pos':
        data = getPaths(ids,dfSs,['posx','posy','posz'])   
    elif varsName == 'dir':
        data = getPaths(ids,dfSs,['dirx','diry','dirz'])
    elif varsName == 'f':
        data = getPaths(ids,dfSs,['fx','fy','fz'])
    return ids, fileNames,data

def drawPath(path,dpath=None,BBox=None,ax=None,yup=True,colorbar=False,pointSize=1):
    """draw path 2D and 3D

    Parameters:
    --------
    path -- array 
    width -- bins width   
    
    Examples:
    --------
    >>> path = np.random.rand(10,4)
    >>> ax,sc = drawPath(path,dpath=None,BBox=None,ax=None)
    >>> cbar = plt.colorbar(sc, ax=ax)
    >>> 'Axes3D' in str(type(ax))
    True
    >>> ax.lines
    <Axes.ArtistList of 1 lines>
    """
    if ax == None:
        fig = plt.figure()
        if path.shape[1] == 4:
            ax = fig.add_subplot(projection='3d')
        else:
            ax = fig.add_subplot()
    ax.set_xlabel('x')

    if path.shape[1] == 4:
        t,x,y,z = path.T
        if hasattr(dpath, "__len__"): 
            qt,u,v,w = dpath.T
        if yup:
            #print('yup')
            ax.set_ylabel('z')
            ax.set_zlabel('y')
            ax.plot(x,z,y)
            sc = ax.scatter(x,z,y,c=t,s=pointSize)
            if hasattr(dpath, "__len__"):
                ax.quiver(x,z,y,u,w,v,color='gray',alpha=0.2)
                sc = ax.scatter(x+u,z+w,y+v,c=t,s=pointSize)
        else:
            ax.set_ylabel('y')
            ax.set_zlabel('z')
            ax.plot(x,y,z)
            sc = ax.scatter(x,y,z,c=t,s=pointSize)
            if hasattr(dpath, "__len__"):
                ax.quiver(x,y,z,u,v,w,color='gray',alpha=0.2)
                sc = ax.scatter(x+u,y+v,z+w,c=t,s=pointSize)
        if colorbar: plt.colorbar(sc, ax=ax)
    if path.shape[1] == 3:
        ax.set_ylabel('y')
        t,x,y = path.T
        ax.plot(x,y)
        sc = ax.scatter(x,y,c=t,s=pointSize)
        if colorbar: plt.colorbar(sc, ax=ax)
        if hasattr(dpath, "__len__"):
            qt,u,v = dpath.T
            ax.quiver(x,y,u,v,color='gray',alpha=0.2)       
    
    if isinstance(BBox , dict):
        setAxLim2BBox(ax,BBox,yup=yup)
    return ax,sc

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generate png preview of records from group')
    parser.add_argument('--path', type=dir_path, help='Path to folder with sessions.')
    parser.add_argument('--opath', type=dir_path, help='Path to output folder if different from folder with serrions (--path).')
    parser.add_argument('--ext', type=str, default='.jpg',  help='Select thumbnails image format (default .jpg).')
    parser.add_argument('--suffix', type=str, default='',  help='Add suffix to file name (default None).')

    args = parser.parse_args()


    pathSes  = args.path
    print('path',pathSes)
    fileNameExt = args.suffix + args.ext
    print('fileNameExt',fileNameExt)
    ids, fileNames, paths = getVarsFromSession(pathSes,'pos')
    ids, fileNames, dpaths = getVarsFromSession(pathSes,'dir')

    groupName = str(pathlib.PurePath(pathSes).stem)
    print('group',groupName)

    if args.opath == None:
        opath = pathlib.PurePath(pathSes)
        print('opath',opath)
    else:
        opath  = pathlib.PurePath(args.opath)
        print('output path',opath)
        #opath =  opath / 'prep' 
        opath =  opath / ( groupName+'-thumbnails')
        print('output path',opath)
        if not os.path.exists(opath):
            os.makedirs(opath)

    for i,(fname,path,dpath) in enumerate(zip(fileNames,paths,dpaths)):
        fig = plt.figure(figsize=(6,6))
        ax = fig.add_subplot(projection='3d')
        t,x,y,z = path.T
        ax,sc = drawPath(path,dpath=dpath,BBox=None,ax=ax)
        # Get rid of colored axes planes
        # First remove fill
        ax.xaxis.pane.fill = False
        ax.yaxis.pane.fill = False
        ax.zaxis.pane.fill = False
        fname = fname + fileNameExt #'.jpg' #'-prev.png'
        print('fname',fname)
        plt.savefig(opath / fname, transparent=True)
        plt.close()
    #plt.show()
    
