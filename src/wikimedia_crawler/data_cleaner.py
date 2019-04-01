import sys
import os
import json

def clean_file(src, dest):

    with open(src, 'r') as rfp:
        json_obj = json.load(rfp)
    
    wikitext = json_obj['parse']['wikitext']['*']
    
    with open(dest, 'w') as wfp:
        wfp.write(wikitext)

def create_cleaned_files(src_dir, dest_dir):

    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    for filename in os.listdir(src_dir):

        fname, _ = os.path.splitext(filename)

        src = os.path.join(src_dir, filename)
        dest = os.path.join(dest_dir, fname + '.txt')
        clean_file(src, dest)
    
def main():

    src_dir = sys.argv[1]
    dest_dir = sys.argv[2]

    create_cleaned_files(src_dir, dest_dir)

main()
