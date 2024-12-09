#Cleaning functions
import pandas as pd
import numpy as np

def clean_string(input_string):
    # Return an empty string if input is NaN or not a string
    if pd.isna(input_string) or not isinstance(input_string, str):
        return ''
    
    # Keep only numerical characters and hyphens
    cleaned_string = ''.join(char for char in input_string if char.isdigit() or char == '-')
    return cleaned_string

#Owen - date cleaning
def clean_dates2(df):
    """ Goes through a column in the DataFrame called "Date" and cleans
    Removes "reported" from the column to just get the date
    Deleted any trailing spaces, and makes sure the format is just numbers and hyphens
    Converts the column to the pandas datetime format
    Removes rows from the data with invalid dates
    Filters to only include dates after 1900 and dates with years that match the "Year" column
    """
    new_df = df.copy()
    #6973 rows
    #Removes "reported" from dates and trailing spaces
    new_df['Date'] = new_df['Date'].str.replace('reported', '', case=False)
    new_df["Date"] = new_df["Date"].apply(lambda x: x.strip() if isinstance(x, str) else x)
    new_df['Date'] = new_df['Date'].str.replace(' ', '-', regex=False)
    new_df['Date'] = new_df['Date'].str.replace(r'-+', '-', regex=True)

    #converts to date format
    new_df['Date'] = pd.to_datetime(new_df['Date'], errors='coerce')

    #drop rows invalid dates
    new_df.dropna(subset=['Date'], inplace=True)
    #5376 rows

    #drop years before 1900
    new_df = new_df[new_df["Year"] >= 1900 ]
    new_df = new_df[new_df['Date'] >= pd.Timestamp('1900-01-01')].reset_index(drop=True)
    #5114 rows

    # Check year from date against Year column
    if 'Year' in new_df.columns:
        new_df = new_df[new_df['Year'] == new_df['Date'].dt.year]
    return new_df

#Eliska
def clean_states(df: pd.DataFrame):
    """ Tidies the "State" column
    Converts "State" column to lower case 
    Only keeps States with at least 5 cases
    Uses a dictionary to update State names to cleaned versions where there were errors
    Converts back to title case
    """
    version_2 = df.copy() #independent copy so we wont mess the potential DF
    version_2 = version_2.dropna(subset=["State"]) #get rid of empty values
    version_2.loc[:, "State"] = version_2["State"].str.lower() #convert to lowercase

    #get rid of countries that occur 5 or less times
    state_counts = version_2["State"].value_counts()
    threshold = 5
    states_to_keep = state_counts[state_counts >= threshold].index
    version_2 = version_2[version_2["State"].isin(states_to_keep)]

    #corrections
    state_corrections = {"westerm australia": "western australia", "western australia" : "western australia",
                        "mirs bay ": "mirs bay", "mirs bay" : "mirs bay",
                        "baja california" : "california",
                        " primorje-gorski kotar county": "primorje-gorski kotar county",
                        }
    version_2["State"] = version_2["State"].replace(state_corrections) # apply corrections
    version_2["State"] = version_2["State"].str.title() #get back the capital letter of each word in states

    return version_2

#Owen
def clean_cols(df: pd.DataFrame):
    """Removes empty columns and names "Fatal" correctly """
    new_df = df.rename(columns={'Unnamed: 11': 'Fatal'})
    new_df = new_df.drop(['href formula', 'href','Case Number', 'Case Number.1',
       'original order', 'Unnamed: 21', 'Unnamed: 22', "pdf"], axis=1)
    new_df = new_df.drop_duplicates()
    return new_df

#Constanza
def clean_type(df: pd.DataFrame):
    """ Cleans "type" column
    Removes anything other than "Provoked" and "Unprovoked", and changes to "Unknown"
    """
    new_df = df.copy()
    new_df['Type'] = new_df['Type'].replace({' Provoked': 'Provoked'})

    values_to_replace = ['Questionable', 'Watercraft', 'Sea Disaster', '?', 'Unconfirmed', 'Unverified', 'Invalid', 'Under investigation', 'Boat']
    new_df['Type'] = new_df['Type'].replace(values_to_replace, 'Unknown')

    return new_df

