#!/usr/bin/python3
import  os
import lecroyparser
import re
from array import array
import ROOT
import numpy as np
import pandas as pd
from scipy import fftpack
from scipy import signal
from tqdm import tqdm
import math as m

#from physlibs.root import functions

"""
to get the maximum fht electron peak derivative and average in made to get the zero crossing point
this is made in the function and is not using the methods Average() and Derivative()
"""

def GetCFDTimeGenLogistic(f,D,par,start=200E-9,stop=250E-9):
    x=np.arange(start,stop,2E-12)#2ps step
    fdel=(par[0]/(1+ np.exp(-(x-par[2]-D)/par[1]))**par[3])
    finverse=-f*(par[0]/(1+ np.exp(-(x-par[2])/par[1]))**par[3])
    yCFD=fdel+finverse
    """
    #for testing
    graph(x,fdel,"time(s)","delayed")
    graph(x,finverse,"time(s)","inverse")
    graph(x,yCFD,"time(s)","sum")
    """
    tarr=0
    for i in range(len(yCFD)-1):
        if yCFD[i]>0 and yCFD[i+1]<0:
            tarr=(x[i]+x[i+1])/2
    if tarr==0:
        print("Not able to find zero crossing")
        tarr=float('nan')
    return tarr



def grapherr(x,y,ex,ey,x_string, y_string, color=4, markerstyle=22, markersize=1):
        plot = ROOT.TGraphErrors(len(x),  np.array(x  ,dtype="d")  ,   np.array(y  ,dtype="d") , np.array(   ex   ,dtype="d"),np.array( ey   ,dtype="d"))
        plot.SetNameTitle(y_string+" vs "+x_string,y_string+" vs "+x_string)
        plot.GetXaxis().SetTitle(x_string)
        plot.GetYaxis().SetTitle(y_string)
        plot.SetMarkerColor(color)#blue
        plot.SetMarkerStyle(markerstyle)
        plot.SetMarkerSize(markersize)
        plot.Write()
        return plot

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

def fill_h(histo_name, array):
    for x in range (len(array)):
        histo_name.Fill((np.array(array[x] ,dtype="d")))

def nparr(list):
    return np.array(list, dtype="d")

def GetStdErr(arr):
    mean=np.mean(arr)
    std=np.std(arr)
    N=len(arr)
    D4=np.sum(np.square(np.square(arr-mean)))/N
    #print(D4)
    return np.sqrt( (D4-std**4)/(N-1) )/(2*std)

def find_nearestIdx(array, value):
    array = np.asarray(array)
    idx = (np.abs(array - value)).argmin()
    return idx

class ScopeSequence:
    def __init__(self, file, name, scopeImpedence=50, AmplifierGain=100,SampRate=10E9):
        self.name = name
        self.scopeImpedence = scopeImpedence
        self.AmplifierGain = AmplifierGain
        self.data = lecroyparser.ScopeData(file)
        self.horizInterval=self.data.horizInterval
        self.waveINsequence=self.data.parseInt32(144)

        self.all_lenght=len(self.data.x)
        self.time_base=self.timebaseSec(self.data.timeBase)#timebase in seconds
        self.div_num=10
        self.SampRate = format(1/self.horizInterval, '.3g')
        #self.waveINsequence=round(self.data.x[-1]/(self.time_base*10))
        #self.waveINsequence=int(self.data.x[-1]/(self.time_base*10))
        #self.pointsPERwave=round(self.time_base*self.div_num/self.data.horizInterval)
        self.pointsPERwave=int(self.all_lenght/self.waveINsequence)

    def timebaseSec(self,time_baseScope):
        """
        given the time base string ex:"20 ns/div"
        return the float in seconds
        """
        split=time_baseScope.split()
        num, unitStr=float(split[0]), split[1]
        if unitStr[0]=="n":
            unit=1E-9
        elif unitStr[0]=="u":
            unit=1E-6
        elif unitStr[0]=="m":
            unit=1E-3
        elif unitStr[0]=="s":
            unit=1.
        else:
            print("NO TIME UNIT DETECTED")
        return num*unit

    def GetWaves(self,cutINhalf=False):
        """
        return the unpacked waves
        """
        waves=[]
        for i in range(self.waveINsequence):
            df = pd.DataFrame({"T" : self.data.x[ self.pointsPERwave*i: self.pointsPERwave*(i+1)]- self.data.x[ self.pointsPERwave*i], "V" :  self.data.y[ self.pointsPERwave*i: self.pointsPERwave*(i+1)]})

            if cutINhalf==False:
                waves.append(df)
            else:
                waves.append(df.head(int(len(df.index)/2)))

        return waves

class TimeAnal:
    """
    takes the two sigmoid TF1 from teh waves and get the arrival times and time difference
    no correction here
    """
    def __init__(self, TF1ref, TF1dut, nameref, namedut):
        self.TF1Ref=TF1ref
        self.TF1Ref.SetRange(self.TF1Ref.GetXmin(), 2*self.TF1Ref.GetXmax())
        self.TF1Dut=TF1dut
        self.TF1Dut.SetRange(self.TF1Dut.GetXmin(), 2*self.TF1Dut.GetXmax())
        self.nameRef=nameref
        self.nameDut=namedut
        self.name=nameref+"VS"+nameref

        self.ArrivalLERef,self.ArrivalLEDut=self.ArrivalTimeLE()

    def GetInverseSigmoid(self):
        #Aref=self.TF1ref.GetParameter(0)
        #muref=self.TF1ref.GetParameter(1)
        #sigmaref=self.TF1ref.GetParameter(2)
        inverseRef=ROOT.TF1("inverseRef", "[2]*log(([0]/x)-1)+[1]",self.TF1Ref.GetXmin(), self.TF1Ref.GetXmax())
        inverseRef.SetParameters(self.TF1Ref.GetParameter(0),self.TF1Ref.GetParameter(1),self.TF1Ref.GetParameter(2))
        inverseDut=ROOT.TF1("inverseDut", "[2]*log(([0]/x)-1)+[1]",self.TF1Dut.GetXmin(), self.TF1Dut.GetXmax())
        inverseDut.SetParameters(self.TF1Dut.GetParameter(0),self.TF1Dut.GetParameter(1),self.TF1Dut.GetParameter(2))
        return [inverseRef,inverseDut]

    def ArrivalTimeLE(self,threshold=0.2):#threshold is the fraction respect to the maxium
        thRef=threshold*self.TF1Ref.GetParameter(0)
        thDut=threshold*self.TF1Dut.GetParameter(0)
        [inverseRef,inverseDut]=self.GetInverseSigmoid()
        return [inverseRef.Eval(thRef),inverseDut.Eval(thDut)]

    def GetNegative(self, fraction=0.2):
        negRef=ROOT.TF1("negRef", "([0]/(1+ exp(-(x-[2])/[1])))",self.TF1Ref.GetXmin(), self.TF1Ref.GetXmax())
        negRef.SetParameters(-1*fraction*self.TF1Ref.GetParameter(0),self.TF1Ref.GetParameter(1),self.TF1Ref.GetParameter(2))
        negDut=ROOT.TF1("negDut", "([0]/(1+ exp(-(x-[2])/[1])))",self.TF1Dut.GetXmin(), self.TF1Dut.GetXmax())
        negDut.SetParameters(-1*fraction*self.TF1Dut.GetParameter(0),self.TF1Dut.GetParameter(1),self.TF1Dut.GetParameter(2))
        return [negRef, negDut]

    def CFD(self, fraction=0.2,delay=1E-9, RTmult=2):
        delay=RTmult*[self.TF1Ref.GetParameter(1),self.TF1Dut.GetParameter(1)]
        xmax=0.8*self.TF1Dut.GetXmax()
        xmin=0.8*self.TF1Dut.GetXmin()
        par0=self.TF1Dut.GetParameter(0)
        par1=self.TF1Dut.GetParameter(1)
        par2=self.TF1Dut.GetParameter(2)

        c=ROOT.TCanvas(str(i),str(i))
        #negative
        negDut=ROOT.TF1("negDut", "([0]/(1+ exp(-(x-[2])/[1])))",xmin,xmax)
        negDut.SetParameters(-1*fraction*par0,par1,par2)
        negDut.SetLineColor(2)
        negDut.Draw()
        negDut.SetMaximum(5E-3)
        negDut.SetMinimum(-1.2E-2)
        #self
        selfDut=ROOT.TF1("selfDut", "([0]/(1+ exp(-(x-"+str((i/10)*delay[1])+"-[2])/[1])))",xmin,xmax)
        selfDut.SetParameters(par0,par1,par2)
        selfDut.SetLineColor(3)
        selfDut.Draw("SAME")
        c.Update()
        #sum
        sumDut=ROOT.TF1("sumDut", "([0]/(1+ exp(-(x-"+str((i/10)*delay[1])+"-[2])/[1])))+("+str(-1*fraction)+"*[0]/(1+ exp(-(x-[2])/[1])))",xmin,xmax)
        sumDut.SetParameters(par0,par1,par2)
        sumDut.SetLineColor(4)
        sumDut.Draw("SAME")
        c.Write()

