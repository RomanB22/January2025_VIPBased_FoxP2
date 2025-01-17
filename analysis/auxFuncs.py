import numpy as np
import matplotlib.pyplot as plt
from scipy import ndimage
import math

def bin_spikes(spike_times, dt, wdw_start, wdw_end):
    # Function that puts spikes into bins
    edges = np.arange(wdw_start, wdw_end, dt)  # Get edges of time bins
    num_bins = edges.shape[0] - 1  # Number of bins
    num_neurons = spike_times.shape[0]  # Number of neurons
    neural_data = np.empty([num_bins, num_neurons])  # Initialize array for binned neural data
    # Count number of spikes in each bin for each neuron, and put in array
    for i in range(num_neurons):
        neural_data[:, i] = np.histogram(spike_times[i], edges)[0]
    return neural_data

def overlapping_window(np_array, window_size=50):
    return ndimage.uniform_filter1d(np_array, size=window_size, axis=1, mode='constant')

def non_overlapping_window(np_array, window_size=50):
    window_hop = window_size
    start_frame = window_size
    end_frame = window_hop * math.floor(float(np_array.shape[1]) / window_hop)
    window = []
    for frame_idx in range(start_frame, end_frame, window_hop):
        window.append(np.mean(np_array[:, frame_idx - window_size:frame_idx],  axis=1)) # Add mean

    return np.transpose(np.vstack(window))

def CalculateRate(SpikesFoxP2, SpikesDec, SpikesInc, window_size, dt, PreWindow_start, PostWindow_end):
    RasterFoxP2 = bin_spikes(SpikesFoxP2, window_size * dt, PreWindow_start, PostWindow_end + dt).T
    RasterDec = bin_spikes(SpikesDec, window_size * dt, PreWindow_start, PostWindow_end + dt).T
    RasterInc = bin_spikes(SpikesInc, window_size * dt, PreWindow_start, PostWindow_end + dt).T

    RateFoxP2 = RasterFoxP2 * 1000 / (window_size * dt)
    RateDec = RasterDec * 1000 / (window_size * dt)
    RateInc = RasterInc * 1000 / (window_size * dt)

    return RateFoxP2, RateDec, RateInc

def PlotRaster(RateFoxP2, RateDec, RateInc, time):
    vmin = min(min(RateFoxP2.flatten()), min(RateDec.flatten()), min(RateInc.flatten()))
    vmax = max(max(RateFoxP2.flatten()), max(RateDec.flatten()), max(RateInc.flatten()))

    trials = np.shape(RateFoxP2)[0]

    fig = plt.figure(figsize=(10, 10))
    plt.subplot(3,1,1)
    plt.imshow(RateFoxP2, cmap='viridis', interpolation='none', aspect='auto',
               vmin=vmin, vmax=vmax, origin='lower', extent=[time[0], time[-1], 0,trials])
    ax1 = plt.gca()

    plt.subplot(3,1,2)
    plt.imshow(RateDec, cmap='viridis', interpolation='none', aspect='auto',
               vmin=vmin, vmax=vmax, origin='lower', extent=[time[0], time[-1], 0,trials])
    ax2 = plt.gca()

    plt.subplot(3,1,3)
    im = plt.imshow(RateInc, cmap='viridis', interpolation='none', aspect='auto',
                    vmin=vmin, vmax=vmax, origin='lower', extent=[time[0], time[-1], 0,trials])

    ax3 = plt.gca()
    ax1.sharex(ax3)
    ax2.sharex(ax3)
    for ax in [ax1, ax2, ax3]:
        ax.set_ylabel('Trial #')
        ax.set_xlabel('Time (ms)')
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.vlines(1800, 0, trials, color='black', linewidth=3)

    fig.subplots_adjust(right=0.9)
    cbar_ax = fig.add_axes([0.92, 0.15, 0.01, 0.7])
    fig.colorbar(im, cax=cbar_ax, label= 'Rate (Hz)')

