![VCFT_Title-Image](README_images/VCFT_Title-Image.jpg)

---

**A detailed walkthrough of the code found in this same repository.**

_**Disclaimer:** This project was done as part of my work with Anthemis. All data shown in this repository are dummy datasets and were not intended to reflect the networks of any VC communities in reality._

## Introduction

**The Venture Capital Fundraising Tool was inspired by the (commonly ignored) increasing impacts that networks have on business outcomes.**  Building strategic relations with investors in the venture capital ecosystem is a method of deal sourcing often employed by VCs. However, when VCs struggle to identify key investors in an objective fashion, it is common practice for VCs to focus on coinvestors that they already know, rather than the ones that they should know. Hence, we believe that networks play a more crucial role in the success in venture capital land than most choose to believe, and that network analysis can be used to rank the "successfulness" of coinvestors in a given VC community.

## The Tool

<img src="/README_images/VCFT_Demo-Gif-resize-infloop.gif?raw=true" class="center">
*(Left): Running the Tool using Terminal. (Right): The intermediate and final outputs of the Tool generated in the user's specified directory.*

The Tool is made up of a series of Python scripts daisy-chained together, with the outputs of one script serving as the input to the next script. It is then run using a Bash script in a Terminal shell, where a simple "How to Use" guide would be echoed. Daisy-chaining the scripts (instead of executing one large script) allows the user to be able to examine the inputs/outputs at each stage of the Tool to get a better intuition of its final recommendations. Additionally, changes can be made to any one part of the process without affecting the rest, allowing for greater flexibility during maintenance of the Tool. The figure below shows the skeleton of the Tool.

![VCFT_Flowchart](README_images/VCFT_Flowchart.jpeg)




## Getting Started

### Local
All required pacakges can be found in the `requirements.txt` file. To install the packages, run

```python
pip install -r requirements.txt
```

## How the Tool Works

The original dataset was acquired from [PitchBook](www.pitchbook.com). A dummy dataset was generated to use as a toy example to conduct our analysis in this repository.





## Thanks

This project would not have been possible without the boldness of the Anthemis team to challenge the conventional and their openness to new ideas. This project was mentored by Erica Young.
