**SHARK ATTACKS ANALYSIS** 

**Introduction**

This project analyzes shark attack data to explore patterns in shark incidents, focusing on factors like location, activity, season, and demographics. By identifying trends, we aim to improve safety awareness and preventative insights for ocean-goers.

**Hypothesis**
Educating users about shark encounter risk factors, including location, time of year, and activity type, will increase their awareness and reduce shark-related incidents.


**Required packages**

Pandas, Numpy, Seaborn and Matplotlib.pyplo


**Data cleaning and analysis functions**

<details>
  <summary>Click to see the list of functions</summary>
  
  - The **clean_string()** function standardizes string values by retaining only numeric characters and hyphens, ensuring that non-numeric characters are removed.
    This approach helps in eliminating inconsistencies that may arise from text variations.
    
  - The **clean_dates2()** function standardizes date formats by removing unnecessary text, formatting spacing, and converting strings to datetime objects, which ensures consistency.
    Handling Techniques : Handling Missing and Irregular Values: Removes non-date rows by coercing invalid dates to NaT and dropping NaNs.
                          Filtering Rows: Drops records before 1900 for relevancy.
                          Consistency Checks: Validates that the year in the date matches the separate 'Year' column, filtering any mismatches.


  - The **clean_states()** function standardizes state names in a dataset by converting them to lowercase and correcting common misspellings. 
    It removes rows with missing state data and filters out states that appear five times or less, focusing on significant entries. Finally, 
    it formats the state names to title case for readability. This process enhances data quality and prepares it for accurate analysis.


  - The **clean_cols function()** streamlines the DataFrame by renaming and removing unnecessary columns, ensuring the data remains relevant and manageable for analysis.
    Handling Techniques: Column Renaming: The function renames the "Unnamed: 11" column to "Fatal," enhancing clarity in the dataset.
                         Column Removal: It drops irrelevant columns like "href formula" and "Case Number" to focus on essential information.
                         Duplicate Removal: The function eliminates duplicate rows, improving data integrity and ensuring each record is unique for accurate analysis.

 - The **clean_type()** standardizes the "Type" column by consolidating variations in naming conventions, particularly for the "Provoked" type.
    It simplifies the dataset by categorizing several ambiguous types into a single "Unknown" category, which enhances clarity and analysis.
    
 - **Clean_country()** function tidies the "Country" column by standardizing names and removing entries that do not represent actual countries.
    This ensures that the dataset accurately reflects the geographical origins of the entries.
    
 - **Hemisphere()** function enriches the DataFrame by adding a "Hemisphere" column based on the geographical location of each country. 
 - Handling Techniques: Mapping: A predefined dictionary maps each country to its respective hemisphere, ensuring consistent classification.
                        Default Handling: Countries not found in the dictionary are assigned a default value of "Na," allowing for easy identification of unclassified entries.
 - **The clean_sex()** function standardizes the "Sex" column to ensure consistency in gender representation within the dataset.
   
 - **Clean_age()**  standardizes various age representations in the dataset.
   Techniques: Uses .replace() for common age values and patterns.
               Strips whitespace and replaces invalid entries (e.g., "Middle age", "unknown") with NaN.
   
 - **Age_group()** function categorizes age into predefined groups.
   Techniques: Utilizes conditional logic to define age ranges, returning "Unknown" for NaN values.

- **Age_groups()** converts age to numeric and assigns age groups.
  Techniques: Applies the age_group function to each age value.

- **Add_month()** extracts the month from a date column.
  Techniques: Converts the "Date" column to datetime and creates a new "Month" column.
  
- **Assign_season()** determines the season based on the month and hemisphere.
  Techniques: Applies logic to assign seasons accordingly.

- **Add_season()** applies the assign_season function to create a "Season" column.
  Techniques: Utilizes .apply() for row-wise operations.

- **Clean_activity()** standardizes activity descriptions.
  Techniques: Converts text to lowercase and counts activity frequencies.
              Replaces infrequent activities with "unknown" and applies corrections.

- **Clean_fatal()** function standardizes fatality indicators.
  Techniques: Maps various representations of fatality status to a consistent format.
  
- **Cleaning()** function centralizes multiple cleaning functions into a single process.
  Techniques: Sequentially applies various cleaning functions to ensure data integrity across the dataset.


</details>

 **Data visualization functions**

<details>
  <summary>Click to see the list of functions</summary>

  Techniques Utilized - Functions groupby(), .agg(),, .pivot_table(), for grouping data, unstack(), .melt(), sort_values()            to prepare them for visualization
  Seaborn and matlplotlib.pyplot libraries, barplot and histplots for data visualization

  Example of functions we have used
  
  - **Grouped_month_hemisphere(df)** -  Analyzes shark activity by month and hemisphere. It groups data using groupby()and counts
    occurrences with .size(). The unstack() method pivots the DataFrame to create columns for each hemisphere, while .fillna(0) and
    .astype(int) ensure no missing values. The DataFrame is sorted and reshaped using .melt() for visualization, culminating in a
    bar plot via sns.barplot().
  - **Visualize_activity_sex_group()** function compares shark incident activities by gender. It groups data using groupby() and
    counts cases, sorting them by frequency. The DataFrame is reshaped for clarity with .melt(), and a bar chart is plotted using
    sns.barplot() for straightforward comparison.
  - **Grouped_decade_incidents(df)** analyzes shark incidents by decade, focusing on data from 1920 to 2010. It groups incidents
    using groupby() to count occurrences and visualizes the frequency of shark attacks per decade with sns.barplot(), revealing
    long-term trends.
  - **grouped_activity_year** code filters shark incident data for decades between 1920 and 2010, focusing on provoked and
    unprovoked types. It then groups the data by decade and type, counting incidents.

</details>

**Results**

Most shark attacks occurred during warmer months depending on the hemisphere.
Surfing and Swimming are at the top of the most dangerous activities.
While USA has the most shark attack incidents, Australia has the most fatal incidents recorded. 
Significant decline in the percentage of fatal shark attacks, dropping from over 60% in the early 1900s to around 5.66% in the 2010
The reported number of shark attacks has significantly increased over the last 100 years, however, this is likely due to increased reporting and increased global population.