def CalculateAvgStd(RateFoxP2, RateDec, RateInc):
    return RateFoxP2.mean(axis=0), RateDec.mean(axis=0), RateInc.mean(axis=0), RateFoxP2.std(axis=0), RateDec.std(axis=0), RateInc.std(axis=0)

def PlotRate(FoxP2_avg, Dec_avg, Inc_avg, FoxP2_std, Dec_std, Inc_std, time, alpha=0.1, Znormed=False, label=['FoxP2','PT5B dec','PT5B inc']):
    yminTot, ymaxTot = [], []
    plt.figure(figsize=(10, 10))
    plt.plot(time, FoxP2_avg, color='black', label=label[0])
    if Znormed:
        ymin = FoxP2_avg - FoxP2_std
        ymax = FoxP2_avg + FoxP2_std
        plt.fill_between(time, ymin, ymax, color='black', alpha=alpha, linewidth=0)
    else:
        ymin = [max(0, i) for i in (FoxP2_avg - FoxP2_std)]
        ymax = FoxP2_avg + FoxP2_std
        plt.fill_between(time, ymin, ymax, color='black', alpha=alpha, linewidth=0)
    yminTot.append(min(ymin))
    ymaxTot.append(max(ymax))

    plt.plot(time, Dec_avg, color='tab:blue', label=label[1])
    if Znormed:
        ymin = Dec_avg - Dec_std
        ymax = Dec_avg + Dec_std
        plt.fill_between(time, ymin, ymax, color='tab:blue', alpha=alpha, linewidth=0)
    else:
        ymin = [max(0, i) for i in (Dec_avg - Dec_std)]
        ymax = Dec_avg + Dec_std
        plt.fill_between(time, ymin, ymax, color='tab:blue', alpha=alpha, linewidth=0)
    yminTot.append(min(ymin))
    ymaxTot.append(max(ymax))

    plt.plot(time, Inc_avg, color='tab:red', label=label[2])
    if Znormed:
        ymin = Inc_avg - Inc_std
        ymax = Inc_avg + Inc_std
        plt.fill_between(time, ymin, ymax, color='tab:red', alpha=alpha, linewidth=0)
    else:
        ymin = [max(0, i) for i in (Inc_avg - Inc_std)]
        ymax = Inc_avg + Inc_std
        plt.fill_between(time, ymin, ymax, color='tab:red', alpha=alpha, linewidth=0)
    yminTot.append(min(ymin))
    ymaxTot.append(max(ymax))

    plt.legend(loc='upper right')
    plt.xlabel('Time (ms)')
    plt.ylabel('Rate (Hz)')
    ax = plt.gca()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.vlines(1800, min(yminTot), max(ymaxTot), color='black', linewidth=3)

def CalculateZNorm(RateFoxP2, RateDec, RateInc):
    return (RateFoxP2-RateFoxP2.mean())/RateFoxP2.std(axis=0), (RateDec-RateDec.mean())/RateDec.std(axis=0), (RateInc-RateInc.mean())/RateInc.std(axis=0)

def CalculateDifference(RateFoxP2, RateDec, RateInc):
    FoxP2_IncRaster_diff = RateFoxP2 - RateInc
    FoxP2_DecRaster_diff = RateFoxP2 - RateDec
    Inc_DecRaster_diff = RateInc - RateDec

    return FoxP2_IncRaster_diff, FoxP2_DecRaster_diff, Inc_DecRaster_diff

