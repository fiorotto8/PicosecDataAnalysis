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

print("culo")

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
parser.add_argument('-d','--draw',help='if 1 is drawing all waveforms defualut is 0', action='store', default='0')
parser.add_argument('-b','--batch',help='Run ROOT in batch mode default=1', action='store', default='1')
parser.add_argument('-c','--channel',help='chennel to analyze defaut=2', action='store', default="2")
parser.add_argument('-s','--selFiles',help='limit in the number of files to analyze defalut=all', action='store', default="all")
parser.add_argument('-n','--name',help='put a name for the SignalScope object if you want', action='store', default="test")
parser.add_argument('-w','--writecsv',help='Disable the csv results writing', action='store', default="1")
parser.add_argument('-po','--polya',help='Disable the complex polya fit', action='store', default="0")

args = parser.parse_args()

#get the run number from path
run_num=args.run
run_path=run_path+run_num+"/"
result_path=result_path+run_num+"/"
#check the active channels
files=next(os.walk(run_path))[2]
files=[f for f in files if '.trc' in f]
active_channels=[0,0,0,0]
for i in range(4):
    if any("C"+str(i+1) in f for f in files):
        active_channels[i]=1
print("################Analysing Run"+run_num+"################")

#check if folder exist, if not create it
if not os.path.isdir(result_path):
     os.makedirs(result_path)

main=ROOT.TFile(result_path+"/Run_"+run_num+".root","RECREATE")#root file creation
#main=ROOT.TFile("Run_"+run_num+".root","RECREATE")#root file creation
if args.batch=="1": ROOT.gROOT.SetBatch(True)
e=1.6E-19

#selection on number of ile to analyze
if args.selFiles=="all":
    num=len(files)
else:
    num=int(args.selFiles)

waves, waves_trk=[],[]
#select only files for the selected channel
files_signal=[item for item in files if 'C'+str(args.channel) in item]
files_trk=[item for item in files if 'C3' in item]
#remove the 0000 sequence
#IN A FUTURE VERSION MAYBE CHECK IF THIS IS NEEDED!!!
    #it can happen that the first sequence is saved wrongly
    #if you do not clear the memory with of the scope with a stop/normal/stop/normal it saves the sequence of the previour run
#files_signal=[item for item in files_signal if "00000" not in item]
#files_trk=[item for item in files_trk if '00000' not in item]

print("Colletting waves")
for i in tqdm.tqdm(range(len(files_signal[:num]))):
    Seq=wf.ScopeSequence(run_path+files_signal[i],"track_"+args.name)
    waves.extend(Seq.GetWaves())
    Seq_trk=wf.ScopeSequence(run_path+files_trk[i],"tracker_"+args.name)
    waves_trk.extend(Seq_trk.GetWaves())

noises, echarges, amplitudes, bad,notReco, sigma, risetime, gain, test0, test1, test2=[] ,[],[], [], [],[],[],[],[],[],[]
ID,x,y=[],[],[]

#get the tracking info once so you don't have to open every time the dataframe
#last row is shitty drop it
df=pd.read_csv(trk_path+"asciiRun"+str(run_num)+".dat", sep="\t", skipfooter=1, engine='python')
track_info=df[[df.columns[0], df.columns[9],df.columns[10]]]
track_info=track_info.set_index(track_info.columns[0])

main.mkdir("RawWaveforms")
main.cd("RawWaveforms")
print("Analyzing")
for i in tqdm.tqdm(range(len(waves))):
#for i in range(len(waves)):
    track=wf.EventIDSignal(waves_trk[i]["T"],waves_trk[i]["V"],"track_"+args.name+str(i))
    #track.WaveGraph(write=True)
    ID.append(track.ID)
    #get coordniates and discaard the non resctostruded events
    if track.ID not in track_info.index:
        notReco.append(i)
        continue
    else:
        #print(ID[i],x,y)
        signal=wf.ScopeSignalSlow(waves[i]["T"],waves[i]["V"],args.name+str(i), risetimeCut=50E-9)
        if args.draw=="1":
            #signal.WaveGraph().Write()
            signal.WaveSave(EpeakLines=True,Write=True)
        #check if signal is bad
        if signal.badSignalFlag==True:
            bad.append(i)
            continue
        else:

            x.append(track_info[track_info.columns[0]][track.ID])
            y.append(track_info[track_info.columns[1]][track.ID])

            sigma.append(signal.SigmaOutNoise)
            noises.append(signal.baseLine)
            echarges.append(signal.EpeakCharge)
            gain.append(signal.Gain)
            risetime.append(signal.risetime)
            amplitudes.append(-1*signal.Ampmin)

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
    del echarges[i]
    del gain[i]
    del risetime[i]
    del x[i]
    del y[i]

