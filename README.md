🦈 Shark Cage Diving: Project Summary
Business Case
* Business Opportunity: To create a thrilling and safe shark cage diving tourism company that offers customers a high chance of seeing sharks in their natural habitat.
* Business Problem: To guarantee customer satisfaction and safety, the company must operate in locations with a high probability of shark sightings. The dataset of attacks can serve as a proxy for where sharks are most active and what species are present.
Problem Statement
To design a successful cage diving tour, our company needs to identify the countries and times of day with the highest frequency of non-fatal shark encounters, which can indicate the best and safest locations for our expeditions.
Hypothesis
* Primary Hypothesis (Where to go?):
“The USA has the highest number of non-fatal shark attacks recorded in the afternoon." This helps the company choose a country and time for their tours.
* Secondary Hypothesis (What will we see?):
"The White shark is the species most frequently involved in non-fatal attacks in the USA." This helps the company market their tours by advertising the type of shark customers are most likely to see.
* Tertiary Hypothesis: (When to go?)
"In the USA, non-fatal shark attacks are most common during the third quarter (July-September), corresponding with the summer season."










To Do List


✅ Day 1: Project Setup & Planning (Completed)
* Define Business Case: Shark Cage Diving Expedition.
* Formulate Hypothesis: "The USA has the highest number of non-fatal shark attacks recorded in the afternoon."
* Initial Data Load: Load the dataset into a pandas DataFrame.
* Initial Inspection: Use .info(), .head(), and .isna().sum() to understand the data's structure and identify initial issues.
________________


⏳ Day 2: Data Cleaning & Wrangling (Focus)
* Drop Irrelevant Columns: Remove all unnecessary metadata and empty columns (pdf, href formula, Unnamed: 21, etc.) using the .drop() method.
* Clean Country Column:
   * Standardize the text to lowercase using .str.lower().
   * Inspect unique values with .value_counts() to find and fix inconsistencies
   * Decide on a strategy to handle the small number of missing values (either fill or drop).
* Clean Fatal Y/N Column:
   * Inspect unique values with .value_counts().
   * Standardize the values to a clear format (e.g., True/False or yes/no).
   * Handle missing or unknown values.
* Clean Time Column:
   * This is the most complex cleaning task. Use Regular Expressions (Regex) to extract patterns.
   * Create a function to categorize the messy time data into broader groups like 'Morning', 'Afternoon', 'Evening', and 'Night'.
* Clean Date and Year Columns:
   * Extract Year from date column to a new column
   * Extract Year from Year to the same column created above
   * Create a new column with quarters extracting data from Date column
________________


🗓️ Day 3: Exploratory Data Analysis (EDA)
* Filter Data: Create a smaller DataFrame that only contains the data needed for your hypothesis (e.g., non-fatal attacks in the USA).
* Group and Aggregate: Use .groupby() and .value_counts() to count the number of attacks for each time category ('Morning', 'Afternoon', etc.) within the USA.
* Create Visualizations: Build a simple bar chart to visually compare the counts for each time category to see if 'Afternoon' is indeed the highest.
________________


🎤 Day 4: Finalize & Prepare Presentation
* Validate Hypothesis: Based on your analysis from Day 3, write a clear conclusion stating whether your hypothesis was supported or refuted by the data.
* Refine Code: Clean up your Jupyter notebook, add comments, and ensure your code is readable and follows best practices.
* Prepare Presentation Slides: Create a short (3-minute) slide deck that tells the story of your findings for the cage diving company, following the presentation structure in your project brief.# Quest-Shark-Attacks
# Quest-Shark-Attacks
