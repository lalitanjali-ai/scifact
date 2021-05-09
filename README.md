The project documentation can be found at: https://lalitanjali-ai.github.io/scifact/index.html

## **INTRODUCTION**

The recent increase in misinformation has stimulated research in fact checking, which is the task of assessing the truthfulness of a sentence or a claim.
Companies such as Facebook and Twitter are prioritizing the implementation of fact checking algorithms to decrease the spread of fake news.

I am trying to solve a similar problem but in the domain of scientific literature. 
Due to rapid growth in the scientific literature, it is difficult for researchers and the general public even more so, to stay up to date on the latest findings. This challenge is especially acute during public health crises like the current COVID-19 pandemic. This is due to the extremely fast rate at which new findings are reported and the risks associated with making decisions are based on outdated or incomplete information. 
I am building a tool to assist researchers and the public in evaluating the correctness of scientific claims.

### Understanding the problem

![](.README_images/5c2e82ee.png)
Fig 1

The task is to select abstracts from the research literature containing evidence that SUPPORTS or REFUTES a given scientific claim, and to identify rationales justifying each decision.

If you look at the Fig 1 above, the scientific paper contains references from numbers 1-7.
On the left of the figure, you can see that the scientific paper contains a sentence that says ”Cardiac injury is common in critical cases of covid 19." It contains the citation numbers 3 and 7 within the sentence. 
The user wants to verify the correctness or veracity of this claim.

This project will detect the citations within this sentence, i.e it will automatically detect that the 3rd and 7th references have been cited, will download these cited documents automatically from the internet and then utilizes the pre-trained models to check if the veracity of the claim.
There are 2 models that will be required for this project:
1) The first model is the Rationale Selection Model: 
   This will look at the claim and select sentences from the cited documents that closely correspond to it. Here on the left, you can see that the rationale selected is “More severe Covid 19 infection…”
2) The second model is the Label Prediction Model: 
   This model will look at the sentences selected by the Rational Selection Model and will tell you if the sentences approve or deny the claim. On the left of the diagram, you can see that the rationale sentence selected supports the claim. This is the decision of the model.


### Workflow

![](.README_images/213585e8.png)
Fig 2

Step 1: Download the model and dataset. 
The two models are Rationale Selection and Label Prediction. We also download a dataset called the Arxiv dataset.

Step 2: Preprocess the arxiv dataset.
Arxiv is an open-access repository which hosts all the scientific papers. The arxiv dataset primarily contains information of all the scientific papers such as their titles, authors and links to download the papers.
If the user wants to verify a claim containing a citation to a paper called “Dual Recurrent Attention Units”, the program will first look this up in this dataset. You can see that the title corresponds to the fist item in the dataset in Fig 2 above. The program will then use the "pdflink" found in the dataset and download the document automatically from the internet. 
Downloading only the required pdfs that are cited within the claim/query helps save search time and space.

Step 3: Capture User Input
The user enters the claim(which is a sentence) to be verified.
The user also enters the name of the scientific paper this claim exists in and the number of top matched abstracts the user would like to view.

Step 4: Program parses user input
The program parses the user input, preprocesses the claim and recognizes the citations within it using regular expressions. There are multiple ways to cite a document. The citations such as [int,int..] work with this project where each int can be referenced to a document by parsing the References section of a scientific document.

Step 5: Download cited documents
The program looks up these citations in the arxiv dataset and downloads them.

Step 6: Implement models and find abstracts that verify the claim
The program uses the pretrained models to find relevant sentences that support the claim and also display the results to the user.






