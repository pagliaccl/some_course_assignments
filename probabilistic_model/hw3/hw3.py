import os
from scipy.stats import multivariate_normal
import warnings
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from collections import defaultdict
import copy

from sklearn.mixture import GaussianMixture

def transForm(inTuple):
    R=float(inTuple[0])
    G=float(inTuple[1])
    B=float(inTuple[2])

    r=R/(R+G+B)
    g=G/(R+G+B)



    alpha=255/(max(r,g,(1-(r+g))))

    Rout=int(alpha*r)
    Gout=int(alpha*g)
    Bout=int(alpha*(1-(r+g)))
    return (Rout,Gout,Bout)

def transForm2(inTuple):
    R=float(inTuple[0])
    G=float(inTuple[1])
    B=float(inTuple[2])

    r=R/(R+G+B)
    g=G/(R+G+B)

    return [r,g]

def questionA(inDir,outDir):
    im = Image.open(inDir)  # Can be many different formats.
    pix = im.load()
    newIm = Image.new('RGB', (225, 225))
    newImPix = newIm.load()
    for x in range(0, 225):
        for y in range(0, 225):
            newImPix[x, y] = transForm(pix[x,y])
    newIm.save(outDir+"/QuesitonA.jpg")

def questionB(inDir,outDir,seed=None):
    im = Image.open(inDir)
    pix = im.load()
    class0Im=Image.new('RGB',(225,225),color='white')
    class1Im=Image.new('RGB',(225,225),color='white')
    class2Im=Image.new('RGB',(225,225),color='white')
    D = [transForm2(pix[x, y]) for x in range(0, 225) for y in range(0, 225)]
    if isinstance(seed, int):
        ggm = GaussianMixture(n_components=3,init_params='random')
        ggm.random_state=seed
    else:
        ggm = GaussianMixture(n_components=3)
    ggm.fit(D)
    for x in range(0, 225):
        for y in range(0, 225):
            pred=ggm.predict(transForm2(pix[x,y]))
            if pred == 0:
                myPlot(class0Im, x, y, pix[x, y])
            if pred == 1:
                myPlot(class1Im, x, y, pix[x, y])
            if pred == 2:
                myPlot(class2Im, x, y, pix[x, y])
    class0Im.save(outDir+'/class0.jpg')
    class1Im.save(outDir+'/class1.jpg')
    class2Im.save(outDir+'/class2.jpg')

    # print ggm._get_parameters()
    # print ggm.score(D)




def myPlot(image, x, y, pixel):
    pix=image.load()
    pix[x,y]=transForm(pixel)

def questionBRnd(inDir,outDir,seed=None,rndNum=10, component=3):
    im = Image.open(inDir)
    pix = im.load()
    D = [transForm2(pix[x, y]) for x in range(0, 225) for y in range(0, 225)]
    prob=0
    for i in range(rndNum):
        classIm=[]
        for i in range(component):
            classIm.append(Image.new('RGB', (225, 225), color='white'))

        if isinstance(seed, int):
            ggm = GaussianMixture(n_components=component,init_params='random',max_iter=200)
            ggm.random_state=seed+i
        else:
            ggm = GaussianMixture(n_components=component)
        ggm.fit(D)
        for x in range(0, 225):
            for y in range(0, 225):
                pred=int(ggm.predict(transForm2(pix[x,y])))
                myPlot(classIm[pred], x, y, pix[x, y])
        score = ggm.score(D)
        if score>prob:
            prob=score
            for n,i in enumerate(classIm):
                i.save(outDir+'/class'+str(n)+'.jpg')
            # print score
            # print ggm.weights_
            # print ggm.means_
            # print ggm.covariances_


    # print ggm._get_parameters()


def retRndTree(inDir,seed=None,rndNum=10,component=3):
    im = Image.open(inDir)
    pix = im.load()
    D = [transForm2(pix[x, y]) for x in range(0, 225) for y in range(0, 225)]
    prob=0
    gmm=GaussianMixture()
    retgmm=GaussianMixture()
    for i in range(rndNum):
        if isinstance(seed, int):
            gmm = GaussianMixture(n_components=component,init_params='random',max_iter=200)
            gmm.random_state=seed+i
        else:
            gmm = GaussianMixture(n_components=component)
        gmm.fit(D)
        score = gmm.score(D)
        if score>prob:
            prob=score
            retgmm=copy.deepcopy(gmm)

    return retgmm