def PlotDiff(FoxP2_avg, Dec_avg, Inc_avg, FoxP2_std, Dec_std, Inc_std, time, alpha=0.1, label=['FoxP2','PT5B dec','PT5B inc'], PlotIncDec=False):
    yminTot, ymaxTot = [], []
    plt.figure(figsize=(10, 10))
    plt.plot(time, FoxP2_avg, color='black', label=label[0])
    ymin = FoxP2_avg - FoxP2_std
    ymax = FoxP2_avg + FoxP2_std
    plt.fill_between(time, ymin, ymax, color='black', alpha=alpha, linewidth=0)
    yminTot.append(min(ymin))
    ymaxTot.append(max(ymax))

    plt.plot(time, Dec_avg, color='tab:blue', label=label[1])
    ymin = Dec_avg - Dec_std
    ymax = Dec_avg + Dec_std
    plt.fill_between(time, ymin, ymax, color='tab:blue', alpha=alpha, linewidth=0)
    yminTot.append(min(ymin))
    ymaxTot.append(max(ymax))

    if PlotIncDec:
        plt.plot(time, Inc_avg, color='tab:red', label=label[2])
        ymin = Inc_avg - Inc_std
        ymax = Inc_avg + Inc_std
        plt.fill_between(time, ymin, ymax, color='tab:red', alpha=alpha, linewidth=0)
        yminTot.append(min(ymin))
        ymaxTot.append(max(ymax))
    plt.hlines(0, min(time), max(time), colors='k', linestyles='--')
    plt.legend(loc='upper right')
    plt.xlabel('Time (ms)')
    plt.ylabel('Rate difference (Hz)')
    ax = plt.gca()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.vlines(1800, min(yminTot), max(ymaxTot), color='black', linewidth=3)

def PlotSurface(X_vector, Y_vector, Z_vector, NumDecreasing, Surface_vector, InVivoInputs=51, colormap='viridis', TimeImplicit=False,
                indexInVivo=1, xlabel='Time (ms)', ylabel='PT5B Inc Rate (Hz)', zlabel='FoxP2 Rate (Hz)', legendlabel='$r_{PT5B_{Dec}}$: $%1.2f$ $Hz$', trajlabels='$r_{PT5B_{Inc}}$: $%1.2f$ $Hz$'):

    if TimeImplicit:
        X_trajectories = np.reshape(X_vector, (-1, 1))  # -1 to infer last dimension
        Y_trajectories = np.reshape(Y_vector, (-1, 1))
        Z_trajectories = np.reshape(Z_vector, (-1, 1))
    else:
        time = np.unique(X_vector)
        X_trajectories = np.reshape(X_vector, (-1, len(time)))  # -1 to infer last dimension
        Y_trajectories = np.reshape(Y_vector, (-1, len(time)))
        Z_trajectories = np.reshape(Z_vector, (-1, len(time)))

    number = np.shape(X_trajectories)[0]
    cmap = plt.get_cmap(colormap)
    colors = [cmap(i) for i in np.linspace(0, 1, number)]

    fig, ax = plt.subplots(subplot_kw={"projection": "3d"}, figsize=(10, 10))
    ax.view_init(elev=30., azim=30)
    ax.plot_trisurf(X_vector, Y_vector, Z_vector, edgecolor='tab:blue', linewidth=0, alpha=0.2,
                    antialiased = True,
                    label= legendlabel % np.array(Surface_vector).mean())

    if not TimeImplicit:
        yy, zz = np.meshgrid(np.linspace(min(Y_vector), max(Y_vector),2),
                             np.linspace(min(Z_vector), max(Z_vector), 2))
        xx = yy * 0 + 1800
        ax.plot_surface(xx, yy, zz, alpha=0.3, color='black', label='Movement time')

    for i in range(np.shape(X_trajectories)[0]):
        if not TimeImplicit:
            marker='.'
            markersize=5
            if i==indexInVivo and NumDecreasing==InVivoInputs:
                plt.plot(X_trajectories[i, :], Y_trajectories[i, :], Z_trajectories[i, :], alpha=0.9, color='r', marker=marker, markersize=markersize,
                         label='In Vivo params: $%1.2f$ $Hz$' % np.mean(Y_trajectories[i, :]))
            else:
                plt.plot(X_trajectories[i, :], Y_trajectories[i, :], Z_trajectories[i, :], alpha=0.9, color=colors[i], label=trajlabels % np.mean(Y_trajectories[i, :]))
    if not TimeImplicit:
        plt.legend(loc='upper right', frameon=False)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_zlabel(zlabel)
    plt.tight_layout()

