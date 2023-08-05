'''
Detrend: this approach is only appropriate for analysing exoplanet data
'''

import numpy
from astropy import units as u
import scipy
from astropy.coordinates import SkyCoord
import glob
import sys
import pylab
import math
import os
import platform
import matplotlib.pyplot as plt
import click

import logging

logger = logging.getLogger(__name__)

def detrend_data(paths, filterCode):
    polyFitRequest=1 # Currently only works with one or two coefficients


    # Load in list of used files
    fileList=[]
    for line in (paths['parent'] / "usedImages.txt").read_text():
        fileList.append(line.strip())

    # Detect Filter Set being used

    fileList = paths['outcatPath'].glob('*diffExcel*csv')
    r=0
    #logger.debug(fileList)
    for file in fileList:
        photFile = numpy.genfromtxt(file, dtype=float, delimiter=',')
        exists=os.path.isfile(str(file).replace('diff','calib'))
        if exists:
            calibFile = numpy.genfromtxt(str(file).replace('diff','calib'), dtype=float, delimiter=',')
            logger.debug("Calibration difference")
            logger.debug(-(photFile[:,1]-calibFile[:,1])[0])
            calibDiff=-((photFile[:,1]-calibFile[:,1])[0])
        #logger.debug(photFile[:,1])
        #logger.debug(photFile[:,0])
        logger.debug(file)
        logger.debug(photFile[:,1])

        baseSubDate=min(photFile[:,0])
        logger.debug(baseSubDate)
        logger.debug(math.floor(baseSubDate))

        photFile[:,0]=photFile[:,0]-baseSubDate


        leftMost = click.prompt("Enter left side most valid date:")
        leftFlat = click.prompt("Enter left side end of flat region:")

        rightFlat = click.prompt("Enter right side start of flat region:")
        rightMost = click.prompt("Enter right side most valid date:")



        # Clip off edges
        clipReject=[]
        for i in range(photFile.shape[0]):
            if photFile[i,0] < float(leftMost) or photFile[i,0] > float(rightMost):
                clipReject.append(i)
                logger.debug(photFile[i,1])
                logger.debug("REJECT")
        logger.debug(photFile.shape[0])
        photFile=numpy.delete(photFile, clipReject, axis=0)
        logger.debug(photFile.shape[0])


        # Get an array holding only the flat bits
        transitReject=[]
        flatFile=numpy.asarray(photFile)
        for i in range(flatFile.shape[0]):
            if (flatFile[i,0] > float(leftMost) and flatFile[i,0] < float(leftFlat)) or (flatFile[i,0] > float(rightFlat) and flatFile[i,0] < float(rightMost)):
                logger.debug("Keep")
            else:
                transitReject.append(i)
                logger.debug(flatFile[i,0])
                logger.debug("REJECT")
        logger.debug(flatFile.shape[0])
        flatFile=numpy.delete(flatFile, transitReject, axis=0)
        logger.debug(flatFile.shape[0])

        #
        polyFit=numpy.polyfit(flatFile[:,0],flatFile[:,1],polyFitRequest)
        logger.debug(polyFit)

        #Remove trend from flat bits
        if polyFitRequest == 2:
            for i in range(flatFile.shape[0]):
                flatFile[i,1]=flatFile[i,1]-(polyFit[2]+(polyFit[1]*flatFile[i,0])+(polyFit[0]*pow(flatFile[i,0],2)))
        elif polyFitRequest ==1:
            for i in range(flatFile.shape[0]):
                flatFile[i,1]=flatFile[i,1]-(polyFit[1]+(polyFit[0]*flatFile[i,0]))


        #Remove trend from actual data
        if polyFitRequest == 2:
            for i in range(photFile.shape[0]):
                photFile[i,1]=photFile[i,1]-(polyFit[2]+(polyFit[1]*photFile[i,0])+(polyFit[0]*pow(photFile[i,0],2)))
        elif polyFitRequest ==1:
            for i in range(photFile.shape[0]):
                photFile[i,1]=photFile[i,1]-(polyFit[1]+(polyFit[0]*photFile[i,0]))


        #return basedate to the data
        photFile[:,0]=photFile[:,0]+baseSubDate


        # ax=plt.plot(photFile[:,0],photFile[:,1],'ro')
        # plt.gca().invert_yaxis()
        # #logger.debug(ax.lines)
        # plt.show()
        # del ax
        # plt.clf()
        # plt.cla()
        # plt.close()
        # plt.close("all")

        # Output trimmed files
        numpy.savetxt(paths['outcatPath'] / 'V{}_diffPeranso.txt'.format(str(r+1)), photFile, delimiter=" ", fmt='%0.8f')
        numpy.savetxt(paths['outcatPath'] / 'V{}_diffExcel.csv'.format(str(r+1)), photFile, delimiter=",", fmt='%0.8f')

        # Output astroImageJ file
        outputPeransoCalib=[]
        #i=0
        for i in range(numpy.asarray(photFile).shape[0]):
            outputPeransoCalib.append([photFile[i][0]-2450000.0,photFile[i][1],photFile[i][2]])
            #i=i+1

        numpy.savetxt(paths['outcatPath'] / 'V{}_diffAIJ.txt'.format(str(r+1)), outputPeransoCalib, delimiter=" ", fmt='%0.8f')
        numpy.savetxt(paths['outcatPath'] / 'V{}_diffAIJ.csv'.format(str(r+1)), outputPeransoCalib, delimiter=",", fmt='%0.8f')

        # Output replot
        pylab.cla()
        outplotx=photFile[:,0]
        outploty=photFile[:,1]
        pylab.xlabel('BJD')
        pylab.ylabel('Differential ' +filterCode+' Mag')
        pylab.plot(outplotx,outploty,'bo')
        pylab.ylim(max(outploty)+0.02,min(outploty)-0.02,'k-')
        pylab.xlim(min(outplotx)-0.01,max(outplotx)+0.01)
        pylab.grid(True)
        pylab.savefig(paths['outputPath'] / 'V{}_EnsembleVarDiffMag.png'.format(str(r+1)))
        pylab.savefig(paths['outputPath'] / 'V{}_EnsembleVarDiffMag.eps'.format(str(r+1)))
        pylab.cla()
        pylab.clf()
        pylab.close()
        pylab.close("all")


        if exists:
            measureReject=[]
            for i in range(calibFile.shape[0]):
                if calibFile[i,1] < float(brightD)+calibDiff or calibFile[i,1] > float(brightV)+calibDiff :
                    measureReject.append(i)
                    logger.debug(calibFile[i,1])
                    logger.debug("REJECT")
            logger.debug(calibFile.shape[0])
            calibFile=numpy.delete(calibFile, measureReject, axis=0)
            logger.debug(calibFile.shape[0])

            # Output trimmed files
            numpy.savetxt(paths['outcatPath'] / 'V{}_calibPeranso.txt'.format(str(r+1)), calibFile, delimiter=" ", fmt='%0.8f')
            numpy.savetxt(paths['outcatPath'] / 'V{}_calibExcel.csv'.format(str(r+1)), calibFile, delimiter=",", fmt='%0.8f')

            # Output astroImageJ file
            outputPeransoCalib=[]
            #i=0
            for i in range(numpy.asarray(calibFile).shape[0]):
                outputPeransoCalib.append([calibFile[i][0]-2450000.0,calibFile[i][1],calibFile[i][2]])
                #i=i+1

            numpy.savetxt(paths['outcatPath'] / 'V{}_calibAIJ.txt'.format(str(r+1)), outputPeransoCalib, delimiter=" ", fmt='%0.8f')
            numpy.savetxt(paths['outcatPath'] / 'V{}_calibAIJ.csv'.format(str(r+1)), outputPeransoCalib, delimiter=",", fmt='%0.8f')
            #r=r+1

        r=r+1
    return
