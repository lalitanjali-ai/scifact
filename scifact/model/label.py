#Load pretrained model
model_label_roberta = torch.load("/content/datasets/label_roberta_large_fever_scifact/pytorch_model.bin")

tokenizer = AutoTokenizer.from_pretrained("/content/datasets/label_roberta_large_fever_scifact")
config = AutoConfig.from_pretrained("/content/datasets/label_roberta_large_fever_scifact", num_labels=3)
model = AutoModelForSequenceClassification.from_pretrained("/content/datasets/label_roberta_large_fever_scifact", config=config).eval().to(device)

LABELS = ['REFUTES', 'NOT ENOUGH INFO', 'SUPPORTS']


# Function to encode all sentences in a pdf and the claim into a dict which will later be used for training
def encode(sentences, claims):
    text = {
        "claim_and_rationale": list(zip(sentences, claims)),
        "only_claim": claims,
        "only_rationale": sentences
    }['claim_and_rationale']

    encoded_dict = tokenizer.batch_encode_plus(
        text,
        max_length=512,
        padding='max_length',
        truncation_strategy='only_first',
        truncation=True,
        return_tensors='pt'
    )

    if encoded_dict['input_ids'].size(1) > 512:
        encoded_dict = tokenizer.batch_encode_plus(
            text,
            max_length=512,
            padding='max_length',
            truncation_strategy='only_first',
            truncation=True,
            return_tensors='pt'
        )

    encoded_dict = {key: tensor.to(device)
                    for key, tensor in encoded_dict.items()}
    return encoded_dict


#Labeling cosine_similarity sentences

def Label_sentences(df):
  results=[]
  with torch.no_grad():
    for i in range(len(df)):
      data=df.sentences[i]
      selection=df.cosine_evidence[i]
      claim=df.claim[i]

      evidence=''
      for i in range(len(selection)):
        evidence+=str(selection[i][0])

      encoded_dict = encode([evidence], [claim])
      label_scores = torch.softmax(model(**encoded_dict)[0], dim=1)[0]
      label_index = label_scores.argmax().item()
      label_confidence = label_scores[label_index].item()
      if len(data)==0:
        results.append({'label': 'NOT ENOUGH INFO', 'confidence': 1})
      else:
        results.append({'label': LABELS[label_index], 'confidence': round(label_confidence, 4)})

  return results
