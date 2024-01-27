# Setting up
Setting up the analysis environment should be straight forward, if both docker and docker compose have been configured - `docker compose up` and then connect to `http://127.0.0.1:8888/lab?token=docker`. 

**Auth/Security**  
The compose environment is assumed to be ran solely in local isolated system without any outside exposure, thus security considerations were skipperd. One can also use the accompanied pyproject.toml and poetry to setup a virtual environment managed by poetry.

# Analysis
All the results should be reproducable just by running `gene_expression_analysis.ipynb` noteoobk within jupyter-lab, after connecting to it. Some of the analysis might take a while, but it should all run in less than an hour.

**Assumptions**  
Data should be in the working directory under `./data` folder.

**Results**  
Results of the analysis are found under "Tests for expression thresholds" and 4 different methods for finding negatively expressed genes (normal tissues) and highly expressed genes (reprogrammed tissues) were considered:

1. Z-scored based filtering of highly and negatively expressed genes
2. Bimodal distribution based filtering of highly and negatively expressed genes
3. Quantile based filtering of highly and negatively expressed genes
4. Grid search based filterig of highly and negatively expressed genes

# Scraping data
Some wip tooling for data scraping are provided, but it is not recommoneded to be used, because it does hit the rate limits and there are more offical ways of getting it.