import os, sys
import argparse
from ROOT import *

def compareHistograms(Phase0RootFile, Phase1RootFile):

    ############## VARIABLES ###############
    ### x-axis range
    xmin = -4.0
    xmax = +4.0
    ### y-axis range
    ymin = 0.0
    ymax = 2.4
    ### ratio plot y-axis range
    ratioYmin = 0.0
    ratioYmax = 3.2 ### 2.2 for |eta|<2.5    -   3.2 for |eta|<4.0
    ### Histo
    histoName = "10"
    ########################################

    cmsver = "10X" if "CMSSW_10" in Phase0RootFile else "12X"
    yAxisTitle = "#bf{x/X_{0}}" if histoName == "10" else "#bf{x/#lambda_{0}}"
    histoType = "X0" if histoName == "10" else "L0"
    #ratioYmax = 2.2 if xmax == 2.5 else 3.2

    file0 = TFile.Open(Phase0RootFile)
    file1 = TFile.Open(Phase1RootFile)

    hist0 = file0.Get(histoName)
    hist1 = file1.Get(histoName)

    hist0.SetTitle("")
    hist1.SetTitle("")

    hist0.SetFillStyle(1001)
    hist0.SetFillColor(kGreen+1)
    hist0.SetLineColor(kBlack)
    hist0.SetLineWidth(1)

    hist1.SetMarkerStyle(8)
    hist1.SetMarkerColor(kBlack)
    hist1.SetMarkerSize(1.5)


    hist0.GetXaxis().SetRangeUser(xmin, xmax)
    hist1.GetXaxis().SetRangeUser(xmin, xmax)

    c1 = TCanvas('c1', 'MB Phase Comparison', 900, 900)
    c1.SetTicks(0, 1)
    gStyle.SetOptStat(0)

    pad1 = TPad("pad1", "pad1",0,0.,1,1)
    pad1.SetTopMargin(0.03)
    pad1.SetLeftMargin(0.15)
    pad1.SetRightMargin(0.03)
    pad1.SetBottomMargin(0.32)
    pad1.Draw()
    pad1.cd()

    hist0.SetTitle("")
    hist0.GetYaxis().SetTitle(yAxisTitle)
    hist0.GetXaxis().SetTitle("#bf{#eta}")
    hist0.GetYaxis().SetTitleSize(0.045)
    hist0.GetYaxis().SetTitleFont(42)
    hist0.GetYaxis().SetTitleOffset(1.35)
    hist1.GetYaxis().SetTitleOffset(1.35)
    hist0.GetXaxis().SetLabelOffset(1000)
    #hist0.GetYaxis().SetNdivisions(515, kTRUE)
    hist0.SetMinimum(ymin)
    hist0.SetMaximum(ymax)
    hist0.Draw("HIST")
    hist1.Draw("EP SAME")



    leg = TLegend(0.55,0.86,0.96,0.96)
    leg.SetBorderSize(0)
    leg.SetFillColor(0)
    leg.SetFillStyle(0)
    leg.SetTextFont(42)
    leg.SetTextSize(0.028)
    leg.AddEntry(hist0,"#bf{Phase 0 pixel detector}","f")
    leg.AddEntry(hist1,"#bf{Phase 1 pixel detector}","p")
    leg.Draw()

    Pave1 = TPaveText(0.15,0.90,0.50,0.93,"NDC")
    Pave1.SetFillColor(0)
    Pave1.SetBorderSize(0)
    Pave1.SetFillStyle(0)
    Pave1.SetTextFont(42)
    Pave1.SetTextSize(0.045)
    Pave1.SetTextColor(kBlack)
    Pave1.SetTextAlign(11)
    Pave1.AddText("#bf{CMS}")
    Pave1.Draw()

    Pave2 = TPaveText(0.15,0.85,0.50,0.90,"NDC")
    Pave2.SetFillColor(0)
    Pave2.SetBorderSize(0)
    Pave2.SetFillStyle(0)
    Pave2.SetTextFont(42)
    Pave2.SetTextSize(0.03)
    Pave2.SetTextColor(kBlack)
    Pave2.SetTextAlign(11)
    Pave2.AddText("#it{Simulation Preliminary}")
    Pave2.Draw()

    ratio = hist1.Clone("ratio")
    ratio.Divide(hist0)

    ratio.GetXaxis().SetRangeUser(xmin, xmax)

    pad2 = TPad("pad2", "pad2",0.,0.02,1,0.30)
    pad2.SetGrid()      
    pad2.SetTopMargin(0)
    pad2.SetBottomMargin(0.30)
    pad2.SetLeftMargin(0.15)
    pad2.SetRightMargin(0.03)
    pad2.Draw()
    pad2.cd()

    ratio.SetMinimum(ratioYmin)
    ratio.SetMaximum(ratioYmax)
    ratio.SetLineColor(kBlack)
    ratio.SetLineWidth(0)
    ratio.SetMarkerSize(1.5)
    ratio.SetMarkerColor(kBlack)
    ratio.GetYaxis().SetNdivisions(505, kTRUE)
    ratio.GetYaxis().SetTitleFont(42)
    ratio.SetTitle("")
    ratio.GetYaxis().SetTitle("#bf{#frac{Phase 1}{ Phase 0 }}")
    ratio.GetXaxis().SetTitleFont(42)
    ratio.GetXaxis().SetTitle("#bf{#eta}")
    ratio.GetXaxis().SetTitleSize(0.20)
    ratio.GetXaxis().SetLabelSize(0.14)
    ratio.GetYaxis().SetLabelSize(0.14)
    ratio.GetYaxis().SetTitleSize(0.12)
    ratio.GetYaxis().SetTitleOffset(0.42)
    ratio.GetXaxis().SetTitleOffset(0.60)
    ratio.Draw("EP")


    pdfName = "CMSSW_%s_eta%s_%s_comparisonMBPhase0AndPhase1" % (cmsver, xmax, histoType)

    c1.Update()
    c1.SaveAs("%s.C" % (pdfName))
    c1.SaveAs("%s.png" % (pdfName))
    c1.SaveAs("%s.pdf" % (pdfName))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-ip0', '--inputPhase0', help='', default="CMSSW_10_matbdg_Pixel_Extended2016.root")
    parser.add_argument('-ip1', '--inputPhase1', help='', default="CMSSW_10_matbdg_Pixel_Extended2017Plan1.root")
    args = parser.parse_args()

    compareHistograms(args.inputPhase0, args.inputPhase1)
