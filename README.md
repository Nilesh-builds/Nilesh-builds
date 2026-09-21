<img src="assets/hero-terminal.svg" width="100%" alt="Nilesh Singh — data analyst x AI evaluation" />

<div align="center">

<img width="280" src="assets/portrait_terminal.png" alt="Terminal-style dot-matrix portrait of Nilesh" />

<br/>

<img src="https://img.shields.io/badge/🎓_BCA%20Data%20Science-Sri%20Balaji%20University-1A2B1A?style=flat-square&labelColor=060D08&color=132016" alt="degree" />
&nbsp;
<img src="https://img.shields.io/badge/📍_Pune-India-1A2B1A?style=flat-square&labelColor=060D08&color=132016" alt="location" />
&nbsp;
<img src="https://img.shields.io/badge/Open%20to-Data%20Analyst%20Roles-CAFF3C?style=flat-square&labelColor=060D08" alt="open-to" />

<br/><br/>

<a href="https://readme-typing-svg.demolab.com?font=Fira+Code&pause=1200&color=CAFF3C&background=060D0800&center=true&vCenter=true&width=620&lines=Data+Quality+%7C+LLM+Evaluation+%7C+Dashboards;Tested+pipelines%2C+not+notebook+demos;Evidence+first%2C+hype+never"><img src="https://readme-typing-svg.demolab.com?font=Fira+Code&pause=1200&color=CAFF3C&background=060D0800&center=true&vCenter=true&width=620&lines=Data+Quality+%7C+LLM+Evaluation+%7C+Dashboards;Tested+pipelines%2C+not+notebook+demos;Evidence+first%2C+hype+never" alt="typing: data quality, LLM evaluation, dashboards" /></a>

<br/>

<a href="https://www.linkedin.com/in/nilesh-singh-b9b6932bb"><img src="https://img.shields.io/badge/LinkedIn-CAFF3C?style=for-the-badge&logo=linkedin&logoColor=060D08&labelColor=060D08" alt="linkedin" /></a>
&nbsp;&nbsp;
<a href="mailto:kumarnilash509@gmail.com"><img src="https://img.shields.io/badge/Email-CAFF3C?style=for-the-badge&logo=gmail&logoColor=060D08&labelColor=060D08" alt="email" /></a>
&nbsp;&nbsp;
<a href="https://github.com/Nilesh-builds"><img src="https://img.shields.io/badge/GitHub-CAFF3C?style=for-the-badge&logo=github&logoColor=060D08&labelColor=060D08" alt="github" /></a>
&nbsp;&nbsp;
<a href="https://nilesh-builds.github.io/"><img src="https://img.shields.io/badge/Portfolio-CAFF3C?style=for-the-badge&logo=googlechrome&logoColor=060D08&labelColor=060D08" alt="portfolio" /></a>
&nbsp;&nbsp;
<a href="https://github.com/Nilesh-builds?tab=stars"><img src="https://img.shields.io/github/stars/Nilesh-builds?style=for-the-badge&color=CAFF3C&labelColor=060D08&logo=github&logoColor=CAFF3C&label=Stars" alt="stars" /></a>

</div>

```bash
$ whoami

BCA student specializing in Data Science at Sri Balaji University, Pune,
building toward Data Analytics and AI Evaluation. I turn messy datasets
into tested pipelines, interpretable models, and dashboards — then explain
what the evidence can and cannot prove.

Alongside coursework, I interned as a Cloud Application Developer at
Codefirst Technology. My work lives after the model: data quality,
evaluation, business trade-offs, and human review.

$ cat .profile

ROLE        =  Data Analyst  |  AI Evaluation
STATUS      =  BCA (Data Science) Student — Sri Balaji University
DOMAIN      =  Analytics  |  Data Quality  |  AI Evaluation
TOOLS       =  Python  |  SQL  |  Power BI  |  Excel  |  R
INTERNSHIP  =  Cloud Application Developer — Codefirst Technology
PORTFOLIO   =  TrainLens  |  Customer Churn Analysis  |  LLM Safety Eval Benchmark
LOCATION    =  Pune, India
OPEN_TO     =  Data Analyst  |  AI Trainer  |  AI Evaluation Roles
```

