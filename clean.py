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
def clean_dates2(df: pd.DataFrame):
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
    """Removes empty columns and named "Fatal" correctly """
    new_df = df.rename(columns={'Unnamed: 11': 'Fatal'})
    new_df = new_df.drop(['href formula', 'href','Case Number', 'Case Number.1',
       'original order', 'Unnamed: 21', 'Unnamed: 22', "pdf"], axis=1)
    new_df = new_df.drop_duplicates()
    return new_df

#Constanza
def clean_type(df: pd.DataFrame):
    """ Cleans "type" column """
    new_df = df.copy()
    new_df['Type'] = new_df['Type'].replace({' Provoked': 'Provoked'})

    values_to_replace = ['Questionable', 'Watercraft', 'Sea Disaster', '?', 'Unconfirmed', 'Unverified', 'Invalid', 'Under investigation', 'Boat']
    new_df['Type'] = new_df['Type'].replace(values_to_replace, 'Unknown')

    return new_df

#Owen
def clean_country(df: pd.DataFrame):
    """Tidies the "Country" column of the DataFrama """
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
    """Adds in a "Hemisphere" column using a dictionary to determine which hemisphere the country is in """

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
        'Saudi Arabia': "North",
        'Senegal': "North",
        'Seychelles': "South",
        'Sierra Leone': "North",
        'Singapore': "North",
        'Solomon Islands': "South",
        'Somalia': "Equator",
        'South Africa': "South",
        'South Korea': "North",
        'Spain': "North",
        'Sri Lanka': "South",
        'St Helena, British Overseas Territory': "South",
        'St Martin': "North",
        'St Helena': "South",
        'Sudan': "North",
        'Taiwan': "North",
        'Tanzania': "Equator",
        'Thailand': "North",
        'Tonga': "South",
        'Trinidad & Tobago': "North",
        'Tunisia': "North",
        'Turkey': "North",
        'Turks & Caicos': "North",
        'USA': "North",
        'United Arab Emirates': "North",
        'United Kingdom': "North",
        'Uruguay': "South",
        'Vanuatu': "South",
        'Venezuela': "North",
        'Vietnam': "North",
        'West Indies': "North",
        'Yemen': "North"
    }

    #is assigning a "Hemisphere" column to new_df by mapping each entry in the "Country" column to a hemisphere based on a dictionary, hemi_dict.
    new_df["Hemisphere"] = new_df["Country"].apply(lambda country: hemi_dict.get(country, "Na"))

    #Code here
    return new_df

#filip
def clean_sex(df: pd.DataFrame):
    df2 = df.copy()
    df2["Sex"] = df2["Sex"].replace({ ' M': 'M', 'M ': 'M', 'M x 2': 'M',})
    df2["Sex"] = df2["Sex"].replace(['.', 'lli', 'N'], np.nan)
    return df2

#filip
def clean_age(shark_df: pd.DataFrame):
    shark_df["Age"] = shark_df["Age"].replace({
        '30s': '30',
        '20/30': '25',
        '20s': '20',
        '50s': '50',
        '40s': '40',
        '60s': '60',
        "20's": '20',
        '18 months': '2',
        '18 or 20': '19',
        '12 or 13': '13',
        '8 or 10': '9',
        '30 or 36': '33',
        '6½': '6',
        '21 & ?': '21',
        '33 or 37': '35',
        'mid-30s': '35',
        '23 & 20': '21',
        '28': '28',
        '20?': '20',
        "60's": '62',
        '32 & 30': '31',
        '16 to 18': '17',
        'mid-20s': '25',
        'Ca. 33': '33',
        '45 ': '45',
        '21 or 26': '24',
        '20 ': '20',
        '>50': '55',
        '18 to 22': '20',
        '9 & 12': '10',
        '? & 19': '19',
        '9 months': '1',
        '25 to 35': '30',
        '23 & 26': '24',
        '33 & 37': '35',
        '25 or 28': '26',
        '30 & 32': '31',
        '50 & 30': '40',
        '13 or 18': '16',
        '34 & 19': '31',
        '33 & 26': '30',
        '2 to 3 months': '1',
        '43': '43',
        '7 or 8': '8',
        '17 & 16': '17',
        'Both 11': '11',
        '9 or 10': '10',
        '36 & 23': '30',
        '10 or 12': '11',
        '31 or 33': '32',
        '2½': '2',
        '13 or 14': '14'
    })

    shark_df["Age"] = shark_df["Age"].str.strip()
    shark_df["Age"] = shark_df["Age"].replace([
        'Middle age', np.nan, '?',
        '!2', 'teen', 'Teen', '!6', '!!', '45 and 15', '28 & 22',
        '9 & 60', 'a minor', '28 & 26', '46 & 34', '28, 23 & 30', 'Teens',
        '36 & 26', '\xa0', ' ', '7      &    31',
        'Elderly', 'adult', '(adult)',
        '37, 67, 35, 27, ? & 27', '21, 34,24 & 35', '17 & 35',
        'X', '"middle-age"', 'MAKE LINE GREEN', '"young"', 'F',
        'young', '  ', 'A.M.',
           '?    &   14', 'M', '',
    ], np.nan)
    return(shark_df)

def age_group(age):
    if pd.isna(age):
        return "Unknown"
    if age >= 100:
        return "100+"
    elif 90 <= age < 100:
        return "90-99"
    elif 80 <= age < 90:
        return "80-89"
    elif 70 <= age < 80:
        return "70-79"
    elif 60 <= age < 70:
        return "60-69"
    elif 50 <= age < 60:
        return "50-59"
    elif 40 <= age < 50:
        return "40-49"
    elif 30 <= age < 40:
        return "30-39"
    elif 20 <= age < 30:
        return "20-29"
    elif 10 <= age < 20:
        return "10-19"
    elif age < 10:
        return "0-9"
    else:
        return "Na"