#Owen
def clean_country(df):
    """Tidies the "Country" column of the DataFrama
    Converts all to title case, and strips trailing spaces
    Usa then converted back to USA
    Removes data for Oceans and Seas, which are not countries
    Replaces some common errors to their correct Country names (eg. Ceylon to Sri Lanka)
    Removes rows with Countries that only have one incident
    """
    new_df = df.copy()
    new_df = new_df.dropna(subset=["Country"])

    # Converts country column to consistent capitalisation and strips spaces
    new_df["Country"] = new_df["Country"].apply(lambda x: x.strip().title())
    new_df["Country"] = new_df["Country"].apply(lambda x: "USA" if x == "Usa" else x)

    #Removes rows that contain Oceans and Seas for the country
    new_df = new_df[~new_df["Country"].str.contains("Ocean", na=False)]
    new_df = new_df[~new_df["Country"].str.contains("Central Pacific", na=False)]
    new_df = new_df[~new_df["Country"].str.contains(" Sea", na=False)]
    new_df = new_df[~new_df["Country"].str.contains("Persian Gulf", na=False)]

    #Corrects country names
    new_df["Country"] = new_df["Country"].replace("Ceylon (Sri Lanka)", "Sri Lanka")
    new_df["Country"] = new_df["Country"].replace("Ceylon", "Sri Lanka")
    new_df["Country"] = new_df["Country"].replace("Maldive Islands", "Maldives")
    new_df["Country"] = new_df["Country"].replace("St. Maartin", "St Martin")
    new_df["Country"] = new_df["Country"].replace("St. Martin", "St Martin")
    new_df["Country"] = new_df["Country"].replace("Reunion Island", "Reunion")
    new_df["Country"] = new_df["Country"].replace("Trinidad", "Trinidad & Tobago")
    new_df["Country"] = new_df["Country"].replace("Tobago", "Trinidad & Tobago")
    new_df["Country"] = new_df["Country"].replace("Turks And Caicos", "Turks & Caicos")
    new_df["Country"] = new_df["Country"].replace("Sudan?", "Sudan")
    new_df["Country"] = new_df["Country"].replace("United Arab Emirates (Uae)?", "United Arab Emirates")
    new_df["Country"] = new_df["Country"].replace("United Arab Emirates (Uae)", "United Arab Emirates")
    new_df["Country"] = new_df["Country"].replace("Western Samoa", "Samoa")
    new_df["Country"] = new_df["Country"].replace("Scotland", "United Kingdom")
    new_df["Country"] = new_df["Country"].replace("Crete", "Greece")
    new_df["Country"] = new_df["Country"].replace("Okinawa", "Japan")
    new_df["Country"] = new_df["Country"].replace("Columbia", "Colombia")
    new_df["Country"] = new_df["Country"].replace("England", "United Kingdom")
    new_df["Country"] = new_df["Country"].replace("New Britain", "Papua New Guinea")
    new_df["Country"] = new_df["Country"].replace("New Guinea", "Papua New Guinea")
    new_df["Country"] = new_df["Country"].replace('St Helena, British Overseas Territory', "St Helena")
    new_df["Country"] = new_df["Country"].replace('Burma', "Myanmar")

    #Counts occurences of each country
    country_counts = new_df["Country"].value_counts() #Contains 6923


    # Filter countries that appear more than two times
    countries_to_keep = country_counts[country_counts > 1].index
    new_df = new_df[new_df["Country"].isin(countries_to_keep)]

    return new_df

#Owen
def hemisphere(df: pd.DataFrame):
    """Adds in a "Hemisphere" column
    This uses a dictionary listing whether each country is in the "North", "South" or on the "Equator"
    If a country is missing from this dictionary it returns "Na"
    """

    new_df = df.copy()

    hemi_dict = {
        'American Samoa': "South",
        'Antigua': 'North',
        'Argentina': "South",
        'Australia': "South",
        'Azores': "North",
        'Bahamas': "North",
        'Barbados': "North",
        'Belize': "North",
        'Bermuda': "North",
        'Brazil': "Equator",
        'Myanmar': "North",
        'Canada': "North",
        'Cape Verde': "North",
        'Cayman Islands': "North",
        'Chile': "South",
        'China': "North",
        'Colombia': "Equator",
        'Costa Rica': "North",
        'Croatia': "North",
        'Cuba': "North",
        'Dominican Republic': "North",
        'Ecuador': "Equator",
        'Egypt': "North",
        'El Salvador': "North",
        'Fiji': "South",
        'France': "North",
        'French Polynesia': "South",
        'Greece': "North",
        'Grenada': "North",
        'Guam': "North",
        'Guinea': "North",
        'Guyana': "North",
        'Haiti': "North",
        'Honduras': "North",
        'Hong Kong': "North",
        'Iceland': "North",
        'India': "North",
        'Indonesia': "Equator",
        'Iran': "North",
        'Iraq': "North",
        'Ireland': "North",
        'Israel': "North",
        'Italy': "North",
        'Jamaica': "North",
        'Japan': "North",
        'Johnston Island': "North",
        'Kenya': "Equator",
        'Kiribati': "Equator",
        'Lebanon': "North",
        'Liberia': "North",
        'Libya': "North",
        'Madagascar': "South",
        'Malaysia': "North",
        'Maldives': "Equator",
        'Malta': "North",
        'Marshall Islands': "North",
        'Martinique': "North",
        'Mauritius': "South",
        'Mexico': "North",
        'Micronesia': "North",
        'Montenegro': "North",
        'Mozambique': "South",
        'Namibia': "South",
        'New Caledonia': "South",
        'New Zealand': "South",
        'Nicaragua': "North",
        'Nigeria': "North",
        'Norway': "North",
        'Palau': "North",
        'Panama': "North",
        'Papua New Guinea': "South",
        'Peru': "South",
        'Philippines': "North",
        'Portugal': "North",
        'Reunion': "South",
        'Russia': "North",
        'Samoa': "South",