class ScopeSignalCividec:
    def __init__(self, x, y, name, scopeImpedence=50, AmplifierGain=100,kernel_size=100, edge_order=2,sigma_thr=2, sigma=5,thresPosStd=None,risetimeCut=None, UseDeriv=True, badDebug=None):
        self.badSignalFlag = False

        self.name = name
        self.noiseHisto = None

        self.scopeImpedence = scopeImpedence
        self.AmplifierGain = AmplifierGain

        self.badDebug=badDebug

        self.sampling = round(x[1]-x[0],15)#round on femtosecond
        self.x=nparr(x)
        self.y=nparr(y)
        self.samples=len(x)
        self.timeMax=self.x[-1]

        #find peak (needed for get the noise)
        self.Ampmin, self.AmpminIdx=self.GetAmplitudeMin()
        self.tFitMax=self.x[self.AmpminIdx]

        if self.tFitMax>250E-9 or self.tFitMax<200E-9:
            self.badSignalFlag = True
            if badDebug is not None: print("bad becasue peak is not in [200,250]ns (noise)")

        #get noise
        self.baseLine=self.GetMeanNoise()
        self.baseLineStd=self.GetStdNoise()
        self.SigmaOutNoise=np.abs(self.Ampmin-self.baseLine)/self.baseLineStd

        if self.SigmaOutNoise<sigma:
            self.badSignalFlag = True
            if badDebug is not None: print("bad from sigmaOutNoise (noise)")

        #check if flicker noise is present
        PosPoints=[p for p in self.y[self.y>0]]
        if len(PosPoints)<1:
            self.PosStd=10
        else:
            self.PosStd=np.std(PosPoints)

        if thresPosStd is not None and self.PosStd>=thresPosStd:
            self.badSignalFlag = True
            if badDebug is not None: print("bad from PositiveStd")

        self.y=self.y-self.baseLine #baseline correction
        #get again the peak (probably not needed)
        self.Ampmin, self.AmpminIdx=self.GetAmplitudeMin()

        #derivation
        y=np.gradient(self.y, edge_order)
        #averaging
        kernel = np.ones(kernel_size) / kernel_size
        self.DerivAv= np.convolve(y, kernel, mode='same')

        #start and stop of epeak
        self.Epeakmin, self.EpeakminIdx=self.GetEpeakMin()
        self.tFitMin=self.x[self.EpeakminIdx]
        if UseDeriv==True:
            self.Epeakmax, self.EpeakmaxIdx=self.GetEpeakMax_fromDerivative()
        else:
            self.Epeakmax, self.EpeakmaxIdx=self.GetEpeakMax(sigma=sigma_thr)

        self.Integral=(np.sum(self.y)/self.AmplifierGain)*(self.scopeImpedence*self.sampling)
        self.EpeakCharge, self.Gain=self.GetGain()

        self.risetime= self.RiseTimeData()
        self.fit=self.SigmoidFit()

        self.risetime=self.RiseTimeFit()
        
        #risetime
        self.risetime= self.RiseTimeData()
        if risetimeCut is not None and (self.risetime<risetimeCut[0] or self.risetime>risetimeCut[1]):
            self.badSignalFlag = True
            if badDebug is not None: print("bad from risetimeCut")

        """
        if fit==True:
            self.sat=self.ArrivalTimeCFDFit()
            #if nan is returned the CFD is out of domain
            #DOMAIN IS:
            #sigma<=Delay/(ln(1/fraction))
            if m.isnan(self.sat):
                self.badSignalFlag = True
                if badDebug is not None: print("bad beacuse of NaN in SAT")
            if satcut is not None and (self.sat<satcut[0] or self.sat>satcut[1]):
                self.badSignalFlag = True
                if badDebug is not None: print("bad from satCut")
        """
    def isBad(self):
        self.badSignalFlag = True

    def __str__(self):
        return self.GetName()

    def GetGain(self, pe=1):
        charge=-1*(np.sum(self.y[self.EpeakminIdx:self.EpeakmaxIdx])/(self.AmplifierGain*self.scopeImpedence))*self.sampling
        return [charge, charge/(pe*1.6e-19)]

    def GetName(self):
        #return self.scopeFile.split('/')[-1].replace('.trc', '')
        return self.name

    def WaveGraph(self, color=4, markerstyle=22, markersize=1, write=False):
        plot = ROOT.TGraph(len(self.x),  np.array(self.x  ,dtype="d")  ,   np.array(self.y  ,dtype="d"))
        plot.SetNameTitle(self.name,self.name)
        plot.GetXaxis().SetTitle("Time(s)")
        plot.GetYaxis().SetTitle("Voltage(V)")
        plot.SetMarkerColor(color)#blue
        plot.SetMarkerStyle(markerstyle)
        plot.SetMarkerSize(markersize)
        if write==True: plot.Write()
        return plot

    def WaveSave(self, size=500, leftmargin=0.17, rightmargin=0.1, EpeakLines=False,Write=False,Zoom=False, Save=False):
        plot=self.WaveGraph()
        y_name=plot.GetYaxis().GetTitle()
        x_name=plot.GetXaxis().GetTitle()
        can1=ROOT.TCanvas(self.name, self.name, size, size)
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
        if Zoom==True:
            plot.GetXaxis().SetRangeUser(0.8*self.Epeakmin, 2*self.Epeakmax)
        plot.Draw("AP")
        if EpeakLines==True:
            can1.Update()
            ymax=ROOT.gPad.GetUymax()
            ymin=ROOT.gPad.GetUymin()
            line=ROOT.TLine(self.Epeakmin,ymin,self.Epeakmin,ymax)
            line.SetLineColor(2)
            line.SetLineWidth(2)
            line.Draw("SAME")
            line1=ROOT.TLine(self.Epeakmax,ymin,self.Epeakmax,ymax)
            line1.SetLineColor(3)
            line1.SetLineWidth(2)
            line1.Draw("SAME")
            line2=ROOT.TLine(self.tFitMax,ymin,self.tFitMax,ymax)
            line2.SetLineColor(4)
            line2.SetLineWidth(2)
            line2.Draw("SAME")
            p=ROOT.TPaveText(.5,.8,.9,.9,"NDC")
            p.AddText("Min peak")
            p.AddText("Max peak")
            p.AddText("Peak")
            p.SetFillStyle(0);

            t1,t2,t3 = ROOT.TText(),ROOT.TText(),ROOT.TText()
            t1=p.GetLineWith("Min")
            t1.SetTextColor(2)
            t2=p.GetLineWith("Max")
            t2.SetTextColor(3)
            t3=p.GetLineWith("Peak")
            t3.SetTextColor(4)

            p.Draw("SAME")
        if Write==True: can1.Write()
        if Save==True: can1.SaveAs("./signals/"+self.name+".png")
        return can1

    def GetAmplitudeMin(self):
        return [np.min(self.y),np.argmin(self.y)]

    def RiseTimeData(self):
        return self.tFitMax-self.tFitMin

    def RiseTimeFit(self,b=1):
        fit=self.fit
        inverse=self.GetInverseSigmoid(self.fit.GetParameter(0),self.fit.GetParameter(1),self.fit.GetParameter(2),b)
        start=inverse.Eval(0.1*self.fit.GetParameter(0))
        stop=inverse.Eval(0.9*self.fit.GetParameter(0))
        return stop-start

    def GetNoiseList(self,fraction=0.8):
        """
        get the list of the noise before the signal
        between the start and a fraction of the min time
        """
        return self.y[self.x<fraction*self.tFitMax]

    def GetMeanNoise(self, minnoise=1E-5):
        all_noise=self.GetNoiseList()
        if len(all_noise)<=1:
            n=minnoise
        else:
            n=np.mean(nparr(all_noise))
        return n

    def GetErrNoise(self):
        noise=nparr(self.GetNoiseList())
        if len(noise)<=1:
            n=1E-20
        else:
            n=np.std(noise)/np.sqrt(len(noise))
        return n

    def GetStdNoise(self,minstd=1-5):
        noise=nparr(self.GetNoiseList())
        if len(noise)<=1:
            std=minstd
        else:
            std=np.std(noise)
        if std==0.: std=minstd
        return std

    def GetNoiseHisto(self):
        if self.noiseHisto: return self.noiseHisto
        noise = self.GetNoiseList()
        self.noiseHisto = ROOT.TH1F('noiseHisto_'+self.GetName(), ';Amplitude (V);Counts', 100, 0.99*min(noise), 1.01*max(noise))
        for i,v in enumerate(self.y):
            self.noiseHisto.Fill(v)
        return self.noiseHisto

    def GetEpeakMin(self, sigma=3):
        """
        return the time of the start of the electron peak
        """
        min=self.Ampmin
        tFitMax=self.tFitMax
        sub_y=self.y[self.x<tFitMax]
        sub_x=self.x[self.x<tFitMax]
        mean=self.baseLine
        std=self.baseLineStd
        x_peak = 0
        i=0
        for i in range(1,len((sub_y))-1):
            if np.abs(sub_y[-i])<(sigma*std):
                x_peak=sub_x [-i]
                break
            else:
                continue
        #if x_peak==0: self.isBad()
        #if self.badDebug is not None: print("bad from not finding the epeak Min")
        return [x_peak,len(sub_y)-i]

    def GetEpeakMax(self, sigma=2):
            """
            return the time of the stop of the electron peak
            with discrimator
            """
            min=self.Ampmin
            tFitMax=self.tFitMax
            offseti=len(self.y[self.x<=tFitMax])
            sub_y=self.y[self.x>tFitMax]
            sub_x=self.x[self.x>tFitMax]
            std=self.baseLineStd
            x_peak = 0
            i=0
            for i in range(len((sub_y))):
                if np.abs(sub_y[i])<(sigma*std):
                    x_peak=sub_x[i]
                    break
                else:
                    continue
            #if x_peak==0: self.isBad()
            #if self.badDebug is not None: print("bad from not finding the epeak Max")
            return [x_peak,offseti+i]

    def GetEpeakMax_fromDerivative(self,window=20):
        """
        return the time of the stop of the electron peak
        currently working fine with derivative Av100
        looking only in window=20ns after electorn peak
        """
        max_samp=round(window*1E-9/self.sampling)
        start=self.EpeakminIdx
        max=0
        tmax=0
        for i in range(max_samp):
            if start+i==self.samples-1:#if the cose is going out the acquired time window
                max=self.DerivAv[start+i]
                tmax=start+i
                #self.isBad()
                #if self.badDebug is not None: print("bad from not finding the epeak Max")

                break
            if self.DerivAv[start+i]>=max:
                max=self.DerivAv[start+i]
                tmax=start+i
            else:
                continue
        return [self.x[tmax],tmax]

    """
    NOT NEEDED
    def Average(self,kernel_size=100):
        kernel = np.ones(kernel_size) / kernel_size
        data_convolved = np.convolve(self.y, kernel, mode='same')
        return ScopeSignal(self.x, data_convolved, str(kernel_size)+"Av_"+self.name)

    NOT NEEDED
    def GetDerivative(self, edge_order=2):
        y=np.gradient(self.y, edge_order)
        return ScopeSignal(self.x, y, "Derivative_"+self.name)
    """

    def SigmoidFit(self,mult1=6.7, mult2=2,test=False,write=False,LeftPoints=25,RightPoints=0):
        start0=self.Ampmin
        start1=self.risetime/mult1
        start2=(self.tFitMax+self.tFitMin)/mult2

        sigmoid=ROOT.TF1("sigmoid", "([0]/(1+ exp(-(x-[2])/[1])))",self.tFitMin-(LeftPoints*self.sampling),self.tFitMax+(RightPoints*self.sampling))
        sigmoid.SetParameters(start0, start1, start2)
        #sigmoid.FixParameter(0,start0)
        #sigmoid.SetParLimits(0,0.9*start0,1.1*start0)
        #sigmoid.SetParLimits(1,0.1*start1,10*start1)
        #sigmoid.FixParameter(2,start2)
        #sigmoid.SetParLimits(2,0.9*start2,1.1*start2)
        plot=self.WaveGraph()
        plot.Fit("sigmoid","RQ","r")
        plot.Fit("sigmoid","RQ","r")
        plot.Fit("sigmoid","RQ","r")
        plot.Fit("sigmoid","RQ","r")
        #print(self.risetime/4/sigmoid.GetParameter(1))
        if write==True: plot.Write()
        if test==True:
            return [start0/sigmoid.GetParameter(0),start1/sigmoid.GetParameter(1), start2/sigmoid.GetParameter(2)]
        else:
            return sigmoid

    def GenSigmoidFit(self,mult1=6.7, mult2=2,test=False,write=False,LeftPoints=25,RightPoints=0):
        start0=self.Ampmin
        start1=self.risetime/mult1
        start2=(self.tFitMax+self.tFitMin)/mult2
        start3=1

        sigmoid=ROOT.TF1("sigmoid", "([0]/(1+ exp(-(x-[2])/[1]))^[3])",self.tFitMin-(LeftPoints*self.sampling),self.tFitMax+(RightPoints*self.sampling))
        sigmoid.SetParameters(start0, start1, start2,start3)
        #sigmoid.FixParameter(0,start0)
        #sigmoid.SetParLimits(0,0.9*start0,1.1*start0)
        #sigmoid.SetParLimits(1,0.1*start1,10*start1)
        #sigmoid.FixParameter(2,start2)
        #sigmoid.SetParLimits(2,0.9*start2,1.1*start2)
        plot=self.WaveGraph()
        plot.Fit("sigmoid","RQ","r")
        #print(self.risetime/4/sigmoid.GetParameter(1))
        if write==True: plot.Write()
        if test==True:
            return [start0/sigmoid.GetParameter(0),start1/sigmoid.GetParameter(1), start2/sigmoid.GetParameter(2), start3/sigmoid.GetParameter(3)]
        else:
            return sigmoid

    def ArrivalTimeLESignal(self, threshold=0.2):
        x=self.x[self.EpeakminIdx:self.AmpminIdx]
        y=self.y[self.EpeakminIdx:self.AmpminIdx]
        for i in range(len(x)):
            if y[i]<=threshold*self.Ampmin:
                tarr=x[i]
                break
            else:
                continue
        return tarr

    def GetInverseSigmoid(self,A,mu,sigma,b=1):
        inverse=ROOT.TF1("inverse", "-[1]*log(([0]/x)**(1/[3])-1)+[2]",self.Ampmin,0)
        inverse.SetParameters(A,mu,sigma,b)
        return inverse

    def GetInverseGenSigmoid(self,A,mu,sigma,exp):
        inverse=ROOT.TF1("inverse", "-[1]*log(([0]/x)**(1/[3])-1)+[2]",self.Ampmin,0)
        inverse.SetParameters(A,mu,sigma,exp)
        return inverse

    def ArrivalTimeLEFit(self, threshold=0.2):
        inverse=self.GetInverseSigmoid()
        thr=threshold*inverse.GetParameter(0)
        return inverse.Eval(thr)

    def GetSignalCFDSignal(self, fr=0.2,dele=0.5E-9):
        indexDelay = int(dele/self.sampling)
        yAttenuated = -1*self.y*fr
        yDelayed = np.roll(self.y, indexDelay)
        yCFD = yAttenuated+yDelayed
        return yCFD

    def ArrivalTimeCFDSignal(self, window=10,fraction=0.2, delay=0.5E-9):
        """
        Not working fine
        IF OUTPUT IS 0 THE METHOD DIN'T FIND ANY ZERO CROSSING
        window is in nanosecods
        """
        yCFD=self.GetSignalCFDSignal(fr=fraction, dele=delay)
        max_samp=round(window/self.sampling)
        yCFDcut=yCFD[self.EpeakminIdx:self.EpeakminIdx+max_samp]
        xcut=self.x[self.EpeakminIdx:self.EpeakminIdx+max_samp]
        tarr=0
        #print(len(yCFDcut))
        for i in range(len(yCFDcut)):
            if yCFDcut[i]>=0 and yCFDcut[i+1]<0:
                tarr=xcut[i]
                break
            else:
                continue
        return tarr

    def ArrivalTimeCFDFit(self, fraction=0.2,delay=1E-9):
        """
        Analytially find the zero crossing of the CFD
        """
        FitFunc=self.SigmoidFit(test=False,write=False)
        sigma=FitFunc.GetParameter(1)
        f=fraction
        D=delay
        mu=FitFunc.GetParameter(2)
        try: sat=-sigma*np.log( ((1/f)-1) / ( m.exp(D/sigma) - (1/f) )  )+mu
        except: pass
        return sat

    def FindParCFD(self, fraction, delay, sigma, mu):
        """
        use this to find the best aprametrs for CFD
        """
        f=fraction
        D=delay# *1E-9
        return -sigma*np.log( ((1/f)-1) / ( m.exp(D/sigma) - (1/f) )  )+mu
    #FFT
    def GetFFT(self,tmin,tmax):
        tempt,tempy = self.x[self.x>=tmin], -1*self.y[self.x>=tmin]
        t,y = tempt[tempt<=tmax], tempy[tempt<=tmax]
        timestep = self.sampling
        yf = fftpack.fft(y)
        xf = fftpack.fftfreq(len(t), d=timestep)
        return xf[xf>0], np.abs(yf)[xf>0]

    def GetPowerSpectrum(self,tmin,tmax, fcut=None):
        xf, yfft = self.GetFFT(tmin,tmax)
        xf, yf = xf[xf>0], np.log10(np.abs(yfft)**2)[xf>0]
        if fcut is not None: xf, yf = xf[xf<fcut], yf[xf<fcut]
        return xf, yf

    def FreqFilter(self, freqmin=None, freqmax=None):
        sample_freq, sig_fft = self.GetFFT()
        filtered_freq = sig_fft.copy()
        if freqmax is not None: filtered_freq[np.abs(sample_freq) > freqmax] = 0
        if freqmin is not None: filtered_freq[np.abs(sample_freq) < freqmin] = 0
        filtered_sig = fftpack.ifft(filtered_freq)
        return self.x, filtered_sig

