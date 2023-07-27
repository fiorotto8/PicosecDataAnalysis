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
import uproot
import gc
gc.collect()

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
parser.add_argument('-d','--draw',help='any value allow to draw all waveform', action='store', default=None)
parser.add_argument('-b','--batch',help='Disable the batch mode of ROOT', action='store', default=None)
parser.add_argument('-pDUT','--posDUT',help='DUT position in tracker default=3', action='store', default="3")
parser.add_argument('-pREF','--posREF',help='REF position in tracker default=1', action='store', default="1")
parser.add_argument('-cDUT','--channelDUT',help='channel of DUT defaut=2', action='store', default="4")
parser.add_argument('-cREF','--channelREF',help='channel of REF defaut=1', action='store', default="1")
parser.add_argument('-s','--selFiles',help='limit in the number of files to analyze defalut=all', action='store', default="all")
parser.add_argument('-n','--name',help='put a name for the SignalScope object if you want', action='store', default="test")
parser.add_argument('-w','--writecsv',help='Disable the csv results writing', action='store', default="1")
parser.add_argument('-po','--polya',help='Disable the complex polya fit', action='store', default="0")
parser.add_argument('-deb','--debugBad',help='Enable some prints for debugging the bad signals', action='store', default=None)
parser.add_argument('-os','--oscilloscope',help='Number of the oscilloscope to use deafult 2', action='store',default="2")

args = parser.parse_args()

#get the run number from path
run_num=args.run
run_path=base_path+"Runs/Pool"+str(args.oscilloscope)+"/Run"+run_num+"/"
result_path=result_path+run_num+"-Pool"+args.oscilloscope+"-CDut"+args.channelDUT+"-CRef"+args.channelREF+"/"
#check the active channels
print(run_path)
files=next(os.walk(run_path))[2]
files=[f for f in files if '.trc' in f]
print("################Analysing Run"+run_num+"################")

#check if folder exist, if not create it
if not os.path.isdir(result_path):
    os.makedirs(result_path)

main=ROOT.TFile(result_path+"/Waves_Run_"+run_num+".root","RECREATE")#root file creation
#main=ROOT.TFile("Run_"+run_num+".root","RECREATE")#root file creation
if args.batch is None: ROOT.gROOT.SetBatch(True)
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

