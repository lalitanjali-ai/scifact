import re
import ast
import pandas as pd
import arxiv
from scipy import spatial
import textract
import os
from scifact.model.label import Label_sentences,encode

import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

print("current working directory model:",os.getcwd())

class pretrained_model():
    def __init__(self):

        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.model_roberta = torch.load(os.getcwd()+"/rationale_roberta_large_fever/pytorch_model.bin", map_location='cpu')
        self.tokenizer = AutoTokenizer.from_pretrained(os.getcwd()+"/rationale_roberta_large_fever/")
        self.model = AutoModelForSequenceClassification.from_pretrained(os.getcwd()+"/rationale_roberta_large_fever/").to(self.device).eval()

    def printwd(self):
        print("working directory pre_trained model:",os.getcwd())

    def cosine_pipeline(self, doc_query, references2, top_matches, data_copy):
        # preprocess the given claim/query
        all_ref = self.preprocess_query(str(doc_query))

        # Extract all relevant references for the claim/query
        ref_str_new, ref_text_list = self.download_all_ref_content(all_ref, references2, data_copy)

        # Processing the ref_text_list for distance methods
        # Converting list of lists into single list
        all_ref_text = []
        for index, row in ref_text_list.iterrows():
            text = row['Text']
            text = ast.literal_eval(text)
            all_ref_text.extend(text)

        self.find_extracts_labels(doc_query, all_ref_text, top_matches)

    # function to pre-process the doc-query
    def preprocess_query(self,doc_query):
        # Extracting only the citations from the query
        match = re.search(r'\[.*?\]', doc_query)

        # Printing the extracted citations from the query
        if match:
            print(match.group())

        test_string = match.group()
        temp = re.findall(r'\d+', test_string)
        all_ref = list(map(int, temp))

        return (all_ref)

    def download_all_ref_content(self, all_ref, references2, data_original):
        ref_str = ''
        ref_text_list = pd.DataFrame(columns=['Ref_no', 'Text'])
        for i in (all_ref):
            # Find the i'th reference in all references
            match = re.search(r"(?<=\[%s\])(.*\n){3}" % i, references2, re.IGNORECASE)

            if match:
                file_to_match = (match.group())

                # Remove \n from the str
                file_to_match = file_to_match.replace('\n', ' ')
                file_to_match = re.sub(u'\u201c', '"', file_to_match)
                file_to_match = re.sub(u'\u201d', '"', file_to_match)

                print("file_to_match:", file_to_match)
                print("ref_number:", i)
                quotes = re.findall(r'["](.*?)["]', file_to_match)
                if quotes:
                    quotes = quotes[0]
                    # Removing punctuation from quotes
                    quotes = quotes[:-1]
                    # print("quotes 1:",quotes)

                else:
                    quotes = file_to_match.partition("\"")[2][:-1]

                # extracting the ith reference from the references part of the pdf and mapping it in the arxiv database
                df1 = data_original[data_original['title'].str.contains(quotes)]
                reference_id = {"id": list(df1['id'])[0]}
                reference_get = next(arxiv.Search(id_list=[reference_id['id']]).get())
                paper_reference = reference_get.download_pdf()
                link = os.getcwd() + paper_reference[1:]

                # Downloading the pdf and extracting the content
                ref_text = textract.process(link, method='pdfminer')

                # Convert text type from bytes to string
                ref_text = ref_text.decode("utf-8")
                data = ref_text.replace('\x0c', '')

                # Considering text between abstract and conclusion
                pos = data.lower().find('abstract')
                pos_ack = data.lower().find('conclusion')
                data = data[pos + len('ABSTRACT'):pos_ack + len('conclusion')]

                data = data.replace('\x0c', '')
                data = data.replace("\r+", " ")
                data = data.replace('\s{3,}', '\n ')
                data = data.replace('\n\n', ' ')
                data = data.replace('\n\s*\n', ' ')
                data = data.replace('\n+', ' ')
                data = data.replace('\n', ' ')
                data = data.replace('\\n', ' ')
                data = data.replace('  ', ' ')
                data = re.sub(r'\s*-\s*', '', data)

                # Removing text inside () and [] in order to remove citations
                data = re.sub(r'\([^)]*\)', '', data)
                data = re.split('\.\s+', data)

                ref_str = ref_str + str(data)
                ref_text_list = ref_text_list.append({'Ref_no': i, 'Text': str(data)}, ignore_index=True)

        return (ref_str, ref_text_list)

    # Function to find cosine similarity given doc query, all ref text and top matches
    def find_extracts_labels(self, doc_query, all_ref_text, top_matches_entered):
        ref_str = str(all_ref_text)
        arxiv_test = pd.DataFrame({'claim': doc_query, 'sentences': [ref_str]})

        # Find evidences using Cosine similarity sentence selection:
        top_matches = 10
        arxiv_test["cosine_evidence"] = self.Cosine_Evidence_Selection(top_matches, arxiv_test)

        print(arxiv_test.shape)
        # Label evidences :
        top_matches = top_matches_entered
        arxiv_test['predicted_labels'] = Label_sentences(arxiv_test)

        print("The claim entered is:", arxiv_test.claim[0], "\n")
        print("The matched extracts are:\n\n")

        for i in range(top_matches):
            print("extract:", arxiv_test.cosine_evidence[0][i][0])
            print("manhattan_dist:", arxiv_test.cosine_evidence[0][i][1], "\n")


    def Cosine_Evidence_Selection(self, top_matches, df):
        number_top_matches = top_matches
        cosine_evidence = []

        for i in range(len(df)):
            sentences = df['sentences'][i]
            sentences = ast.literal_eval(sentences)
            claim = df['claim'][i]

            # Create embeddings of all sentences in the sentences list
            sentence_embeddings_new = []
            for i in range(len(sentences)):
                sentence_embeddings_new.append(
                    self.tokenizer.encode(sentences[i], padding='max_length', max_length=512, add_special_tokens=True,
                                     truncation=True))

            # Create query/claim embeddings
            query_embeddings = self.tokenizer.encode(claim, padding='max_length', max_length=512, add_special_tokens=True)

            results = []
            c = 0
            for i in range(len(sentences)):
                distances = spatial.distance.euclidean(sentence_embeddings_new[i], query_embeddings)
                results.append([sentences[i], distances])
                c += 1

            results.sort(key=lambda i: i[1], reverse=True)

            cosine_evidence.append(results[0:number_top_matches])

        return cosine_evidence

    def Cosine_Evidence_Selection_predict(self, df):

        with torch.no_grad():
            for i in range(len(df)):
                data = df.sentences[i]
                selection = df.cosine_evidence[i]
                claim = df.claim[i]

                evidence = ''
                for i in range(len(selection)):
                    evidence += str(selection[i][0])

                encoded_dict = encode([evidence], [claim])

        return encoded_dict


