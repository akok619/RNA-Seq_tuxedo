# This script was created by Anna Kropornicka from UW-Madison
# To run type: python runtuxedosuite.py filenames.csv directoryfile.txt


import sys, csv, subprocess


# Creates lists (samplenames, combonames, fastqfiles1, fastqfiles2) of files using the filenames.csv
def extractfilenames(pairedend):

    samplenames = []
    combonames = []
    fastqfiles1 = []
    fastqfiles2 = []

    with open(sys.argv[1],'r') as f1:
    
        file1 = csv.reader(f1,delimiter='\t')
        next(file1) # skip header

        if pairedend == 'y':
            samplenames, combonames, fastqfiles1, fastqfiles2 = zip(*file1) # creates tupules

        elif pairedend == 'n':
            #print zip(*file1)
            samplenames, combonames, fastqfiles1 = zip(*file1) # creates tupules

        else:
            sys.exit('You typed something incorrect. Rerun the code.')

    #print samplenames,combonames,fastqfiles1
    return samplenames,combonames,fastqfiles1,fastqfiles2

# Creates a list of working directories using the directoryfile.txt
def extractdirectories():
    directories = []
    with open(sys.argv[2],'r') as f2:
        lines = filter(None, (line.rstrip() for line in f2))
        #print lines
        for x in lines: # can i iterate over lines similarly as I would for f2?
            if x[0] == '#':
                pass
            else:
                directories.append(x)

    return directories

# Asks user if fastq files are compressed and how many threads to use
def userquestions(filedir):

    compress = raw_input("Are your fastq files compressed? (y/n) ")
    if compress == 'y':
        end = raw_input("What is the file extension? (Ex.: .gz) ")
        bashCommand = "gunzip "+filedir+"*"+end
        runcommand(bashCommand)
    elif compress == 'n':
        pass
    else:
        sys.exit('You typed something incorrect. Rerun the code.')
    threads = raw_input("How many threads should the programs use? (Typically we use 8): ")
    return threads

# Runs commands
def runcommand(bashCommand):
    
    print 'Now running:'
    print bashCommand
    process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
    output = process.communicate() [0]

# Runs tophat 
def runtophat(samplenames,fastqfiles,filedir,threads):

    print 'Now running Tophat'
    print

    for x,y in zip(samplenames,fastqfiles):
        fileout = filedir[0]+'tophat/'+x+'_thout'
        fastqs = filedir[3]+y
        
        # tophat: If you want to add additional parameters please append it to the end using: + "parameters"
        # example: bashCommand = "tophat -p "+threads+" -G "+filedir[2]+" -o "+fileout+" "+ filedir[1] + " " + fastqs + " -p parameter"
        bashCommand = "tophat -p "+threads+" -G "+filedir[2]+" -o "+fileout+" "+ filedir[1] + " " + fastqs
        runcommand(bashCommand)

# Runs cufflinks and generates the assemblies.txt file for cuffmerge
def runcufflinks(samplenames,filedir,threads):
    
    print 'Now running Cufflinks'
    print

    assemlist = []
    thlist = []

    for x in samplenames:
        filetopout = filedir[0]+'tophat/'+x+'_thout/accepted_hits.bam'
        filecuffout = filedir[0]+'cufflinks/'+x+'_clout'

        # cufflinks: If you want to add additional parameters please append it to the end using: + "parameters"
        # example: bashCommand = "cufflinks -p "+threads+" -o "+filecuffout+" "+ filetopout + " -p parameter"
        bashCommand = "cufflinks -p "+threads+" -o "+filecuffout+" "+ filetopout
        runcommand(bashCommand)

        assemlist.append(filecuffout+'/transcripts.gtf')
        thlist.append(filetopout)

    with open(filedir[0]+'assemblies.txt','w') as f:
        f.write('\n'.join(assemlist))

    return thlist

# Runs cuffdiff and generates a file called diff_out in your working directory that can be used with cummeRbund in R
def runcuffdiff(combonames,filedir,thlist,threads):

    uniquecombo = set(combonames)
    curlist = []
    outlist = []
    
    for i, (x,y) in enumerate(zip(thlist,combonames)):
        if (i != 0) and (i != len(thlist)-1) and (y != combonames[i-1]): # current comboname is not the same as the previous one
            outlist.append(','.join(curlist))
            curlist = []
            curlist.append(x)
        elif (i != 0) and (i != len(thlist)-1) and (y == combonames[i-1]): # current comboname is the same as the previous one
            curlist.append(x)
        elif (i == len(thlist)-1) and (y != combonames[i-1]):
            outlist.append(x)
        elif (i == len(thlist)-1) and (y == combonames[i-1]):
            curlist.append(x)
            outlist.append(','.join(curlist))
        else: # (i == 0)
            curlist.append(x)

    # cuffdiff: If you want to add additional parameters please append it to the end using: + "parameters"
    # example: runcommand("cuffdiff -o "+filedir[0]+"diff_out -b "+filedir[1]+".fa -p "+threads+" -L "+','.join(uniquecombo)+' -u '+filedir[0]+'merged_asm/merged.gtf '+' '.join(outlist) + " -p parameters")
    runcommand("cuffdiff -o "+filedir[0]+"diff_out -b "+filedir[1]+".fa -p "+threads+" -L "+','.join(uniquecombo)+' -u '+filedir[0]+'merged_asm/merged.gtf '+' '.join(outlist))


def main():

    paired = raw_input("Do you have paired end reads? (y/n) ")

    # What are your sample names and fastq file names?
    samples,cnames,fastqs1,fastqs2 = extractfilenames(paired)

    # What are the directories where files can be found (see example called 'runtuxedodirectories.txt')
    dirs = extractdirectories()
    #print dirs
    # Extract files?
    threads = userquestions(dirs[3])

    # Turn fastq files into a comprehensible thing
    fastqs = []
    if paired == 'y':
        for x,y in zip(fastqs1,fastqs2):
            fastqs = fastqs1+' '+dirs[3]+fastqs2
    else:
        fastqs = fastqs1

    runcommand("mkdir "+dirs[0]+"tophat") # all tophat files can be found in this directory
    runtophat(samples,fastqs,dirs,threads)

    runcommand("mkdir "+dirs[0]+"/cufflinks") # all cufflinks files can be found in this directory

    tophatlist = runcufflinks(samples,dirs,threads) 

# for debugging:
#    tophatlist = []
#    for x in samples:
#        filetopout = dirs[0]+'tophat/'+x+'_thout/accepted_hits.bam'
#        tophatlist.append(filetopout)

    # Runs cuffmerge which generates a file merged_asm/merged.gtf in your working directory
    # cuffmerge: If you want to add additional parameters please append it to the end using: + "parameters"
    # example: runcommand("cuffmerge -g "+dirs[2]+" -s "+dirs[1]+".fa -p "+threads+" "+dirs[0]+"assemblies.txt -o "+dirs[0] + " -p parameters")
    runcommand("cuffmerge -g "+dirs[2]+" -s "+dirs[1]+".fa -p "+threads+" "+dirs[0]+"assemblies.txt -o "+dirs[0])

    runcuffdiff(cnames,dirs,tophatlist,threads)

###########################################################################

if __name__ == "__main__":
    main()
