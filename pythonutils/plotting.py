############################
# @file plotting.py
# @author Douglas Applegate
# @date 10/12/07
#
# Provides convienient wrappers around common plotting tasks
#  using numpy and pylab
############################

__cvs_id__ = "$Id: plotting.py,v 1.1 2008-01-17 19:12:38 dapple Exp $"

############################

import matplotlib.pylab as pylab
import numpy

############################

def doFormating(**formating):
    if 'title' in formating:
        pylab.title(formating['title'])
    if 'xlabel' in formating:
        pylab.xlabel(formating['xlabel'])
    if 'ylabel' in formating:
        pylab.ylabel(formating['ylabel'])

############################

def histogram(a, bins=10, range=None, log = False, normed = False,
              filename = None,
              **formating):

    hist, bins = numpy.histogram(a, bins, range, normed)

    width = bins[1] - bins[0]

    pylab.bar(bins[:-1], hist[:-1], width=width, log=log)
    doFormating(**formating)
    pylab.show()
    if filename is not None:
        pylab.savefig(filename)
        pylab.clf()

#############################

def stackedHistogram(data, bins=10, range=None, log = False, normed = False,
                     filename = None, labels = None,
                     **formating):

    histograms = []
    d1 = data[0]
    curHist, bins = numpy.histogram(d1, bins = bins, range = range, normed = normed)
    histograms.append(curHist)

    for d in data[1:]:
        curHist, bins = numpy.histogram(d, bins = bins, normed = normed)
        histograms.append(curHist)

    width = bins[1] - bins[0]

    colors = 'b r k g c m y w'.split()
    nRepeats = len(data) / len(colors)
    for i in xrange(nRepeats):
        colors = colors.extend(colors)

    for histo, color in zip(histograms, colors):

        pylab.bar(bins[:-1], histo[:-1], width = width, log=log,
                  edgecolor = color, facecolor = None)


        
        
    doFormating(**formating)
    pylab.show()
    if filename is not None:
        pylab.savefig(filename)
        pylab.clf()



#############################

def histogram2d(x, y, bins=10, range=None, normed=False, weights=None,
                log = False,
                filename = None,
                **formating):
    
    hist, x, y = numpy.histogram2d(x, y, bins, range, normed, weights)

    if log is True:
        hist = numpy.log(hist)
    
    X, Y = pylab.meshgrid(x,y)
    pylab.pcolor(X, Y,hist.transpose())
    pylab.colorbar()
    doFormating(**formating)
    pylab.show()
    if filename is not None:
        pylab.savefig(filename)
        pylab.clf()