class ScopeSignalSlow:
    def __init__(self, x, y, name, scopeImpedence=50, AmplifierGain=100,sigma_thr=2, sigmaBad=5, risetimeCut=None, badDebug=None, EpeakBadDisable=False):
        self.badSignalFlag = False

        self.badDebug=badDebug
        self.EpeakBadDisable=EpeakBadDisable

        self.name = name
        self.noiseHisto = None

        self.scopeImpedence = scopeImpedence
        self.AmplifierGain = AmplifierGain

        self.sampling = round(x[1]-x[0],15)#round on femtosecond
        self.x=nparr(x)
        self.y=nparr(y)
        self.samples=len(x)

        #derivation
        #y=np.gradient(self.y, edge_order)
        #averaging
        #kernel = np.ones(kernel_size) / kernel_size
        #self.DerivAv= np.convolve(y, kernel, mode='same')

        #find peak
        self.Ampmin, self.AmpminIdx=self.GetAmplitudeMin()
        self.tFitMax=self.x[self.AmpminIdx]
        #get noise
        self.baseLine=self.GetMeanNoise()
        self.baseLineStd=self.GetStdNoise()
        self.SigmaOutNoise=np.abs(self.Ampmin-self.baseLine)/self.baseLineStd

        if self.SigmaOutNoise<sigmaBad:
            self.badSignalFlag = True
            if badDebug is not None: print("bad because of sigma not out noise")

        self.y=self.y-self.baseLine #baseline correction
        #get again the peak (probably not needed)
        self.Ampmin, self.AmpminIdx=self.GetAmplitudeMin()
        #if negative (positive in origin) the signal is defentiley bad
        #just beacuse it was baseline subtracket
        if self.Ampmin>0:
            self.badSignalFlag = True
            if badDebug is not None: print("bad because of positive minimum")

        self.Epeakmin, self.EpeakminIdx=self.GetEpeakMin(sigma=sigma_thr)
        self.tFitMin=self.x[self.EpeakminIdx]
        self.Epeakmax, self.EpeakmaxIdx=self.GetEpeakMax(sigma=sigma_thr)
        #risetime 90 to 10 is not eprfect 
        if self.badSignalFlag==True:
            self.risetime= self.RiseTimeData()
        else:
            self.risetime=self.RiseTime1090()

        if risetimeCut is not None:
            if self.risetime<risetimeCut:
                self.badSignalFlag = True
                if badDebug is not None: print("bad because of risetime cut")

        #self.EpeakCharge, self.Gain=self.GetGain()

    def isBad(self):
        self.badSignalFlag = True

    def __str__(self):
        return self.GetName()

    def GetGain(self, pe=1):
        charge=-1*(np.sum(self.y[self.EpeakminIdx:self.EpeakmaxIdx])/(self.AmplifierGain*self.scopeImpedence))*self.sampling
        return [charge, charge/(pe*1.6e-19)]

    def GetName(self):
        #return self.scopeFile.split('/')[-1].replace('.trc', '')
        return self.name

    def WaveGraph(self, color=4, markerstyle=22, markersize=1, write=False):
        plot = ROOT.TGraph(len(self.x),  np.array(self.x  ,dtype="d")  ,   np.array(self.y  ,dtype="d"))
        plot.SetNameTitle(self.name,self.name)
        plot.GetXaxis().SetTitle("Time(s)")
        plot.GetYaxis().SetTitle("Voltage(V)")
        plot.SetMarkerColor(color)#blue
        plot.SetMarkerStyle(markerstyle)
        plot.SetMarkerSize(markersize)
        if write==True: plot.Write()
        return plot

    def WaveSave(self, size=800, leftmargin=0.17, rightmargin=0.1, EpeakLines=False,Write=False,Zoom=False, Save=False):
        plot=self.WaveGraph()
        y_name=plot.GetYaxis().GetTitle()
        x_name=plot.GetXaxis().GetTitle()
        can1=ROOT.TCanvas(self.name, self.name, size, size)
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
        if Zoom==True:
            plot.GetXaxis().SetRangeUser(0.8*self.Epeakmin, 2*self.Epeakmax)
        plot.SetMarkerSize(0.001)
        plot.SetLineColor(4)
        plot.Draw("ALP")
        if EpeakLines==True:
            can1.Update()
            ymax=ROOT.gPad.GetUymax()
            ymin=ROOT.gPad.GetUymin()
            line=ROOT.TLine(self.Epeakmin,ymin,self.Epeakmin,ymax)
            line.SetLineColor(2)
            line.SetLineWidth(2)
            line.Draw("SAME")
            line1=ROOT.TLine(self.Epeakmax,ymin,self.Epeakmax,ymax)
            line1.SetLineColor(3)
            line1.SetLineWidth(2)
            line1.Draw("SAME")
            line2=ROOT.TLine(self.tFitMax,ymin,self.tFitMax,ymax)
            line2.SetLineColor(4)
            line2.SetLineWidth(2)
            line2.Draw("SAME")
            p=ROOT.TPaveText(.5,.8,.9,.9,"NDC")
            p.AddText("Min peak")
            p.AddText("Max peak")
            p.AddText("Peak")
            p.SetFillStyle(0)

            t1,t2,t3 = ROOT.TText(),ROOT.TText(),ROOT.TText()
            t1=p.GetLineWith("Min")
            t1.SetTextColor(2)
            t2=p.GetLineWith("Max")
            t2.SetTextColor(3)
            t3=p.GetLineWith("Peak")
            t3.SetTextColor(4)

            p.Draw("SAME")
        if Write==True: can1.Write()
        if Save==True: can1.SaveAs(self.name+".png")
        return can1

    def GetAmplitudeMin(self):
        return [np.min(self.y),np.argmin(self.y)]

    def RiseTimeData(self):
        return self.tFitMax-self.tFitMin

    def RiseTime1090(self):
        #print("CULO",self.Ampmin)
        sub_y=self.y[self.x<=self.tFitMax]
        sub_x=self.x[self.x<=self.tFitMax]
        y10,y90=0.1*self.Ampmin, 0.9*self.Ampmin
        i=1
        while sub_y[-i]<=y90:
            i=i+1
        x90,y90found=sub_x[-i],sub_y[-i]
        i=1
        while sub_y[-i]<=y10:
            i=i+1

        x10,y10found=sub_x[-i],sub_y[-i]
        #print("to find",y10,y90)
        #print("found",y10found,y90found)
        #print("found+1",self.y[start-i])
        #print(x90,x10,self.tFitMax,self.tFitMin)
        return x90-x10

    def GetNoiseList(self,fraction=0.5):
        """
        get the list of the noise before the signal
        between the start and a fraction of the min time
        """
        #print(fraction*self.tFitMax)
        return self.y[self.x<fraction*self.tFitMax]

    def GetMeanNoise(self, minnoise=1E-5):
        all_noise=self.GetNoiseList()
        #print(all_noise)
        if len(all_noise)<=1:
            n=minnoise
        else:
            n=np.mean(nparr(all_noise))
        return n

    def GetErrNoise(self):
        noise=nparr(self.GetNoiseList())
        if len(noise)<=1:
            n=1E-20
        else:
            n=np.std(noise)/np.sqrt(len(noise))
        return n

    def GetStdNoise(self, minstd=1E-5):
        noise=nparr(self.GetNoiseList())
        if len(noise)<=1:
            std=minstd
        else:
            std=np.std(noise)
        if std==0.: std=minstd
        return std

    def GetNoiseHisto(self):
        if self.noiseHisto: return self.noiseHisto
        noise = self.GetNoiseList()
        self.noiseHisto = ROOT.TH1F('noiseHisto_'+self.GetName(), ';Amplitude (V);Counts', 100, 0.99*min(noise), 1.01*max(noise))
        for i,v in enumerate(self.y):
            self.noiseHisto.Fill(v)
        return self.noiseHisto

    def GetEpeakMin(self, sigma=2):
        """
        return the time of the start of the electron peak
        """
        min=self.Ampmin
        tFitMax=self.tFitMax
        sub_y=self.y[self.x<tFitMax]
        sub_x=self.x[self.x<tFitMax]
        std=self.baseLineStd
        x_peak = 0
        i=0
        for i in range(1,len((sub_y))-1):
            if np.abs(sub_y[-i])<(sigma*std):
                x_peak=sub_x [-i]
                break
            else:
                continue
        if x_peak==0 and self.EpeakBadDisable is False:
            self.isBad()
            if self.badDebug is not None: print("bad because epeak start at index 0")
        return [x_peak,len(sub_y)-i]


    def GetEpeakMax(self, sigma=2):
        """
        return the time of the stop of the electron peak
        """
        min=self.Ampmin
        tFitMax=self.tFitMax
        offseti=len(self.y[self.x<=tFitMax])
        sub_y=self.y[self.x>tFitMax]
        sub_x=self.x[self.x>tFitMax]
        std=self.baseLineStd
        x_peak = 0
        i=0
        for i in range(len((sub_y))):
            if np.abs(sub_y[i])<(sigma*std):
                x_peak=sub_x[i]
                break
            else:
                continue
        if x_peak==0 and self.EpeakBadDisable is False:
            self.isBad()
            if self.badDebug is not None: print("bad because epeak finishes at index 0")

        #print(x_peak,self.x[offseti+i])
        return [x_peak,offseti+i]


    def GetEpeakMax_fromDerivative(self,window=20):
        """
        return the time of the stop of the electron peak
        currently working fine with derivative Av100
        looking only in window=20ns after electorn peak
        """
        max_samp=round(window*1E-9/self.sampling)
        start=self.EpeakminIdx
        max=0
        tmax=0
        for i in range(max_samp):
            if start+i==self.samples-1:#if the cose is going out the acquired time window
                max=self.DerivAv[start+i]
                tmax=start+i
                self.isBad()
                break
            if self.DerivAv[start+i]>=max:
                max=self.DerivAv[start+i]
                tmax=start+i
            else:
                continue
        return [self.x[tmax],tmax]

    """
    NOT NEEDED
    def Average(self,kernel_size=100):
        kernel = np.ones(kernel_size) / kernel_size
        data_convolved = np.convolve(self.y, kernel, mode='same')
        return ScopeSignal(self.x, data_convolved, str(kernel_size)+"Av_"+self.name)

    NOT NEEDED
    def GetDerivative(self, edge_order=2):
        y=np.gradient(self.y, edge_order)
        return ScopeSignal(self.x, y, "Derivative_"+self.name)
    """
    def SigmoidFit(self,mult1=4, mult2=2,test=False,write=False):
        start0=self.Ampmin
        start1=self.risetime/mult1
        start2=(self.tFitMax+self.tFitMin)/mult2

        sigmoid=ROOT.TF1("sigmoid", "([0]/(1+ exp(-(x-[2])/[1])))",self.tFitMin,self.tFitMax)
        sigmoid.SetParameters(start0, start1, start2)
        sigmoid.FixParameter(0,start0)
        #sigmoid.SetParLimits(0,0.9*start0,1.1*start0)
        sigmoid.SetParLimits(1,0.1*start1,10*start1)
        #sigmoid.FixParameter(2,start2)
        sigmoid.SetParLimits(2,0.95*start2,1.05*start2)
        plot=self.WaveGraph()
        plot.Fit("sigmoid","RQ","r")
        #print(self.risetime/4/sigmoid.GetParameter(1))
        if write==True: plot.Write()
        if test==True:
            return [start0/sigmoid.GetParameter(0),start1/sigmoid.GetParameter(1), start2/sigmoid.GetParameter(2)]
        else:
            return sigmoid

    def GenSigmoidFit(self,mult1=6.7, mult2=2,test=False,write=False,LeftPoints=25,RightPoints=0):
        start0=self.Ampmin
        start1=self.risetime/mult1
        start2=(self.tFitMax+self.tFitMin)/mult2
        start3=1

        sigmoid=ROOT.TF1("sigmoid", "([0]/(1+ exp(-(x-[2])/[1]))^[3])",self.tFitMin-(LeftPoints*self.sampling),self.tFitMax+(RightPoints*self.sampling))
        sigmoid.SetParameters(start0, start1, start2,start3)
        #sigmoid.FixParameter(0,start0)
        #sigmoid.SetParLimits(0,0.9*start0,1.1*start0)
        #sigmoid.SetParLimits(1,0.1*start1,10*start1)
        #sigmoid.FixParameter(2,start2)
        #sigmoid.SetParLimits(2,0.9*start2,1.1*start2)
        plot=self.WaveGraph()
        plot.Fit("sigmoid","RQ","r")
        #print(self.risetime/4/sigmoid.GetParameter(1))
        if write==True: plot.Write()
        if test==True:
            return [start0/sigmoid.GetParameter(0),start1/sigmoid.GetParameter(1), start2/sigmoid.GetParameter(2), start3/sigmoid.GetParameter(3)]
        else:
            return sigmoid


    def ArrivalTimeLESignal(self, threshold=0.2):
        x=self.x[self.EpeakminIdx:self.AmpminIdx]
        y=self.y[self.EpeakminIdx:self.AmpminIdx]
        for i in range(len(x)):
            if y[i]<=threshold*self.Ampmin:
                tarr=x[i]
                break
            else:
                continue
        return tarr

    def GetInverseSigmoid(self):
        FitFunc=self.SigmoidFit(test=False,write=False)
        inverse=ROOT.TF1("inverse", "-[1]*log(([0]/x)-1)+[2]",self.Ampmin,0)
        inverse.SetParameters(FitFunc.GetParameter(0),FitFunc.GetParameter(1),FitFunc.GetParameter(2))
        return inverse

    def GetInverseGenSigmoid(self,A,mu,sigma,exp):
            inverse=ROOT.TF1("inverse", "-[1]*log(([0]/x)**(1/[3])-1)+[2]",self.Ampmin,0)
            inverse.SetParameters(A,mu,sigma,exp)
            return inverse

    def ArrivalTimeLEFit(self, threshold=0.2):
        inverse=self.GetInverseSigmoid()
        thr=threshold*inverse.GetParameter(0)
        return inverse.Eval(thr)


    def GetSignalCFDSignal(self, fr=0.2,dele=0.5E-9):
        indexDelay = int(dele/self.sampling)
        yAttenuated = -1*self.y*fr
        yDelayed = np.roll(self.y, indexDelay)
        yCFD = yAttenuated+yDelayed
        return yCFD

    def ArrivalTimeCFDSignal(self, window=10,fraction=0.2, delay=0.5E-9):
        """
        Not working fine
        IF OUTPUT IS 0 THE METHOD DIN'T FIND ANY ZERO CROSSING
        window is in nanosecods
        """
        yCFD=self.GetSignalCFDSignal(fr=fraction, dele=delay)
        max_samp=round(window/self.sampling)
        yCFDcut=yCFD[self.EpeakminIdx:self.EpeakminIdx+max_samp]
        xcut=self.x[self.EpeakminIdx:self.EpeakminIdx+max_samp]
        tarr=0
        #print(len(yCFDcut))
        for i in range(len(yCFDcut)):
            if yCFDcut[i]>=0 and yCFDcut[i+1]<0:
                tarr=xcut[i]
                break
            else:
                continue
        return tarr

    def ArrivalTimeCFDFit(self, fraction=0.2,delay=0.5E-9):
        """
        Analytially find the zero crossing of the CFD
        """
        FitFunc=self.SigmoidFit(test=False,write=True)
        sigma=FitFunc.GetParameter(1)
        f=fraction
        D=delay
        mu=FitFunc.GetParameter(2)
        return -sigma*np.log( ((1/f)-1) / ( m.exp(D/sigma) - (1/f) )  )+mu


    def FindParCFD(self, fraction, delay, sigma, mu):
        """
        use this to find the best aprametrs for CFD
        """
        f=fraction
        D=delay# *1E-9
        return -sigma*np.log( ((1/f)-1) / ( m.exp(D/sigma) - (1/f) )  )+mu

