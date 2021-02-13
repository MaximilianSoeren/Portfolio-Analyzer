"""
This application will create a localy hosted website that will let you interact with data taken from a csv-file
taken from your depot. And will allow you to interact and explore said data in different ways.
"""
# Importing all modules / files we need
import streamlit as st
import pandas as pd
import os
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
#----------------------here are all classes defined that are used-----------------------------------



class Data_Frame_Consors:
    def __init__(self, new_df):
        self.new_df = new_df

    def get_depot_name(self):  # This function gets the depot name
        return self.new_df.iloc[0:1, :1]

    def get_depot_value(self):
        return self.new_df.iloc[3:4, :1]

    def get_depot_dev_abs(self):
        return self.new_df.iloc[3:4, 1:2]

    def get_depot_dev_per(self):
        return self.new_df.iloc[3:4, 2:3]

    def get_pos_name(self):
        return self.new_df.iloc[6:, :1].dropna().head(-1)

    def get_pos_wkn(self):
        return self.new_df.iloc[6:, 1:2].dropna().head(-1)

    def get_pos_type(self):
        return self.new_df.iloc[6:, 2:3].dropna().head(-1)

    def get_pos_shares(self):
        return self.new_df.iloc[6:, 3:4].dropna().head(-1)
    
    def get_pos_ex(self):
        return self.new_df.iloc[6:, 12:13].dropna().head(-1)

    def get_pos_value(self):
        return self.new_df.iloc[6:, 13:14].dropna().head(-1)
    
    def get_pos_dev_abs(self):
        return self.new_df.iloc[6:, 14:15].dropna().head(-1)

    def get_pos_dev_per(self):
        return self.new_df.iloc[6:, 16:17].dropna().head(-1)

    def get_for_sorting(self):
        return self.new_df.iloc[5:].dropna()

    def replace_header_w_first_row(self):
        new_df = self.new_df.rename(columns=self.new_df.iloc[0]).drop(
            self.new_df.index[0])
        return new_df

    def get_best_position_absolute(self):
        df1 = self.new_df.replace_header_w_first_row(
            self.new_df.get_for_sorting())
        df2 = df1['Entwicklung absolut'].apply(lambda x: x.replace('.', ''))
        df2 = df2.apply(lambda x: x.replace(',', '.'))
        df1['Entwicklung absolut'] = df2
        df1['Entwicklung absolut'] = df1['Entwicklung absolut'].astype(float)
        df_sorted = df1.sort_values(['Entwicklung absolut'], ascending=False)
        df_first = df_sorted.head(1)
        df_name = df_first['Name']
        df_att_percent = df_first['Entwicklung prozentual'].astype(str) + " %"
        df_att_abs = df_first['Entwicklung absolut'].astype(str) + " €"
        df_fixed = df_name + " | " + df_att_abs + " | " + df_att_percent
        return df_fixed

    # this is horrible, please future me, find a better solution.
    def get_best_position_percentage(self):
        df1 = self.new_df.replace_header_w_first_row(
            self.new_df.get_for_sorting())
        df2 = df1['Entwicklung prozentual'].apply(lambda x: x.replace('.', ''))
        df2 = df2.apply(lambda x: x.replace(',', '.'))
        df1['Entwicklung prozentual'] = df2
        df1['Entwicklung prozentual'] = df1['Entwicklung prozentual'].astype(
            float)
        df_sorted = df1.sort_values(['Entwicklung prozentual'],
                                    ascending=False)
        df_first = df_sorted.head(1)
        df_name = df_first['Name']
        df_att_percent = df_first['Entwicklung prozentual'].astype(str) + " %"
        df_att_abs = df_first['Entwicklung absolut'].astype(str) + " €"
        df_fixed = df_name + " | " + df_att_abs + " | " + df_att_percent
        return df_fixed