def PlotRate3D(X_vector, Y_vector, Z_vector, NumDecreasing, InVivoInputs=51, indexInVivo=1, colormap='viridis',
               xlabel='Time (ms)', ylabel='PT5B Inc Rate (Hz)', mode='xy', marker='', TimeImplicit=False, legendlabel='$r_{PT5B_{Inc}}$: $%1.2f$ $Hz$'):
    if TimeImplicit:
        X_trajectories = X_vector  # -1 to infer last dimension
        Y_trajectories = Y_vector
        Z_trajectories = Z_vector
    else:
        time = np.unique(X_vector)
        X_trajectories = np.reshape(X_vector, (-1, len(time)))  # -1 to infer last dimension
        Y_trajectories = np.reshape(Y_vector, (-1, len(time)))
        Z_trajectories = np.reshape(Z_vector, (-1, len(time)))

    number = np.shape(X_trajectories)[0]
    cmap = plt.get_cmap(colormap)
    colors = [cmap(i) for i in np.linspace(0, 1, number)]

    if mode == 'xy':
        if TimeImplicit:
            plt.plot(X_trajectories, Y_trajectories, linestyle='', marker=marker, alpha=0.9,
                     label=legendlabel % np.mean(Y_trajectories))
        else:
            for i in range(np.shape(X_trajectories)[0]):
                if i == indexInVivo and NumDecreasing == InVivoInputs:
                    plt.plot(X_trajectories[i, :], Y_trajectories[i, :], marker='.', alpha=0.9, color='r',
                             label=legendlabel % np.mean(Y_trajectories[i, :]))
                else:
                    plt.plot(X_trajectories[i, :], Y_trajectories[i, :], marker=marker, alpha=0.9, color=colors[i],
                             label=legendlabel % np.mean(Y_trajectories[i, :]))
            ax = plt.gca()
            ax.vlines(1800, min(Y_trajectories.flatten()), max(Y_trajectories.flatten()), color='black', linewidth=3)
    elif mode == 'xz':
        if TimeImplicit:
            plt.plot(X_trajectories, Z_trajectories, linestyle='', marker=marker, alpha=0.9,
                     label=legendlabel % np.mean(Y_trajectories))
        else:
            for i in range(np.shape(X_trajectories)[0]):
                if i == indexInVivo and NumDecreasing == InVivoInputs:
                    plt.plot(X_trajectories[i, :], Z_trajectories[i, :], marker='.', alpha=0.9, color='r',
                             label=legendlabel % np.mean(Y_trajectories[i, :]))
                else:
                    plt.plot(X_trajectories[i, :], Z_trajectories[i, :], marker=marker, alpha=0.9, color=colors[i],
                             label=legendlabel % np.mean(Y_trajectories[i, :]))
                    xlabel = xlabel
                    ylabel = ylabel
            ax = plt.gca()
            ax.vlines(1800, min(Z_trajectories.flatten()), max(Z_trajectories.flatten()), color='black', linewidth=3)
    elif mode == 'yz':
        if TimeImplicit:
            plt.plot(Y_trajectories, Z_trajectories, linestyle='', marker=marker, alpha=0.9,
                     label=legendlabel % np.mean(Y_trajectories))
        else:
            for i in range(np.shape(X_trajectories)[0]):
                if i == indexInVivo and NumDecreasing == InVivoInputs:
                    plt.plot(Y_trajectories[i, :], Z_trajectories[i, :], marker='.', alpha=0.9, color='r',
                             label=legendlabel % np.mean(Y_trajectories[i, :]))
                else:
                    plt.plot(Y_trajectories[i, :], Z_trajectories[i, :], marker=marker, alpha=0.9, color=colors[i],
                             label=legendlabel % np.mean(Y_trajectories[i, :]))
    ax = plt.gca()
    plt.legend(loc='upper right', frameon=False)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    plt.tight_layout()