class EventIDSignal():
    def __init__(self,x,y,name):
        self.notReco=False
        self.x=x
        self.y=y
        self.name=name
        self.Ampmin, self.AmpminIdx=self.GetAmplitudeMin()
        self.Ampmax, self.AmpmaxIdx=self.GetAmplitudeMax()
        self.ID=self.GetEventID()

    def NotReco(self):
        self.notReco = True

    def GetEventID(self, baud_rate=40E6, n_bits=16):
        "per eventID only on CH3"
        Ts = self.x[2]-self.x[1]
        y_thr = (self.Ampmin+self.Ampmax)/2
        y_dig = np.array(self.y < y_thr);
        bit_l = round(1/baud_rate/Ts)
        idx=np.where(y_dig>0.5)
        idx_first=idx[0][0]
        sampling = np.arange(1, n_bits+1,1)*bit_l+idx_first+round(bit_l/2)
        bitstream = y_dig[sampling]
        eventID = int(''.join(map(lambda bitstream: str(int(bitstream)), bitstream)), 2)
        return eventID

    def WaveGraph(self, color=4, markerstyle=22, markersize=1, write=False):
        plot = ROOT.TGraph(len(self.x),  np.array(self.x  ,dtype="d")  ,   np.array(self.y  ,dtype="d"))
        plot.SetNameTitle(self.name,self.name)
        plot.GetXaxis().SetTitle("Time(s)")
        plot.GetYaxis().SetTitle("Voltage(V)")
        plot.SetMarkerColor(color)#blue
        plot.SetMarkerStyle(markerstyle)
        plot.SetMarkerSize(markersize)
        if write==True: plot.Write()
        return plot

    #do not use it is time consuming
    def GetCoordinates(self, path):
        df=pd.read_csv(path, sep="\t")
        selected=df.loc[df[df.columns[0]]==str(self.ID)]
        if selected.empty:
            self.NotReco()
            return [0,0,0]
        else:
            return [selected[df.columns[9]],selected[df.columns[10]],selected[df.columns[11]]]

    def GetAmplitudeMin(self):
        return [np.min(self.y),np.argmin(self.y)]
    def GetAmplitudeMax(self):
        return [np.max(self.y),np.argmax(self.y)]

