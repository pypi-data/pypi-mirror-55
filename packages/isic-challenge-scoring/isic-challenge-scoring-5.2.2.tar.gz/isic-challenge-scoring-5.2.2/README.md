# ISIC: Skin Lesion Analysis Towards Melanoma Detection Scoring

[![CircleCI](https://circleci.com/gh/ImageMarkup/isic-challenge-scoring.svg?style=svg)](https://circleci.com/gh/ImageMarkup/isic-challenge-scoring)
[![GitHub license](https://img.shields.io/badge/license-Apache%202-blue.svg)](https://raw.githubusercontent.com/ImageMarkup/isic-challenge-scoring/master/LICENSE)

Automated scoring code for the [ISIC Challenge](http://challenge.isic-archive.com).

## Installation
### Python
```bash
pip install isic_challenge_scoring
```

### Docker
```bash
docker pull isic/isic-challenge-scoring:latest
```

## Usage
### Python
#### Segmentation (Task 3)
```bash
isic-challenge-scoring classification /path/to/ISIC_GroundTruth.csv /path/to/ISIC_prediction.csv
```
