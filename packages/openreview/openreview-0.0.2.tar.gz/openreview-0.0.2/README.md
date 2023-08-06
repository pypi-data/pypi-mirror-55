# OpenReview Python Client

Unlike other openreview client this doesn't require any webdriver. This package obtain openreview submission through the web api addresses.


## Install

```
pip install openreview
```

## Usage

```
import openreview
submission = openreview.extract_forum('NeurIPS.cc/2019/Reproducibility_Challenge/-/NeurIPS_Submission')
print(len(submission))
```