class DerivSignal(ScopeSignalCividec):#this class is basically just for draw the derivative
    def __init__(self,ScopeSignalCividec,kernel_size=100, edge_order=2):
        self.x=ScopeSignalCividec.x
        #derivation
        y=np.gradient(ScopeSignalCividec.y, edge_order)
        #averaging
        kernel = np.ones(kernel_size) / kernel_size
        self.y= np.convolve(y, kernel, mode='same')
        self.name="Deriv_"+ScopeSignalCividec.name

        self.tFitMax=ScopeSignalCividec.tFitMax
        self.Epeakmin=ScopeSignalCividec.Epeakmin
        self.EpeakminIdx=ScopeSignalCividec.EpeakminIdx
        self.Epeakmax=ScopeSignalCividec.Epeakmax
        self.EpeakmaxIdx=ScopeSignalCividec.EpeakmaxIdx

    def WaveGraph(self, color=4, markerstyle=22, markersize=1):
        plot = ROOT.TGraph(len(self.x),  np.array(self.x  ,dtype="d")  ,   np.array(self.y  ,dtype="d"))
        plot.SetNameTitle(self.name,self.name)
        plot.GetXaxis().SetTitle("Time(s)")
        plot.GetYaxis().SetTitle("Voltage(V)")
        plot.SetMarkerColor(color)#blue
        plot.SetMarkerStyle(markerstyle)
        plot.SetMarkerSize(markersize)
        #plot.Write()
        return plot

    def WaveSave(self, size=800, leftmargin=0.17, rightmargin=0.1, EpeakLines=False,Write=False,Zoom=False, Save=False):
        plot=self.WaveGraph()
        y_name=plot.GetYaxis().GetTitle()
        x_name=plot.GetXaxis().GetTitle()
        can1=ROOT.TCanvas(self.name, self.name, size, size)
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
        if Zoom==True:
            plot.GetXaxis().SetRangeUser(0.8*self.Epeakmin, 2*self.Epeakmax)
        plot.Draw("AP")
        if EpeakLines==True:
            can1.Update()
            ymax=ROOT.gPad.GetUymax()
            ymin=ROOT.gPad.GetUymin()
            line=ROOT.TLine(self.Epeakmin,ymin,self.Epeakmin,ymax)
            line.SetLineColor(2)
            line.SetLineWidth(2)
            line.Draw("SAME")
            line1=ROOT.TLine(self.Epeakmax,ymin,self.Epeakmax,ymax)
            line1.SetLineColor(2)
            line1.SetLineWidth(2)
            line1.Draw("SAME")
        if Write==True: can1.Write()
        if Save==True: can1.SaveAs(self.name+".png")
        return can1

