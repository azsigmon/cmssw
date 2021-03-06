#!/usr/bin/env python
"""
_RunPromptReco_

Test wrapper to generate a reco config and actually push it into cmsRun for
testing with a few input files etc from the command line

"""

import sys
import getopt

from Configuration.DataProcessing.GetScenario import getScenario



class RunPromptReco:

    def __init__(self):
        self.scenario = None
        self.writeRECO = False
        self.writeAOD = False
        self.writeMINIAOD = False
	self.writeDQM = False
	self.writeDQMIO = False
        self.noOutput = False
        self.globalTag = None
        self.inputLFN = None
        self.alcaRecos = None

    def __call__(self):
        if self.scenario == None:
            msg = "No --scenario specified"
            raise RuntimeError, msg
        if self.globalTag == None:
            msg = "No --global-tag specified"
            raise RuntimeError, msg
        if self.inputLFN == None:
            msg = "No --lfn specified"
            raise RuntimeError, msg

        try:
            scenario = getScenario(self.scenario)
        except Exception, ex:
            msg = "Error getting Scenario implementation for %s\n" % (
                self.scenario,)
            msg += str(ex)
            raise RuntimeError, msg

        print "Retrieved Scenario: %s" % self.scenario
        print "Using Global Tag: %s" % self.globalTag

        dataTiers = []
        if self.writeRECO:
            dataTiers.append("RECO")
            print "Configuring to Write out RECO"
        if self.writeAOD:
            dataTiers.append("AOD")
            print "Configuring to Write out AOD"
        if self.writeMINIAOD:
            dataTiers.append("MINIAOD")
            print "Configuring to Write out MiniAOD"
	if self.writeDQM:
            dataTiers.append("DQM")
            print "Configuring to Write out DQM"
	if self.writeDQMIO:
            dataTiers.append("DQMIO")
            print "Configuring to Write out DQMIO"
        if self.alcaRecos:
            dataTiers.append("ALCARECO")
            print "Configuring to Write out ALCARECO"

        try:
            kwds = {}

            if self.noOutput:
                kwds['outputs'] = []
            else:
                outputs = []
                for dataTier in dataTiers:
                    outputs.append({ 'dataTier' : dataTier,
                                     'eventContent' : dataTier,
                                     'moduleLabel' : "write_%s" % dataTier })
                kwds['outputs'] = outputs

                if self.alcaRecos:
                    kwds['skims'] = self.alcaRecos

            process = scenario.promptReco(self.globalTag, **kwds)

        except NotImplementedError, ex:
            print "This scenario does not support Prompt Reco:\n"
            return
        except Exception, ex:
            msg = "Error creating Prompt Reco config:\n"
            msg += str(ex)
            raise RuntimeError, msg

        process.source.fileNames.append(self.inputLFN)

        import FWCore.ParameterSet.Config as cms

        process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(10) )

        psetFile = open("RunPromptRecoCfg.py", "w")
        psetFile.write(process.dumpPython())
        psetFile.close()
        cmsRun = "cmsRun -e RunPromptRecoCfg.py"
        print "Now do:\n%s" % cmsRun



if __name__ == '__main__':
    valid = ["scenario=", "reco", "aod", "miniaod","dqm", "dqmio", "no-output",
             "global-tag=", "lfn=", "alcarecos=" ]
    usage = \
"""
RunPromptReco.py <options>

Where options are:
 --scenario=ScenarioName
 --reco (to enable RECO output)
 --aod (to enable AOD output)
 --miniaod (to enable MiniAOD output)
 --dqm (to enable DQM output)
 --dqmio (to enable DQMIO output)
 --no-output (create config with no output, overrides other settings)
 --global-tag=GlobalTag
 --lfn=/store/input/lfn
 --alcarecos=plus_seprated_list

Example:

python RunPromptReco.py --scenario=cosmics --reco --aod --dqmio --global-tag GLOBALTAG --lfn=/store/whatever --alcarecos=TkAlCosmics0T+MuAlGlobalCosmics

python RunPromptReco.py --scenario=pp --reco --aod --dqmio --global-tag GLOBALTAG --lfn=/store/whatever --alcarecos=TkAlMinBias+SiStripCalMinBias

"""
    try:
        opts, args = getopt.getopt(sys.argv[1:], "", valid)
    except getopt.GetoptError, ex:
        print usage
        print str(ex)
        sys.exit(1)


    recoinator = RunPromptReco()

    for opt, arg in opts:
        if opt == "--scenario":
            recoinator.scenario = arg
        if opt == "--reco":
            recoinator.writeRECO = True
        if opt == "--aod":
            recoinator.writeAOD = True
        if opt == "--miniaod":
            recoinator.writeMINIAOD = True
        if opt == "--dqm":
            recoinator.writeDQM = True
        if opt == "--dqmio":
            recoinator.writeDQMIO = True
        if opt == "--no-output":
            recoinator.noOutput = True
        if opt == "--global-tag":
            recoinator.globalTag = arg
        if opt == "--lfn" :
            recoinator.inputLFN = arg
        if opt == "--alcarecos":
            recoinator.alcaRecos = [ x for x in arg.split('+') if len(x) > 0 ]

    recoinator()
