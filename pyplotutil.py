import matplotlib.pyplot as plt
import math

def norm(data_list):
    total = sum(data_list)
    return [x / total for x in data_list]

def cumulative(data_list):
    indices = list(range(0, len(data_list)))
    return [sum(data_list[0:x+1]) for x in indices]

def exp_list(data_list, a):
    return [math.exp(a*x) for x in data_list]

def plot_by_key(datasets, key, x, xname):
    plt.xlabel(xname)
    for name, d in datasets.items():
        line = plt.plot(x, d[key], label="{name}_{key}".format(name=name, key=key))

    plt.legend()
    
def plot_keys(dataset, keys, x, xname, title=None):
    if title!=None:
        plt.title(title)
    plt.xlabel(xname)
    for key in keys:
        plt.plot(x, dataset[key], label = key)

    plt.legend()
    
def projection_error(projections, expected_total):
    return [abs(o - expected_total)/expected_total for o in projections]

def make_subplots(datasets, metrickeys, x, xname, rows=2, columns=2, height=10, width=10, title=None):
    """
    datakeys refer to the metrics
    """
    plt.figure(figsize=(width, height))

    for n in range(0, len(metrickeys)):
        mkey = metrickeys[n]
        plt.subplot(rows, columns, n+1)
        plt.ylabel("{mkey}".format(mkey=mkey))
        plot_by_key(datasets, mkey, x, xname)
        
    plt.subplots_adjust(left=0.2, wspace=0.8, top=0.8)

    if title!=None:
        plt.suptitle(title, y = 1)
        plt.tight_layout()
        plt.savefig(title)
    else:
        plt.tight_layout()
        
def make_subplot_set(datasets, setkeys, metrickeys, x, xname, rows=2, columns=2, height=10, width=10, title=None):  
    plt.figure(figsize=(width, height))

    for n in range(0, len(setkeys)):
        skey = setkeys[n]
        plt.subplot(rows, columns, n+1)
        plt.ylabel("{skey}".format(skey=skey))
        plot_keys(datasets[skey], metrickeys, x, xname, title=skey)
        
    plt.subplots_adjust(left=0.2, wspace=0.8, top=0.8)

    if title!=None:
        plt.suptitle(title, y = 1)
        plt.tight_layout()
        plt.savefig(title)
    else:
        plt.tight_layout()
        
def samplefirst_subplot(data, samplekeys, metrickeys, x, xname, rows, columns):
    for n in range(0, len(samplekeys)):
        skey = samplekeys[n]
        plt.subplot(rows, columns, n+1)
        plt.ylabel(skey)
        plot_keys(data[skey], metrickeys, x, xname, title=skey)
        
def metricfirst_subplot(data, samplekeys, metrickeys, x, xname, rows, columns):
    for n in range(0, len(metrickeys)):
        mkey = metrickeys[n]
        plt.subplot(rows, columns, n+1)
        plt.ylabel(mkey)
        plot_by_key(filter_dict(data, samplekeys), mkey, x, xname)
        
def cross_subplot(data, samplekeys, metrickeys, x, xname, rows, columns):
    for s in range(0, len(samplekeys)):
        skey = samplekeys[s]
        for m in range(0, len(metrickeys)):
            mkey = metrickeys[m]
            plt.subplot(rows, columns, 2*s + m + 1)
            plt.ylabel(skey)
            plt.xlabel(mkey)
            plt.title("{skey}_{mkey}".format(skey=skey, mkey=mkey))
            plt.plot(x, data[skey][mkey], label = mkey)
            
loopmode_mapping = {
    'sample' : samplefirst_subplot,
    'metric' : metricfirst_subplot,
    'cross' : cross_subplot
}
        
def make_subplot_set_with_loopmode(data, samplekeys, metrickeys, x, xname, loopmode='sample', rows=2, columns=2, height=10, width=10, title=None):
    """
    data is a dict of dict, outer keys are the dataset keys/names, inner keys are the metrics related to each sample
    loopmodes:
        sample will graph all metrics on one chart, with each sample as a subplot
        metric will put each metric on its own chart, with each sample as a curve on every chart
        cross will do each sample one at a time, showing each metric on one chart at a time
    """
    plt.figure(figsize=(width, height))
    
    loopmode_mapping = {
        'sample' : samplefirst_subplot,
        'metric' : metricfirst_subplot,
        'cross' : cross_subplot
    }
    
    f = loopmode_mapping[loopmode]
    f(data, samplekeys, metrickeys, x, xname, rows, columns)
        
    plt.subplots_adjust(left=0.2, wspace=0.8, top=0.8)

    if title!=None:
        plt.suptitle(title, y = 1)
        plt.tight_layout()
        plt.savefig(title)
    else:
        plt.tight_layout()
        
def filter_dict(d, keys):
    return {key: d[key] for key in keys}