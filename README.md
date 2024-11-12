Assessing the impact of the WHO Framework Convention on Tobacco Control on Prevalence of Tobacco Use and Cardiovascular Disease Mortality.
===
by [Wei Jan, Chang](mailto:weijan.chang@gmail.com)

# Data Source

Download raw data from open access database:

* [WHO Mortality Database](https://platform.who.int/mortality/themes/theme-details/topics/topic-details/MDB/cardiovascular-diseases)
* [WHO The Global Health Observatory](https://www.who.int/data/gho/data/themes/topics/sdg-target-3_a-tobacco-control)
* [Signature and Ratification of FCTC from UN](https://treaties.un.org/pages/ViewDetails.aspx?src=TREATY&mtdsg_no=IX-4&chapter=9&clang=_en)

# Installation

Download and install [Git](https://git-scm.com/downloads)
Download and install [Python](https://www.python.org/downloads/)

```
conda create -n [ENV_NAME] python=3.10 
conda activate [ENV_NAME]  
cd [CLONED_DIRECTORY]
pip install -r requirements.txt
```

- Buildup the src path

```
conda install conda-build
conda develop src
cd src
```

# Usage

## Cleaning process

`from utility import select_df`

## Preprocess the WHO CVD mortality data

`from utility import preprocess_cvd, create_age_grouping`

## Preprocess the Prevalence of Tobacco Use data

run cleaning process first and `from utility import tobacco_layout_modified`

## Merge CVD df and tobacco df

`from utility import tobacco_layout_modified`

## Determine countries who signed the WHO FCTC treaty

`WHOFCTC_parties_date.py`

# Data visualization

## Preprocess

`preprocess_analysis.py`

## create figures

`ploy.py`