#
# this function will get the worst position in the portfolio depended on the absolute value (most € lost)

    def get_worst_position_absolute(self):
        df1 = self.new_df.replace_header_w_first_row(
            self.new_df.get_for_sorting())
        df2 = df1['Entwicklung absolut'].apply(lambda x: x.replace('.', ''))
        df2 = df2.apply(lambda x: x.replace(',', '.'))
        df1['Entwicklung absolut'] = df2
        df1['Entwicklung absolut'] = df1['Entwicklung absolut'].astype(float)
        df_sorted = df1.sort_values(['Entwicklung absolut'])
        df_first = df_sorted.head(1)
        df_name = df_first['Name']
        df_att_percent = df_first['Entwicklung prozentual'].astype(str) + " %"
        df_att_abs = df_first['Entwicklung absolut'].astype(str) + " €"
        df_fixed = df_name + " | " + df_att_abs + " | " + df_att_percent
        return df_fixed

        # this function will get the worst position in the portfolio depended on the percentage value (most % lost)
    def get_worst_position_percentage(self):
        df1 = self.new_df.replace_header_w_first_row(
            self.new_df.get_for_sorting())
        df2 = df1['Entwicklung prozentual'].apply(lambda x: x.replace('.', ''))
        df2 = df2.apply(lambda x: x.replace(',', '.'))
        df1['Entwicklung prozentual'] = df2
        df1['Entwicklung prozentual'] = df1['Entwicklung prozentual'].astype(
            float)
        df_sorted = df1.sort_values(['Entwicklung prozentual'])
        df_first = df_sorted.head(1)
        df_name = df_first['Name']
        df_att_percent = df_first['Entwicklung prozentual'].astype(str) + " %"
        df_att_abs = df_first['Entwicklung absolut'].astype(str) + " €"
        df_fixed = df_name + " | " + df_att_abs + " | " + df_att_percent
        return df_fixed

    # creating a function for plotly pie chat that shows the % of the Portfolio of the positions
    def fig_pie_poisitions_per(self):
        lables = self.get_pos_name()
        df1 = self.new_df.replace_header_w_first_row(
            self.new_df.get_for_sorting())
        df2 = df1['Gesamtwert EUR'].apply(lambda x: x.replace('.', ''))
        df2 = df2.apply(lambda x: x.replace(',', '.'))
        df1['Gesamtwert EUR'] = df2
        df1['Gesamtwert EUR'] = df1['Gesamtwert EUR'].astype(float)
        values_of_pos = df1['Gesamtwert EUR']
        values = (values_of_pos / sum(values_of_pos)) * 100
        fig = go.Figure(
            data=[go.Pie(labels=lables, values=values)])
        return fig

    # creates a function that shows the number of shares of each position in a bar graph
    def fig_bar_positions_nr(self):
        df1 = self.new_df.replace_header_w_first_row(
            self.new_df.get_for_sorting())
        fig = px.bar(data_frame=df1,
                             x=df1['Name'],
                             y=df1['Stück/Nominal'])
        return fig

    # is a function that shows the important bits of data from the whole DF. But in a way so you can sort it withint the dataframe.
    def get_sorted_dataframe(self):
        df1 = self.new_df.replace_header_w_first_row(
            self.new_df.get_for_sorting())
        df2 = df1.apply(lambda x: x.str.replace('.', ''))
        df2 = df2[[
            'Gesamtwert EUR', 'Stück/Nominal', 'Einstandskurs inkl. NK',
            'Einstandswert', 'Veränderung Intraday', 'Entwicklung absolut',
            'Entwicklung prozentual'
        ]].apply(lambda x: x.str.replace(',', '.'))
        df3 = df2.astype('float', errors='ignore')
        df1 = pd.concat(
            [self.get_pos_name(),
             self.get_pos_wkn(), df3], axis=1)
        df1 = df1.rename(columns={'Depot': 'Name', 'Inhaber': 'WKN'})
        return df1


class Data_Frame_ING:
    def __init__(self, new_df):
        self.new_df = new_df

    def get_for_sorting(self):
        return self.new_df.iloc[:].dropna()





class Data_Frame_Comdirect:
    def __init__(self, new_df):
        self.new_df = new_df

    def get_for_sorting(self):
        return self.new_df



#--This is the start of the website. BUT ONLY the upload functions. The rest is defined lower.------------------------------------------
# Defining all CSS styles that are needed (DARKMODE ETC)
darkmode = """
<style>
body {
  background-color: black;
  color: white
  }
.css-2trqyj{
    color: black
}
p {
    color: white;
    }
</style>
"""
st.markdown(darkmode, unsafe_allow_html=True)

