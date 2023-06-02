import waveform as wf
import numpy as np
import sys
import ROOT
import lecroyparser
import argparse
import glob
import pandas as pd
import os, glob
import tqdm
import math as m
import time

file = open("path.txt", "r")
for string in file:
    exec(string)
file.close()

def nparr(list):
    return np.array(list, dtype="d")

def fill_h(histo_name, array):
    for x in range (len(array)):
        histo_name.Fill((np.array(array[x] ,dtype="d")))

def hist(list, x_name, channels=100, linecolor=4, linewidth=4):

    array=np.array(list ,dtype="d")

    hist=ROOT.TH1D(x_name,x_name,channels,0.99*np.min(array),1.01*np.max(array))
    fill_h(hist,array)
    hist.SetLineColor(linecolor)
    hist.SetLineWidth(linewidth)
    hist.GetXaxis().SetTitle(x_name)
    hist.GetYaxis().SetTitle("Entries")
    hist.Write()
    #hist.SetStats(False)
    hist.GetYaxis().SetMaxDigits(3);
    hist.GetXaxis().SetMaxDigits(3);
    #hist.Write()
    return hist

def hist2D(name,list_x, list_y, x_name, y_name, channels=20, linecolor=4, linewidth=4):
    def fill_h(histo_name, array_x, array_y):
        for x in range (len(array_x)):
            histo_name.Fill(array_x[x],array_y[x])

    array_x, array_y=nparr(list_x), nparr(list_y)

    hist=ROOT.TH2D(name,name,channels,0.9*np.min(array_x),1.1*np.max(array_x),channels,0.9*np.min(array_y),1.1*np.max(array_y))
    fill_h(hist,array_x, array_y)
    hist.SetLineColor(linecolor)
    hist.SetLineWidth(linewidth)
    hist.GetXaxis().SetTitle(x_name)
    hist.GetYaxis().SetTitle(y_name)
    hist.Write()
    hist.SetStats(False)
    hist.GetYaxis().SetMaxDigits(3);
    hist.GetXaxis().SetMaxDigits(3);
    #hist.Write()
    return hist

def canvas(plot,name="test", size=800, leftmargin=0.1, rightmargin=0.2,tmin=0, tmax=0, Tline=False):
    y_name=plot.GetYaxis().GetTitle()
    x_name=plot.GetXaxis().GetTitle()
    can1=ROOT.TCanvas(name, name)
    can1.SetFillColor(0);
    can1.SetBorderMode(0);
    can1.SetBorderSize(2);
    can1.SetLeftMargin(leftmargin);
    can1.SetRightMargin(rightmargin);
    can1.SetTopMargin(0.1);
    can1.SetBottomMargin(0.1);
    can1.SetFrameBorderMode(0);
    can1.SetFrameBorderMode(0);
    can1.SetFixedAspectRatio();
    plot.GetXaxis().SetRangeUser(0.8*tmin, 2*tmax)
    plot.Draw("ALP")

    if Tline==True:
        can1.Update()
        ymax=ROOT.gPad.GetUymax()
        ymin=ROOT.gPad.GetUymin()
        line=ROOT.TLine(tmin,ymin,tmin,ymax)
        line.SetLineColor(2)
        line.SetLineWidth(2)
        line.Draw("SAME")

        line1=ROOT.TLine(tmax,ymin,tmax,ymax)
        line1.SetLineColor(2)
        line1.SetLineWidth(2)
        line1.Draw("SAME")


    can1.Write()
    can1.SaveAs(name+".png")
    return can1

def graph(x,y,x_string, y_string, color=4, markerstyle=22, markersize=1):
        plot = ROOT.TGraph(len(x),  np.array(x  ,dtype="d")  ,   np.array(y  ,dtype="d"))
        plot.SetNameTitle(y_string+" vs "+x_string,y_string+" vs "+x_string)
        plot.GetXaxis().SetTitle(x_string)
        plot.GetYaxis().SetTitle(y_string)
        plot.SetMarkerColor(color)#blue
        plot.SetMarkerStyle(markerstyle)
        plot.SetMarkerSize(markersize)
        plot.Write()
        return plot

