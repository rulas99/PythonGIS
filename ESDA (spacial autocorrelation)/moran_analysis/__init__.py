import esda
import libpysal as lps
import matplotlib.pyplot as plt

from numpy import random, polyfit

from matplotlib import colors
from seaborn import kdeplot

from matplotlib import gridspec

def moranAnalysis(agebs,col,suptitle, titleM1, cmap='viridis', q=6, sig = 0.05, k=5, save=False):
    '''
    agebs :  geodataframe 
    col : column of interes
    suptitle : principal title of all plot
    titleM1 : title of the first map (categorical equalinterval of the col)
    cmap : cmap of the first map
    q : number of classes in the first map
    sig : significance value for hot a cold spots analysys with local Moran I
    k : number of k-neighbors for weigth-matrix
    save : path for destination map
    '''
    df = agebs.dropna().copy()
    wq =  lps.weights.KNN.from_dataframe(df,k=k)
    wq.transform = 'r'

    price = df[col]
    lag_migra = lps.weights.lag_spatial(wq, price)

    random.seed(12345)
    
    mi = esda.moran.Moran(price, wq)

    li = esda.moran.Moran_Local(price, wq)

    sig = 1 * (li.p_sim < sig)
    hotspot = 1 * (sig * li.q==1)
    coldspot = 2 * (sig * li.q==3)
    spots = hotspot + coldspot

    spot_labels = [ 'No significativo', 'Hot spot (AA)', 'Cold spot (BB)']
    labels = [spot_labels[i] for i in spots]

    fig5 = plt.figure(constrained_layout=True,figsize=(15,7),dpi=300)

    plt.suptitle(suptitle,fontsize=23,y=1.1)
    #plt.title('Elaborado por: Raúl de la Rosa',fontsize=10,loc='left',color='gray')

    widths = [15, 15,10]
    heights = [7, 7]
    spec5 = fig5.add_gridspec(ncols=3, nrows=2, width_ratios=widths,
                              height_ratios=heights)

    ax2 = fig5.add_subplot(spec5[:, 0])
    ax1 = fig5.add_subplot(spec5[:, 1])
    ax4 = fig5.add_subplot(spec5[0, 2])
    ax3 = fig5.add_subplot(spec5[1, 2])

    ax1.set_title('Autocorrelación espacial (I de Moran local)',fontsize=14, y=-.1)
    ax2.set_title(titleM1,fontsize=14, y=-.1)

    ax1.set_axis_off()
    ax2.set_axis_off()

    hmap = colors.ListedColormap(['blue', 'red', 'lightgrey'])

    df.assign(cl=labels).plot(column='cl', categorical=True,
            k=3, cmap=hmap, linewidth=0.1, ax=ax1,
            edgecolor='white', legend=True, legend_kwds={'frameon':False})

    df.plot(column=col, linewidth=0.05, edgecolor='white',cmap=cmap,legend=True,ax=ax2,scheme='EqualInterval', 
            k=q, legend_kwds={'frameon':False})

    kdeplot(mi.sim, shade=True, ax=ax3)
    ax3.vlines(mi.I, 0, 10, color='r')
    #ax3.vlines(mi.EI, 0,10, color='k')
    ax3.set_xlabel("I de Moran")
    ax3.spines['right'].set_visible(False)
    ax3.spines['top'].set_visible(False)
    ax3.spines['left'].set_visible(False)
    ax3.set_yticks([])
    ax3.set_ylabel('')
    ax3.tick_params(axis='both', which='major', labelsize=8, rotation=45)    
    ax3.text(mi.I-(4*mi.I/10),17.5,f'p-value: {round(mi.p_sim,3)}')
    ax3.text(mi.I-(4*mi.I/10),15.5,f'z-score: {round(mi.z_sim,3)}')

    b, a = polyfit(price, lag_migra, 1)

    ax4.scatter(price, lag_migra, ec='firebrick',color='#de1756',alpha=.15,s=7)
    ax4.vlines(price.mean(), lag_migra.min(), lag_migra.max(), linestyle='--')
    ax4.hlines(lag_migra.mean(), price.min(), price.max(), linestyle='--')
    ax4.plot(price, a + b*price, 'k',linewidth=2)
    #ax4.set_ylabel('Suma ponderada de sus vecinos (KNN)')
    ax4.set_xlabel('% nacid@s en otra enitdad')
    ax4.set_title(f'I de Moran: {round(b,3)}')
    ax4.spines['right'].set_visible(False)
    ax4.spines['top'].set_visible(False)
    ax4.tick_params(axis='both', which='major', labelsize=8) 
    
    if save:
        plt.savefig(save,dpi=400,bbox_inches='tight',transparent=False)

    plt.show()