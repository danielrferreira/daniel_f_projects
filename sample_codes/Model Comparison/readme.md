# Model Comparison

This code came from my [pySETTV](https://github.com/danielrferreira/pySETTV/tree/main/05%20-%20Validate/Model%20Comparison) repository. I noticed a gap when moving from SAS Miner to R and Python, so I decided to create a class with some functions to compare models. It focuses on categorical outcomes and contains:

- Table with many fit statistics accross all models and datasets (e.g. Train, Validation, Test), formatted to highlight best models.
- Graph with all fit statistics by model and datasets
- ROC curve comparison + Area under curve

The py file contains a class called problem and the notebook show how to import and use it. 