def graph2D(name, x,y,z,x_string="x",y_string="y",z_string="z"):
    plot = ROOT.TGraph2D(len(x),  nparr(x), nparr(y), nparr(z))
    plot.SetNameTitle(name, name+";"+x_string+";"+y_string+";"+z_string)
    #plot.Write()
    return plot

max_mult=1.
def Canvas2D(plot,path,maxZ,Np=200,min=15,max=45, option="surf2"):
    c=ROOT.TCanvas(plot.GetName(),plot.GetName(), 750, 700)
    c.SetFillColor(0);
    c.SetBorderMode(0);
    c.SetBorderSize(2);
    c.SetLeftMargin(0.15);
    c.SetRightMargin(0.2);
    c.SetTopMargin(0.1);
    c.SetBottomMargin(0.1);
    c.SetFrameBorderMode(0);
    c.SetFrameBorderMode(0);
    c.SetFixedAspectRatio();

    plot.Draw(option)
    plot.SetNpx(Np)
    plot.SetNpy(Np)
    c.Update()

    plot.GetXaxis().SetRangeUser(min,max)
    plot.GetYaxis().SetRangeUser(min,max)
    plot.GetZaxis().SetRangeUser(0,max_mult*maxZ)
    plot.GetZaxis().SetTitleOffset(2)
    c.Write()
    c.SaveAs(path+str(plot.GetName())+".png")

def Canvas1D(plot):
    c=ROOT.TCanvas(plot.GetName(),plot.GetName(), 1000, 1000)
    c.SetFillColor(0);
    c.SetBorderMode(0);
    c.SetBorderSize(2);
    c.SetLeftMargin(0.15);
    c.SetRightMargin(0.2);
    c.SetTopMargin(0.1);
    c.SetBottomMargin(0.1);
    c.SetFrameBorderMode(0);
    c.SetFrameBorderMode(0);
    c.SetFixedAspectRatio();

    plot.Draw()

    c.SaveAs(path+str(plot.GetName())+".png")


parser = argparse.ArgumentParser(description='Analyze waveform from a certain Run', epilog='Version: 1.0')
parser.add_argument('-r','--run',help='number of run contained in the standard_path (REMEMBER THE 0 if <100)', action='store')
parser.add_argument('-b','--batch',help='disable the batch mode of ROOT', action='store', default=None)
parser.add_argument('-c','--channel',help='chennel to analyze default=2', action='store', default="2")
parser.add_argument('-s','--selFiles',help='limit in the number of files to analyze defalut=all', action='store', default="all")
parser.add_argument('-n','--name',help='put a name for the SignalScope object if you want, default=test', action='store', default="test")
parser.add_argument('-g','--geo',help='Modify geo cut radius [mm], Default=2 mm', action='store',  default=2)
parser.add_argument('-d','--draw',help='any value allow to draw all waveform default None', action='store', default=None)
parser.add_argument('-w','--writecsv',help='any value will disable the csv results writing, default None', action='store', default=None)
parser.add_argument('-po','--polya',help='any value will disable the complex polya fit, default None', action='store', default=None)
parser.add_argument('-deb','--debugBad',help='Enable some prints for debugging the bad signals', action='store', default=None)
parser.add_argument('-all','--analyseAll',help='Enable the analyis of all the waveforms also the one not reconstructed', action='store', default=None)

args = parser.parse_args()

#get the run number from path
run_num=args.run
run_path=run_path+run_num+"/"
result_path=result_path+run_num+"/"
#check the active channels
files=next(os.walk(run_path))[2]
files=[f for f in files if '.trc' in f]
print("################Analysing Run"+run_num+"################")

#check if folder exist, if not create it
if not os.path.isdir(result_path):
    os.makedirs(result_path)

main=ROOT.TFile(result_path+"/Run_"+run_num+".root","RECREATE")#root file creation
#main=ROOT.TFile("Run_"+run_num+".root","RECREATE")#root file creation
if args.batch is None: ROOT.gROOT.SetBatch(True)
e=1.6E-19

#selection on number of file to analyze
if args.selFiles=="all":
    num=len(files)
else:
    num=int(args.selFiles)

waves, waves_trk=[],[]
#select only files for the selected channel
files_signal=[item for item in files if 'C'+str(args.channel) in item]
files_trk=[item for item in files if 'C3' in item]
files_signal.sort()
files_trk.sort()

