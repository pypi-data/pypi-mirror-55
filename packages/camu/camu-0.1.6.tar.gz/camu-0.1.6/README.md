<p align="center">
  <img height="200" src="images/CaMu_py.png" alt="Camu Logo"/>
</p>

# Installation

`CaMu.py` can easily be installed using pip. Just run the command:

```bash
pip install camu
```

pip will automatically install the required versions of the python packages that are included within `CaMu.py`.

Additionally, it is necessary to have **samtools** >= 0.1.19 and **gatk**>=4.1.2 installed and added to the path.

# Usage

After installing `CaMu.py`, the main module `camu` can be run via
```bash
python3 -m camu <additional parameter>
```

Giving *-h* or *--help* as additional parameter opens the help page.

Here you can see all additional parameters you need to pass in order to run `camu`.

For the overall script it is necessary to provide a text file giving the paths all samples VCF files in column 1 and the corresponding BAM files in column 2 with *-i*.

Additionally, the path to the control BAM file has to be provided via *-c*.

Finally, the path to the reference genome has to be given with *-r*.

If you want to run any script separately, you can call the script using

```bash
python3 -m <scriptname>
```

where \<scriptname\> has to be exchanged by one of the 5 modules given below (`preprocessing.py`, `filterDupAndLinked.py`, etc.).

# Filtering false-positive candidate mutations to accelerate DNM-counting for direct µ estimates

For direct estimation of the spontaneous mutation rate µ, it is necessary to calculate the rate of spontaneous de-novo mutations (DNM) occuring per site per generation.
Consequently, counting DNM is essential for estimating µ.

The raw approach is:
* Sequencing samples and control --> FASTQ files
* Assembly of sequencing results --> BAM files
* perform some filtering steps
* Variant calling 
* extraction of variants occurring in samples but not in control --> candidate mutations

The resulting list of candidate mutations (CM) currently has to be manually curated using a genome browser like IGV.

Unfortunately, approx. 90 % of these CM are no true DNM, they turn out to be false-positives.

**CaMu.py** aims to accelerate the whole procedure of DNM counting by filtering out the vast majority of false-positive CM and by preparing the remaining CM for fast manual curation with IGV. 

**CaMu.py** consists of 5 main Python modules:
1. `preprocessing.py`
2. `filterDupAndLinked.py`  
3. `detectFIO.py`
4. `snapshotIGV.py`
5. `IGVsessions.py`


`preprocessing.py` starts with an input text file containing paths to all sampels' VCF files in column 1 and paths to all corresponding BAM files in column 2.
These VCF and BAM files are fread out nd further processed in order to find variants that are possible DNM - the candidate mutations CM.

The rough is approach is the following:

<p align="center">
  <img height="200" src="images/Preprocessing.png" alt="Preprocessing pipeline"/>
</p>

The following scripts within `CaMu.py` further filter the CM for those that fully linked to other mutations, those that are only included due to reads that are most probably PCR duplicates and for those variants occurring in other samples or several times in the control sample's BAM file.

Finally, for all the remaining CM IGV Sessions and IGV snapshots are created within `IGVsessions.py` and `snapshotIGV.py` to further simplify the manual curation of the remaining CM.

Here is an overview:

<p align="center">
  <img height="200" src="images/workflowCaMu.png" alt="CaMu overview"/>
</p>




