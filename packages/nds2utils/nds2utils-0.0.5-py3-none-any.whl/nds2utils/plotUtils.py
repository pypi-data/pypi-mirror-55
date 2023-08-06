import os, sys, time
import numpy as np
import matplotlib as mpl
mpl.rcParams.update({'text.usetex': False,
                     'figure.figsize': (12, 9),
                     'font.family': 'serif',
                     'lines.linewidth': 2.5,
                     'font.size': 16,
                     'xtick.labelsize': 'large',
                     'ytick.labelsize': 'large',
                     'legend.fancybox': True,
                     'legend.fontsize': 12,
                     'legend.framealpha': 0.7,
                     'legend.handletextpad': 0.5,
                     'legend.labelspacing': 0.2,
                     'legend.loc': 'best',
                     'savefig.dpi': 80,
                     'pdf.compression': 9})
mpl.use('TKAgg')
import matplotlib.pyplot as plt

from .dataUtils import linear_log_ASD

# Convenience
def quick_ASD_grab(dataDict, chan, calibrated=True):
    '''
    Inputs:
    dataDict = data dictionary structure containing chanA PSD
    chan     = str. channel name we want to grab ASD from
    Output:
    ff = frequency vector in Hz
    ASD = amplitude spectral density of chan   = sqrt( <|chan|^2> )
    Returned as tuple = (ff, ASD)
    '''
    ff = dataDict[chan]['ff']
    ASD = dataDict[chan]['ASD']

    if calibrated:
        if 'calASD' in dataDict[chanB][chanA].keys():
            TF = dataDict[chanB][chanA]['calASD']

    return ff, ASD

def quick_PSD_grab(dataDict, chan, calibrated=True):
    '''
    Inputs:
    dataDict = data dictionary structure containing chanA PSD
    chan     = str. channel name we want to grab ASD from
    Output:
    ff = frequency vector in Hz
    PSD = power spectral density of chan   = <|chan|^2>
    Returned as tuple = (ff, PSD)
    '''
    ff = dataDict[chan]['ff']
    PSD = dataDict[chan]['PSD']

    if calibrated:
        if 'calPSD' in dataDict[chanB][chanA].keys():
            TF = dataDict[chanB][chanA]['calPSD']

    return ff, PSD

def quick_CSD_grab(dataDict, chanA, chanB, calibrated=True):
    '''
    Inputs:
    dataDict = data dictionary structure containing chanB * chanA CSD
    chanA    = str. channel name we want for channel A, the non-conjugated channel
    chanB    = str. channel name we want for channel B, the conjugated channel
    Output:
    ff = frequency vector in Hz
    CSD = cross spectral density of chanA and chanB = <chanB^*|chanA>
    Returned as tuple = (ff, CSD)
    '''
    ff = dataDict[chanB][chanA]['ff']
    CSD = dataDict[chanB][chanA]['CSD']

    if calibrated:
        if 'calCSD' in dataDict[chanB][chanA].keys():
            TF = dataDict[chanB][chanA]['calCSD']

    return ff, CSD

def quick_TF_grab(dataDict, chanA, chanB, calibrated=True):
    '''
    Inputs:
    dataDict   = data dictionary structure containing chanB / chanA TF
    chanA      = str. channel name we want for channel A, the input channel
    chanB      = str. channel name we want for channel B, the output channel
    calibrated = bool. returns a calibrated TF if possible. Default is true.
    Output:
    ff = frequency vector in Hz
    TF = transfer function from chanA to chanB = B/A
    coh = power coherence of A and B = |CSD|^2/(PSD_A * PSD_B)
    Returned as tuple = (ff, TF, coh)
    '''
    ff = dataDict[chanB][chanA]['ff']
    TF = dataDict[chanB][chanA]['TF']
    coh = dataDict[chanB][chanA]['coh']

    if calibrated:
        if 'calTF' in dataDict[chanB][chanA].keys():
            TF = dataDict[chanB][chanA]['TF']

    return ff, TF, coh