def make_ellipses(gmm, ax):
    # colors = np.random.rand(len(gmm.weights_), 1)
    # colors = [int(i % 23) for i in range(len(gmm.weights_))]
    colors=['red', 'green', 'blue', 'purple']+['navy', 'turquoise', 'darkorange']

    if len(gmm.weights_)==3:
        colors=['navy', 'turquoise', 'darkorange']
    idx=0
    for n in range(len(gmm.weights_)):
        if gmm.covariance_type == 'full':
            covariances = gmm.covariances_[n][:2, :2]
        elif gmm.covariance_type == 'tied':
            covariances = gmm.covariances_[:2, :2]
        elif gmm.covariance_type == 'diag':
            covariances = np.diag(gmm.covariances_[n][:2])
        elif gmm.covariance_type == 'spherical':
            covariances = np.eye(gmm.means_.shape[1]) * gmm.covariances_[n]
        v, w = np.linalg.eigh(covariances)
        u = w[0] / np.linalg.norm(w[0])
        angle = np.arctan2(u[1], u[0])
        angle = 180 * angle / np.pi  # convert to degrees
        v = 6. * np.sqrt(2) * np.sqrt(v)
        ell = mpl.patches.Ellipse(gmm.means_[n, :2], v[0], v[1],
                                  180 + angle,facecolor='None',edgecolor=colors[idx],linewidth=2)
                                  # ,edgecolor=color,facecolor='white')
        ell.set_clip_box(ax.bbox)
        ell.set_alpha(1)
        ax.add_artist(ell)
        idx+=1

def scatter(inDir,gmm):
    # colors = np.random.rand(len(gmm.weights_), 1)
    # colors= [int(i % 23) for i in range(len(gmm.weights_))]
    colors=['red', 'green', 'blue', 'purple']+['navy', 'turquoise', 'darkorange']
    im = Image.open(inDir)
    pix = im.load()
    D = [transForm2(pix[x, y]) for x in range(0, 225) for y in range(0, 225)]
    DClassifed= defaultdict(list)
    means=gmm.means_

    for x,y in D:
        i= gmm.predict((x,y))
        DClassifed[str(i)].append((x,y))


    idx=0
    for c in DClassifed.values():
        # print colors[idx]
        i = [x for x, y in c]
        j = [y for x, y in c]
        plt.scatter(i, j, color=colors[idx],alpha=0.2)
        idx+=1

    for i,j in means:
        plt.scatter(i, j, color=colors[idx], marker='+', s=50)


def plotScatterAndEll(inDir,outDir,seed=101, iterN=10, component=5):
    ax = plt.subplot()
    tree=retRndTree(inDir,seed,iterN,component)
    make_ellipses(tree,ax)
    scatter(inDir,tree)
    plt.xlim([0,1])
    plt.ylim([0,1])
    plt.savefig(outDir)
    plt.clf()

def getpdf(tree,x,y):
    p=[]
    for i in range(len(tree.weights_)):
        mean=tree.means_[i]
        cov=tree.covariances_[i]
        # print 'mean is '
        # print mean
        # print 'var is '
        # print cov
        rv = multivariate_normal(mean, cov)
        alpha=tree.weights_[i]
        p.append(alpha*rv.pdf((x,y)))
        # print p

    ret=[]
    for i in range(len(tree.weights_)):
        ret.append(p[i]/sum(p))
    return ret

def drawPDF(inDir, outDir, component=3):
    tree=retRndTree(inDir,seed=101,component=component,rndNum=10)
    im = Image.open(inDir)
    pix = im.load()
    D = [transForm2(pix[x, y]) for x in range(0, 225) for y in range(0, 225)]
    temp=[]
    for x, y in D:
        pdf=getpdf(tree, x,y)
        temp.append(list(pdf))
    for i in range(component):
        print "here"
        x1=[x for x, y in D]
        y1=[y for x, y in D]
        P=np.array(temp)[:,i]
        temP=[]
        for j in P:
                temP.append(str(1-j))

        plt.scatter(x1,y1,c=temP,cmap='gray',alpha=0.2)
        plt.gray()
        if not os.path.exists(outDir):
            os.makedirs(outDir)
        plt.savefig(outDir+"/component_"+str(i)+".jpg")
        plt.cla()



if __name__ == '__main__':
    warnings.filterwarnings("ignore")
    inDir="/Users/Pagliacci/Desktop/ECE 443/hw3/TestImage.jpg"
    outDir="/Users/Pagliacci/Desktop/ECE 443/hw3/question_with_"
    for component in range (3,6):
        out = outDir + str(component) + "_component"
        if not os.path.exists(out):
            os.makedirs(out)
        questionA(inDir,out)
        questionBRnd(inDir,out,101,5,component)
        plotScatterAndEll(inDir,out+"/quesitonB2.jpg", component=component)
        drawPDF(inDir,out+"/questionB2",component=component)
    out = outDir + str(3) + "_newcomponent"
    if not os.path.exists(out):
        os.makedirs(out)

    questionB(inDir,out)


