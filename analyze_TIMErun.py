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
parser.add_argument('-w','--writecsv',help='any value will disable the csv results writing, default None', action='store', default=None)

args = parser.parse_args()

#get the run number from path
run_num=args.run
run_path=run_path+run_num+"/"
result_path=result_path+run_num+"/"

INfile = uproot.open(result_path+"/Raw_Run_"+run_num+".root")
df=INfile["Tree"].arrays(library="pd")

filteredDF=df

#cut on sigmoid mean
#filteredDF=df[df["sigmoid meanDUT"]<240E-9]
filteredDF=filteredDF.drop(filteredDF[filteredDF["sigmoid meanDUT"]<210E-9].index)
filteredDF=filteredDF.drop(filteredDF[filteredDF["sigmoid meanDUT"]>240E-9].index)


#cut on risetime
filteredDF=filteredDF.drop(filteredDF[filteredDF["risetimeDUT"]>0.8E-9].index)
filteredDF=filteredDF.drop(filteredDF[filteredDF["risetimeDUT"]<0.5E-9].index)


#cut on amplitude
#filteredDF=filteredDF.drop(filteredDF[filteredDF["amplitudeDUT"]<15E-3].index)


#geometric cut
DUTx_m,DUTy_m=np.mean(filteredDF["XDUT"]),np.mean(filteredDF["YDUT"])
filteredDF=filteredDF.drop(filteredDF[   (filteredDF["XDUT"]-DUTx_m)**2+(filteredDF["YDUT"]-DUTy_m)**2>4   ].index)

#filteredDF=filteredDF[(df["XDUT"]-DUTx_m)**2+(df["YDUT"]-DUTy_m)**2<5]


f=0.2
Ddut=np.mean(filteredDF["risetimeDUT"])*(1-f)
Dref=np.mean(filteredDF["risetimeREF"])*(1-f)
#Dref, Ddut=0.5E-9,0.5E-9
#print(Dref, Ddut)

satDUT=-filteredDF["sigmoid sigmaDUT"]*np.log( ((1/f)-1) / ( np.exp(Ddut/filteredDF["sigmoid sigmaDUT"]) - (1/f) )  )+filteredDF["sigmoid meanDUT"]
satREF=-filteredDF["sigmoid sigmaREF"]*np.log( ((1/f)-1) / ( np.exp(Dref/filteredDF["sigmoid sigmaREF"]) - (1/f) )  )+filteredDF["sigmoid meanREF"]

times=satREF-satDUT
filteredDF=filteredDF.assign(satDUT=satDUT, satREF=satREF,particleTime=times)

#drop nan from sat calculation
filteredDF=filteredDF.dropna()

mean=np.mean(times)
#cut on sat +/- 400ps
filteredDF=filteredDF.drop(filteredDF[   filteredDF["particleTime"]<mean-3E-10   ].index)
filteredDF=filteredDF.drop(filteredDF[   filteredDF["particleTime"]>mean+3E-10   ].index)


print(np.mean(filteredDF["particleTime"]),np.std(filteredDF["particleTime"]))
OUTfile=uproot.recreate(result_path+"/Filtered_Run_"+run_num+".root")
OUTfile["Tree"]=filteredDF

if args.writecsv is None:
    f = open(csv_path+"resultsTIME.csv", "a")
    #print(csv_path+"resultsTIME.csv")
    #Run NUM;RUN TYPE;MEAN RISETIME;ARITMETIC MEAN AMPLITUDE;AMPLITUDE FIT;ERR AMPLITUDE;CHI2/NDF;survived Waves from cuts
    f.write(str(run_num)+";"+"TIME"+";"+str(np.mean(filteredDF["amplitudeDUT"]))+";"+str(np.mean(filteredDF["risetimeDUT"]))+";"+str(np.std(filteredDF["particleTime"]))+";"+str(wf.GetStdErr(filteredDF["particleTime"]))+"\n")
    f.close()
gc.collect()