files_DUT.sort()
files_REF.sort()
files_trk.sort()

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
# 8-->PosStd
# 9-->amplitude fit
# 10-->sigma fit
# 11-->average fit
# 12-->risetime
"""
data,dataDUT,dataREF, notReco,badDUT, badREF=[],[],[],[],[],[]

#get the tracking info once so you don't have to open every time the dataframe
#last row is shitty drop it
df=pd.read_csv(trk_path+"asciiRun"+str(run_num)+".dat", sep="\t", skipfooter=1,skiprows = 1, engine='python', header=None)
#we need to get the first column for event counter then the 3+3*pos, 3+3*pos+1
#where pos is the position of the detector usually 1 for MCP and changing for the DUT (MM#)
track_info=df[[df.columns[0], df.columns[3+3*int(args.posREF)],df.columns[3+3*int(args.posREF)+1], df.columns[3+3*int(args.posDUT)],df.columns[3+3*int(args.posDUT)+1]]]
track_info=track_info.set_index(track_info.columns[0])

#OLD without tracker position
#track_info=df[[df.columns[0], "X"+args.channelREF+" ","Y"+args.channelREF+" ", "X"+args.channelDUT+" ","Y"+args.channelDUT+" "]]
#track_info=track_info.set_index(track_info.columns[0])
test0R,test1R,test2R=[],[],[]
test0D,test1D,test2D=[],[],[]
track_info=track_info.rename(columns={track_info.columns[0]: 'xREF', track_info.columns[1]: 'yREF',track_info.columns[2]: 'xDUT', track_info.columns[3]: 'yDUT'})
#print(track_info)
main.mkdir("RawWaveforms/DUT/Fit")
main.mkdir("RawWaveforms/REF/Fit")
main.mkdir("RawWaveforms/DUT/Signal")
main.mkdir("RawWaveforms/REF/Signal")
main.mkdir("RawWaveforms/TRK")
print("Analyzing")
for i in tqdm.tqdm(range(len(wavesDUT))):
    track=wf.EventIDSignal(waves_trk[i]["T"],waves_trk[i]["V"],"track_"+args.name+str(i))
    if i <10:
        main.cd("RawWaveforms/TRK")
        track.WaveGraph(write=True)
    if args.draw is not None:
        main.cd("RawWaveforms/TRK")
        track.WaveGraph(write=True)
    #get coordniates and discaard the non resctostruded events
    if track.ID not in track_info.index and 1:
        notReco.append(i)
        continue
    else:
        signalDUT=wf.ScopeSignalCividec(wavesDUT[i]["T"],wavesDUT[i]["V"],"DUT_"+args.name+str(i),thresPosStd=5E-3, badDebug=args.debugBad)
        signalREF=wf.ScopeSignalCividec(wavesREF[i]["T"],wavesREF[i]["V"],"REF_"+args.name+str(i), UseDeriv=False, badDebug=args.debugBad)
        if args.draw is not None or i<50:# and signalDUT.badSignalFlag==False:
            main.cd("RawWaveforms/DUT/Signal")
            signalDUT.WaveSave(EpeakLines=True,Write=True,Zoom=True)
            #wf.DerivSignal(signalDUT).WaveSave(EpeakLines=True,Write=True,Zoom=True)
            main.cd("RawWaveforms/REF/Signal")
            signalREF.WaveSave(EpeakLines=True,Write=True,Zoom=True)
            #fit
            main.cd("RawWaveforms/DUT/Fit")
            signalDUT.SigmoidFit(write=True)
            main.cd("RawWaveforms/REF/Fit")
            signalREF.SigmoidFit(write=True)
        #check if signal is bad
        if signalDUT.badSignalFlag==True:
            badDUT.append(i)
            """
            print(i)
            main.cd("RawWaveforms/DUT/Signal")
            signalDUT.WaveSave(EpeakLines=True,Write=True,Zoom=True)
            main.cd("RawWaveforms/DUT/Fit")
            signalDUT.SigmoidFit(write=True)
            """
            continue
        elif signalREF.badSignalFlag==True:
            badREF.append(i)
            continue
        #else:
        data.append([i,track_info["xDUT"][track.ID],track_info["yDUT"][track.ID], signalDUT.baseLine, signalDUT.EpeakCharge, -1*signalDUT.Ampmin, signalDUT.SigmaOutNoise, signalDUT.PosStd,signalDUT.fit.GetParameter(0),signalDUT.fit.GetParameter(1),signalDUT.fit.GetParameter(2),signalDUT.fit.GetChisquare()/signalDUT.fit.GetNDF(),signalDUT.risetime,
                    track_info["xREF"][track.ID],track_info["yREF"][track.ID], signalREF.baseLine, signalREF.EpeakCharge, -1*signalREF.Ampmin, signalREF.SigmaOutNoise, signalREF.PosStd,signalREF.fit.GetParameter(0),signalREF.fit.GetParameter(1),signalREF.fit.GetParameter(2),signalREF.fit.GetChisquare()/signalREF.fit.GetNDF(),signalREF.risetime])
        #TEST
        testD=signalDUT.SigmoidFit(test=True)
        testR=signalREF.SigmoidFit(test=True)
        test0D.append(testD[0])
        test1D.append(testD[1])
        test2D.append(testD[2])
        test0R.append(testR[0])
        test1R.append(testR[1])
        test2R.append(testR[2])

main.cd()
hist(test0D,"par0D")
hist(test1D,"par1D")
hist(test2D,"par2D")
hist(test0R,"par0R")
hist(test1R,"par1R")
hist(test2R,"par2R")

"""
#OLD
cols=["X","Y","noise","echarge","amplitude","sigma","risetime","SAT","PosStd"]
dataDUT.append([track_info["xDUT"][track.ID],track_info["yDUT"][track.ID], signalDUT.baseLine, signalDUT.EpeakCharge, -1*signalDUT.Ampmin, signalDUT.SigmaOutNoise,signalDUT.risetime,signalDUT.ArrivalTimeCFDFit(), signalDUT.PosStd])
dataREF.append([track_info["xREF"][track.ID],track_info["yREF"][track.ID], signalREF.baseLine, signalREF.EpeakCharge, -1*signalREF.Ampmin, signalREF.SigmaOutNoise,signalREF.risetime,signalREF.ArrivalTimeCFDFit(), signalREF.PosStd])
"""
"""
if args.draw=="1":# and signalDUT.badSignalFlag==False:
    print(i)
    main.cd("RawWaveforms/DUT/Fit")
    signalDUT.SigmoidFit(write=True)
    main.cd("RawWaveforms/REF/Fit")
    signalREF.SigmoidFit(write=True)
"""
print("Fraction of NOTRECO bad events:",len(notReco)/len(wavesDUT))
print("Fraction of DUT bad events:",len(badDUT)/(len(wavesDUT)-len(notReco)))
print("Fraction of REF bad events:",len(badREF)/(len(wavesDUT)-len(notReco)))
print("Fraction of remaining events:",1-((len(badDUT)-len(badREF))/(len(wavesDUT))))
#print(notReco)
#print(badDUT)
#print(badREF)

main.Close()
#reopen the file with uproot to write the ttree tabular
file=uproot.recreate(result_path+"/Raw_Run_"+run_num+".root")

cols=["original index","XDUT","YDUT","noiseDUT","echargeDUT","amplitudeDUT","sigmaDUT","PosStdDUT","sigmoid ampltitudeDUT","sigmoid sigmaDUT","sigmoid meanDUT","Chi2RedDUT","risetimeDUT","XREF","YREF","noiseREF","echargeREF","amplitudeREF","sigmaREF","PosStdREF","sigmoid ampltitudeREF","sigmoid sigmaREF","sigmoid meanREF","Chi2RedREF","risetimeREF"]


dfDUT = pd.DataFrame(data,columns=cols)

file["Tree"]=dfDUT

gc.collect()