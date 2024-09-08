import datetime, os
def saveFig(self,plt):
    dateandclock=datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    plt.savefig(os.path.join('Saved_plots/','behav_fig_%s.png' %(dateandclock)))
    print('Figure saved in Saved_plots/ as behav_fig_%s.png.'%(dateandclock))