# Quick plotting
def bode(ff,
         TF,
         label='TF',
         title='Transfer Function',
         units='cts/cts',
         xlims=None,
         ylims=None,
         logbin=False,
         num_points=1000,
         fig=None ):
    '''
    Plots a very simple bode plot.
    Run plt.ion() before for convenience.

    Inputs:
    ff     = frequency vector in Hz.
    TF     = array of complex numbers.  Represents the tranfer function for the bode plot.
    label  = str.  Legend label for the TF.  Default is 'TF'.
    title  = str.  Title of the figure.
    units  = str. Units for the y-axis.  Default is cts/cts.
    xlims  = array containing two floats.  x-axis limits on the plot.  Default is None.
    ylims  = array containing two floats.  y-axis limits on the plot.  Default is None.
    logbin      = bool.  If True, logbins the ASDs.  Default is False.
    num_points  = int.  If logbin == True, logbins using this number of points.  Default is 1000.
    fig    = matplotlib figure object upon which to make the plot.

    Output:
    fig = matplotlib figure object.
    '''
    newFig = False
    if xlims == None:
        xlims = [ff[1], ff[-1]]
    if fig == None:
        newFig = True
        fig = plt.figure(figsize=(16,12))
        s1 = fig.add_subplot(211)
        s2 = fig.add_subplot(212)
    else:
        s1 = fig.get_axes()[0]
        s2 = fig.get_axes()[1]

    if logbin:
        logf_low = ff[1]
        logf_high = ff[-1]
        fflog = np.logspace(np.log10(logf_low), np.log10(logf_high), num_points)
        _, plotTFreal = linear_log_ASD(fflog, ff, np.real(TF))
        _, plotTFimag = linear_log_ASD(fflog, ff, np.imag(TF))
        plotTF = plotTFreal + 1j* plotTFimag
        #plotff, plotcoh = linear_log_ASD(fflog, ff, coh)
    else:
        plotff = ff
        plotTF = TF
        #plotcoh = coh

    s1.loglog(plotff, np.abs(plotTF), label=label)
    s2.semilogx(plotff, 180/np.pi*np.angle(plotTF))

    if newFig == True:
        s1.set_title(title)
        s2.set_yticks([-180, -90, 0, 90, 180])

        s1.set_xlim(xlims)
        s2.set_xlim(xlims)
        if ylims is not None:
            s1.set_ylim(ylims)

        s1.set_ylabel('Magnitude [%s]'%units)
        s2.set_ylabel('Phase [degrees]')
        s2.set_xlabel('Frequency [Hz]')

        s1.grid(which='major', ls='-')
        s2.grid(which='major', ls='-')
        s1.grid(which='minor', ls='--')
        s2.grid(which='minor', ls='--')

    s1.legend()
    plt.tight_layout()
    plt.show()
    return fig

def bode_coh(ff,
             TF,
             coh,
             label='TF',
             title='Transfer Function',
             units='cts/cts',
             xlims=None,
             ylims=None,
             logbin=False,
             num_points=1000,
             fig=None ):
    '''
    Plots a very simple bode plot, with coherence.
    Run plt.ion() before for convenience.

    Inputs:
    ff     = frequency vector in Hz.
    TF     = array of complex numbers.  Represents the tranfer function for the bode plot.
    coh    = array of real numbers.  Represents the power coherence between the two channels.
    label  = str.  Legend label for the TF.  Default is 'TF'.
    title  = str.  Title of the figure.
    units  = str. Units for the y-axis.  Default is cts/cts.
    xlims  = array containing two floats.  x-axis limits on the plot.  Default is None.
    ylims  = array containing two floats.  y-axis limits on the plot.  Default is None.
    logbin      = bool.  If True, logbins the ASDs.  Default is False.
    num_points  = int.  If logbin == True, logbins using this number of points.  Default is 1000.
    fig    = matplotlib figure object upon which to make the plot.

    Output:
    fig = matplotlib figure object.
    '''
    newFig = False
    if xlims == None:
        xlims = [ff[1], ff[-1]]
    if fig == None:
        newFig = True
        fig = plt.figure(figsize=(16,12))
        s1 = fig.add_subplot(311)
        s2 = fig.add_subplot(312)
        s3 = fig.add_subplot(313)
    else:
        s1 = fig.get_axes()[0]
        s2 = fig.get_axes()[1]
        s3 = fig.get_axes()[2]

    if logbin:
        logf_low = ff[1]
        logf_high = ff[-1]
        fflog = np.logspace(np.log10(logf_low), np.log10(logf_high), num_points)
        _, plotTFreal = linear_log_ASD(fflog, ff, np.real(TF))
        _, plotTFimag = linear_log_ASD(fflog, ff, np.imag(TF))
        plotTF = plotTFreal + 1j* plotTFimag
        plotff, plotcoh = linear_log_ASD(fflog, ff, coh)
    else:
        plotff = ff
        plotTF = TF
        plotcoh = coh

    s1.loglog(plotff, np.abs(plotTF), label=label)
    s2.semilogx(plotff, 180/np.pi*np.angle(plotTF))
    s3.semilogx(plotff, plotcoh)

    if newFig == True:
        s1.set_title(title)
        s2.set_yticks([-180, -90, 0, 90, 180])

        s1.set_xlim(xlims)
        s2.set_xlim(xlims)
        s3.set_xlim(xlims)
        if ylims is not None:
            s1.set_ylim(ylims)

        s1.set_ylabel('Magnitude [%s]'%units)
        s2.set_ylabel('Phase [degrees]')
        s2.set_ylabel('Power Coherence')
        s2.set_xlabel('Frequency [Hz]')

        s1.grid(which='major', ls='-')
        s2.grid(which='major', ls='-')
        s3.grid(which='major', ls='-')
        s1.grid(which='minor', ls='--')
        s2.grid(which='minor', ls='--')
        s3.grid(which='minor', ls='--')

    s1.legend()
    plt.tight_layout()
    plt.show()
    return fig

