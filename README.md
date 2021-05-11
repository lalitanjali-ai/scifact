
## ***INTRODUCTION***

The recent increase in misinformation has stimulated research in fact checking, which is the task of assessing the truthfulness of a sentence or a claim.
Companies such as Facebook and Twitter are prioritizing the implementation of fact checking algorithms to decrease the spread of fake news.

I am trying to solve a similar problem but in the domain of scientific literature. 
Due to rapid growth in the scientific literature, it is difficult for researchers and the general public even more so, to stay up to date on the latest findings. This challenge is especially acute during public health crises like the current COVID-19 pandemic. This is due to the extremely fast rate at which new findings are reported and the risks associated with making decisions are based on outdated or incomplete information. In this project, I am building a tool to assist researchers and the public in evaluating the correctness of scientific claims.

## ***LINKS***

**The project documentation can be found at**: https://lalitanjali-ai.github.io/scifact/

**PPT Presentation**: https://drive.google.com/file/d/1LEctjJUwYvr0pfQY_3W6kHB_0dPH10s0/view?usp=sharing

**Video presentation**: https://youtu.be/j6jMqDcav1w

## ***RUN IT YOURSELF***

**STEP 1**: Download required packages from the pipfile
pipenv install

**STEP 2**: Run Luigi Pipeline
pipenv run python -m scifact

If required, you can download the Dataset and Models using the following links:

arxiv dataset: https://advancedpythonmeenu.s3.us-east-2.amazonaws.com/scifact/arxivData.json

label_predicion_model: https://advancedpythonmeenu.s3.us-east-2.amazonaws.com/scifact/label_roberta_large_fever_scifact.zip

rationale_selection_model: https://advancedpythonmeenu.s3.us-east-2.amazonaws.com/scifact/rationale_roberta_large_fever.zip