class SignalPlot():#this class is basically just for debugging
    def __init__(self, x, y,name,kernel_size=100, edge_order=2):
        self.name = name
        self.x=nparr(x)
        self.y=nparr(y)
        self.samples=len(x)
        #derivation
        y=np.gradient(self.y, edge_order)
        #averaging
        kernel = np.ones(kernel_size) / kernel_size
        self.DerivAv= np.convolve(y, kernel, mode='same')

    def DerGraph(self, color=4, markerstyle=22, markersize=1):
        plot = ROOT.TGraph(len(self.x),  np.array(self.x  ,dtype="d")  ,   self.DerivAv)
        plot.SetNameTitle(self.name,self.name)
        plot.GetXaxis().SetTitle("Time(s)")
        plot.GetYaxis().SetTitle("Deriv_Voltage(V)")
        plot.SetMarkerColor(color)#blue
        plot.SetMarkerStyle(markerstyle)
        plot.SetMarkerSize(markersize)
        plot.Write()
        return plot

    def WaveGraph(self, color=4, markerstyle=22, markersize=1):
        plot = ROOT.TGraph(len(self.x),  np.array(self.x  ,dtype="d")  ,   np.array(self.y  ,dtype="d"))
        plot.SetNameTitle(self.name,self.name)
        plot.GetXaxis().SetTitle("Time(s)")
        plot.GetYaxis().SetTitle("Voltage(V)")
        plot.SetMarkerColor(color)#blue
        plot.SetMarkerStyle(markerstyle)
        plot.SetMarkerSize(markersize)
        plot.Write()
        return plot

    def WaveSave(self, size=800, leftmargin=0.17, rightmargin=0.1,Write=False):
        plot=self.WaveGraph()
        y_name=plot.GetYaxis().GetTitle()
        x_name=plot.GetXaxis().GetTitle()
        can1=ROOT.TCanvas(self.name, self.name, size, size)
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
        plot.Draw("AP")
        if Write==True: can1.Write()
        can1.SaveAs(self.name+".png")
        return can1

