# RNA-Seq_tuxedo
Using tophat, cufflinks, cuffmerge, and cuffdiff you can analyze your RNA-Seq data starting from fastq files. See Trapnell et al. 2014 for more information (http://www.nature.com/nprot/journal/v7/n3/abs/nprot.2012.016.html).


This python code is a pipeline that can unzip fastq files and call tophat (https://ccb.jhu.edu/software/tophat/index.shtml), cufflinks (http://cole-trapnell-lab.github.io/cufflinks/), cuffmerge (http://cole-trapnell-lab.github.io/cufflinks/cuffmerge/) and cuffdiff (http://cole-trapnell-lab.github.io/cufflinks/cuffdiff/) automatically. Note that tophat, cufflinks and cuffdiff can take a long time to run. All of these are called using default settings. Feel free to adjust the code if you want to add additional parameters (open the python script and search for the keyword parameters and follow the instructions). I recommend then using R and cummeRbund to process the resulting data. Use the cummeRbund manual for more information (http://bioconductor.org/packages/2.11/bioc/vignettes/cummeRbund/inst/doc/cummeRbund-manual.pdf).


You will need two files in addition to the python script (runtuxedosuite.py): a filenames file and a directory list file. 


####Filenames file (Ex:filenames.csv)
One will contain a tab delimited .csv file (with Unicode UTF-8 character sets) that has a header for each of the columns (3 or 4 columns total). The first column contains a unique idenifier (with no spaces) for each of your samples (including replicates, ex: MEF_1, MEF_2, etc.). The second column has a unique identifier to group each of your replicates (ex.: MEF). The third and fourth column identify which fastq files corresponds to each replicate/sample (ending in fastq or fq, if it's compressed do not include the file extension --> if your file is sample1.fastq.gz only type sample1.fastq). You will have 4 columns if you have paired end reads (one column per fastq file). 


####Directories file (Ex: directoryfile.txt)
This file contains 4 different items on separate lines (it's important to maintain the following order): 

1.  The first item will be the working directory. This is the directory where everything will be saved.

2.  The second item is the directory and name of the genome you will be using (please include the name but no extension, ex: if you are using mouse (mm10.fa), type: /this/is/where/the/genome/is/mm10).

3.  The third item is the gene annotation file (.gtf file). Please include the directory, name and extension (.gtf) of the file.

4.  The fourth item is the directory that contains your fastq files.

The python script will ignore blank lines and lines beginning with a '#'.

####Running the code
To run the pipeline, type:
python runtuxedosuite.py filenames.csv directoryfile.txt

**Ex:** python ~/Desktop/runtuxedosuite.py ~/Desktop/filenames.csv ~/Desktop/directoryfile.txt

The script will then ask you a series of yes or no questions. Please type 'y' for yes and 'n' for no. Hit enter after each, if you deviate from this the program will stop running. Finally it will ask how many threads you want to programs to use (type a numerical number, default is 1 we typically use 8).

####Program versions
What programs and versions this script currently works with:
Ubuntu 15.10
Python 2.7.10
Bowtie2 2.2.5 (http://bowtie-bio.sourceforge.net/bowtie2/index.shtml)
Tophat 2.1.0
Cufflinks 2.2.1
Cuffmerge 1.0.0
Cuffdiff 2.2.1

If you are able to run this script on versions other than the ones listed above, please email me at anna.kropornicka (at) gmail.com and I will update this list.

All outputs can be fed into R and used with cummeRbund (http://compbio.mit.edu/cummeRbund/). The current pipeline does not run R and all subsequent analysis.

####Sequences and annotation files
You can download sequence and annotation files from: http://useast.ensembl.org/info/data/ftp/index.html?redirect=no
OR: http://hgdownload.cse.ucsc.edu/downloads.html

####Other notes
This script assumes you have already successfully installed all necessary programs and their dependencies (see the paper by Trapnell et al., 2014 - http://www.nature.com/nprot/journal/v7/n3/full/nprot.2012.016.html). If there are any bugs (I am not an expert) please email anna.kropornicka (at) gmail.com and I will try to get to them asap. Good luck!
