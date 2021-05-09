import luigi
from scifact.tasks.tasks import find_display_abstracts
import argparse


pdf_name = "Dual Recurrent Attention Units "
doc_query = 'Bilinear representations Fukui et al. [7] use compact bi-linear pooling to' \
            ' attend over the image features and com-bine it with the language representation.'
top_matches = 5

parser = argparse.ArgumentParser("Input query")
parser.add_argument("-p", "--pdf_name", default=pdf_name)
parser.add_argument("-d", "--doc_query", default=doc_query)
parser.add_argument("-t", "--top_matches", default=top_matches)


def main(args=None):
    args = parser.parse_args(args=args)
    luigi.build([find_display_abstracts(pdf_name=args.pdf_name,doc_query=args.doc_query,top_matches=args.top_matches)],local_scheduler=True)