class ChargeDistr():
    def __init__(self, x, name, channels, bin="lin", rangeFrac=0.01):
        self.name = name
        self.x=nparr(x)
        self.entries=len(self.x)
        self.channels=channels
        self.range=[(1-rangeFrac)*np.min(self.x),(1+rangeFrac)*np.max(self.x)]
        #set automatically if these are charges or amplitudes
        if np.mean(x)<1E-6:
            self.type="Charge (C)"
        else:
            self.type="Amplitude (-V)"
        self.hist=self.GetHist(bin=bin)


    def GetHist(self, linecolor=4, linewidth=4,Norm=False,bin="lin"):
        if self.type=="Charge (C)":
            if bin=="lin":
                hist=ROOT.TH1D(self.name+"_ChargeDistr",self.name+"_ChargeDistr",self.channels,self.range[0], self.range[1])
            elif bin=="log":
                custom_bins=np.logspace(np.log10(self.range[0]),np.log10(self.range[1]), self.channels+1)
                hist=ROOT.TH1D(self.name+"_ChargeDistr",self.name+"_ChargeDistr",self.channels,custom_bins)
        else:
            if bin=="lin":
                hist=ROOT.TH1D(self.name+"_AmpDistr",self.name+"_AmpDistr",self.channels,self.range[0], self.range[1])
            elif bin=="log":
                custom_bins=np.logspace(np.log10(self.range[0]),np.log10(self.range[1]), self.channels+1)
                hist=ROOT.TH1D(self.name+"_AmpDistr",self.name+"_AmpDistr",self.channels,custom_bins)

        for x in self.x: hist.Fill(x)
        if Norm==True:
            for i in range(self.channels):
                hist.SetBinContent(i,hist.GetBinContent(i)/self.entries)
        hist.SetLineColor(linecolor)
        hist.SetLineWidth(linewidth)
        if self.type=="Charge (C)":
            hist.GetXaxis().SetTitle("Charge (C)")
        else:
            hist.GetXaxis().SetTitle("Amplitudes (-V)")
        hist.GetYaxis().SetTitle("Entries")
        #hist.SetStats(False)
        hist.GetYaxis().SetMaxDigits(3);
        hist.GetXaxis().SetMaxDigits(3);
        return hist

    def PolyaFit(self,printStart=False,GetChi=True, save=False, path="./",rangemin="max"):
        hist=self.hist
        #polyaTF1=ROOT.TF1("polyaTF1", "[0]*ROOT::Math::negative_binomial_pdf([0],x,[1])" ,self.range[0], self.range[1])
        amp=hist.GetBinContent(hist.GetMaximumBin())
        mean=hist.GetMean()
        theta=1
        if printStart==True: print(amp,mean,theta)
        #polyaTF1=ROOT.TF1("polyaTF1","[0]*(ROOT::Math::tgamma(x+[1])/(ROOT::Math::tgamma(x+1)*ROOT::Math::tgamma([1])))*(TMath::Power(([2]/[1]),x))*(TMath::Power((1+([2]/[1])),-x-[1]))" ,0, 3*theta)
        polyaTF1=ROOT.TF1("polyaTF1",'[0]*TMath::Power(1+[2],1+[2])/ROOT::Math::tgamma(1+[2])*TMath::Power(x/[1],[2])*TMath::Exp(-(1+[2])*x/[1])' ,0, hist.GetMaximumBin())

        polyaTF1.SetParameters(amp,mean, theta)
        polyaTF1.SetParNames("Amplitude", "Gain", "theta")

        #polyaTF1.SetParLimits(0,0.9*amp,1.1*amp)
        #polyaTF1.SetParLimits(1,0.1*mean,10*mean)
        #polyaTF1.SetParLimits(2,0.1*theta,10*theta)

        if rangemin=="max":
            hist.Fit("polyaTF1","RQ","r")
        else:
            hist.Fit("polyaTF1","Q","",rangemin,hist.GetMaximumBin())
        hist.Write()

        if save==True:
            if self.type=="Charge (C)":
                c=ROOT.TCanvas(self.name+"_ChargeDistr",self.name+"_ChargeDistr"    ,800,800)
            else:
                c=ROOT.TCanvas(self.name+"_AmplitudeDistr",self.name+"_AmplitudeDistr"    ,800,800)
            hist.SetStats(False)
            hist.Draw()
            c.SetLogy()
            p=ROOT.TPaveText(.5,.75,.9,.9,"NDC")
            p.AddText("Mean: "+str("{:2e}".format(polyaTF1.GetParameter(1))))
            p.AddText("Error: "+str("{:2e}".format(polyaTF1.GetParError(1))))
            p.AddText("CHI2/NDF: "+str("{:2e}".format(polyaTF1.GetChisquare()/polyaTF1.GetNDF())))
            p.SetFillStyle(0);
            p.Draw("SAME")
            c.Update()
            c.Write()
            c.SaveAs(path+str(hist.GetName())+".png")

        if GetChi==False:
            output=nparr([polyaTF1.GetParameter(0),polyaTF1.GetParameter(1),polyaTF1.GetParError(1),polyaTF1.GetParameter(1)/(1+polyaTF1.GetParameter(2))])
        else:
            output=nparr([polyaTF1.GetParameter(0),polyaTF1.GetParameter(1),polyaTF1.GetParError(1),polyaTF1.GetParameter(1)/(1+polyaTF1.GetParameter(2)), polyaTF1.GetChisquare()/polyaTF1.GetNDF()])

        return output

    def ComplexPolya(self,path="./"):
        hist=self.hist
        #get bin of the maxium
        peakpos=hist.GetBinCenter(hist.GetMaximumBin())
        #Gaus fit near the peak to understand the parameters
        gaussian=ROOT.TF1("gaussian",'gaus',peakpos*0.9, peakpos*1.1)
        hist.Fit("gaussian","Q","",hist.GetBinCenter(hist.GetMaximumBin()-5), hist.GetBinCenter(hist.GetMaximumBin()+5))
        if self.type=="Charge (C)":
            hist.Fit("gaussian","Q","",hist.GetBinCenter(hist.GetMaximumBin()-20), hist.GetBinCenter(hist.GetMaximumBin()+25))
        else:
            hist.Fit("gaussian","Q","",hist.GetBinCenter(hist.GetMaximumBin()-20), hist.GetBinCenter(hist.GetMaximumBin()+25))
        A,m,s=gaussian.GetParameter(0),gaussian.GetParameter(1),gaussian.GetParameter(2)
        hist.Write()

        #ploya fit with gaus fixed (not the amplitude)
        polyaTF1=ROOT.TF1("polyaTF1",'[0]*TMath::Power(1+[2],1+[2])/ROOT::Math::tgamma(1+[2])*TMath::Power(x/[1],[2])*TMath::Exp(-(1+[2])*x/[1])+gaus(3)' ,0,np.max(self.x))
        polyaTF1.SetParameters(0.1*A,hist.GetMean(), 1,A,m,s)
        #polyaTF1.FixParameter(4,m)
        #polyaTF1.FixParameter(5,s)
        #polyaTF1.SetParLimits(5,s*0.9,s*1.1)
        polyaTF1.SetParNames("Amplitude", "Gain", "theta", "A","m","s")
        if self.type=="Charge (C)":
            hist.Fit("polyaTF1","Q","",0,np.max(self.x))
            hist.Fit("polyaTF1","Q","",m-s,np.max(self.x))
        else:
            polyaTF1.SetParLimits(4,0.5*m, 1.5*m)
            polyaTF1.SetParLimits(5,0.5*s, 1.5*s)
            polyaTF1.SetParLimits(1,2*m,np.max(self.x))
            #polyaTF1.SetParLimits(1,0.5*s, 1.5*s)
            #polyaTF1.SetParLimits(2,0.5*s, 1.5*s)
            #polyaTF1.SetParLimits(3,0.5*s, 1.5*s)
            #polyaTF1.SetParLimits(4,0.5*s, 1.5*s)
            #polyaTF1.SetParLimits(4,0.5*s, 1.5*s)
            #polyaTF1.FixParameter(4,m)
            #polyaTF1.FixParameter(5,s)
            #polyaTF1.FixParameter(0,34.3252)
            #polyaTF1.FixParameter(1,0.00942031)
            #polyaTF1.FixParameter(2,2.48819)
            #polyaTF1.FixParameter(3,2340)
            #polyaTF1.FixParameter(4,m)
            #polyaTF1.SetParameter(0,34.3252)
            #polyaTF1.SetParameter(1,0.00942031)
            #polyaTF1.SetParameter(2,2.48819)
            #polyaTF1.SetParameter(3,2340)
            #polyaTF1.SetParameter(4,m)
            #polyaTF1.SetParameter(5,s)
            #hist.Fit("polyaTF1","Q","",m-3*s,np.max(self.x))
            hist.Fit("polyaTF1","Q","",0,np.max(self.x))

        #hist.Write()
        hist.SetStats(False)

        if self.type=="Charge (C)":
            c=ROOT.TCanvas(self.name+"_ChargeDistr",self.name+"_ChargeDistr"    ,800,800)
        else:
            c=ROOT.TCanvas(self.name+"_AmplitudeDistr",self.name+"_AmplitudeDistr"    ,800,800)
        hist.Draw()
        c.SetLogy()

        #just draw the functions
        g=ROOT.TF1("g",'gaus')
        g.SetParameters(polyaTF1.GetParameter(3),polyaTF1.GetParameter(4),polyaTF1.GetParameter(5))
        g.SetLineColor(3)
        g.Draw("SAME")
        poldraw=ROOT.TF1("poldraw",'[0]*TMath::Power(1+[2],1+[2])/ROOT::Math::tgamma(1+[2])*TMath::Power(x/[1],[2])*TMath::Exp(-(1+[2])*x/[1])')
        poldraw.SetParameters(polyaTF1.GetParameter(0),polyaTF1.GetParameter(1),polyaTF1.GetParameter(2))
        poldraw.SetLineColor(4)
        poldraw.Draw("SAME")


        p=ROOT.TPaveText(.5,.75,.9,.9,"NDC")
        p.AddText("Mean: "+str("{:2e}".format(polyaTF1.GetParameter(1))))
        p.AddText("Error: "+str("{:2e}".format(polyaTF1.GetParError(1))))
        p.AddText("CHI2/NDF: "+str("{:2e}".format(polyaTF1.GetChisquare()/polyaTF1.GetNDF())))
        p.SetFillStyle(0);

        p.Draw("SAME")
        c.Update()

        c.Write()
        c.SaveAs(path+str(hist.GetName())+".png")

        return [polyaTF1.GetParameter(0),polyaTF1.GetParameter(1),polyaTF1.GetParError(1),polyaTF1.GetParameter(1)/(1+polyaTF1.GetParameter(2)), polyaTF1.GetChisquare()/polyaTF1.GetNDF()]