# Uploader inside a collapsable div, that automatically reads the csv files according to the type.
expander = st.beta_expander('', expanded=True)
with expander:
    col1, col2, col3 = st.beta_columns(3)

    with col1:
        uploaded_file_consors = st.file_uploader("CONSORS", type=".csv", key=1)
    if uploaded_file_consors:
        df_consors = Data_Frame_Consors(pd.read_csv(uploaded_file_consors, sep=";", encoding="utf-8"))
    with col2:
        uploaded_file_ign = st.file_uploader("ING", type=".csv",key=2)
    if uploaded_file_ign:
        df_ign = Data_Frame_ING(pd.read_csv(uploaded_file_ign, sep=";", encoding="iso-8859-1", skiprows=4))
    with col3:
        uploaded_file_comdirect = st.file_uploader("COMDIRECT", type=".csv", key=3)
    if uploaded_file_comdirect:
        df_comdirect = Data_Frame_Comdirect(pd.read_csv(uploaded_file_comdirect, sep=';', encoding='iso-8859-1', skiprows=1))

#Creating dataframes from all csv files.

# Defining the structure of the website
header = st.beta_container()

# all of the below code is to build the landing page / page that comes up when Navigation -> Depot
with header:
    st.title("Willkommen zu deinem Dashboard")
    st.text(
        "Sobald du eine CSV Datei deines Portfolios *CONSORS | ING | COMDIRECT* hochgeladen hast, kannst du hier"
        "alle wichtigen Informationen nachschauen.")
    st.text("Bitte wähle unten aus welche Portfolios du auswerten willst.")
    st.write("---")
    col1, col2, col3 = st.beta_columns(3)
    with col1:
        st.write("Consors")
        consors = st.checkbox("CONSORS", key=1)
    with col2:
        st.write("ING")
        ing = st.checkbox("ING", key=2)
    with col3:
        st.write("Comdirect")
        comdirect =  st.checkbox("", key=3)
    st.write("---")
# df_final_consors = pd.DataFrame(columns=["Name", "ISIN", "Art", "Stück", "Gesamtwert", "Stückpreis", "Entwicklung Absolut(Aktie)", "Entwicklung Prozentual(Aktie)", "Handelsplatz"])


#---------------------here are all the functions used------------------------------------

# THis function creates a new dataframe from the Consors CSV and makes that ready to be merged with the other dataframes by renaming columns and headers.
def get_consors_df_to_merge():
    df1 = Data_Frame_Consors.get_for_sorting(df_consors)
    df1_header = df1.rename(columns=df1.iloc[0]).drop(df1.index[0])
    df1_size = df1_header.drop(["Einstandskurs inkl. NK", "Währung/Prozent", "Datum/Zeit", "Einstandswert", "Veränderung Intraday"], axis=1)
    df_for_merge_consors = df1_size.rename(columns={"WKN": "WKN/ISIN", "Gattung": "Art", "Stück/Nominal": "Stück", "Kurs": "Stückpreis", "Gesamtwert EUR": "Gesamtwert",
                                         "Entwicklung absolut": "Entwicklung Absolut", "Entwicklung prozentual": "Entwicklung Prozentual"})
    return df_for_merge_consors



def get_ing_df_to_merge():
    df1 = Data_Frame_ING.get_for_sorting(df_ign)
    df_size = df1.drop(columns=["Zeit", "Währung", "Währung.1", "Währung.2", "Währung.3", "Währung.4", "Einstandskurs", "Einstandswert"], axis=1)
    df_for_merge_ing = df_size.rename(columns={"ISIN": "WKN/ISIN", "Einheitskennzeichen": "Art", "Stück/Nominale": "Stück", "Bewertungskurs": "Stückpreis", "Kurswert": "Gesamtwert",
                                         "Gewinn/Verlust": "Entwicklung Absolut", "Gewinn/Verlust (%)": "Entwicklung Prozentual", "Wertpapiername": "Name"})
    df_for_merge_ing = df_for_merge_ing.apply(lambda x: x.str.replace('Stück', 'Aktie'))
    return df_for_merge_ing

def get_comdirect_to_merge():
    df1 = Data_Frame_Comdirect.get_for_sorting(df_comdirect)
    # df1_header = df1.rename(columns=df1.iloc[0]).drop(df1.index[0])
    df1_com = df1.drop(columns=[ "Kaufwert in EUR", "Währung", "Notizen", "Diff. abs", "Diff. %", "Kaufkurs in EUR", "Datum",  "Zeit", "Unnamed: 17"], axis=1)
    df1_com = df1_com.dropna()
    df_to_merge_comdirect = df1_com.rename(columns={"WKN": "WKN/ISIN", "Typ": "Art", "Stück/Nom.": "Stück", "Akt. Kurs": "Stückpreis", "Wert in EUR": "Gesamtwert",
                                         "Diff. abs.1": "Entwicklung Absolut", "Diff. %.1": "Entwicklung Prozentual", "Bezeichnung": "Name", "Börse": "Handelsplatz"})

    # df1_com = df1_com.dropna()
    return df_to_merge_comdirect