print("Colletting waves")
for i in tqdm.tqdm(range(len(files_signal[:num]))):
    Seq=wf.ScopeSequence(run_path+files_signal[i],"track_"+args.name)
    waves.extend(Seq.GetWaves())
    Seq_trk=wf.ScopeSequence(run_path+files_trk[i],"tracker_"+args.name)
    waves_trk.extend(Seq_trk.GetWaves())

#noises, amplitudes, sigma, risetime, test0, test1, test2=[] ,[],[], [], [],[],[]
#ID,x,y=[],[],[]

#get the tracking info once so you don't have to open every time the dataframe
#last row is shitty drop it
df=pd.read_csv(trk_path+"asciiRun"+str(run_num)+".dat", sep="\t", skipfooter=1, engine='python')
track_info=df[[df.columns[0], "X"+args.channel+" ","Y"+args.channel+" "]]
track_info=track_info.set_index(track_info.columns[0])

main.mkdir("RawWaveforms")
main.cd("RawWaveforms")
print("Analyzing")
results=[]

def AnalWave(waveT,waveV,name):
    signal=wf.ScopeSignalSlow(waveT,waveV,name,sigma_thr=0,sigmaBad=0,risetimeCut=0,badDebug=args.debugBad,EpeakBadDisable=True)
    return [signal.badSignalFlag,signal.SigmaOutNoise,signal.baseLine,signal.risetime,-1*signal.Ampmin]

for i in tqdm.tqdm(range(len(waves))):
    track=wf.EventIDSignal(waves_trk[i]["T"],waves_trk[i]["V"],"track_"+args.name+str(i))
    if track.ID not in track_info.index:
        if args.analyseAll is not None:
            results.append([track.ID in track_info.index]+[None,None]+AnalWave(waves[i]["T"],waves[i]["V"],args.name+str(i)))
        else:
            results.append([track.ID in track_info.index]+[None,None,None,None,None,None,None])
    else:
        results.append([track.ID in track_info.index]+[track_info[track_info.columns[0]][track.ID]]+[track_info[track_info.columns[1]][track.ID]]+AnalWave(waves[i]["T"],waves[i]["V"],args.name+str(i)))
    if args.draw is not None:
        wf.ScopeSignalSlow(waves[i]["T"],waves[i]["V"],args.name+str(i)).WaveSave(EpeakLines=True, Write=True)

#df contains all the data and they are saved
df = pd.DataFrame(results, columns = ["Reco","X","Y","BadFlag", "SigmaOutNoise", "Baseline", "risetime", "Amplitude"])
df.to_csv(result_path+"/data_Run_"+run_num+".csv",sep=";")
recofrac=(len(waves)-np.sum(df["Reco"]))/len(waves)

main.mkdir("allData")
main.cd("allData")
sigma,noises, risetime, amplitudes=df["SigmaOutNoise"].tolist(),df["Baseline"].tolist(),df["risetime"].tolist(),df["Amplitude"].tolist()
hist(noises, "Baseline")
hist(amplitudes, "Amplitudes (-V)")
hist(sigma, "Min sigma outside noise")
hist(risetime, "Risetime (s)")

#remove from df the non reco events and teh events out of the global radius
df=df.drop(df[df["Reco"]==False].index)
#cut on 12,5mm radius
x_m,y_m=np.mean(df["X"].tolist()), np.mean(df["X"].tolist())
df=df.drop(df[   (pow((df["X"]-x_m),2)+pow((df["Y"]-y_m),2))>pow(12.5,2)     ].index)

main.mkdir("RecoData")
main.cd("RecoData")
x,y,sigma,noises, risetime, amplitudes=df["X"].tolist(),df["Y"].tolist(),df["SigmaOutNoise"].tolist(),df["Baseline"].tolist(),df["risetime"].tolist(),df["Amplitude"].tolist()

badfrac=(np.sum(df["BadFlag"]))/len(x)
lenBef=len(x)

