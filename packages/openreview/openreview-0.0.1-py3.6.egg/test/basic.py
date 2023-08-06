from openreview import extract_forum, extract_note

if __name__ == '__main__':
    results = extract_forum('NeurIPS.cc/2019/Reproducibility_Challenge/-/NeurIPS_Submission')
    print(len(results))
    if len(results):
        print(results[0])
    results = extract_note('SJzWAHHxUr')
    print(len(results))
    if len(results):
        print(results[0])