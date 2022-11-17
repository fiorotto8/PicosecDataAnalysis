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
import multiprocess as mp

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

parser = argparse.ArgumentParser(description='Analyze waveform from a certain Run', epilog='Version: 1.0')
parser.add_argument('-tp','--trackerpath',help='path contiaining the tracker data', action='store', default="./tracker/")
parser.add_argument('-r','--run',help='number of run contained in the standard_path (REMEMBER THE 0 if <100)', action='store')
parser.add_argument('-d','--draw',help='if 1 is drawing all waveforms defualut is 0', action='store', default='0')
parser.add_argument('-b','--batch',help='Run ROOT in batch mode default=1', action='store', default='1')
parser.add_argument('-c','--channel',help='chennel to analyze defaut=2', action='store', default="2")
parser.add_argument('-s','--selFiles',help='limit in the number of files to analyze defalut=all', action='store', default="all")
parser.add_argument('-po','--polya',help='Disable the complex polya fit', action='store', default="1")
parser.add_argument('-n','--name',help='put a name for the SignalScope object if you want', action='store', default="test")
parser.add_argument('-w','--writecsv',help='Disable the csv results writing', action='store', default="1")
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
if args.batch=="1": ROOT.gROOT.SetBatch(True)
e=1.6E-19

#selection on number of ile to analyze
if args.selFiles=="all":
    num=len(files)
else:
    num=int(args.selFiles)


#select only files for the selected channel
files=[item for item in files if 'C'+str(args.channel) in item]
start=time.time()
print("Colletting waves...")
waves=[]
for file in tqdm.tqdm(files[:num]):
    Seq=wf.ScopeSequence(run_path+file,"track_"+args.name)
    waves.extend(Seq.GetWaves())


print("Collecting time (s):", time.time()-start)


main.mkdir("RawWaveforms")
main.cd("RawWaveforms")
print("Analyzing...")
start=time.time()
def AnalWave(waveT,waveV,name,risetimeCut=50E-9):
    signal=wf.ScopeSignalSlow(waveT,waveV,name,risetimeCut=50E-9)
    return [signal.badSignalFlag,signal.SigmaOutNoise,signal.baseLine,signal.EpeakCharge,signal.risetime,-1*signal.Ampmin]
#if drawing cannot paralelize
if args.draw=="0":
    pool = mp.Pool(mp.cpu_count())
    results = pool.starmap(AnalWave,[(wave["T"],wave["V"],args.name+str(i)) for wave in waves])
    pool.close()
else:
    results=[]
    for wave in waves:
        results.append(AnalWave(wave["T"],wave["V"],args.name+str(i)))

print("Analyzing time (s):", time.time()-start)

df = pd.DataFrame(results, columns = ["BadFlag", "SigmaOutNoise", "Baseline", "Epeakcharge", "risetime", "AmpMin"])
df.to_csv(result_path+"/data_Run_"+run_num+".csv",sep=";")
#drop bad signals
baddf=df[df["BadFlag"]==True]
df = df.drop(df[df["BadFlag"]==True].index)
sigma,noises, echarges, risetime, amplitudes=df["SigmaOutNoise"].tolist(),df["Baseline"].tolist(),df["Epeakcharge"].tolist(),df["risetime"].tolist(),df["AmpMin"].tolist()

if len(sigma)!=0:
    main.cd()
    hist(noises, "baseline (V)")
    hist(amplitudes, "Amplitudes (-V)")
    hist(echarges, "Epeak Charge (C)")
    hist(sigma, "Min sigma outside noise")
    hist(risetime, "Risetime (s)")
    print("Fraction bad WFs:", len(baddf["BadFlag"])/len(waves))
    hist2D("EchargeRisetimeCorr", risetime,echarges,"Risetime(s)","Echarge(C)")
    hist2D("AmpChargeCorr", amplitudes,echarges,"Amplitudes(-V)","Echarge(C)")
    graph(np.arange(0,len(amplitudes),1),amplitudes,"Time(a.u.)","Amplitudes(-V)")

    #with the slow amplifier the charge is not exactly the charge beacuse
    #the amplifier Gain is not exacly know (well we can calibrate it)
    #However, to measure PE/MIP we do the ratio between mean charges so
    #it is just an offset
    charge=wf.ChargeDistr(echarges, "Run"+str(run_num))

    if args.polya=="1":
        a=charge.ComplexPolya(echarges,path=result_path)
    else:
        a=charge.PolyaFit(save=True, path=result_path)
    print("Mean Charge Run"+str(run_num),a[1],"+/-",a[2], "Chi2/NDF:",a[4])

if args.writecsv=="1":
    f = open(base_path+"resultsPE.csv", "a")
    #Run NUM;RUN TYPE;MEAN RISETIME;ERR RISETIME;ARIRMETIC MEAN CHARGE;CHARGE FIT;ERR CHARGE;CHI2/NDF;survived Waves from cuts
    f.write(str(run_num)+";"+"SPE"+";"+str(np.mean(risetime))+";"+str(np.mean(echarges))+";"+str(a[1])+";"+str(a[2])+";"+str(a[4])+";"+str(1-(len(baddf["BadFlag"])/len(waves)))+"\n")
    f.close()




















#