hist(x, "X (mm)")
hist(y, "Y (mm)")
hist(noises, "Baseline")
hist(amplitudes, "Amplitudes (-V)")
hist(sigma, "Min sigma outside noise")
hist(risetime, "Risetime (s)")
ampPlot=graph2D("Amplitudes map NoCut",x, y,amplitudes, "x (mm)", "y (mm)", "Amplitude (V)")
risetimePlot=graph2D("Risetime map NoCut",x, y,risetime, "x (mm)", "y (mm)", "Risetime (s)")
sigmaPlot=graph2D("sigma map NoCut",x, y,sigma, "x (mm)", "y (mm)", "sigma (a.u.)")
noisePlot=graph2D("noise map NoCut",x, y,noises, "x (mm)", "y (mm)", "noise (V)")
Canvas2D(ampPlot,result_path,np.max(amplitudes),Np=50,min=0, max=50)
Canvas2D(risetimePlot,result_path,np.max(risetime),Np=50,min=0, max=50)
Canvas2D(sigmaPlot,result_path,np.max(risetime),Np=50,min=0, max=50)
Canvas2D(noisePlot,result_path,np.max(risetime),Np=50,min=0, max=50)

#GEO CUT
geo_cut=args.geo #mm round the max radius where the cherenkov come is still inside
main.mkdir("GeoCut")
main.cd("GeoCut")
df=df.drop(df[   (pow((df["X"]-x_m),2)+pow((df["Y"]-y_m),2))>pow(geo_cut,2)     ].index)
x,y,sigma,noises, risetime, amplitudes=df["X"].tolist(),df["Y"].tolist(),df["SigmaOutNoise"].tolist(),df["Baseline"].tolist(),df["risetime"].tolist(),df["Amplitude"].tolist()

geofrac=(lenBef-len(x))/lenBef

hist(x, "X (mm)")
hist(y, "Y (mm)")
hist(noises, "Baseline")
hist(amplitudes, "Amplitudes (-V)")
hist(sigma, "Min sigma outside noise")
hist(risetime, "Risetime (s)")
ampPlot=graph2D("Amplitudes map GeoCut",x, y,amplitudes, "x (mm)", "y (mm)", "Amplitude (V)")
risetimePlot=graph2D("Risetime map GeoCut",x, y,risetime, "x (mm)", "y (mm)", "Risetime (s)")
sigmaPlot=graph2D("sigma map GeoCut",x, y,sigma, "x (mm)", "y (mm)", "sigma (a.u.)")
noisePlot=graph2D("noise map GeoCut",x, y,noises, "x (mm)", "y (mm)", "noise (V)")
Canvas2D(ampPlot,result_path,np.max(amplitudes),Np=50,min=0, max=50)
Canvas2D(risetimePlot,result_path,np.max(risetime),Np=50,min=0, max=50)
Canvas2D(sigmaPlot,result_path,np.max(risetime),Np=50,min=0, max=50)
Canvas2D(noisePlot,result_path,np.max(risetime),Np=50,min=0, max=50)

main.cd()
amps=wf.ChargeDistr(amplitudes, "Run"+str(run_num),channels=200,bin="lin")

if args.polya is not None:
    b=amps.ComplexPolya(path=result_path)
else:
    b=amps.PolyaFit(save=True, path=result_path)

print("Fraction of not Reco Events:",recofrac)
print("Fraction of bad cut events (only reconstructed):", badfrac)
print("Fraction of geo cut events (only reconstructed):", geofrac)
print("Remaining fraction:", len(x)/len(waves))
print("Mean Amplitude Run"+str(run_num),b[1],"+/-",b[2], "Chi2/NDF:",b[4])

if args.writecsv is None:
    f = open(csv_path+"resultsPE.csv", "a")
    #Run NUM;RUN TYPE;MEAN RISETIME;ARITMETIC MEAN AMPLITUDE;AMPLITUDE FIT;ERR AMPLITUDE;CHI2/NDF;survived Waves from cuts
    f.write(str(run_num)+";"+"PE"+";"+str(np.mean(risetime))+";"+str(np.mean(amplitudes))+";"+str(b[1])+";"+str(b[2])+";"+str(b[4])+";"+str(1-(len(x)/len(waves)))+"\n")
    f.close()

