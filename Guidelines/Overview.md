# Dissertation Overview
Basic ideas, structure, topics to consider etc.  

## Introduction
Lay out basic idea of project.  
Applied aspect: webapp, what it does, basic technologies, machine learning/tensorflow.  
Theoretical aspect: correlation between prices, influences, any maths/theorems/hypotheses etc, theory to do with prediction.  

### Aims / Goals / Objectives / Ideas
Create a webapp that displays up to date (<1min~) graphs of currency prices, traditional and crypto. Incorporate machine learning to recognise patterns/trends. NLP for analysing content across the web to "predict" changes in prices (twitter specifically, mentioned by @JohnnyGlynn) - world events (tweeted about, using keywords) have an effect on traditional currencies.  

Discuss ideas in detail in thesis, more conceptual, some maths etc, theory behind ML/pattern recognition.  

Thesis 20-30k~ words.

### Thesis Layout

*Given  / Suggested* -  
Cover Sheet, Table of Contents, Table of Illustrations, Introduction...  
Body of document - Methodology, Technology Review, System Design, System Evaluation...  
Conclusion, References, Appendices  
Beginning / end won't change much.  
  
Possible main body headings / ideas -  
1. Project Concept  
2. Explain Cryptocurrency  
3. Crypto vs Traditional - lead into blockchain / diff technologies. Centralised vs decentralised. Crypto based on hype / more secure, traditional dependent on governments / world events etc. Crashes / recession etc in both. Rise of crypto?  
4. Something to lead into project itself - maybe put project concept here instead? Aforementioned within introduction?   
5. Methodology / Planning etc  
6. Technologies Used / System Design  
7. System Evaluation  

Will likely break body into separate sections. 1, 2, 3 / maybe 4 based on theory / research / concepts. 5, 6, 7 focus on actual project itself, will be more technical.  
"Technology Review" of 10+ pages suggested, will use theory aspect (1-3/4) for that but might not be one long review. Might talk about traditional at the start and focus on crypto for review?   

## Technologies / Components  
Python, Flask, MongoDB, (ChartJS / D3), Vue.js, Tensorflow, Docker (?), Github, Heroku/Azure (?).

## Web App Layout  
**Main Page**  
Graph with prices, can filter prices shown. Last hour/day/week?  
General price prediction for the following day (based on numbers to begin, move on to NLP). Update and retrain with whatever's in the database each day.  
RSS Feed with cryptocurrency related posts from reddit/hackernews.  

**Other**  
Possible blog post feature, admins can create posts, anyone can read. More admins can be added if desired.  

## Issues / Problems Encountered  
@taraokelly - D3 / Vue vs ChartJS
Azure / AWS / Heroku