def age_groups(shark_df: pd.DataFrame):
    shark_df["Age"] = pd.to_numeric(shark_df["Age"], errors="coerce")
    shark_df["Age Group"]= shark_df["Age"].apply(age_group)
    return shark_df

def add_month(shark_df: pd.DataFrame):
    shark_df['Date'] = pd.to_datetime(shark_df['Date'], errors='coerce')
    shark_df['Month'] = shark_df['Date'].dt.month
    return shark_df

def assign_season(row):
    month = row['Month']
    hemisphere = row['Hemisphere']
    
    if hemisphere == 'North':
        if month in [12, 1, 2]:
            return 'Winter'
        elif month in [3, 4, 5]:
            return 'Spring'
        elif month in [6, 7, 8]:
            return 'Summer'
        elif month in [9, 10, 11]:
            return 'Fall'
    elif hemisphere == 'South':
        if month in [12, 1, 2]:
            return 'Summer'
        elif month in [3, 4, 5]:
            return 'Fall'
        elif month in [6, 7, 8]:
            return 'Winter'
        elif month in [9, 10, 11]:
            return 'Spring'
    return 'Unknown'

def add_season(shark_df: pd.DataFrame):
    shark_df['Season'] = shark_df.apply(assign_season, axis=1)
    return shark_df

def clean_activity(df: pd.DataFrame):
    version_2 = df.copy()
    
    #converts to lower case
    version_2.loc[:, "Activity"] = version_2["Activity"].str.lower()

    #version_2 = version_2.dropna(subset=["Activity"])

    #count activities
    activities = version_2["Activity"].value_counts()
    threshold = 5
    new_activities = activities[activities >= threshold].index

     # Replace NaN with "Unknown"
    version_2["Activity"] = version_2["Activity"].fillna("unknown")

    # Replace activities below threshold with "Unknown"
    version_2.loc[~version_2["Activity"].isin(new_activities), "Activity"] = "unknown"


    acivity_corrections = {"swimming": "swimming", "bathing": "swimming","treading water": "swimming", " swimming" : "swimming", "floating on his back": "swimming", "swimming ": "swimming", "freedom swimming":"swimming",
                       "free diving": "diving", "free diving for abalone" : "diving",
                       "diving for trochus" : "diving", "skindiving" : "diving",
                       "spearfishing on scuba": "spearfishing", "spearfishing / free diving": "spearfishing", "spearfishing": "spearfishing",
                       " spearfishing" : "spearfishing", "spearfishing " : "spearfishing",
                       "diving for abalone": "diving", "unknown":"unknown", 
                       "stand-up paddleboarding": "paddleboarding", "paddleboarding":"paddleboarding",
                        "surf skiing ": "surf ski", "surf-skiing": "surf ski", "surf skiing":"surf ski"," surf skiing":"surf ski", "surf skiing ":"surf ski",
                        "sitting on surfboard" : "surfing", "surfing":"surfing", "surfing (sitting on his board)" : "surfing", "surfing ": "surfing", " surfing": "surfing",
                        "fishing for mackerel": "fishing", "wade fishing" : "fishing",
                        "body boarding": "body surfing", "freediving": "diving",
                        "walking": "wading", "wading": "wading", "standing": "wading",
                       "scuba diving": "diving", "diving": "diving", "pearl diving" : "diving", "snorkeling": "diving",
                       "kayak fishing": "fishing", "fishing for sharks" : "fishing", "shark fishing" : "fishing",
                        "hard hat diving": "diving", "paddleskiing" : "paddle boarding", "fell overboard" : "sailing",
                       "floating" : "swimming", "fishing on a boat": "fishing", "surf fishing": "fishing", " fishing": "fishing", "fishing ": "fishing"
                        }
    version_2["Activity"] = version_2["Activity"].replace(acivity_corrections) # apply corrections
    version_2["Activity"] = version_2["Activity"].str.title()

    return version_2

def clean_fatal(df: pd.DataFrame) -> pd.DataFrame:
    # Create a mapping for the valid values
    valid_values = {
        'Y': 'Y',
        'N': 'N',
        'UNKNOWN': 'UNKNOWN',
        'n': 'N',
        ' N': 'N',
        'Nq': 'N',
        'F': 'UNKNOWN',  # Assuming 'F' means fatal but is not standardized
        '': 'UNKNOWN'  # Any empty strings to UNKNOWN
    }
    
    # Replace the values using the mapping
    df['Fatal'] = df['Fatal'].replace(valid_values)
    
    # Optional: Handle any remaining invalid entries by setting them to 'UNKNOWN'
    df['Fatal'] = df['Fatal'].where(df['Fatal'].isin(['Y', 'N', 'UNKNOWN']), 'UNKNOWN')
    
    return df

def cleaning(df: pd.DataFrame):
    df2 = df.copy()
    df2 = clean_dates2(df2)
    df2 = clean_country(df2)
    df2 = clean_type(df2)
    df2 = clean_states(df2)
    df2 = clean_age(df2)
    df2 = clean_sex(df2)
    df2 = clean_cols(df2)
    df2 = age_groups(df2)
    df2 = hemisphere(df2)
    df2 = add_month(df2)
    df2 = add_season(df2)
    df2 = clean_activity(df2)
    df2 = clean_fatal(df2)
    return df2