"""
#DRAWING CUT
#calculate centroid of device by average
x_m,y_m=np.mean(x), np.mean(y)
draw_cut=100#mm radius from the center
maskIDX_drawcut=[]#indeces to remove
for i in range(len(x)):
    if (pow((x[i]-x_m),2)+pow((y[i]-y_m),2))>draw_cut:
        maskIDX_drawcut.append(i)
    else:
        continue
#perform cut
for i in sorted(maskIDX_drawcut, reverse=True):
    del amplitudes[i]
    del risetime[i]
    del x[i]
    del y[i]

#datafraem with all the data
data=pd.DataFrame({"X":x,"Y":y,"risetime":risetime,"amplitudes":amplitudes})
data.to_csv(result_path+"data_"+str(run_num)+".csv",sep=";")

main.mkdir("DRAW CUT")
main.cd("DRAW CUT")
print("Fraction not Reco events:", len(notReco)/len(waves))
print("Fraction bad WFs:", len(bad)/(len(waves)-len(notReco)))
ampPlot=graph2D("Amplitudes map DRAW CUT",x, y,amplitudes, "x (mm)", "y (mm)", "Amplitude (V)")
risetimePlot=graph2D("Risetime map DRAW CUT",x, y,risetime, "x (mm)", "y (mm)", "Risetime (s)")
Canvas2D(ampPlot,result_path,np.max(amplitudes),Np=50,min=0, max=50)
Canvas2D(risetimePlot,result_path,np.max(risetime),Np=50,min=0, max=50)

hist(amplitudes, "Amplitudes (-V) DRAW CUT")
hist(sigma, "Min sigma outside noise DRAW CUT")
hist(risetime, "Risetime (s) DRAW CUT")
hist(x, "x distr DRAW CUT")
hist(y, "y_distr DRAW CUT")

#CUTS
#calculate centroid of device by average
x_m,y_m=np.mean(x), np.mean(y)
#geo_cut=1.5
geo_cut=args.geo #mm round the max radius where the cherenkov come is still inside
maskIDX_geocut=[]#indeces to remove
for i in range(len(x)):
    if (pow((x[i]-x_m),2)+pow((y[i]-y_m),2))>pow(geo_cut,2):
        maskIDX_geocut.append(i)
    else:
        continue
#perform cut
for i in sorted(maskIDX_geocut, reverse=True):
    del amplitudes[i]
    del risetime[i]
    del x[i]
    del y[i]

#datafraem with all the data in the circle
dataCUT=pd.DataFrame({"X":x,"Y":y,"risetime":risetime,"amplitudes":amplitudes})
dataCUT.to_csv(result_path+"CUTdata_"+str(run_num)+".csv",sep=";")

print("Fraction of cut events:", len(x)/(len(waves)-len(notReco)-len(bad)))
print("Fraction of remaining events:", len(x)/len(waves))

main.mkdir("GEO CUT")
main.cd("GEO CUT")
hist(amplitudes, "Amplitudes (-V) GEO CUT")
hist(risetime, "Risetime (s) GEO CUT")

ampPlot=graph2D("Amplitudes map GEO CUT",x, y,amplitudes, "x (mm)", "y (mm)", "Amplitude (V)")
risetimePlot=graph2D("Risetime map GEO CUT",x, y,risetime, "x (mm)", "y (mm)", "Risetime (s)")
Canvas2D(ampPlot,result_path,np.max(amplitudes),Np=50,min=0,max=50)
Canvas2D(risetimePlot,result_path,np.max(risetime),Np=50,min=0,max=50)

#with the slow amplifier the charge is not exactly the charge beacuse
#the amplifier Gain is not exacly know (well we can calibrate it)
#However, to measure PE/MIP we do the ratio between mean charges so
#it is just an offset
main.cd()
amps=wf.ChargeDistr(amplitudes, "Run"+str(run_num),channels=200,bin="lin")

if args.polya is not None:
    b=amps.ComplexPolya(path=result_path)
else:
    b=amps.PolyaFit(save=True, path=result_path)
print("Mean Amplitude Run"+str(run_num),b[1],"+/-",b[2], "Chi2/NDF:",b[4])



if args.writecsv is None:
    f = open(csv_path+"resultsPE.csv", "a")
    #Run NUM;RUN TYPE;MEAN RISETIME;ARITMETIC MEAN AMPLITUDE;AMPLITUDE FIT;ERR AMPLITUDE;CHI2/NDF;survived Waves from cuts
    f.write(str(run_num)+";"+"PE"+";"+str(np.mean(risetime))+";"+str(np.mean(amplitudes))+";"+str(b[1])+";"+str(b[2])+";"+str(b[4])+";"+str(1-(len(x)/len(waves)))+"\n")
    f.close()
"""