def bodes(ffs,
          TFs,
          labels=None,
          title='Transfer Function',
          units='cts/cts',
          xlims=None,
          ylims=None,
          logbin=False,
          num_points=1000,
          fig=None ):
    '''
    Plots a very simple bode plot for multiple TFs.
    Run plt.ion() before for convenience.

    Inputs:
    ffs    = vertically stacked frequency vectors in Hz.
             Use ffs = np.vstack((ff_1, ff_2, ..., ff_N)).
    TFs    = vertically stacked arrays of complex numbers.
             Represents the tranfer functions for the bode plot.
             Use TFs = np.vstack((TF_1, TF_2, ..., TF_N)).
    labels = str.  Legend labels for the TFs.  Default is None.
    title  = str.  Title of the figure.
    units  = str. Units for the magnitude y-axis.  Default is cts.
    xlims  = array containing two floats.  x-axis limits on the plot.  Default is None.
    ylims  = array containing two floats.  y-axis limits on the plot.  Default is None.
    logbin      = bool.  If True, logbins the ASDs.  Default is False.
    num_points  = int.  If logbin == True, logbins using this number of points.  Default is 1000.
    fig    = matplotlib figure object upon which to make the plot.

    Output:
    fig = matplotlib figure object.
    '''
    newFig = False
    if xlims == None:
        xlims = [ffs[0][1], ffs[0][-1]]
    if fig == None:
        newFig = True
        fig = plt.figure(figsize=(16,12))
        s1 = fig.add_subplot(211)
        s2 = fig.add_subplot(212)
    else:
        s1 = fig.get_axes()[0]
        s2 = fig.get_axes()[1]

    for ii, ff, TF in zip(np.arange(len(ffs)), ffs, TFs):
        if labels is not None:
            label = labels[ii]
        else:
            label = 'TF {}'.format(ii)

        if logbin:
            logf_low = ff[1]
            logf_high = ff[-1]
            fflog = np.logspace(np.log10(logf_low), np.log10(logf_high), num_points)
            _, plotTFreal = linear_log_ASD(fflog, ff, np.real(TF))
            _, plotTFimag = linear_log_ASD(fflog, ff, np.imag(TF))
            plotTF = plotTFreal + 1j* plotTFimag
            #plotff, plotcoh = linear_log_ASD(fflog, ff, coh)
        else:
            plotff = ff
            plotTF = TF
            #plotcoh = coh

        s1.loglog(plotff, np.abs(plotTF), label=label)
        s2.semilogx(plotff, 180/np.pi*np.angle(plotTF))

    if newFig == True:
        s1.set_title(title)
        s2.set_yticks([-180, -90, 0, 90, 180])

        s1.set_xlim(xlims)
        s2.set_xlim(xlims)
        if ylims is not None:
            s1.set_ylim(ylims)

        s1.set_ylabel('Magnitude [%s]'%units)
        s2.set_ylabel('Phase [degrees]')
        s3.set_ylabel('Coherent Power')
        s3.set_xlabel('Frequency [Hz]')

        s1.grid(which='major', ls='-')
        s2.grid(which='major', ls='-')
        s3.grid(which='major', ls='-')
        s1.grid(which='minor', ls='--')
        s2.grid(which='minor', ls='--')
        s3.grid(which='minor', ls='--')

    s1.legend()
    plt.tight_layout()
    plt.show()
    return fig

