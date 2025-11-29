# MLCerts -- Source Code (ICSE 2026)

aux.pdf provides additional supplementary material for the paper.   

## Certificate Datasets

Raw PEM certificates used in differential testing can be downloaded [here](https://zenodo.org/records/15971208).

- 12 synthetic certificate datasets.
- MLCerts 1M dataset.
- Frankencerts 8M dataset.
- Transcert 30K dataset. 

## Differential Testing Framework 

Please refer to [/differential-testing/](/differential-testing/README.md) directory. 

## Language Models

The code, documentation and saved models are available together for download [here](https://zenodo.org/records/15971208).  

## Code for Paper Results

Please refer to [/paper-code/](/paper-code/README.md) directory. 

We use IPython Notebooks for producing paper results. The scripts used for different purposes are indexed below:   

1. Certificate corpus analysis: Tables 1 and 3
2. Graphs/Graph-DiscrepanciesVSCoverage: Figure 2
3. Graphs/Graph-Matrix: Figure 3
4. Graphs/Graph-Temperature: Figure 4
5. Graphs/Graph-CertCountVSDiscrepanvies: Figure 5
6. Zlint for 00000s + Diversity Comparison Zlint: Figure 6 and 5.3.2 analysis
7. Library checkpointing: Figure 7
8. Discrepancy analysis + Library logs analysis : 5.3.1 analysis 

For all notebooks, the output information should be intact to help avoid re-running code. 

## BibTeX

Please cite our paper if you rely on the artifacts for your work.

```
@inproceedings{icse2026-hallucinating-certificates,
  title     = {{Hallucinating Certificates: Differential Testing of TLS Certificate Validation Using Generative Language Models}},
  author    = {Paracha, Talha and Posluns, Kyle and Borgolte, Kevin and Lindorfer, Martina and Choffnes, David},
  booktitle = {Proceedings of the 48th IEEE/ACM International Conference on Software Engineering (ICSE)},
  date      = {2026-04},
  edition   = {48},
  editor    = {Mezini, Mira and Zimmermann, Thomas},
  location  = {Rio de Janeiro, Brazil},
  publisher = {Association for Computing Machinery (ACM)/Institute of Electrical and Electronics Engineers (IEEE)}
}
```
