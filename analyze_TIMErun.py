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

def cart2pol(x, y):
    x=x-np.mean(x)
    y=y-np.mean(y)
    rho = np.sqrt(np.square(x) + np.square(y))
    phi = np.arctan2(y, x)
    return(rho, phi)

def pol2cart(rho, phi):
    x = rho * np.cos(phi)
    y = rho * np.sin(phi)
    return(x, y)

def fill_h(histo_name, array):
    for x in range (len(array)):
        histo_name.Fill((np.array(array[x] ,dtype="d")))

def hist(list, x_name, channels=100, linecolor=4, linewidth=4,write=True):

    array=np.array(list ,dtype="d")

    hist=ROOT.TH1D(x_name,x_name,channels,0.99*np.min(array),1.01*np.max(array))
    fill_h(hist,array)
    hist.SetLineColor(linecolor)
    hist.SetLineWidth(linewidth)
    hist.GetXaxis().SetTitle(x_name)
    hist.GetYaxis().SetTitle("Entries")
    if write==True: hist.Write()
    #hist.SetStats(False)
    hist.GetYaxis().SetMaxDigits(3);
    hist.GetXaxis().SetMaxDigits(3);
    #hist.Write()
    return hist

def hist2D(name,list_x, list_y, x_name="x", y_name="y", channels=20, linecolor=4, linewidth=4):
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

def plotsDF(df, textOFF):
    #1D plots
    hist2D(textOFF+" XY distribution",df[df.columns[0]], df[df.columns[1]], channels=50)
    for c in df.columns:
        hist(df[c], textOFF+c)
    #2D plots
    for c in df.columns[2:]:
        plot=graph2D(textOFF+" map "+c,df[df.columns[0]],df[df.columns[1]],df[c], "x (mm)", "y (mm)", c)
        Canvas2D(plot,result_path,np.max(df[c]),Np=50,min=0, max=50)

parser = argparse.ArgumentParser(description='Analyze waveform from a certain Run', epilog='Version: 1.0')
parser.add_argument('-r','--run',help='number of run contained in the standard_path (REMEMBER THE 0 if <100)', action='store')
parser.add_argument('-d','--draw',help='if 1 is drawing all waveforms defualut is 0', action='store', default='0')
parser.add_argument('-b','--batch',help='Run ROOT in batch mode default=1', action='store', default='1')
parser.add_argument('-cDUT','--channelDUT',help='channel of DUT defaut=2', action='store', default="2")
parser.add_argument('-cREF','--channelREF',help='channel of REF defaut=1', action='store', default="1")
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


wavesDUT, wavesREF, waves_trk=[],[],[]
#select only files for the selected channel
files_DUT=[item for item in files if 'C'+str(args.channelDUT) in item]
files_REF=[item for item in files if 'C'+str(args.channelREF) in item]
files_trk=[item for item in files if 'C3' in item]

print("Colletting waves")
for i in tqdm.tqdm(range(len(files_DUT[:num]))):
    Seq_DUT=wf.ScopeSequence(run_path+files_DUT[i],"DUT_"+args.name)
    Seq_REF=wf.ScopeSequence(run_path+files_REF[i],"REF_"+args.name)
    Seq_trk=wf.ScopeSequence(run_path+files_trk[i],"tracker_"+args.name)
    wavesDUT.extend(Seq_DUT.GetWaves())
    wavesREF.extend(Seq_REF.GetWaves())
    waves_trk.extend(Seq_trk.GetWaves())

#structure:
"""
# 0-->X
# 1-->Y
# 2-->noise
# 3-->echarge
# 4-->amplitude
# 5-->sigma
# 6-->risetime
# 7-->SAT
"""
dataDUT, dataREF, notReco,badDUT, badREF=[],[],[],[],[]

#get the tracking info once so you don't have to open every time the dataframe
#last row is shitty drop it
df=pd.read_csv(trk_path+"asciiRun"+str(run_num)+".dat", sep="\t", skipfooter=1, engine='python')
track_info=df[[df.columns[0], "X"+args.channelREF+" ","Y"+args.channelREF+" ", "X"+args.channelDUT+" ","Y"+args.channelDUT+" "]]
track_info=track_info.set_index(track_info.columns[0])
track_info=track_info.rename(columns={track_info.columns[0]: 'xREF', track_info.columns[1]: 'yREF',track_info.columns[2]: 'xDUT', track_info.columns[3]: 'yDUT'})