def bodes_coh(ffs,
              TFs,
              cohs,
              labels=None,
              title='Transfer Function',
              units='cts/cts',
              xlims=None,
              ylims=None,
              logbin=False,
              num_points=1000,
              fig=None ):
    '''
    Plots a very simple bode plot for multiple TFs.
    Run plt.ion() before for convenience.

    Inputs:
    ffs    = vertically stacked frequency vectors in Hz.
             Use ffs = np.vstack((ff_1, ff_2, ..., ff_N)).
    TFs    = vertically stacked arrays of complex numbers.
             Represents the tranfer functions for the bode plot.
             Use TFs = np.vstack((TF_1, TF_2, ..., TF_N)).
    cohs   = vertically stacked power coherence vectors.
             Use cohs = np.vstack((coh_1, coh_2, ..., coh_N)).
    labels = str.  Legend labels for the TFs.  Default is None.
    title  = str.  Title of the figure.
    units  = str. Units for the magnitude y-axis.  Default is cts.
    xlims  = array containing two floats.  x-axis limits on the plot.  Default is None.
    ylims  = array containing two floats.  y-axis limits on the plot.  Default is None.
    logbin      = bool.  If True, logbins the ASDs.  Default is False.
    num_points  = int.  If logbin == True, logbins using this number of points.  Default is 1000.
    fig    = matplotlib figure object upon which to make the plot.

    Output:
    fig = matplotlib figure object.
    '''
    newFig = False
    if xlims == None:
        xlims = [ffs[0][1], ffs[0][-1]]
    if fig == None:
        newFig = True
        fig = plt.figure(figsize=(16,12))
        s1 = fig.add_subplot(311)
        s2 = fig.add_subplot(312)
        s3 = fig.add_subplot(313)
    else:
        s1 = fig.get_axes()[0]
        s2 = fig.get_axes()[1]
        s3 = fig.get_axes()[2]

    for ii, ff, TF, coh in zip(np.arange(len(ffs)), ffs, TFs, cohs):
        if labels is not None:
            label = labels[ii]
        else:
            label = '{}'.format(ii)

        if logbin:
            logf_low = ff[1]
            logf_high = ff[-1]
            fflog = np.logspace(np.log10(logf_low), np.log10(logf_high), num_points)
            _, plotTFreal = linear_log_ASD(fflog, ff, np.real(TF))
            _, plotTFimag = linear_log_ASD(fflog, ff, np.imag(TF))
            plotTF = plotTFreal + 1j* plotTFimag
            plotff, plotcoh = linear_log_ASD(fflog, ff, coh)
        else:
            plotff = ff
            plotTF = TF
            plotcoh = coh

        s1.loglog(plotff, np.abs(plotTF), label=label)
        s2.semilogx(plotff, 180/np.pi*np.angle(plotTF))
        s3.semilogx(plotff, plotcoh)

    if newFig == True:
        s1.set_title(title)
        s2.set_yticks([-180, -90, 0, 90, 180])

        s1.set_xlim(xlims)
        s2.set_xlim(xlims)
        s3.set_xlim(xlims)
        if ylims is not None:
            s1.set_ylim(ylims)

        s1.set_ylabel('Magnitude [%s]'%units)
        s2.set_ylabel('Phase [degrees]')
        s3.set_ylabel('Coherent Power')
        s3.set_xlabel('Frequency [Hz]')

        s1.grid(which='major', ls='-')
        s2.grid(which='major', ls='-')
        s3.grid(which='major', ls='-')
        s1.grid(which='minor', ls='--')
        s2.grid(which='minor', ls='--')
        s3.grid(which='minor', ls='--')

    s1.legend()
    plt.tight_layout()
    plt.show()
    return fig

def plot_ASDs(dataDict,
              plot_chans=None,
              label_tag=None,
              title='Spectra',
              units='cts',
              xlims=None,
              ylims=None,
              cal_applied=True,
              logbin=False,
              num_points=1000,
              fig=None):
    '''
    Plots the ASDs in a dataDict from getPSDs() output.
    Automatically plots calibrated ASDs if available.
    Use plt.ion() for convenience.

    Inputs:
    dataDict    = data dictionary structure containing ASDs
    plot_chans  = array of channel names corresponding to the channels you want plotted.
                  If None, all channels are plotted.  Default is None.
    label_tag   = str.  Tag on the end of the legend label for each plotted channel name.  Default is None.
    title       = str.  Title of the figure.
    units       = str. Units for the y-axis numerator (denominator is always rtHz).  Default is cts.
    xlims       = array containing two floats.  x-axis limits on the plot.  Default is None.
    ylims       = array containing two floats.  y-axis limits on the plot.  Default is None.
    cal_applied = bool.  If True, plots calibrated ASDs where possible.  Default is True.
    logbin      = bool.  If True, logbins the ASDs.  Default is False.
    num_points  = int.  If logbin == True, logbins using this number of points.  Default is 1000.
    fig         = matplotlib figure object upon which to make the plot.

    Output:
    fig = matplotlib figure object
    '''

    if plot_chans == None:
        plot_chans = np.array(list(dataDict.keys()))

    newFig = False
    if fig is None:
        newFig = True
        fig = plt.figure(figsize=(16,12))
    else:
        axes = fig.gca()
        lines = axes.lines

    channels = dataDict.keys()
    for ii, chan in enumerate(channels):
        if chan not in plot_chans:
            continue

        alpha = 1.0
        ls = '-'
        if ii >= 30:
            alpha = 0.5
            ls = '--'
        elif ii >= 20:
            alpha = 1
            ls = '--'
        elif ii >= 10:
            alpha = 0.5
        #print chan
        ff = dataDict[chan]['ff']
        ASD = dataDict[chan]['ASD']

        if xlims == None:
            xlims = [ff[1], ff[-1]]

        if label_tag == None:
            label = chan.replace('_', ' ')
        else:
            label = '{} {}'.format(chan.replace('_', ' '), label_tag)

        if 'calFunc' in dataDict[chan].keys() and cal_applied==True:
            label = 'Calibrated {}'.format(label)
            calFunc = dataDict[chan]['calFunc']
            plotASD = ASD * np.abs(calFunc(ff))
        else:
            plotASD = ASD

        if logbin:
            logf_low = ff[1]
            logf_high = ff[-1]
            fflog = np.logspace(np.log10(logf_low), np.log10(logf_high), num_points)
            plotff, plotASD = linear_log_ASD(fflog, ff, plotASD)
        else:
            plotff = ff

        plt.loglog(plotff, plotASD, alpha=alpha, ls=ls, label=label)

    if xlims is not None:
        plt.xlim(xlims)
    if ylims is not None:
        plt.ylim(ylims)

    if newFig:
        plt.grid(which='major', ls='-')
        plt.grid(which='minor', ls='--')
        plt.title('{} - {}'.format(title, time.strftime('%b %d, %Y')))
        plt.xlabel('Frequency [Hz]')
        plt.ylabel('ASD [$\mathrm{%s}/\sqrt{\mathrm{Hz}}$]'%units)

    plt.legend()

    plt.tight_layout()
    plt.show()
    return fig

