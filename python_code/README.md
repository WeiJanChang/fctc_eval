MPH Dissertation
======
by Wei-Jan, Chang (cc9868422@gmail.com/ wei-jan.chang@ucdconnect.ie)

* Originated from [mph_dissertation](https://bitbucket.org/wei-janchang/mph_dissertation/src/master/), rewrite and clean git history in current version
* Pipeline for Dissertation in Master of Public Health


How do I get set up?
======

Installations
----

Download and install Git: https://git-scm.com/downloads

Download and install Miniconda: https://docs.conda.io/en/latest/miniconda.html


Conda environment setup
----
see the python packages that required in [requirements.txt](/requirements.txt)

```bash
conda create -n mph_dissertation
conda activate mph_dissertation
conda install python=3.8.12 pip
pip install -r requirements.txt
```

* setup

```bash
python setup.py develop
```

Module used for data visualization and analysis
=====

## masking

- `utility.py`:

## ratified date

- `WHOFCTC_parties_date.py`: 

## analysis
- `analysis.py`

How to run the main script?
=====

### DATA STRUCTURE

- **Suite2p output**: ED_ID(i.e., 210315_YW006) / suite2p / plane{'x'}/
- **Analysis output**: ED_ID / plane{'x'}
- **Population analysis(ETL concat)**: ED_ID / concat_plane*
- **Analysis cache**: Behavioral cache save in STIMPY_ROOT, whereas binned calcium activities cache save in S2P_ROOT
- Check source code in the `cli.py` and `cli_output.py`
- See also the example in the [bash script](/bash_script/dev_branch)
  ```bash
  python -m <module.py> <subparser> \
  -S $STIMPY_ROOT -S $S2P_ROOT -D $EXP_DATE -A $ANIMAL_ID <options>
  ```