def sort_df(df):
    df = df[["Name", "WKN/ISIN", "Art", "Stück", "Gesamtwert", "Stückpreis", "Entwicklung Absolut", "Entwicklung Prozentual", "Handelsplatz"]]
    return df


def join_all_df():
    df_merged_all = pd.concat([get_comdirect_to_merge(), get_consors_df_to_merge(), get_ing_df_to_merge()], ignore_index=True)
    df_merged_all = df_merged_all[["Name", "WKN/ISIN", "Art", "Stück", "Gesamtwert", "Stückpreis", "Entwicklung Absolut", "Entwicklung Prozentual", "Handelsplatz"]]
    return df_merged_all


def join_consors_ing():
    df_merged_consors_ing = pd.concat([get_consors_df_to_merge(), get_ing_df_to_merge()])
    df_merged_consors_ing = df_merged_consors_ing[["Name", "WKN/ISIN", "Art", "Stück", "Gesamtwert", "Stückpreis", "Entwicklung Absolut", "Entwicklung Prozentual", "Handelsplatz"]]
    return df_merged_consors_ing


def join_consors_comdirect():
    df_merged_consors_comdirect = pd.concat([get_consors_df_to_merge(), get_comdirect_to_merge()])
    df_merged_consors_comdirect = df_merged_consors_comdirect[["Name", "WKN/ISIN", "Art", "Stück", "Gesamtwert", "Stückpreis", "Entwicklung Absolut", "Entwicklung Prozentual", "Handelsplatz"]]
    return df_merged_consors_comdirect


def join_ing_comdirect():
    df_merged_ing_comdirect = pd.concat([get_comdirect_to_merge(), get_ing_df_to_merge()])
    df_merged_ing_comdirect = df_merged_ing_comdirect[["Name", "WKN/ISIN", "Art", "Stück", "Gesamtwert", "Stückpreis", "Entwicklung Absolut", "Entwicklung Prozentual", "Handelsplatz"]]
    return df_merged_ing_comdirect


def make_column_into_float(df):
    df1_new = df[["Name", "WKN/ISIN", "Art", "Handelsplatz"]]
    df2_new = df[["Stück", "Gesamtwert", "Stückpreis", "Entwicklung Absolut", "Entwicklung Prozentual"]]
    df2_new = df2_new.apply(lambda x: x.str.replace('.', ''))
    df2_new = df2_new.apply(lambda x: x.str.replace(',', '.'))
    df2_new = df2_new.apply(lambda x: x.str.replace('%', ''))
    df2_new = df2_new.astype('float')
    df_fixed = pd.concat([df1_new, df2_new], axis=1)
    df_fixed = df_fixed[["Name", "WKN/ISIN", "Art", "Stück", "Gesamtwert", "Stückpreis", "Entwicklung Absolut", "Entwicklung Prozentual", "Handelsplatz"]]
    return df_fixed


# This function will show the total value of any portfolio df combination (or just single df)
def get_total_value_portfolio(df):
    total_value = df["Gesamtwert"].sum().round(2)
    return total_value

def get_total_growth_abs_portfolio(df):
    total_value = df["Entwicklung Absolut"].sum().round(2)
    return total_value

def get_total_growth_per_portfolio(df):
    total_value = df["Entwicklung Prozentual"].sum().round(2)
    return total_value
# this function takes a float value and converts it into string type.
def convert_float_into_str(value):
    value = value.astype('str')
    return value

# This function will spit out the total portfolio value of all 3 portfolios combined
def get_depot_value_total():
    df = join_all_df()
    df_float = make_column_into_float(df)
    df_value = get_total_value_portfolio(df_float)
    df_str = convert_float_into_str(df_value)
    return df_str

# this function calculates the total absolute (VALUE) growth of all 3 portfolios
def get_growth_abs_total():
    df = join_all_df()
    df_float = make_column_into_float(df)
    df_value = get_total_growth_abs_portfolio(df_float)
    df_str = convert_float_into_str(df_value)
    return df_str

