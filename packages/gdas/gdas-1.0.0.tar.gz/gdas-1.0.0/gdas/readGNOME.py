###############################################################################
# Copyright (c) 2019, GNOME Collaboration.
# Produced at the University of Mainz
#
# Written by J. Smiga (joseph.smiga@gmail.com)
#
# All rights reserved.
# This file is part of GDAS.
# For details, see https://gnome.pages.gitlab.rlp.net/gdas/
# For details about use and distribution, please read GDAS/LICENSE.
###############################################################################
# Code for reading GNOME data.
#
# Summary of contents:
# getDataFromFile()-----Gets magnetometer data from single file.
# getFListInRange()-----Gets list of files in time range.
# getDataInRange()------Gets list of data from files in time range.
# getFileNameTime()-----Gets file time from its name.
# getFListFromDates()---Gets list of file names from dates.
# getStartTimes()-------Gets list of start times for set of data files.
# getSaneList()---------Finds which data files contain only 'sane' data.

from gwpy.timeseries import TimeSeries,TimeSeriesList
import h5py
import time, calendar
from os import listdir
from os.path import isfile, join

def getDataFromFile(fName, convert=False):
    '''
    Gets magnetometer data from file.
    
    fName: str
        Name of file
    convert: boolean (default: False)
        Whether to use conversion function from file.
        
    returns (data, sanity data) as astropy TimeSeries
    
    Note: must evaluate values in 'sanity' (e.g., using 'value' attribute) to get boolean
    '''
    h5pyFile = h5py.File(fName,'r')
    saneList = h5pyFile['SanityChannel']
    dataList = h5pyFile['MagneticFields']
    
    # get mag field attributes
    attrs = dataList.attrs
    sampRate = float(attrs['SamplingRate(Hz)'])
    startT = time.mktime(time.strptime(attrs['Date']+' '+attrs['t0'], '%Y/%m/%d %H:%M:%S.%f'))
    # get milliseconds
    decPt = attrs['t0'].rfind('.')
    if(decPt >= 0): # has decimal point
        startT += float('0'+attrs['t0'][decPt:])

    # get sanity attributes
    saneAttrs = saneList.attrs
    saneRate = float(saneAttrs['SamplingRate(Hz)'])
    saneStart = time.mktime(time.strptime(saneAttrs['Date']+' '+saneAttrs['t0'], '%Y/%m/%d %H:%M:%S.%f'))
    # get milliseconds
    decPt = saneAttrs['t0'].rfind('.')
    if(decPt >= 0): # has decimal point
        saneStart += float('0'+saneAttrs['t0'][decPt:])
    
    # create data TimeSeries
    dataTS = TimeSeries(dataList, sample_rate=sampRate, epoch=startT) # put data in TimeSeries
    if(convert):
        convStr = attrs['MagFieldEq'] #string contatining conversion function
        unitLoc = convStr.find('[') # unit info is at end in []
        if(unitLoc >= 0): # unit given
            convStr = convStr[:unitLoc] # get substring before units
        convStr=convStr.replace('MagneticFields','dataTS') # relabel with correct variable
        exec('dataTS = '+convStr) # dynamic execution to convert dataTS
    # create sanity TimeSeries
    saneTS = TimeSeries(saneList, sample_rate=saneRate, epoch=saneStart)
    
    h5pyFile.close()    
    return dataTS, saneTS