class DiscriminatorScaler():
    """
    baseline from all the sample!
    """
    def __init__(self, x, y, name, sampling=1E10, deadtime=50E-9, thresold=-2.4E-3, thresSigma=None, smoothing=None):
        self.name = name
        self.x=nparr(x)
        self.leng=len(self.x)
        y=nparr(y)
        if smoothing is not None:
            kernel = np.ones(smoothing) / smoothing
            self.y= np.convolve(y, kernel, mode='same')
        else:
            self.y=y
        self.dead_points=sampling*deadtime
        self.sampling=sampling
        self.baseline, self.std=np.mean(self.y),np.std(self.y)
        self.min=np.min(self.y)
        self.max=np.max(self.y)
        if thresSigma is not None and thresold is None: self.threshold=-1*thresSigma*self.std
        elif thresold is not None and thresSigma is None: self.threshold=thresold
        else: raise Exception("Both threshold are ON or both are None")

    def GetHist(self, linecolor=4, linewidth=4, channels=1E5,write=False):
        hist=ROOT.TH1D("voltage distribution","voltage distribution",channels,0.99*self.min,1.01*self.max)
        fill_h(hist,self.y)
        hist.SetLineColor(linecolor)
        hist.SetLineWidth(linewidth)
        hist.GetXaxis().SetTitle("Voltages")
        hist.GetYaxis().SetTitle("Entries")
        hist.GetYaxis().SetMaxDigits(3);
        hist.GetXaxis().SetMaxDigits(3);
        if write==True: hist.Write()
        return hist

    def GetGraph(self, color=4, markerstyle=22, markersize=1, write=True):
        plot = ROOT.TGraph(len(self.x),  self.x, self.y)
        plot.SetNameTitle("Voltage vs time","Voltage vs time")
        plot.GetXaxis().SetTitle("Time(s)")
        plot.GetYaxis().SetTitle("Voltage(V)")
        plot.SetMarkerColor(color)#blue
        plot.SetMarkerStyle(markerstyle)
        plot.SetMarkerSize(markersize)
        if write==True: plot.Write()
        return plot

    def GetCountsAmps(self, risetimeCut=[0.25E-9,2.5E-9], debugPlot=False):
        #for every discrimated wave (with self.threshold and self.dead_points gate) return the max amplitude and the risetimes
        counter, index, timesIdxstart,timesIdxstop, amplitudes, risetimes=0, 0, [], [], [], []
        while index<self.leng:
            if self.y[int(index)]<(self.baseline+self.threshold):
                #print(self.y[int(index)], (self.baseline+self.threshold))
                #get index start and stop
                trg_index=index
                max_index=index+np.argmin(self.y[int(index):int(index+self.dead_points)])
                #print(trg_index, max_index)
                risetemp=(max_index-trg_index)/self.sampling

                if risetemp>=risetimeCut[0] and risetemp<risetimeCut[1]:
                    timesIdxstart.append(trg_index)
                    timesIdxstop.append(max_index)
                    #compute risetime and amplitude
                    risetimes.append(risetemp)
                    amplitudes.append(np.min(self.y[int(index):int(index+self.dead_points)]))
                    index=index+self.dead_points+1
                    counter=counter+1
                    if debugPlot==True: self.SaveGraphCounter(int(trg_index), int(max_index),(max_index-trg_index)/self.sampling , Write=True)
                else:
                    index=index+1

            else:
                index=index+1
        return [counter, amplitudes, timesIdxstart, timesIdxstop, risetimes]

    def GetFFT(self):
        t,y = self.x, self.y
        timestep = 1/self.sampling
        yf = fftpack.fft(y)
        xf = fftpack.fftfreq(self.leng, d=timestep)
        return xf, yf

    def GetPowerSpectrum(self, fcut=None):
        xf, yfft = self.GetFFT()
        xf, yf = xf[xf>0], np.log10(np.abs(yfft)**2)[xf>0]
        if fcut is not None: xf, yf = xf[xf<fcut], yf[xf<fcut]
        return xf, yf

    def FreqFilter(self, freqmin=None, freqmax=None):
        sample_freq, sig_fft = self.GetFFT()
        filtered_freq = sig_fft.copy()
        if freqmax is not None: filtered_freq[np.abs(sample_freq) > freqmax] = 0
        if freqmin is not None: filtered_freq[np.abs(sample_freq) < freqmin] = 0
        filtered_sig = fftpack.ifft(filtered_freq)
        return self.x, filtered_sig

    """
    def GetCountsAmps(self,threshold=2, gate=10E-9, debugPlot=True):
        #moving baseline
        counter, index, timesIdxstart,timesIdxstop, amplitudes, risetimes=0, 0, [], [], [], []
        scout_baseline=100
        index=scout_baseline#start from point
        while index<self.leng:
            #get running baseline
            subY=self.y[int(index-scout_baseline):int(index)]
            Baseline=np.mean(subY)
            stdBaseline=np.std(subY)
            level=Baseline-threshold*stdBaseline
            #check if out baseline
            if self.y[int(index)]<=level:
                #get index start and stop
                trg_index=index
                max_index=index+np.argmin(self.y[int(index):int(index+(gate*self.sampling))])
                #print(trg_index, max_index)
                risetemp=(max_index-trg_index)/self.sampling
                #for now ok.........
                timesIdxstart.append(trg_index)
                timesIdxstop.append(max_index)
                #compute risetime and amplitude
                risetimes.append(risetemp)
                amplitudes.append(np.min(self.y[int(index):int(index+(gate*self.sampling))]))
                index=index+(gate*self.sampling)+1
                counter=counter+1
                if debugPlot==True: self.SaveGraphCounter(int(trg_index), int(max_index),(max_index-trg_index)/self.sampling , Write=True)

            else:
                index=index+1

        return [counter, amplitudes, timesIdxstart, timesIdxstop, risetimes]
    """

    def PlotDiscrim(self,timesIdx, name=None, size=600, leftmargin=0.17, rightmargin=0.1, Lines=True,Write=False, save=False):
        plot=self.GetGraph(write=False)
        #y_name=plot.GetYaxis().GetTitle()
        #x_name=plot.GetXaxis().GetTitle()
        can1=ROOT.TCanvas(self.name, self.name, size, size)
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
        plot.Draw("AP")
        if Lines==True:
            can1.Update()
            ymax=ROOT.gPad.GetUymax()
            ymin=ROOT.gPad.GetUymin()
            xmax=ROOT.gPad.GetUxmax()
            xmin=ROOT.gPad.GetUxmin()
            line=ROOT.TLine(xmin,self.baseline+self.threshold,xmax,self.baseline+self.threshold)
            line.SetLineColor(4)
            line.SetLineWidth(2)
            line.Draw("SAME")
            for i, idx in enumerate(timesIdx):
                exec("line"+str(i)+"=ROOT.TLine(self.x["+str(int(idx))+"],ymin,self.x["+str(int(idx))+"],ymax)")
                exec("line"+str(i)+".SetLineColor(2)")
                exec("line"+str(i)+".SetLineWidth(1)")
                exec("line"+str(i)+".Draw('SAME')")
        if Write==True: can1.Write()
        if save==True:
            if name is None: can1.SaveAs("plot.png")
            else: can1.SaveAs(str(name)+".png")
        return can1

    def IntervalPlot(self, times):
        intervals=[]
        for i in range(len(times)-1):
            intervals.append(times[i+1]-times[i])
        hist(intervals, "Distribution of time intervals", channels=10)
        return intervals

    def SaveGraphCounter(self, start, stop, risetime,plot_delay=1000 , size=800, leftmargin=0.17, rightmargin=0.1, Lines=True,Write=False):
        if int(start)-int(plot_delay*0.1)<0: off_start=0
        else: off_start=int(start)-int(plot_delay*0.1)
        if int(stop)+plot_delay>self.leng: off_stop=self.leng
        else: off_stop=int(stop)+plot_delay
        plot=graph(self.x[off_start:off_stop],self.y[off_start:off_stop],"time(s)", "voltage(V)", write=False)
        y_name=plot.GetYaxis().GetTitle()
        x_name=plot.GetXaxis().GetTitle()
        can1=ROOT.TCanvas(y_name+" vs "+x_name, y_name+" vs "+x_name, size, size)
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
        plot.Draw("AP")
        if Lines==True:
            can1.Update()
            ymax=ROOT.gPad.GetUymax()
            ymin=ROOT.gPad.GetUymin()
            line1=ROOT.TLine(self.x[start],ymin,self.x[start],ymax)
            line1.SetLineColor(2)
            line1.SetLineWidth(2)
            line1.Draw("SAME")
            line2=ROOT.TLine(self.x[stop],ymin,self.x[stop],ymax)
            line2.SetLineColor(2)
            line2.SetLineWidth(2)
            line2.Draw("SAME")
            p=ROOT.TPaveText(.5,.8,.9,.9,"NDC")
            p.AddText("risetime(s): "+ str(risetime))
            p.SetFillStyle(0);
            p.Draw("SAME")
        if Write==True: can1.Write()
        return can1