<img src="assets/divider.svg" width="100%" alt="" />

## `> ls /projects --sort=impact`

### &#9654; TrainLens — AI Training Data Quality Platform

<img src="https://raw.githubusercontent.com/Nilesh-builds/trainlens/main/assets/dashboard.png" width="100%" alt="TrainLens dashboard" />

Customer-support data quality and evaluation platform: five quality dimensions, eleven checks, Groq batch labeling with rule-based fallback, confidence-based human review queue, and accuracy / F1 / calibration reporting. Benchmarked on 852 synthetic conversations at a 98.85% quality score.

**Stack:** Python · pandas · DuckDB · Streamlit · Plotly · scikit-learn
**Live demo:** [TrainLens Dashboard](https://trainlens-gv48ihtbq6nbapgfrlworc.streamlit.app/) · **Repo:** [`Nilesh-builds/trainlens`](https://github.com/Nilesh-builds/trainlens)

### &#9654; LLM Safety & Response Evaluation Benchmark

<img src="https://raw.githubusercontent.com/Nilesh-builds/llm-safety-eval-benchmark/main/docs/screenshots/dashboard.png" width="100%" alt="LLM evaluation evidence dashboard" />

A controlled benchmark scoring AI responses across 9 dimensions — instruction following, factuality, relevance, bias, toxicity, refusal quality, prompt injection resistance, hallucination, consistency — entirely on free-tier APIs. Rule-based checks plus a 2-model LLM-judge ensemble with 95% bootstrap intervals. Judges validated against references (11/11) and blind human review (human-vs-human κ=0.902). GPT-OSS-120B composite 4.28 vs GPT-OSS-20B 4.18.

**Stack:** Python · Groq free-tier APIs · pandas · matplotlib · Streamlit · Jupyter
**Live demo:** [LLM Evaluation Evidence Dashboard](https://llm-safety-eval-benchmark-vrjugdrizxtaqt38s6mgep.streamlit.app/) · **Repo:** [`Nilesh-builds/llm-safety-eval-benchmark`](https://github.com/Nilesh-builds/llm-safety-eval-benchmark)

### &#9654; Customer Churn Analysis — Telco Dataset

<img src="https://raw.githubusercontent.com/Nilesh-builds/customer-churn-analysis/main/assets/dashboard.png" width="100%" alt="Customer churn decision support dashboard" />

Production-style churn analysis: data-quality checks, SQL views, leakage-safe modeling with cross-validation and calibration, cost-sensitive thresholds, and a live human-review dashboard. Balanced Random Forest chosen on business reasoning, not accuracy alone.

**Stack:** Python · SQL · Pandas · scikit-learn · Streamlit
**Live demo:** [Customer Churn Decision Support](https://nilesh-customer-churn.streamlit.app/) · **Repo:** [`Nilesh-builds/customer-churn-analysis`](https://github.com/Nilesh-builds/customer-churn-analysis)

### &#9654; AI HR Automation Suite — 6 n8n Workflows

Six automation workflows streamlining HR end-to-end: employee onboarding, leave management, sentiment & feedback analysis, policy Q&A bot, AI resume screener & ranker, and a WhatsApp HR chatbot — Google Sheets as the shared data store, GPT-4 as the AI layer, Gmail/Slack/WhatsApp for alerts.

**Stack:** n8n · Google Sheets · OpenAI GPT-4 · Gmail/Slack/WhatsApp
**Repo:** [`Nilesh-builds/ai-hr-automation-suite`](https://github.com/Nilesh-builds/ai-hr-automation-suite)

<img src="assets/divider.svg" width="100%" alt="" />

```bash
$ ls /tech-stack --grouped

languages/   python  r  html  css  bash
data/        postgres  mysql
cloud/       aws  git  github  vscode
```

<div align="center">

<img title="Python" src="https://skillicons.dev/icons?i=python&theme=dark" alt="python" />
<img title="R" src="https://skillicons.dev/icons?i=r&theme=dark" alt="r" />
<img title="HTML" src="https://skillicons.dev/icons?i=html&theme=dark" alt="html" />
<img title="CSS" src="https://skillicons.dev/icons?i=css&theme=dark" alt="css" />
<img title="Bash" src="https://skillicons.dev/icons?i=bash&theme=dark" alt="bash" />
<img title="PostgreSQL" src="https://skillicons.dev/icons?i=postgres&theme=dark" alt="postgres" />
<img title="MySQL" src="https://skillicons.dev/icons?i=mysql&theme=dark" alt="mysql" />
<img title="AWS" src="https://skillicons.dev/icons?i=aws&theme=dark" alt="aws" />
<img title="Git" src="https://skillicons.dev/icons?i=git&theme=dark" alt="git" />
<img title="GitHub" src="https://skillicons.dev/icons?i=github&theme=dark" alt="github" />
<img title="VS Code" src="https://skillicons.dev/icons?i=vscode&theme=dark" alt="vscode" />

<br/>

<img src="https://img.shields.io/badge/Power%20BI-CAFF3C?style=flat-square&logo=powerbi&logoColor=000000&labelColor=060D08" alt="powerbi" />
<img src="https://img.shields.io/badge/Excel-CAFF3C?style=flat-square&logo=microsoftexcel&logoColor=000000&labelColor=060D08" alt="excel" />
<img src="https://img.shields.io/badge/SQL-CAFF3C?style=flat-square&logo=postgresql&logoColor=000000&labelColor=060D08" alt="sql" />
<img src="https://img.shields.io/badge/Streamlit-CAFF3C?style=flat-square&logo=streamlit&logoColor=000000&labelColor=060D08" alt="streamlit" />
<img src="https://img.shields.io/badge/scikit--learn-CAFF3C?style=flat-square&logo=scikitlearn&logoColor=000000&labelColor=060D08" alt="sklearn" />
<img src="https://img.shields.io/badge/PySpark-CAFF3C?style=flat-square&logo=apachespark&logoColor=000000&labelColor=060D08" alt="pyspark" />

</div>

## `> cat analytics-expertise.json`

| Domain | Proficiency | Details |
| :-- | :-- | :-- |
| **Data Cleaning & EDA** | `█████ Advanced` | Pandas, missing-value handling, outlier detection, feature engineering |
| **Machine Learning** | `████░ Intermediate` | Logistic Regression, Random Forest, Decision Trees, model selection on business criteria |
| **Data Visualization** | `████░ Intermediate` | Power BI dashboards, Excel reporting, matplotlib/seaborn charting |
| **SQL & Databases** | `████░ Intermediate` | Querying, joins, aggregation for analysis-ready datasets |
| **Statistical Analysis** | `████░ Intermediate` | Hypothesis-driven EDA, risk scoring, business recommendation write-ups |
| **Cloud (AWS)** | `███░░ Working Knowledge` | Cloud-native architecture from Codefirst Technology internship |

<img src="assets/divider.svg" width="100%" alt="" />

## `> cat experience.log`

**Cloud Application Developer (Intern)** — **Codefirst Technology**

Hands-on experience building cloud-native applications, applying AWS fundamentals alongside coursework in data science.

`AWS` `Cloud-Native Architecture` `Application Development`

## `> git log --oneline /education`

<div align="center">

<img src="https://img.shields.io/badge/BCA%20—%20Data%20Science-Sri%20Balaji%20University-CAFF3C?style=for-the-badge&logo=academia&logoColor=000000&labelColor=060D08" alt="education" />

</div>

## `> cat certifications.sh`

<div align="center">

<img src="https://img.shields.io/badge/Power%20BI%20for%20Data%20Analysts-Microsoft%20Press-CAFF3C?style=flat-square&labelColor=060D08" alt="powerbi-cert" />
<img src="https://img.shields.io/badge/SQL%20for%20Data%20Analysis-CAFF3C?style=flat-square&labelColor=060D08" alt="sql-cert" />
<img src="https://img.shields.io/badge/Python%20for%20Data%20Analysis-CAFF3C?style=flat-square&labelColor=060D08" alt="python-cert" />
<img src="https://img.shields.io/badge/Machine%20Learning%20with%20Python-CAFF3C?style=flat-square&labelColor=060D08" alt="ml-cert" />
<img src="https://img.shields.io/badge/Deep%20Learning%3A%20Image%20Recognition-CAFF3C?style=flat-square&labelColor=060D08" alt="dl-cert" />
<img src="https://img.shields.io/badge/R%20for%20Data%20Science-CAFF3C?style=flat-square&labelColor=060D08" alt="r-cert" />
<img src="https://img.shields.io/badge/Excel%20%2B%20ChatGPT%20Power%20Tips-CAFF3C?style=flat-square&labelColor=060D08" alt="excel-cert" />
<img src="https://img.shields.io/badge/Intro%20to%20Data%20Science-CAFF3C?style=flat-square&labelColor=060D08" alt="ds-cert" />
<img src="https://img.shields.io/badge/Advanced%20Algorithmic%20Thinking-CAFF3C?style=flat-square&labelColor=060D08" alt="algo-cert" />

</div>

<img src="assets/divider.svg" width="100%" alt="" />

## `> git stats --global`

<div align="center">

<img height="165" src="https://github-readme-streak-stats.herokuapp.com/?user=Nilesh-builds&hide_border=true&background=0A0F08&stroke=CAFF3C&ring=8AFF57&fire=39FF14&currStreakLabel=CAFF3C&sideLabels=8AFF57&dates=8AFF57&currStreakNum=CAFF3C&sideNums=CAFF3C" alt="streak" />

<br/>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/github-snake-dark.svg" />
  <source media="(prefers-color-scheme: light)" srcset="assets/github-snake.svg" />
  <img alt="contribution snake" src="assets/github-snake-dark.svg" />
</picture>

</div>

## `> cat current-focus.yaml`

```yaml
learning:
  - Advanced machine learning & model evaluation
  - Power BI dashboard design for business storytelling

building:
  - trainlens                   # Customer-support data quality, AI labeling, and evaluation dashboard
  - llm-safety-eval-benchmark  # 9-dimension LLM safety benchmark, free-tier APIs, judge validation
  - customer-churn-analysis   # Telco churn EDA + ML + Power BI
  - ai-hr-automation-suite    # 6 n8n workflows automating HR processes

studying:
  - BCA, Data Science — Sri Balaji University, Pune

open_to:
  - Data Analyst roles
  - Business Analyst roles
  - AI Trainer roles
```

## `> ping me`

<div align="center">

<a href="mailto:kumarnilash509@gmail.com"><img src="https://img.shields.io/badge/Gmail-CAFF3C?style=for-the-badge&logo=gmail&logoColor=000000&labelColor=060D08" alt="gmail" /></a>
<a href="https://www.linkedin.com/in/nilesh-singh-b9b6932bb"><img src="https://img.shields.io/badge/LinkedIn-CAFF3C?style=for-the-badge&logo=linkedin&logoColor=000000&labelColor=060D08" alt="linkedin" /></a>
<a href="https://github.com/Nilesh-builds"><img src="https://img.shields.io/badge/GitHub-CAFF3C?style=for-the-badge&logo=github&logoColor=000000&labelColor=060D08" alt="github" /></a>
<a href="https://nilesh-builds.github.io/"><img src="https://img.shields.io/badge/Portfolio-CAFF3C?style=for-the-badge&logo=googlechrome&logoColor=000000&labelColor=060D08" alt="portfolio" /></a>

</div>

---

<div align="center">

<sub><i>// student by day &nbsp;|&nbsp; building an analytics portfolio, one dataset at a time</i></sub>

<br/><br/>

<img width="100%" src="https://capsule-render.vercel.app/api?type=waving&height=120&section=footer&color=0a0f08&fontColor=CAFF3C" alt="footer" />

</div>