def compare_ASDs(dataDict1,
                 dataDict2,
                 plot_chans=None,
                 label_tag1=None,
                 label_tag2=None,
                 title='Spectra',
                 units='cts',
                 xlims=None,
                 ylims=None,
                 cal_applied=True,
                 logbin=False,
                 num_points=1000,
                 fig=None):
    '''
    Plots the ASDs in dataDict1 and dataDict2 for quick comparison at two different times.
    Automatically plots calibrated ASDs if available.
    Use plt.ion() for convenience.

    Inputs:
    dataDict    = data dictionary structure containing ASDs
    plot_chans  = array of channel names corresponding to the channels you want plotted.
                  If None, all channels are plotted.  Default is None.
    label_tag1  = str.  Tag on the end of the legend label for channels in dataDict1.  Default is None.
    label_tag2  = str.  Tag on the end of the legend label for channels in dataDict2.  Default is None.
    title       = str.  Title of the figure.
    units       = str. Units for the y-axis numerator (denominator is always rtHz).  Default is cts.
    xlims       = array containing two floats.  x-axis limits on the plot.  Default is None.
    ylims       = array containing two floats.  y-axis limits on the plot.  Default is None.
    cal_applied = bool.  If True, plots calibrated ASDs where possible.  Default is True.
    logbin      = bool.  If True, logbins the ASDs.  Default is False.
    num_points  = int.  If logbin == True, logbins using this number of points.  Default is 1000.
    fig         = matplotlib figure object upon which to make the plot.

    Output:
    fig = matplotlib figure object
    '''

    if plot_chans == None:
        plot_chans = np.array(list(dataDict1.keys()))

    newFig = False
    if fig is None:
        newFig = True
        fig = plt.figure(figsize=(16,12))
    else:
        axes = fig.gca()
        lines = axes.lines

    channels = dataDict1.keys()
    for ii, chan in enumerate(channels):
        if chan not in plot_chans:
            continue
        #print chan
        ff1  = dataDict1[chan]['ff']
        ASD1 = dataDict1[chan]['ASD']
        ff2  = dataDict2[chan]['ff']
        ASD2 = dataDict2[chan]['ASD']

        if xlims == None:
            xlims = [ff1[1], ff1[-1]]

        if label_tag1 == None:
            label1 = chan.replace('_', ' ')
        else:
            label1 = '{} {}'.format(chan.replace('_', ' '), label_tag1)
        if label_tag2 == None:
            label2 = chan.replace('_', ' ')
        else:
            label2 = '{} {}'.format(chan.replace('_', ' '), label_tag2)

        if 'calFunc' in dataDict1[chan].keys() and cal_applied==True:
            label1 = 'Calibrated {}'.format(label1)
            calFunc = dataDict1[chan]['calFunc']
            plotASD1 = ASD1 * np.abs(calFunc(ff1))
        else:
            plotASD1 = ASD1

        if 'calFunc' in dataDict2[chan].keys() and cal_applied==True:
            label2 = 'Calibrated {}'.format(label2)
            calFunc = dataDict2[chan]['calFunc']
            plotASD2 = ASD2 * np.abs(calFunc(ff2))
        else:
            plotASD2 = ASD2

        if logbin:
            logf_low = ff1[1]
            logf_high = ff1[-1]
            fflog = np.logspace(np.log10(logf_low), np.log10(logf_high), num_points)
            plotff1, plotASD1 = linear_log_ASD(fflog, ff1, plotASD1)
            plotff2, plotASD2 = linear_log_ASD(fflog, ff2, plotASD2)
        else:
            plotff1 = ff1
            plotff2 = ff2

        l1, = plt.loglog(plotff1, plotASD1, alpha=0.5, label=label1)
        l2, = plt.loglog(plotff2, plotASD2, color=l1.get_color(), label=label2)

    if xlims is not None:
        plt.xlim(xlims)
    if ylims is not None:
        plt.ylim(ylims)

    if newFig:
        plt.grid()
        plt.grid(which='minor', ls='--')
        plt.title('{} - {}'.format(title, time.strftime('%b %d, %Y')))
        plt.xlabel('Frequency [Hz]')
        plt.ylabel('ASD [$\mathrm{%s}/\sqrt{\mathrm{Hz}}$]'%units)

    plt.legend()

    plt.tight_layout()
    plt.show()
    return fig

