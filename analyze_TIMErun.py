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

#DUT
noisesDUT, echargesDUT, amplitudesDUT, badDUT,notRecoDUT, sigmaDUT, risetimeDUT=[],[],[],[],[],[],[]
xDUT,yDUT=[],[],[]
#REF
noisesREF, echargesREF, amplitudesREF, badREF,notRecoREF, sigmaREF, risetimeREF=[],[],[],[],[],[],[]
xREF,yREF=[],[],[]

#get the tracking info once so you don't have to open every time the dataframe
#last row is shitty drop it
df=pd.read_csv(trk_path+"asciiRun"+str(run_num)+".dat", sep="\t", skipfooter=1, engine='python')
track_info=df[[df.columns[0], df.columns[9],df.columns[10]]]
track_info=track_info.set_index(track_info.columns[0])

