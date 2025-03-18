# uni-data-driven-dm
This repository contains script for analysis of the [LastFM Asia Social Network](http://snap.stanford.edu/data/feather-lastfm-social.html) data set. 

## Table of Contents
1. [Overview](#overview)
2. [Installation](#installation)
3. [Usage](#usage)

## Overview

The repository consists of the two major parts:
1. `app` - Includes the implementation of methods / function used for the analysis of the data set.
2. `scripts` - Contains all the actual scripts that can be run to analize the graph.

The graph (data set) is located in the [data/](data) folder. Note that dutring the analysis, we consider the networks as an undirected, unweighted, and with no attributes. 

## Installation

The required Python version is `3.12.7`

1. Clone the repo
```sh
git clone https://github.com/baby-platom/uni-data-driven-dm.git
```

2. Create virtual environment and install the dependencies
```sh
python -m venv myenv
source myenv/bin/activate

pip install -r requirements.txt
```

Optionally: 
- Create the `.env` file based on the [configs](app/configs.py)
- Use [uv](https://docs.astral.sh/uv/) for dependencies management

## Usage

Review the [scripts/](scripts) folder: every `.py` file there is a script that you can run to calculate some metric(s) of a graph. To see the results, look into a corresponding `.log` file in the [scripts/logs/](scripts/logs) folder and if applicable, in the [plots/](plots) folder to review plots and visulizations of calculated statistics.