def plot_TF(dataDict,
            chanA,
            chanB,
            label=None,
            title='Spectra',
            units='cts/cts',
            xlims=None,
            ylims=None,
            cal_applied=True,
            logbin=False,
            num_points=1000,
            fig=None):
    '''
    Plots all the TFs in a data dictionary, always using chanA as the A channel for the TF.
    Will plot TF 1 = chanB1/chanA, TF 2 = chanB2/chanA, etc.
    Automatically plots calibrated TFs if available.
    Use plt.ion() for convenience.

    Inputs:
    dataDict    = data dictionary structure containing TFs
    chanA       = str. channel to be used as the A channel.  Must be a key in the above data dictionary.
    chanB       = str. channel to be used as the B channel.  Must be a key in the above data dictionary.
    plot_chans  = array of channel names corresponding to the channels you want plotted.
                  If None, all channels are plotted.  Default is None.
    label_tag   = str.  Tag on the end of the legend label for each plotted channel name.  Default is None.
    title       = str.  Title of the figure.
    units       = str. Units for the y-axis numerator (denominator is always rtHz).  Default is cts.
    xlims       = array containing two floats.  x-axis limits on the plot.  Default is None.
    ylims       = array containing two floats.  y-axis limits on the plot.  Default is None.
    cal_applied = bool.  If True, plots calibrated ASDs where possible.  Default is True.
    logbin      = bool.  If True, logbins the ASDs.  Default is False.
    num_points  = int.  If logbin == True, logbins using this number of points.  Default is 1000.
    fig         = matplotlib figure object upon which to make the plot.

    Output:
    fig = matplotlib figure object
    '''
    ff, TF, coh = quick_TF_grab(dataDict, chanA, chanB, calibrated=cal_applied)
    fig = bode_coh( ff,
                    TF,
                    coh,
                    label=label,
                    title=title,
                    units=units,
                    xlims=xlims,
                    ylims=ylims,
                    logbin=logbin,
                    num_points=num_points,
                    fig=fig )
    return fig


