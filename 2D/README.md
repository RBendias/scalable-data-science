# Spatial Analysis Instructions


The goal of the task is to determine the number of tweets sent per neighborhood using the GeoSaprk library. To do this, we use a data set consisting of the coordinates of the tweets and the polygon data of the new yorks neighborhoods. 


### Requirements
This code is written in Python 3 and GeoSpark. For running the code the open-source web application Jupyter Notebook is needed. For instance, you can install the [machine learning workspace](https://github.com/ml-tooling/ml-workspace) docker container, with jupyter notebook and machine learning tools pre-installed.

Please download the nyc-data folder provided on ISIS.

To use GeoSpark in combination with Jupyter Notebooks you need to set environment variables and install Python libraries. Use the creat_env environment file for this and follow some steps:
1. Run `conda environment conda env create -f create_env.yml` from the current directory 
2. Activate the installed environment with `conda activate geospark_demo`
3. Run `pip install envkernel`
4. Create a new kernel with `envkernel conda --name conda_test_kernel /opt/conda/envs/geospark_demo/`


### Run
To execute the code first select the *geospark_demo* kernel in the juptyer notebook and then run all cells. Depending on the data storage location, the data path in the notebook must be adjusted.  