main.mkdir("DRAW CUT")
main.cd("DRAW CUT")
print("Fraction not Reco events:", len(notReco)/len(waves))
print("Fraction bad WFs:", len(bad)/(len(waves)-len(notReco)))
echargePlot=graph2D("charge map DRAW CUT",x, y,echarges, "x (mm)", "y (mm)", "e-peak charge (C)")
ampPlot=graph2D("Amplitudes map DRAW CUT",x, y,amplitudes, "x (mm)", "y (mm)", "Amplitude (V)")
risetimePlot=graph2D("Risetime map DRAW CUT",x, y,risetime, "x (mm)", "y (mm)", "Risetime (s)")
Canvas2D(echargePlot,result_path,np.max(echarges),Np=50,min=0, max=50)
Canvas2D(ampPlot,result_path,np.max(amplitudes),Np=50,min=0, max=50)
Canvas2D(risetimePlot,result_path,np.max(risetime),Np=50,min=0, max=50)

hist(amplitudes, "Amplitudes (-V) DRAW CUT")
hist(echarges, "Charge (C) DRAW CUT")
hist(gain, "SinglePE Gain DRAW CUT")
hist(sigma, "Min sigma outside noise DRAW CUT")
hist(risetime, "Risetime (s) DRAW CUT")
hist(x, "x distr DRAW CUT")
hist(y, "y_distr DRAW CUT")

#CUTS
#calculate centroid of device by average
x_m,y_m=np.mean(x), np.mean(y)
geo_cut=9#mm round the max radius where the cherenkov come is still inside
maskIDX_geocut=[]#indeces to remove
for i in range(len(x)):
    if (pow((x[i]-x_m),2)+pow((y[i]-y_m),2))>geo_cut:
        maskIDX_geocut.append(i)
    else:
        continue
#perform cut
for i in sorted(maskIDX_geocut, reverse=True):
    del amplitudes[i]
    del echarges[i]
    del gain[i]
    del risetime[i]
    del x[i]
    del y[i]

print("Fraction of cut events:", len(x)/(len(waves)-len(notReco)-len(bad)))
print("Fraction of remaining events:", len(x)/len(waves))

main.mkdir("GEO CUT")
main.cd("GEO CUT")
hist(amplitudes, "Amplitudes (-V) GEO CUT")
hist(gain, "SinglePE Gain GEO CUT")
hist(risetime, "Risetime (s) GEO CUT")
hist(echarges, "Charge (C) GEO CUT")

echargePlot=graph2D("charge map GEO CUT",x, y,echarges, "x (mm)", "y (mm)", "e-peak charge (C)")
ampPlot=graph2D("Amplitudes map GEO CUT",x, y,amplitudes, "x (mm)", "y (mm)", "Amplitude (V)")
risetimePlot=graph2D("Risetime map GEO CUT",x, y,risetime, "x (mm)", "y (mm)", "Risetime (s)")
Canvas2D(echargePlot,result_path,np.max(echarges),Np=50,min=0,max=50)
Canvas2D(ampPlot,result_path,np.max(amplitudes),Np=50,min=0,max=50)
Canvas2D(risetimePlot,result_path,np.max(risetime),Np=50,min=0,max=50)

#with the slow amplifier the charge is not exactly the charge beacuse
#the amplifier Gain is not exacly know (well we can calibrate it)
#However, to measure PE/MIP we do the ratio between mean charges so
#it is just an offset
main.cd()
charge=wf.ChargeDistr(echarges, "Run"+str(run_num))
if args.polya=="1":
    a=charge.ComplexPolya(echarges,path=result_path)
else:
    a=charge.PolyaFit(save=True, path=result_path,channels=50)
print("Mean Charge Run"+str(run_num),a[1],"+/-",a[2], "Chi2/NDF:",a[4])

if args.writecsv=="1":
    f = open(base_path+"resultsPE.csv", "a")
    #Run NUM;RUN TYPE;MEAN RISETIME;ERR RISETIME;ARIRMETIC MEAN CHARGE;CHARGE FIT;ERR CHARGE;CHI2/NDF;survived Waves from cuts
    f.write(str(run_num)+";"+"PE"+";"+str(np.mean(risetime))+";"+str(np.mean(echarges))+";"+str(a[1])+";"+str(a[2])+";"+str(a[4])+";"+str(len(x)/len(waves))+"\n")
    f.close()



















#
