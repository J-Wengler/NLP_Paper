# Manubot Repository for "Comparison of keyword extraction and word vector generation methods for identifying related genomic datasets in the public domain"

<!-- usage note: edit the H1 title above to personalize the manuscript -->

[![HTML Manuscript](https://img.shields.io/badge/manuscript-HTML-blue.svg)](https://J-Wengler.github.io/NLP_Paper/)
[![PDF Manuscript](https://img.shields.io/badge/manuscript-PDF-blue.svg)](https://J-Wengler.github.io/NLP_Paper/manuscript.pdf)
<!-- usage note: delete CI badges above for services not used by your manuscript -->

## Manuscript description

<!-- usage note: edit this section. -->

Data-sharing requirements have led to wide availability of genomic datasets in public repositories. Researchers can reuse and combine these datasets to address novel hypotheses. However, after identifying one or more datasets that are relevant to a particular research question, a researcher may have difficult identifying other datasets that are also relevant, due to the quantity of available datasets and lack of structure with which they are described. In this study, we focus specifically on Gene Expression Omnibus, a repository that contains genomic data from hundreds of thousands of experiments. Notable efforts have been made to manually annotate these data but not been able to keep pace as new datasets are submitted. To address this problem, we use natural language processing (NLP). Under the assumption that a researcher has manually identified a subset of available datasets related to a particular research topic, we use NLP algorithms to extract keywords from the abstract associated with each dataset. Next we summarize the keywords using diverse embedding algorithms. (TODO: I'm sure there's a better way to say this.) 

TODO: Describe briefly here about the theoretical approaches that we compared more so than the specific software packages. Without making it too long, make sure to cover all of the approaches. 
Concerning word vector generation we test two primary factors, domain and training algorithm. Domain refers to the type of text that each model is trainined on. We compare biomedical specific text (StarGEO abstracts) with readily available models trained on wikipedia data. Once a domain has been identified there are two options for training algorithms. The first is continous-bag-of-words (CBOW). CBOW trains by predicting the target word from the context words that surround it. The second option is skip-gram. Skip-gram trains by predicting the context words from the target word essentially the reverse of CBOW.

We test nine keyword extraction methods. Three of the methods are statistical models while the other six are graphical methods. The statistical methods are TF-IDF, KP-Miner, and YAKE. TF-IDF works by comparing the frequency of each word found in the passage to its frequency in other passages that exist in the corpus. KP-Miner evaluates each word 
based on the context surrounding the words to identify keywords. YAKE combines elements of both TF-IDF and KP-Miner by
using the context while also taking into account the frequency at which the word appears in the document. The first
graphical approach we test is TextRank which is based off of a web technique called PageRank which is used for
identifying related webpages through hyperlinks. TextRank performs a similar analysis with text by creating a graph
where each word is represented as a node. Relationships between words are drawn as connected nodes. These relationships
are used to identify keywords. TopicRank is a process similar to TextRank but the text is preprocessed to create n-grams
of nouns and adjectives as keyphrase candidates before creating a graph with them to identify keywords. SingleRank is
another extension of TextRank with each node having a weight value assigned to it. PositionRank is a more complicated
extension of TextRank where the position of the word within the sentence is assigned a weight along with actual context
as in TextRank. TopicalPageRank is another extension of TextRank that seeks to improve experience by weighting those words
that appear more in the document. The last graphical approach is MultipartiteRank which uses a multipartite graph to construct
the initial graph and calculate weights between nodes. 

 We found that different combinations of keyword extraction methods and word vector generation yield very different results. This variety
 was also reflected across the query domains. These results show that natural language processing is a powerful tool that can be harnessed
 for data collection and more research needs to be done in this area.

## Manubot

<!-- usage note: do not edit this section -->

Manubot is a system for writing scholarly manuscripts via GitHub.
Manubot automates citations and references, versions manuscripts using git, and enables collaborative writing via GitHub.
An [overview manuscript](https://greenelab.github.io/meta-review/ "Open collaborative writing with Manubot") presents the benefits of collaborative writing with Manubot and its unique features.
The [rootstock repository](https://git.io/fhQH1) is a general purpose template for creating new Manubot instances, as detailed in [`SETUP.md`](SETUP.md).
See [`USAGE.md`](USAGE.md) for documentation how to write a manuscript.

Please open [an issue](https://git.io/fhQHM) for questions related to Manubot usage, bug reports, or general inquiries.

### Repository directories & files

The directories are as follows:

+ [`content`](content) contains the manuscript source, which includes markdown files as well as inputs for citations and references.
  See [`USAGE.md`](USAGE.md) for more information.
+ [`output`](output) contains the outputs (generated files) from Manubot including the resulting manuscripts.
  You should not edit these files manually, because they will get overwritten.
+ [`webpage`](webpage) is a directory meant to be rendered as a static webpage for viewing the HTML manuscript.
+ [`build`](build) contains commands and tools for building the manuscript.
+ [`ci`](ci) contains files necessary for deployment via continuous integration.

## License

<!--
usage note: edit this section to change the license of your manuscript or source code changes to this repository.
We encourage users to openly license their manuscripts, which is the default as specified below.
-->

[![License: CC BY 4.0](https://img.shields.io/badge/License%20All-CC%20BY%204.0-lightgrey.svg)](http://creativecommons.org/licenses/by/4.0/)
[![License: CC0 1.0](https://img.shields.io/badge/License%20Parts-CC0%201.0-lightgrey.svg)](https://creativecommons.org/publicdomain/zero/1.0/)

Except when noted otherwise, the entirety of this repository is licensed under a CC BY 4.0 License ([`LICENSE.md`](LICENSE.md)), which allows reuse with attribution.
Please attribute by linking to https://github.com/J-Wengler/NLP_Paper.

Since CC BY is not ideal for code and data, certain repository components are also released under the CC0 1.0 public domain dedication ([`LICENSE-CC0.md`](LICENSE-CC0.md)).
All files matched by the following glob patterns are dual licensed under CC BY 4.0 and CC0 1.0:

+ `*.sh`
+ `*.py`
+ `*.yml` / `*.yaml`
+ `*.json`
+ `*.bib`
+ `*.tsv`
+ `.gitignore`

All other files are only available under CC BY 4.0, including:

+ `*.md`
+ `*.html`
+ `*.pdf`
+ `*.docx`

Please open [an issue](https://github.com/J-Wengler/NLP_Paper/issues) for any question related to licensing.