def get_growth_per_total():
    df = join_all_df()
    df_float = make_column_into_float(df)
    df_value = get_total_growth_per_portfolio(df_float)
    df_str = convert_float_into_str(df_value)
    return df_str

# This function creates a piec_chart that shows the % of each position based on the value of that position compared to the total value
def pie_position_dist_per():
    df_float = make_column_into_float(join_all_df())
    df_float.loc[df_float['Gesamtwert'] < 0.1, 'Name'] = "Other"
    fig = px.pie(df_float, values="Gesamtwert", names="Name")
    return fig




# This will delete the header and index of said dataframe AND convert it to a string.
def no_header_no_index(df):
    df_new = df.to_string(index=None, header=None)
    return df_new
    # df_sorted = df_float.sort_values(by="Gesamtwert", ascending=False)
    # values = (df_float["Gesamtwert"] / sum(df_float["Gesamtwert"])) * 100
    # values_fixed = df_sorted(10)

# this will replace the header of the given Dataframe with the first row of said dataframe
def replace_header_w_first_row(self):
    new_df = self.new_df.rename(columns=self.new_df.iloc[0]).drop(
        self.new_df.index[0])
    return new_df


# # this will turn any single value into a float type.
# def fig_pie_poisitions_per(df):
#     values_of_pos = df1['Gesamtwert EUR']
#     values = (values_of_pos / sum(values_of_pos)) * 100
#     fig = go.Figure(
#         data=[go.Pie(labels=lables, values=values)])
#     return fig





#this will turn a column of the dataframe into float type.
# def turn_str_into_float(col):
#     df1 = replace_header_w_first_row(
#         classes.Data_Frame_Consors.get_for_sorting())
#     df2 = df2[col].apply(lambda x: x.replace(',', '.'))
#     df1[col] = df2
#     df1[col] = df1[col].astype(float)
#     return df1[col]



if consors and ing and comdirect:
        col1, col2, col3 = st.beta_columns(3)
        with col1:
            st.header("Depotwert")
            st.subheader(get_depot_value_total() + " €")
        with col2:
            st.header("Depotentwicklung €")
            st.subheader(get_growth_abs_total() + " €")
        with col3:
            st.header("Depotentwicklung %")
            st.subheader(get_growth_per_total() + " %")
        st.write(pie_position_dist_per())









if consors and ing and not comdirect:
    pass

if consors and comdirect and not ing:
    pass

if ing and comdirect and not consors:
    pass

if consors and not ing and comdirect:
    pass

if ing and not consors and comdirect:
    pass

if comdirect and not ing and consors:
    pass
# ----------------------------------------------------------------------------------------------------------------------
#     # this is the display functions for "Protfolioname / Gesamtdepotwert / Entwicklung...



# #     # ----------------------------------------------------------------------------------------------------------------------
# #     # display functions for best / worst stock
# with features2:
#     col4, col5 = st.beta_columns(2)
#     best_share = col4.beta_expander("Beste Aktie")
#     with best_share:
#         st.subheader(
#             (no_header_no_index(classes.get_best_position_absolute())))
#         st.subheader(
#             (no_header_no_index(df.get_best_position_percentage())))
#     worst_share = col5.beta_expander("Schlechteste Aktie")
#     with worst_share:
#         st.subheader((no_header_no_index(get_worst_position_absolute())))
#         st.subheader(
#             (no_header_no_index(get_worst_position_percentage())))
#     col4.write("---")
#     col5.write('---')
# with features3:
#     portfolio_per = col4.beta_expander("% der Position vom Portfolio")
#     with portfolio_per:
#         st.plotly_chart(fig_pie_poisitions_per())
#     portfolio_shares = col5.beta_expander("Stückanzahl pro Position")
#     with portfolio_shares:
#         st.plotly_chart(fig_bar_positions_nr())
#     col5.write('---')
#     col4.write("---")
# with features4:
#     all_data = st.beta_expander("Alles im Überblick")
#     with all_data:
#         st.write(get_sorted_dataframe())

#------------here we define the rest of the programm----------------------

# st.write(get_consors_df_to_merge())
# st.write(get_ing_df_to_merge())
# st.write(get_comdirect_to_merge())
st.write(make_column_into_float(join_all_df()))
# st.header(get_total_value_portfolio(make_column_into_float(get_comdirect_to_merge())))