def getFListInRange(station, startTime, endTime, path='./', verbose=False):
    '''
    Get list of file names for GNOME experiment within a time period.
    
    Data located in folder of the form 'path/station/yyyy/mm/dd/'.
    Time range uses the start time listed in the 'hdf5' file name.
    
    station: str
        Name of station.
    startTime: float (unix time), str
        Earliest time. String formatted as 'yyyy-mm-dd-HH-MM-SS' (omitted values defaulted as 0)
    endTime: float (unix time), str
        Last time. Format same as startTime
    path: str (default './')
        Location of files
    verbose: bool (default False)
        Verbose output
        
    returns list of file names
    '''
    # put date in consistant format
    # Note that the file names do not contain milliseconds, so "time" tuple is ok
    makeSU = True # Need to calculate start time in unix
    makeEU = True # Need to calculate end time in unix
    if(not type(startTime) is str): # given unix time
        startUnix = startTime
        makeSU = False
        startTime = time.strftime('%Y-%m-%d-%H-%M-%S',time.gmtime(startTime)) 
    if(not type(endTime) is str): # given unix time
        endUnix = endTime
        makeEU = False
        endTime = time.strftime('%Y-%m-%d-%H-%M-%S',time.gmtime(endTime))
    
    # Format start/end times (in array and unix time, if needed)
    startTList = [0.]*9 # date-time tuples (note that last 3 should never be changed)
    endTList   = [0.]*9
    startTime = str.split(startTime,'-')
    endTime = str.split(endTime,'-')
    startTList[:len(startTime)] = [int(t) if len(t)>0 else 0. for t in startTime]
    endTList[:len(endTime)]     = [int(t) if len(t)>0 else 0. for t in endTime]
    if(makeSU):
        startUnix = calendar.timegm(startTList)
    if(makeEU):
        endUnix = calendar.timegm(endTList)
        
    # check for bad input
    if(startUnix > endUnix):
        if(verbose):
            print('getFListInRange() --- Bad input time range (check order).')
        return []
    
    # create array of dates (used for folders)
    dummy = [0.]*9
    dummy[0:3] = startTList[0:3] # start date (beginning of day)
    currTime = calendar.timegm(dummy)
    dates = []
    while(currTime < endUnix):
        dates.append(time.strftime('%Y/%m/%d/',time.gmtime(currTime))) # path segment
        currTime += 86400 # add a day
    
    fList = [] #will hold list of files
    
    for i in range(len(dates)):
        firstDate = i==0 # use these bools to skip checks for middle dates
        lastDate = i==len(dates)-1
        
        dataDir = join(path,station,dates[i]) #directory of files from date
        
        try:
            # get list of files (ignore, e.g., folders)
            foldFiles = [f for f in listdir(dataDir) if isfile(join(dataDir, f))]
            
            # add file to list if it is in time range
            # files like: fribourg01_20170102_122226.hdf5
            for f in foldFiles:
                inRange = not (firstDate or lastDate)
                if(not inRange): # need to check
                    fTime = f.split('_')[2].split('.')[0] # get time 'hhmmss'
                    fTime = fTime[0:2]+':'+fTime[2:4]+':'+fTime[4:6] # time format hh:mm:ss
#                     print dates[i]+fTime, f
                    fTime = calendar.timegm(time.strptime(dates[i]+fTime, '%Y/%m/%d/%H:%M:%S')) # in unix
                    if(fTime >= startUnix and fTime < endUnix):
                        inRange = True
#                     print '\t', inRange
                if(inRange): # add file to list
                    fList.append(join(dataDir, f))
                # in case the file list is not sorted, look through all files.
        except OSError:
            if(verbose):
                print('getFListInRange() --- Data not found for:', dates[i])
    
    return fList

def getDataInRange(station, startTime, endTime, sortTime=True, convert=False, path='./', verbose=False):
    '''
    Get list of data in time range
    
    station: str
        Name of station.
    startTime: float (unix time), str
        Earliest time. String formatted as 'yyyy-mm-dd-HH-MM-SS' 
        (omitted values defaulted as 0)
    endTime: float (unix time), str
        Last time. Format same as startTime
    sortTime: bool (default: True)
        Actively sort output by start time (using data in file)
    convert: boolean (default: False)
        Whether to use conversion function from file.
    path: str (default './')
        Location of files
    verbose: bool (default False)
        Verbose output
    
    returns (data, sanity, fileList). Data and sanity are astropy TimeSeriesList
    
    Note: must evaluate values in 'sanity' (e.g., using 'value' attribute) to get boolean
    Note: use, e.g., dataTSL.join(pad=float('nan'),gap='pad') to combine 
    TimeSeriesList into single Time series.
    '''
    if(verbose):
        print('getDataInRange() --- Finding files')
    fList = getFListInRange(station, startTime, endTime, path=path)
    numFiles = len(fList)
    
    # get data
    if(verbose):
        print('getDataInRange() --- Reading files')
    dataList = [None]*numFiles
    saneList = [None]*numFiles
    for i in range(numFiles):
        dataList[i],saneList[i] = getDataFromFile(fList[i],convert=convert)
    
    # sort if needed
    if(sortTime):
        if(verbose):
            print('getDataInRange() --- Sorting data')
        # do insertion sort (likely that list is sorted)
        sortIndex = range(numFiles) # sorted list of indices
        
        for sRange in range(1, numFiles): # sRange is size of sorted segment
            # note, sortIndex[sRange] = sRange
            insPtTime = dataList[sRange].epoch # for point being inserted
            insHere = sRange # place to insert point
            while(insHere > 0 and dataList[sortIndex[insHere-1]].epoch > insPtTime): 
                insHere -= 1 # decrement until finding place to insert
            # insert point
            dummy1 = sRange # point being moved
            while(insHere <= sRange):
                dummy2 = sortIndex[insHere]
                sortIndex[insHere] = dummy1
                dummy1 = dummy2
                insHere+=1
    else:
        sortIndex = range(numFiles)
    
    # put data in TimeSeriesList
    dataTSL = TimeSeriesList()
    saneTSL = TimeSeriesList()
    for i in sortIndex:
        dataTSL.append(dataList[i])
        saneTSL.append(saneList[i])
    return dataTSL, saneTSL, [fList[i] for i in sortIndex]