main.mkdir("RawWaveforms/DUT/Fit")
main.mkdir("RawWaveforms/REF/Fit")
main.mkdir("RawWaveforms/DUT/Signal")
main.mkdir("RawWaveforms/REF/Signal")
print("Analyzing")
for i in tqdm.tqdm(range(len(wavesDUT))):
    track=wf.EventIDSignal(waves_trk[i]["T"],waves_trk[i]["V"],"track_"+args.name+str(i))
    #get coordniates and discaard the non resctostruded events
    if track.ID not in track_info.index:
        notReco.append(i)
        continue
    else:
        signalDUT=wf.ScopeSignalCividec(wavesDUT[i]["T"],wavesDUT[i]["V"],"DUT_"+args.name+str(i), risetimeCut=0.5E-9,sigma=5,fit=True)
        signalREF=wf.ScopeSignalCividec(wavesREF[i]["T"],wavesREF[i]["V"],"REF_"+args.name+str(i), risetimeCut=0.1E-9,sigma=5,fit=True)
        if args.draw=="1" and signalDUT.badSignalFlag==False:
            main.cd("RawWaveforms/DUT/Signal")
            signalDUT.WaveSave(EpeakLines=True,Write=True,Zoom=True)
            main.cd("RawWaveforms/REF/Signal")
            signalREF.WaveSave(EpeakLines=True,Write=True,Zoom=True)
        #check if signal is bad
        if signalDUT.badSignalFlag==True:
            badDUT.append(i)
            continue
        elif signalREF.badSignalFlag==True:
            badREF.append(i)
            continue
        else:
            dataDUT.append([track_info["xDUT"][track.ID],track_info["yDUT"][track.ID], signalDUT.baseLine, signalDUT.EpeakCharge, -1*signalDUT.Ampmin, signalDUT.SigmaOutNoise, signalDUT.risetime, signalDUT.sat])
            dataREF.append([track_info["xREF"][track.ID],track_info["yREF"][track.ID], signalREF.baseLine, signalREF.EpeakCharge, -1*signalREF.Ampmin, signalREF.SigmaOutNoise, signalREF.risetime, signalREF.sat])
            if args.draw=="1" and signalDUT.badSignalFlag==False:
                main.cd("RawWaveforms/DUT/Fit")
                signalDUT.SigmoidFit(write=True)
                main.cd("RawWaveforms/REF/Fit")
                signalREF.SigmoidFit(write=True)

cols=["X","Y","noise","echarge","amplitude","sigma","risetime","SAT"]

#create dataframe and plot results
main.mkdir("NO CUT PLOT")
main.cd("NO CUT PLOT")
dfDUT = pd.DataFrame(dataDUT,columns=cols)
dfREF = pd.DataFrame(dataREF,columns=cols)

rDUT,thetaDUT=cart2pol(dfDUT["X"],dfDUT["Y"])
rREF,thetaREF=cart2pol(dfREF["X"],dfREF["Y"])
dfDUT=dfDUT.assign(radius=rDUT,angle=thetaDUT)
dfREF=dfREF.assign(radius=rREF,angle=thetaREF)

plotsDF(dfDUT,"DUT NO CUT")
plotsDF(dfREF,"REF NO CUT")
timeDIFF=dfDUT["SAT"]-dfREF["SAT"]
hist(timeDIFF, "time difference NO CUT",channels=500)

xmDUT, ymDUT, xmREF, ymREF=np.mean(dfDUT["X"]),np.mean(dfDUT["Y"]),np.mean(dfREF["X"]),np.mean(dfREF["Y"])
draw_cut=4#mm radius from the center both the detector!

drop_indexDUT,drop_indexREF=[],[]
drop_index=dfDUT[dfDUT["radius"] > draw_cut].index
drop_index.union(dfDUT[dfREF["radius"] > draw_cut].index)
#drop_indexREF=dfREF[pow((dfREF["X"]-xmREF),2)+pow((dfREF["Y"]-ymREF),2) > draw_cut].index
eventDrawCut=1-len(drop_index)/(len(dfDUT["X"]))
print("Survival after GEO cut:",eventDrawCut)
dfDUT,dfREF = dfDUT.drop(drop_index),dfREF.drop(drop_index)

main.mkdir("GEO CUT PLOT")
main.cd("GEO CUT PLOT")
plotsDF(dfDUT,"DUT GEO CUT")
plotsDF(dfREF,"REF GEO CUT")
timeDIFF=dfDUT["SAT"]-dfREF["SAT"]
hist(timeDIFF, "time difference GEO CUT",channels=100)

TimeCut=0.3E-9
#try to cut
timeDiffSel, TDmin, TDmax=[], np.median(timeDIFF)-3*TimeCut, np.median(timeDIFF)+3*TimeCut
for td in timeDIFF:
    #print(td,TDmax,TDmin)
    if td>=TDmin and TDmax<=TDmax:
        timeDiffSel.append(td)
timeHist=hist(timeDiffSel, "time difference GEO CUT",channels=100,write=True)
