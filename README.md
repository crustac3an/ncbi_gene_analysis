# Setting up
Setting up the analysis environment should be straight forward, if both docker and docker compose have been configured - `docker compose up` and then connect to `http://127.0.0.1:8888/lab?token=docker`. 

**Auth/Security**  
The compose environment is assumed to be ran solely in local isolated system without any outside exposure, thus security considerations were skipperd. One can also use the accompanied pyproject.toml and poetry to setup a virtual environment managed by poetry.

# Analysis
All the results should be reproducable just by running `gene_expression_analysis.ipynb` noteoobk within jupyter-lab, after connecting to it. Some of the analysis might take a while, but it should all run in less than an hour.

**Data**  
Data should be in the working directory under `./data` folder. The data folder has to be created manually and the data uploaded there (either by having access to the data download link or scraping it - see below about scraping).

**Results**  
Results of the analysis are found under "Tests for expression thresholds" and 4 different methods for finding negatively expressed genes (normal tissues) and highly expressed genes (reprogrammed tissues) were considered:

1. Z-scored based filtering of highly and negatively expressed genes
2. Bimodal distribution based filtering of highly and negatively expressed genes
3. Quantile based filtering of highly and negatively expressed genes
4. Grid search based filterig of highly and negatively expressed genes

**Intepretation**  
It was hard to find a gene that was negatively expressed in all of the normal tissue samples and highly expressed in all of the reprogrammed ones (*counts if it is expressed on one of the days per reprogrammed sample*). Thus, a relaxation was done where for the negatively expressed a lower share was ok and the limit was set at 80%. This can be adjusted at the start of the notebook with the default value settings.

# Scraping data
Some wip tooling for data scraping are provided, but it is not recommoneded to be used, because it does hit the rate limits and there are more offical ways of getting it.