def plot_TFs_A(dataDict,
               chanA,
               plot_chans=None,
               label_tag=None,
               title='Spectra',
               units='cts/cts',
               xlims=None,
               ylims=None,
               cal_applied=True,
               logbin=False,
               num_points=1000,
               fig=None):
    '''
    Plots all the TFs in a data dictionary, always using chanA as the A channel for the TF.
    Will plot TF 1 = chanB1/chanA, TF 2 = chanB2/chanA, etc.
    Automatically plots calibrated TFs if available.
    Use plt.ion() for convenience.

    Inputs:
    dataDict    = data dictionary structure containing TFs
    chanA       = str. channel to be always be used as the A channel.  Must be a key in the above data dictionary.
    plot_chans  = array of channel names corresponding to the channels you want plotted.
                  If None, all channels are plotted.  Default is None.
    label_tag   = str.  Tag on the end of the legend label for each plotted channel name.  Default is None.
    title       = str.  Title of the figure.
    units       = str. Units for the y-axis numerator (denominator is always rtHz).  Default is cts.
    xlims       = array containing two floats.  x-axis limits on the plot.  Default is None.
    ylims       = array containing two floats.  y-axis limits on the plot.  Default is None.
    cal_applied = bool.  If True, plots calibrated ASDs where possible.  Default is True.
    logbin      = bool.  If True, logbins the ASDs.  Default is False.
    num_points  = int.  If logbin == True, logbins using this number of points.  Default is 1000.
    fig         = matplotlib figure object upon which to make the plot.

    Output:
    fig = matplotlib figure object
    '''

    if plot_chans == None:
        plot_chans = np.array(list(dataDict.keys()))

    newFig = False
    if fig is None:
        newFig = True
        fig, (s1, s2, s3) = plt.subplots(3)
    else:
        s1, s2, s3 = fig.get_axes()

    channels = dataDict.keys()
    for ii, chanB in enumerate(channels):
        if chanA == chanB:
            continue
        if chanB not in plot_chans:
            continue

        ff, TF, coh = quick_TF_grab(dataDict, chanA, chanB, calibrated=cal_applied)

        label = '{B}/{A} TF'.format(B=chanB, A=chanA)
        if cal_applied and 'calTF' in dataDict[chanB][chanA].keys():
            label = '{} Calibrated'.format(label)
        if logbin:
            label = '{} Logbinned'.format(label)
        if not label_tag == None:
            label = '{} {}'.format(label, label_tag)

        if logbin:
            logf_low = ff[1]
            logf_high = ff[-1]
            fflog = np.logspace(np.log10(logf_low), np.log10(logf_high), num_points)
            _, plotTFreal = linear_log_ASD(fflog, ff, np.real(TF))
            _, plotTFimag = linear_log_ASD(fflog, ff, np.imag(TF))
            plotTF = plotTFreal + 1j* plotTFimag
            plotff, plotcoh = linear_log_ASD(fflog, ff, coh)
        else:
            plotff = ff
            plotTF = TF
            plotcoh = coh

        s1.loglog(plotff, np.abs(plotTF), label=label)
        s2.semilogx(plotff, 180/np.pi*np.angle(plotTF))
        s3.semilogx(plotff, plotcoh)

    if newFig == True:
        s1.set_title(title)
        s2.set_yticks([-180, -90, 0, 90, 180])

        s1.set_xlim(xlims)
        s2.set_xlim(xlims)
        s3.set_xlim(xlims)
        if ylims is not None:
            s1.set_ylim(ylims)

        s1.set_ylabel('Magnitude [%s]'%units)
        s2.set_ylabel('Phase [degrees]')
        s3.set_ylabel('Coherent Power')
        s3.set_xlabel('Frequency [Hz]')

        s1.grid(which='major', ls='-')
        s2.grid(which='major', ls='-')
        s3.grid(which='major', ls='-')
        s1.grid(which='minor', ls='--')
        s2.grid(which='minor', ls='--')
        s3.grid(which='minor', ls='--')

    s1.legend(fontsize=12)
    plt.tight_layout()
    plt.show()
    return fig

def plot_TFs_B(dataDict,
               chanB,
               plot_chans=None,
               label_tag=None,
               title='Spectra',
               units='cts',
               xlims=None,
               ylims=None,
               cal_applied=True,
               logbin=False,
               num_points=1000,
               fig=None):
    '''
    Plots all the TFs in a data dictionary, always using chanB as the B channel for the TF.
    Will plot TF 1 = chanB/chanA1, TF 2 = chanB/chanA2, etc.
    Automatically plots calibrated TFs if available.
    Use plt.ion() for convenience.

    Inputs:
    dataDict    = data dictionary structure containing TFs
    chanB       = str. channel to be always be used as the B channel.  Must be a key in the above data dictionary.
    plot_chans  = array of channel names corresponding to the channels you want plotted.
                  If None, all channels are plotted.  Default is None.
    label_tag   = str.  Tag on the end of the legend label for each plotted channel name.  Default is None.
    title       = str.  Title of the figure.
    units       = str. Units for the y-axis numerator (denominator is always rtHz).  Default is cts.
    xlims       = array containing two floats.  x-axis limits on the plot.  Default is None.
    ylims       = array containing two floats.  y-axis limits on the plot.  Default is None.
    cal_applied = bool.  If True, plots calibrated ASDs where possible.  Default is True.
    logbin      = bool.  If True, logbins the ASDs.  Default is False.
    num_points  = int.  If logbin == True, logbins using this number of points.  Default is 1000.
    fig         = matplotlib figure object upon which to make the plot.

    Output:
    fig = matplotlib figure object
    '''

    if plot_chans == None:
        plot_chans = np.array(list(dataDict.keys()))

    newFig = False
    if fig is None:
        newFig = True
        fig, (s1, s2, s3) = plt.subplots(3)
    else:
        s1, s2, s3 = fig.get_axes()

    channels = dataDict.keys()
    for ii, chanA in enumerate(channels):
        if chanA == chanB:
            continue
        if chanA not in plot_chans:
            continue

        ff, TF, coh = quick_TF_grab(dataDict, chanA, chanB, calibrated=cal_applied)

        label = '{B}/{A} TF'.format(B=chanB, A=chanA)
        if cal_applied and 'calTF' in dataDict[chanB][chanA].keys():
            label = '{} Calibrated'.format(label)
        if logbin:
            label = '{} Logbinned'.format(label)
        if not label_tag == None:
            label = '{} {}'.format(label, label_tag)

        if logbin:
            logf_low = ff[1]
            logf_high = ff[-1]
            fflog = np.logspace(np.log10(logf_low), np.log10(logf_high), num_points)
            _, plotTFreal = linear_log_ASD(fflog, ff, np.real(TF))
            _, plotTFimag = linear_log_ASD(fflog, ff, np.imag(TF))
            plotTF = plotTFreal + 1j* plotTFimag
            plotff, plotcoh = linear_log_ASD(fflog, ff, coh)
        else:
            plotff = ff
            plotTF = TF
            plotcoh = coh

        s1.loglog(plotff, np.abs(plotTF), label=label)
        s2.semilogx(plotff, 180/np.pi*np.angle(plotTF))
        s3.semilogx(plotff, plotcoh)

    if newFig == True:
        s1.set_title(title)
        s2.set_yticks([-180, -90, 0, 90, 180])

        s1.set_xlim(xlims)
        s2.set_xlim(xlims)
        s3.set_xlim(xlims)
        if ylims is not None:
            s1.set_ylim(ylims)

        s1.set_ylabel('Magnitude [%s]'%units)
        s2.set_ylabel('Phase [degrees]')
        s3.set_ylabel('Coherent Power')
        s3.set_xlabel('Frequency [Hz]')

        s1.grid(which='major', ls='-')
        s2.grid(which='major', ls='-')
        s3.grid(which='major', ls='-')
        s1.grid(which='minor', ls='--')
        s2.grid(which='minor', ls='--')
        s3.grid(which='minor', ls='--')

    s1.legend(fontsize=12)
    plt.tight_layout()
    plt.show()
    return fig

