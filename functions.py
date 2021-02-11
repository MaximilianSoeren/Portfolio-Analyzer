# Defining all functions used in this code
import imports
import classes as cl


def reading_csv_consors(csv):
    df = cl.Data_Frame_Consors(
        imports.pd.read_csv(csv,
                            sep=';',
                            thousands='.',
                            delimiter=',',
                            encoding='utf-8'))
    return df

def reading_csv_ing(csv):
    df = cl.Data_Frame_Consors(
        imports.pd.read_csv(csv,
                            sep=';',
                            skiprows=5,
                            encoding='utf-8'))
    return df


def reading_csv_comdirect(csv):
     df = cl.Data_Frame_Consors(
        imports.pd.read_csv(csv,
                            sep=';',
                            skiprows=1
                            encoding='utf-8'))
    return df

# This will delete the header and index of said dataframe AND convert it to a string.
def no_header_no_index(df):
    df_new = df.to_string(index=None, header=None)
    return df_new


# this will replace the header of the given Dataframe with the first row of said dataframe
def replace_header_w_first_row(self):
    new_df = self.new_df.rename(columns=self.new_df.iloc[0]).drop(
        self.new_df.index[0])
    return new_df


# this will turn any single value into a float type.
def turn_str_into_float_single_datapoint(func, col):
    df1 = func
    df2 = df1[col].apply(lambda x: x.replace('.', ''))
    df2 = df2.apply(lambda x: x.replace(',', '.'))
    df1[col] = df2
    df1[col] = df1[col].astype(float)
    return df1[col]


#this will turn a column of the dataframe into float type.
def turn_str_into_float(col):
    global df
    df1 = replace_header_w_first_row(
        classes.Data_Frame_Consors.get_for_sorting())
    df2 = df1[col].apply(lambda x: x.replace('.', ''))
    df2 = df2.apply(lambda x: x.replace(',', '.'))
    df1[col] = df2
    df1[col] = df1[col].astype(float)
    return df1[col]


def Data_Frame_Consors():
    df = imports.pd.Dataframe(columns=[
        "Name", "WKN/ISIN", "Art", "Gesamtwert", "Stück",
        "Entwicklung absolut", "Entwicklung prozentual", "Handelsplatz",
        "Gesamtdepotwert", "Entwicklung Depot absolute",
        "Entwicklung Depot prozentual"
    ])