def CreateNeuronalArithmeticMatrix(df, TimeWindow1, TimeWindow2, AMPAWeight):
    MatrixInVivo = []
    MatrixMirrorDecre = []
    MatrixOnlyIncre = []

    # In Vivo values
    for NumIncreasing in [int(18 * 0.25), int(18 * 0.5), int(18 * 0.75), 18, int(18 * 1.25), int(18 * 1.5),
                          int(18 * 1.75), int(18 * 2), int(18 * 2.25), int(18 * 2.5)]:
        for NumDecreasing in [int(51 * 0.25), int(51 * 0.5), int(51 * 0.75), 51, int(51 * 1.25), int(51 * 1.5),
                              int(51 * 1.75), int(51 * 2), int(51 * 2.25), int(51 * 2.5)]:
            dfMasked_1 = df[(df['NumIncreasing'] == NumIncreasing) & (df['NumDecreasing'] == NumDecreasing)
                            & (df['Time'] >= TimeWindow1[0]) & (df['Time'] <= TimeWindow1[1])
                            & (df['AMPAWeight'] == AMPAWeight)]

            dfMasked_2 = df[(df['NumIncreasing'] == NumIncreasing) & (df['NumDecreasing'] == NumDecreasing)
                            & (df['Time'] >= TimeWindow2[0]) & (df['Time'] <= TimeWindow2[1])
                            & (df['AMPAWeight'] == AMPAWeight)]

            for Condition in ['InVivo', 'OnlyIncre', 'MirrorDecre']:
                dfAux1 = dfMasked_1[dfMasked_1['Condition'] == Condition][
                    ['FoxP2Rate', 'DecRate', 'IncRate']].mean().values
                dfAux2 = dfMasked_2[dfMasked_2['Condition'] == Condition][
                    ['FoxP2Rate', 'DecRate', 'IncRate']].mean().values

                # NumIncreasing, NumDecreasing, DecRate in window1, IncRate in window1, FoxP2 in window1, and same for window2
                column = [NumIncreasing, NumDecreasing, dfAux1[1], dfAux1[2], dfAux1[0], dfAux2[1], dfAux2[2],
                          dfAux2[0]]
                if Condition == 'InVivo': MatrixInVivo.append(column)
                if Condition == 'MirrorDecre': MatrixMirrorDecre.append(column)
                if Condition == 'OnlyIncre': MatrixOnlyIncre.append(column)

    MatrixInVivo = np.array(MatrixInVivo)
    MatrixMirrorDecre = np.array(MatrixMirrorDecre)
    MatrixOnlyIncre = np.array(MatrixOnlyIncre)

    return MatrixInVivo, MatrixMirrorDecre, MatrixOnlyIncre

def CalculateAvgRatePerNeuron(MatrixInVivo):
    AvgDecreasing1 = 0
    AvgIncreasing1 = 0
    AvgDecreasing2 = 0
    AvgIncreasing2 = 0

    for i in range(len(MatrixInVivo)):
        AvgDecreasing1 += MatrixInVivo[i, 2] / MatrixInVivo[i, 1]
        AvgIncreasing1 += MatrixInVivo[i, 3] / MatrixInVivo[i, 0]
        AvgDecreasing2 += MatrixInVivo[i, 5] / MatrixInVivo[i, 1]
        AvgIncreasing2 += MatrixInVivo[i, 6] / MatrixInVivo[i, 0]

    AvgDecreasing1 /= i + 1
    AvgIncreasing1 /= i + 1
    AvgDecreasing2 /= i + 1
    AvgIncreasing2 /= i + 1

    return AvgDecreasing1, AvgIncreasing1, AvgDecreasing2, AvgIncreasing2

def IO_rateVsPT5BIncre(Matrix, TimeWindowIndex, colormap='viridis'):
    cmap = plt.get_cmap(colormap)
    colors = [cmap(i) for i in np.linspace(0, 1, 10)]

    if TimeWindowIndex == 1:
        index=3
    elif TimeWindowIndex == 2:
        index=6
    for i in range(10):
        plt.plot(Matrix[i::10, index], Matrix[i::10, index+1], '-',
                 label='$PT5B_{dec}$ rate=$%2.1f$ $Hz$' % np.mean(Matrix[i::10, index-1]), color=colors[i])
    plt.legend(loc='best', frameon=False)
    plt.xlabel('$PT5B_{inc}$ rate (Hz)')
    plt.ylabel('FoxP2 rate (Hz)')
    ax = plt.gca()
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.tight_layout()