def plot_raw_data(dataDict,
                  seconds=1,
                  downsample=1,
                  title='Raw Data',
                  units='cts',
                  fig=None ):
    '''
    Plots the time series data in a dataDict.
    Be careful that you plot only a resonable amount of seconds, 1 second will plot 16384 data points per channel.
    If you really want the whole data, set seconds=None.
    Use plt.ion() for convenience.

    Inputs:
    dataDict   = data dictionary structure containing raw data.
    seconds    = float.  Number of seconds of data to plot.  Default is 1 second.
                 Be careful not to plot too much without downsampling, this can make the plot slow.
    downsample = int.  Ratio at which to downsample the data.  Default is 1.
                 For example, downsample=2 will remove every other data point.
    title      = str.  Title of the figure.
    units      = str. Units for the y-axis.  Default is cts.
    fig        = matplotlib figure object upon which to make the plot.

    Output:
    fig = matplotlib figure object

    ### Example ###

    import numpy as np
    import nds2utils
    import nds2utils.dataUtils as du
    import nds2utils.plotUtils as pu

    channels = np.array(['H1:CAL-DELTAL_EXTERNAL_DQ', 'H1:PSL-ISS_SECONDLOOP_RIN_OUTER_OUT_DQ'])
    gps_start = 1256805122
    gps_stop  = 1256805222
    binwidth = 1.0 # Hz
    overlap = 0.25
    dataDict = du.getCSDs(channels, gps_start, gps_stop, binwidth, overlap)

    import matplotlib.pyplot as plt
    plt.ion()
    fig = pu.plot_raw_data(dataDict, seconds=12.3, downsample=2**10)

    '''
    newFig = False
    if fig is None:
        newFig = True
        fig = plt.figure(figsize=(16,12))
    else:
        axes = fig.gca()
        lines = axes.lines
    #print(newFig)

    channels = list(dataDict.keys())
    subplots = np.array([])
    for ii, chan in enumerate(channels):
        #print chan
        fs = dataDict[chan]['fs']
        if seconds == None:
            index = -1
        else:
            index = int(seconds * fs)

        # Get the correct amount of time
        # times = dataDict[chan]['times'][:index]
        times = np.arange(len(dataDict[chan]['data']))/float( dataDict[chan]['fs'] )
        times = times[:index]
        data = dataDict[chan]['data'][:index]

        # Downsample the plotted data
        times = times[::downsample]
        data = data[::downsample]

        label = chan.replace('_', ' ')

        ss = fig.add_subplot(len(channels), 1, ii+1)
        ss.plot(times, data, label=label)
        subplots = np.append(subplots, ss)
        # if newFig:
        #     ss = fig.add_subplot(len(channels), 1, ii+1)
        #     ss.plot(times, data, label=label)
        #     subplots = np.append(subplots, ss)
        # else:
        #     oldData = lines[ii].get_data()
        #     lines[ii].set_ydata(data)
        #     fig.canvas.draw()
        #     fig.canvas.flush_events()

    if newFig:
        for ss in subplots:
            ss.grid(which='major', ls='-')
            ss.grid(which='minor', ls='--')
            ss.set_ylabel('Raw Data [%s]'%units)
            ss.legend()
        subplots[0].set_title('{} - {}'.format(title, time.strftime('%b %d, %Y')))
        subplots[-1].set_xlabel('Time [s]')

        plt.tight_layout()
        plt.show()
    return fig
