# World Happiness Report - Dataset Overview

## 1. Context

The **World Happiness Report** is a landmark survey of the state of global happiness. 
* The first report was published in **2012**
* The second in **2013**
* The third in **2015**
* The fourth in the **2016 Update**
* The **World Happiness 2017**, which ranks 155 countries by their happiness levels, was released at the United Nations at an event celebrating International Day of Happiness on March 20th.

The report continues to gain global recognition as governments, organizations, and civil society increasingly use happiness indicators to inform their policy-making decisions. Leading experts across fields — economics, psychology, survey analysis, national statistics, health, public policy, and more — describe how measurements of well-being can be used effectively to assess the progress of nations. The reports review the state of happiness in the world today and show how the new science of happiness explains personal and national variations in happiness.

---

## 2. Content & Methodology

The happiness scores and rankings use data from the **Gallup World Poll**. 

### The Cantril Ladder
The scores are based on answers to the main life evaluation question asked in the poll, known as the **Cantril Ladder**:
> Respondents are asked to think of a ladder with the best possible life for them being a **10** and the worst possible life being a **0**, and to rate their own current lives on that scale.

* The scores are derived from nationally representative samples for the years 2013–2016 and use Gallup weights to ensure representativeness.

### The 6 Key Contributing Factors
The columns following the happiness score estimate the extent to which each of six factors contributes to making life evaluations higher in each country compared to **Dystopia** (a hypothetical benchmark country):
1. **Economic production** (GDP per Capita)
2. **Social support** (Family)
3. **Life expectancy** (Healthy Life Expectancy)
4. **Freedom** (Freedom to make life choices)
5. **Absence of corruption** (Trust in Government / Corruption)
6. **Generosity**

> [!NOTE]
> These six factors have **no impact** on the total score reported for each country; rather, they explain *why* some countries rank higher than others.

---

## 3. Key Concepts & FAQ

### What is Dystopia?
**Dystopia** is an imaginary country that has the world’s least-happy people. 
* **Purpose:** To serve as a baseline/benchmark against which all countries can be favorably compared (no country performs more poorly than Dystopia) in terms of each of the six key variables. This allows each sub-bar in the visualization to have a positive width.
* **Calculation:** Dystopia is characterized by the lowest observed national averages for each of the six key variables. Since life would be very unpleasant with the lowest income, lowest life expectancy, lowest generosity, highest corruption, least freedom, and least social support, it is termed **Dystopia** (in contrast to Utopia).

### What are the Residuals?
The **residuals** (or unexplained components) differ for each country:
* They reflect the extent to which the six variables either **over-explain** or **under-explain** average life evaluations (2014–2016).
* The average residual across all countries is approximately zero.
* While some country residuals can be substantial (occasionally exceeding 1 point on the 0–10 scale), they are always much smaller than the calculated benchmark value in Dystopia, where average life is rated at **1.85** on the 0 to 10 scale.

### What do the columns succeeding the Happiness Score describe?
* The columns (`GDP per Capita`, `Family`, `Life Expectancy`, `Freedom`, `Generosity`, `Trust Government Corruption`) describe the extent to which each factor contributes to evaluating national happiness.
* **Dystopia Residual metric:** 
  $$\text{Dystopia Residual} = \text{Dystopia Happiness Score (1.85)} + \text{Unexplained Residual Value}$$

---

> [!WARNING]
> **Important Note for Data Modeling & Clustering:**  
> If you sum all these six factors plus the Dystopia Residual, you obtain the **Happiness Score**.  
> Therefore:
> 1. In predictive modeling, it is trivial or unreliable to model them directly to predict the Happiness Score.
> 2. In **clustering (gom cụm - Đề tài 16)**, ** tuyệt đối KHÔNG đưa `Happiness Score` hay `Happiness Rank` vào làm đặc trưng gom cụm**. Nhóm chỉ sử dụng 6 yếu tố cơ sở (và các chỉ số thực tế) để phân nhóm quốc gia, sau đó mới dùng `Happiness Score` để hậu kiểm và so sánh mức độ hạnh phúc giữa các cụm.