def getFileNameTime(fileName):
    '''
    Gives unix time from file name (does not read file). 
    Files of the form */yyyy/mm/dd/*hhmmss.hdf5, no '/' after/in last *
    
    fileName: str
        file name
    
    return unix time of file, according to name
    '''
    fileComp = str.split(fileName,'/')
    fileComp = fileComp[-4:] # last 4 elements
    year = int(fileComp[0])
    month = int(fileComp[1])
    day = int(fileComp[2])
    
    dayTime = fileComp[3][-11:-5] # hhmmss
    hour = int(dayTime[:2])
    minute = int(dayTime[2:4])
    second = int(dayTime[4:])
    
    timeList = [year, month, day, hour, minute, second,0,0,0] # date-time tuples (note that last 3 should never be changed)
    return calendar.timegm(timeList)

def getFListFromDates(station,dates,path='./', verbose=False):
    '''
    Gets list of files from a date (relies on file organization: path/station/yyyy/mm/dd/).
    
    station: str
        Name of station used in file system
    dates: list<str>
        List of date strings (format: year-month-day)
    path: str (default './')
        Data path of folder holding station folders
    verbose: bool (default: False)
        print when file not found 
    
    returns list of file names
    '''
    if(type(dates) is str): # make 'dates' an array is single val given
        dates = [dates]
    fList = [] #will hold list of files
    
    for date in dates:
        dArr = [int(s) for s in date.split('-') if s.isdigit()] #split date into integer array
        dataDir = join(path,station,"{0:04d}/{1:02d}/{2:02d}".format(dArr[0],dArr[1],dArr[2])) #directory of files from date
        
        # append list of files (exclude directories). Use full path
        try:
            fList.extend([join(dataDir, f) for f in listdir(dataDir) if isfile(join(dataDir, f))]) 
        except OSError:
            if(verbose):
                print('Data not found for:', date)
    
    return fList

def getStartTimes(fList):
    '''
    Gets start time (in sec since UNIX epoch) for file list. 
    
    fList: List<str>
        list of file names
    
    retruns list of start times
    '''
    nFiles = len(fList)
    stTimes = [0.]*nFiles
    for i in range(nFiles):
#         if(not i%1000): #print progress
#             print i,'/',nFiles
        
        f = fList[i]
        h5pyFile= h5py.File(f,'r')
        magFieldAttrs = h5pyFile['MagneticFields'].attrs
        timeStr = magFieldAttrs['Date'] + ' ' + magFieldAttrs['t0'] + ' UTC'
        h5pyFile.close()
        
        # get time since epoch (in sec)
        stTimes[i] = calendar.timegm(time.strptime(timeStr, "%Y/%m/%d %H:%M:%S.%f %Z"))
    
    return stTimes

def getSaneList(fList, working=None):
    '''
    Gets list of good data, i.e., those with perfect samity channels
    
    fList: list<str>
        list of file names
    working: list<int>
        indices of working stations. If not specified, all stations are used.
    
    returns list of good files (indices)
    '''
    saneList = []
    if(not working): # no filter specified
        working = range(len(fList))
    
    for i in range(len(fList)):
        fName = fList[i]
        h5pyFile = h5py.File(fName,'r')
        sane = h5pyFile['SanityChannel']
        isGood = True
        
        for check in sane: # go through every second to find bad parts
            if(not check):
                isGood = check
                break; # can break out if one bad is found
        if(isGood):
            saneList.append(i)
        h5pyFile.close()
    
    return saneList
