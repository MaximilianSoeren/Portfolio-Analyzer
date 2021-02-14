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
import plotly as pl
#----------------------here are all classes defined that are used-----------------------------------
st.beta_set_page_config(layout="wide")
# Defining the classes for the different Dataframes of each CSV that is uploaded

class Data_Frame_Consors:
    def __init__(self, new_df):
        self.new_df = new_df

    def get_for_sorting(self):
        return self.new_df.iloc[5:].dropna()


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
.st-bm{
    color: white;
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
    st.subheader("Ich hoffe ihr könnt hiermit etwas anfangen und es gibt euch einsichten die Ihr vielleicht vorher so nicht gesehen habt."
                "Ich wüscnhe euch viel spaß hiermit. Maxi <3")
    st.text(
        "Sobald du eine CSV Datei deines Portfolios *CONSORS | ING | COMDIRECT* hochgeladen hast, kannst du hier"
        "alle wichtigen Informationen nachschauen.")
    st.text("Bitte wähle unten aus welche deiner Portfolios du auswerten willst.")
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
        comdirect =  st.checkbox("COMDIRECT", key=3)
    st.write("---")

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

def get_comdirect_df_to_merge():
    df1 = Data_Frame_Comdirect.get_for_sorting(df_comdirect)
    # df1_header = df1.rename(columns=df1.iloc[0]).drop(df1.index[0])
    df1_com = df1.drop(columns=[ "Kaufwert in EUR", "Währung", "Notizen", "Diff. abs", "Diff. %", "Kaufkurs in EUR", "Datum",  "Zeit", "Unnamed: 17"], axis=1)
    df1_com = df1_com.dropna()
    df_to_merge_comdirect = df1_com.rename(columns={"WKN": "WKN/ISIN", "Typ": "Art", "Stück/Nom.": "Stück", "Akt. Kurs": "Stückpreis", "Wert in EUR": "Gesamtwert",
                                         "Diff. abs.1": "Entwicklung Absolut", "Diff. %.1": "Entwicklung Prozentual", "Bezeichnung": "Name", "Börse": "Handelsplatz"})

    # df1_com = df1_com.dropna()
    return df_to_merge_comdirect


def join_all_df():
    df_merged_all = pd.concat([get_comdirect_df_to_merge(), get_consors_df_to_merge(), get_ing_df_to_merge()], ignore_index=True)
    df_merged_all = df_merged_all[["Name", "WKN/ISIN", "Art", "Stück", "Gesamtwert", "Stückpreis", "Entwicklung Absolut", "Entwicklung Prozentual", "Handelsplatz"]]
    return df_merged_all


def join_consors_ing():
    df_merged_consors_ing = pd.concat([get_consors_df_to_merge(), get_ing_df_to_merge()])
    df_merged_consors_ing = df_merged_consors_ing[["Name", "WKN/ISIN", "Art", "Stück", "Gesamtwert", "Stückpreis", "Entwicklung Absolut", "Entwicklung Prozentual", "Handelsplatz"]]
    return df_merged_consors_ing


def join_consors_comdirect():
    df_merged_consors_comdirect = pd.concat([get_consors_df_to_merge(), get_comdirect_df_to_merge()])
    df_merged_consors_comdirect = df_merged_consors_comdirect[["Name", "WKN/ISIN", "Art", "Stück", "Gesamtwert", "Stückpreis", "Entwicklung Absolut", "Entwicklung Prozentual", "Handelsplatz"]]
    return df_merged_consors_comdirect


def join_ing_comdirect():
    df_merged_ing_comdirect = pd.concat([get_comdirect_df_to_merge(), get_ing_df_to_merge()])
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
def get_depot_value_total(df):
    df_float = make_column_into_float(df)
    df_value = get_total_value_portfolio(df_float)
    df_str = convert_float_into_str(df_value)
    return df_str

# this function calculates the total absolute (VALUE) growth of all 3 portfolios
def get_growth_abs_total(df):
    df_float = make_column_into_float(df)
    df_value = get_total_growth_abs_portfolio(df_float)
    df_str = convert_float_into_str(df_value)
    return df_str

def get_growth_per_portfolio(df):
    df1 = make_column_into_float(df)
    df_value = ((get_total_growth_abs_portfolio(df1) / get_total_value_portfolio(df1)) * 100).round(2)
    df_str = convert_float_into_str(df_value)
    return df_str


def pie_position_dist_per(df):
    df_float = make_column_into_float(df)
    a = df_float['Gesamtwert'] / sum(df_float["Gesamtwert"])
    df_float.loc[a < 0.01, 'Name'] = "Other"
    fig = px.pie(df_float, values="Gesamtwert", names="Name", template="plotly_dark")
    return fig

def bar_position_dist_share(df):
    df_float = make_column_into_float(df)
    a = df_float['Stück'] / sum(df_float["Stück"])
    df_float.loc[a < 0.01, 'Name'] = "Other"
    fig = px.pie(df_float, values="Stück", names="Name", template="plotly_dark")
    return fig

# This will delete the header and index of said dataframe AND convert it to a string.

def get_total_shares(df):
    df1 = make_column_into_float(df)
    total_value = sum(df1["Stück"])
    total_rounded = round(total_value, 3)
    return total_rounded

def get_avrg_value_per_share(df):
    df_float = make_column_into_float(df)
    df_value = get_total_value_portfolio(df_float)
    avrg_value = df_value / get_total_shares(df)
    avrg_value = avrg_value.round(2)
    return avrg_value


def get_avrg_growth_per_share_per(df):
    df_float = make_column_into_float(df)
    df_growrth = get_total_growth_per_portfolio(df_float)
    avrg_share =  get_avrg_value_per_share(df)
    avrg_growth = df_growrth / avrg_share
    avrg_growth = avrg_growth.round(2)
    return avrg_growth

def get_avrg_growth_per_share_abs(df):
    df_float = make_column_into_float(df)
    df_abs = get_total_growth_abs_portfolio(df_float)
    avrg_share =  get_avrg_value_per_share(df)
    avrg_growth = df_abs / avrg_share
    avrg_growth = avrg_growth.round(2)
    return avrg_growth

# gets the best position based on value growth if all 3 potfolios are uploaded
def get_best_pos_val(df):
    df_float = make_column_into_float(df)
    df_sorted = df_float.sort_values("Entwicklung Absolut", ascending=False)
    df_sorted = df_sorted.head(1)
    df_name = df_sorted["Name"]
    df_value = df_sorted["Entwicklung Absolut"].astype('str')
    df_fixed = df_name + " | " + df_value + " €"
    df_fixed = df_fixed.to_string(index=None)
    return df_fixed 

def get_best_pos_per(df):
    df_float = make_column_into_float(df)
    df_sorted = df_float.sort_values("Entwicklung Prozentual", ascending=False)
    df_sorted = df_sorted.head(1)
    df_name = df_sorted["Name"]
    df_value = df_sorted["Entwicklung Prozentual"].astype('str')
    df_fixed = df_name + " | " + df_value + " %"
    df_fixed = df_fixed.to_string(index=None)
    return df_fixed 

def get_worst_pos_val(df):
    df_float = make_column_into_float(df)
    df_sorted = df_float.sort_values("Entwicklung Absolut")
    df_sorted = df_sorted.head(1)
    df_name = df_sorted["Name"]
    df_value = df_sorted["Entwicklung Absolut"].astype('str')
    df_fixed = df_name + " | " + df_value + " €"
    df_fixed = df_fixed.to_string(index=None)
    return df_fixed 

def get_worst_pos_per(df):
    df_float = make_column_into_float(df)
    df_sorted = df_float.sort_values("Entwicklung Prozentual")
    df_sorted = df_sorted.head(1)
    df_name = df_sorted["Name"]
    df_value = df_sorted["Entwicklung Prozentual"].astype('str')
    df_fixed = df_name + " | " + df_value + " %"
    df_fixed = df_fixed.to_string(index=None)
    return df_fixed 


def get_10best_pos_abs(df):
    df_float = make_column_into_float(df)
    df_sorted = df_float.sort_values("Entwicklung Absolut", ascending=False)
    df_sorted = df_sorted.head(10)
    df_name = df_sorted["Name"]
    df_value = df_sorted["Entwicklung Absolut"].astype('str')
    df_fixed = df_name + " | " + df_value + " €"
    df_fixed = df_fixed.rename("Top 10 Aktien nach €")
    df_fixed = df_fixed.reset_index(drop=True)
    return df_fixed 

def get_10best_pos_per(df):
    df_float = make_column_into_float(df)
    df_sorted = df_float.sort_values("Entwicklung Prozentual", ascending=False)
    df_sorted = df_sorted.head(10)
    df_name = df_sorted["Name"]
    df_value = df_sorted["Entwicklung Prozentual"].astype('str')
    df_fixed = df_name + " | " + df_value + " %"
    df_fixed = df_fixed.rename("Top 10 Aktien nach %")
    df_fixed = df_fixed.reset_index(drop=True)
    return df_fixed 

def get_10worst_pos_abs(df):
    df_float = make_column_into_float(df)
    df_sorted = df_float.sort_values("Entwicklung Absolut")
    df_sorted = df_sorted.head(10)
    df_name = df_sorted["Name"]
    df_value = df_sorted["Entwicklung Absolut"].astype('str')
    df_fixed = df_name + " | " + df_value + " €"
    df_fixed = df_fixed.rename("Top 10 Aktien nach €")
    df_fixed = df_fixed.reset_index(drop=True)
    return df_fixed 

def get_10worst_pos_per(df):
    df_float = make_column_into_float(df)
    df_sorted = df_float.sort_values("Entwicklung Prozentual")
    df_sorted = df_sorted.head(10)
    df_name = df_sorted["Name"]
    df_value = df_sorted["Entwicklung Prozentual"].astype('str')
    df_fixed = df_name + " | " + df_value + " %"
    df_fixed = df_fixed.rename("Top 10 Aktien nach %")
    df_fixed = df_fixed.reset_index(drop=True)
    return df_fixed 



if consors and ing and comdirect:
    col1, col2, col3 = st.beta_columns(3)
    with col1:
        st.header("Depotwert")
        st.subheader(get_depot_value_total(join_all_df()) + " €")
    with col2:
        st.header("Depotentwicklung €")
        st.subheader(get_growth_abs_total(join_all_df()) + " €")
    with col3:
        st.header("Depotentwicklung %")
        st.subheader(get_growth_per_portfolio(join_all_df()) + " %")
    st.write("---")
    ba = st.beta_expander("Beste Aktien")
    with ba:
        col4, col5 = st.beta_columns(2)
        with col4:
            st.subheader(get_best_pos_val(join_all_df()))
        with col5:
            st.subheader(get_best_pos_per(join_all_df()))
    wa = st.beta_expander("Schlechteste Aktien")
    with wa:
        col6, col7 = st.beta_columns(2)
        with col6:
            st.subheader(get_worst_pos_val(join_all_df()))
        with col7:
            st.subheader(get_worst_pos_per(join_all_df()))
    col8, col9, col10, col11 = st.beta_columns(4)
    with col8:
        top10val = st.beta_expander("Beste 10 Aktien €")
        with top10val:
            for i in get_10best_pos_abs(join_all_df()):
                st.write(i)
    with col9:
        top10per = st.beta_expander("Beste 10 Aktien %")
        with top10per:
            for i in get_10best_pos_per(join_all_df()):
                st.write(i)
    with col10:
        bad10val = st.beta_expander("Schlechteste 10 Aktien €")
        with bad10val:
            for i in get_10worst_pos_abs(join_all_df()):
                st.write(i)
    with col11:
        bad10per = st.beta_expander("Schlechteste 10 Aktien %")
        with bad10per:
            for i in get_10worst_pos_per(join_all_df()):
                st.write(i)
    col12, col13 = st.beta_columns(2)
    with col12:
        ver_per = st.beta_expander("Anteil der Aktien am Gesamtdepot gemessen am Wert")
        with ver_per:
            st.write(pie_position_dist_per(join_all_df()))
    with col13:
        ver_share = st.beta_expander("Anteil der Aktien am Gesamtdepot gemessen nach Stück")
        with ver_share:
            st.write(bar_position_dist_share(join_all_df()))
    col14, col15, col16, col17 = st.beta_columns(4)
    with col14:
        stk1 = st.beta_expander("Anteile Gesamt")
        with stk1:
            st.subheader(get_total_shares(join_all_df()))
    with col15:
        stk2 = st.beta_expander("Durschnitspreis pro Anteil")
        with stk2:
            st.subheader(convert_float_into_str(get_avrg_value_per_share(join_all_df())) + " €")
    with col16:
        stk3 = st.beta_expander("Durschnitsanstieg pro Aktie €")
        with stk3:
            st.subheader(convert_float_into_str(get_avrg_growth_per_share_abs(join_all_df())) + " €")
    with col17:
        stk4 = st.beta_expander("Durschnitsanstieg pro Aktie %")
        with stk4:
            st.subheader(convert_float_into_str(get_avrg_growth_per_share_per(join_all_df())) + " %")
    df = st.beta_expander("Datentabelle Anzeigen")
    with df:
        st.write(join_all_df())


if consors and ing and not comdirect:
    col1, col2, col3 = st.beta_columns(3)
    with col1:
        st.header("Depotwert")
        st.subheader(get_depot_value_total(join_consors_ing()) + " €")
    with col2:
        st.header("Depotentwicklung €")
        st.subheader(get_growth_abs_total(join_consors_ing()) + " €")
    with col3:
        st.header("Depotentwicklung %")
        st.subheader(get_growth_per_portfolio(join_consors_ing()) + " %")
    st.write("---")
    ba = st.beta_expander("Beste Aktien")
    with ba:
        col4, col5 = st.beta_columns(2)
        with col4:
            st.subheader(get_best_pos_val(join_consors_ing()))
        with col5:
            st.subheader(get_best_pos_per(join_consors_ing()))
    wa = st.beta_expander("Schlechteste Aktien")
    with wa:
        col6, col7 = st.beta_columns(2)
        with col6:
            st.subheader(get_worst_pos_val(join_consors_ing()))
        with col7:
            st.subheader(get_worst_pos_per(join_consors_ing()))
    col8, col9, col10, col11 = st.beta_columns(4)
    with col8:
        top10val = st.beta_expander("Beste 10 Aktien €")
        with top10val:
            for i in get_10best_pos_abs(join_consors_ing()):
                st.write(i)
    with col9:
        top10per = st.beta_expander("Beste 10 Aktien %")
        with top10per:
            for i in get_10best_pos_per(join_consors_ing()):
                st.write(i)
    with col10:
        bad10val = st.beta_expander("Schlechteste 10 Aktien €")
        with bad10val:
            for i in get_10worst_pos_abs(join_consors_ing()):
                st.write(i)
    with col11:
        bad10per = st.beta_expander("Schlechteste 10 Aktien %")
        with bad10per:
            for i in get_10worst_pos_per(join_consors_ing()):
                st.write(i)
    col12, col13 = st.beta_columns(2)
    with col12:
        ver_per = st.beta_expander("Anteil der Aktien am Gesamtdepot gemessen am Wert")
        with ver_per:
            st.write(pie_position_dist_per(join_consors_ing()))
    with col13:
        ver_share = st.beta_expander("Anteil der Aktien am Gesamtdepot gemessen nach Stück")
        with ver_share:
            st.write(bar_position_dist_share(join_consors_ing()))
    col14, col15, col16, col17 = st.beta_columns(4)
    with col14:
        stk1 = st.beta_expander("Anteile Gesamt")
        with stk1:
            st.subheader(get_total_shares(join_consors_ing()))
    with col15:
        stk2 = st.beta_expander("Durschnitspreis pro Anteil")
        with stk2:
            st.subheader(convert_float_into_str(get_avrg_value_per_share(join_consors_ing())) + " €")
    with col16:
        stk3 = st.beta_expander("Durschnitsanstieg pro Aktie €")
        with stk3:
            st.subheader(convert_float_into_str(get_avrg_growth_per_share_abs(join_consors_ing())) + " €")
    with col17:
        stk4 = st.beta_expander("Durschnitsanstieg pro Aktie %")
        with stk4:
            st.subheader(convert_float_into_str(get_avrg_growth_per_share_per(join_consors_ing())) + " %")
    df = st.beta_expander("Datentabelle Anzeigen")
    with df:
        st.write(join_consors_ing())


if consors and comdirect and not ing:
    col1, col2, col3 = st.beta_columns(3)
    with col1:
        st.header("Depotwert")
        st.subheader(get_depot_value_total(join_consors_comdirect()) + " €")
    with col2:
        st.header("Depotentwicklung €")
        st.subheader(get_growth_abs_total(join_consors_comdirect()) + " €")
    with col3:
        st.header("Depotentwicklung %")
        st.subheader(get_growth_per_portfolio(join_consors_comdirect()) + " %")
    st.write("---")
    ba = st.beta_expander("Beste Aktien")
    with ba:
        col4, col5 = st.beta_columns(2)
        with col4:
            st.subheader(get_best_pos_val(join_consors_comdirect()))
        with col5:
            st.subheader(get_best_pos_per(join_consors_comdirect()))
    wa = st.beta_expander("Schlechteste Aktien")
    with wa:
        col6, col7 = st.beta_columns(2)
        with col6:
            st.subheader(get_worst_pos_val(join_consors_comdirect()))
        with col7:
            st.subheader(get_worst_pos_per(join_consors_comdirect()))
    col8, col9, col10, col11 = st.beta_columns(4)
    with col8:
        top10val = st.beta_expander("Beste 10 Aktien €")
        with top10val:
            for i in get_10best_pos_abs(join_consors_comdirect()):
                st.write(i)
    with col9:
        top10per = st.beta_expander("Beste 10 Aktien %")
        with top10per:
            for i in get_10best_pos_per(join_consors_comdirect()):
                st.write(i)
    with col10:
        bad10val = st.beta_expander("Schlechteste 10 Aktien €")
        with bad10val:
            for i in get_10worst_pos_abs(join_consors_comdirect()):
                st.write(i)
    with col11:
        bad10per = st.beta_expander("Schlechteste 10 Aktien %")
        with bad10per:
            for i in get_10worst_pos_per(join_consors_comdirect()):
                st.write(i)
    col12, col13 = st.beta_columns(2)
    with col12:
        ver_per = st.beta_expander("Anteil der Aktien am Gesamtdepot gemessen am Wert")
        with ver_per:
            st.write(pie_position_dist_per(join_consors_comdirect()))
    with col13:
        ver_share = st.beta_expander("Anteil der Aktien am Gesamtdepot gemessen nach Stück")
        with ver_share:
            st.write(bar_position_dist_share(join_consors_comdirect()))
    col14, col15, col16, col17 = st.beta_columns(4)
    with col14:
        stk1 = st.beta_expander("Anteile Gesamt")
        with stk1:
            st.subheader(get_total_shares(join_consors_comdirect()))
    with col15:
        stk2 = st.beta_expander("Durschnitspreis pro Anteil")
        with stk2:
            st.subheader(convert_float_into_str(get_avrg_value_per_share(join_consors_comdirect())) + " €")
    with col16:
        stk3 = st.beta_expander("Durschnitsanstieg pro Aktie €")
        with stk3:
            st.subheader(convert_float_into_str(get_avrg_growth_per_share_abs(join_consors_comdirect())) + " €")
    with col17:
        stk4 = st.beta_expander("Durschnitsanstieg pro Aktie %")
        with stk4:
            st.subheader(convert_float_into_str(get_avrg_growth_per_share_per(join_consors_comdirect())) + " %")
    df = st.beta_expander("Datentabelle Anzeigen")
    with df:
        st.write(join_consors_comdirect())


if ing and comdirect and not consors:
    col1, col2, col3 = st.beta_columns(3)
    with col1:
        st.header("Depotwert")
        st.subheader(get_depot_value_total(join_ing_comdirect()) + " €")
    with col2:
        st.header("Depotentwicklung €")
        st.subheader(get_growth_abs_total(join_ing_comdirect()) + " €")
    with col3:
        st.header("Depotentwicklung %")
        st.subheader(get_growth_per_portfolio(join_ing_comdirect()) + " %")
    st.write("---")
    ba = st.beta_expander("Beste Aktien")
    with ba:
        col4, col5 = st.beta_columns(2)
        with col4:
            st.subheader(get_best_pos_val(join_ing_comdirect()))
        with col5:
            st.subheader(get_best_pos_per(join_ing_comdirect()))
    wa = st.beta_expander("Schlechteste Aktien")
    with wa:
        col6, col7 = st.beta_columns(2)
        with col6:
            st.subheader(get_worst_pos_val(join_ing_comdirect()))
        with col7:
            st.subheader(get_worst_pos_per(join_ing_comdirect()))
    col8, col9, col10, col11 = st.beta_columns(4)
    with col8:
        top10val = st.beta_expander("Beste 10 Aktien €")
        with top10val:
            for i in get_10best_pos_abs(join_ing_comdirect()):
                st.write(i)
    with col9:
        top10per = st.beta_expander("Beste 10 Aktien %")
        with top10per:
            for i in get_10best_pos_per(join_ing_comdirect()):
                st.write(i)
    with col10:
        bad10val = st.beta_expander("Schlechteste 10 Aktien €")
        with bad10val:
            for i in get_10worst_pos_abs(join_ing_comdirect()):
                st.write(i)
    with col11:
        bad10per = st.beta_expander("Schlechteste 10 Aktien %")
        with bad10per:
            for i in get_10worst_pos_per(join_ing_comdirect()):
                st.write(i)
    col12, col13 = st.beta_columns(2)
    with col12:
        ver_per = st.beta_expander("Anteil der Aktien am Gesamtdepot gemessen am Wert")
        with ver_per:
            st.write(pie_position_dist_per(join_ing_comdirect()))
    with col13:
        ver_share = st.beta_expander("Anteil der Aktien am Gesamtdepot gemessen nach Stück")
        with ver_share:
            st.write(bar_position_dist_share(join_ing_comdirect()))
    col14, col15, col16, col17 = st.beta_columns(4)
    with col14:
        stk1 = st.beta_expander("Anteile Gesamt")
        with stk1:
            st.subheader(get_total_shares(join_ing_comdirect()))
    with col15:
        stk2 = st.beta_expander("Durschnitspreis pro Anteil")
        with stk2:
            st.subheader(convert_float_into_str(get_avrg_value_per_share(join_ing_comdirect())) + " €")
    with col16:
        stk3 = st.beta_expander("Durschnitsanstieg pro Aktie €")
        with stk3:
            st.subheader(convert_float_into_str(get_avrg_growth_per_share_abs(join_ing_comdirect())) + " €")
    with col17:
        stk4 = st.beta_expander("Durschnitsanstieg pro Aktie %")
        with stk4:
            st.subheader(convert_float_into_str(get_avrg_growth_per_share_per(join_ing_comdirect())) + " %")
    df = st.beta_expander("Datentabelle Anzeigen")
    with df:
        st.write(join_ing_comdirect())


if consors and (not ing) and (not comdirect):
    col1, col2, col3 = st.beta_columns(3)
    with col1:
        st.header("Depotwert")
        st.subheader(get_depot_value_total(get_consors_df_to_merge()) + " €")
    with col2:
        st.header("Depotentwicklung €")
        st.subheader(get_growth_abs_total(get_consors_df_to_merge()) + " €")
    with col3:
        st.header("Depotentwicklung %")
        st.subheader(get_growth_per_portfolio(get_consors_df_to_merge()) + " %")
    st.write("---")
    ba = st.beta_expander("Beste Aktien")
    with ba:
        col4, col5 = st.beta_columns(2)
        with col4:
            st.subheader(get_best_pos_val(get_consors_df_to_merge()))
        with col5:
            st.subheader(get_best_pos_per(get_consors_df_to_merge()))
    wa = st.beta_expander("Schlechteste Aktien")
    with wa:
        col6, col7 = st.beta_columns(2)
        with col6:
            st.subheader(get_worst_pos_val(get_consors_df_to_merge()))
        with col7:
            st.subheader(get_worst_pos_per(get_consors_df_to_merge()))
    col8, col9, col10, col11 = st.beta_columns(4)
    with col8:
        top10val = st.beta_expander("Beste 10 Aktien €")
        with top10val:
            for i in get_10best_pos_abs(get_consors_df_to_merge()):
                st.write(i)
    with col9:
        top10per = st.beta_expander("Beste 10 Aktien %")
        with top10per:
            for i in get_10best_pos_per(get_consors_df_to_merge()):
                st.write(i)
    with col10:
        bad10val = st.beta_expander("Schlechteste 10 Aktien €")
        with bad10val:
            for i in get_10worst_pos_abs(get_consors_df_to_merge()):
                st.write(i)
    with col11:
        bad10per = st.beta_expander("Schlechteste 10 Aktien %")
        with bad10per:
            for i in get_10worst_pos_per(get_consors_df_to_merge()):
                st.write(i)
    col12, col13 = st.beta_columns(2)
    with col12:
        ver_per = st.beta_expander("Anteil der Aktien am Gesamtdepot gemessen am Wert")
        with ver_per:
            st.write(pie_position_dist_per(get_consors_df_to_merge()))
    with col13:
        ver_share = st.beta_expander("Anteil der Aktien am Gesamtdepot gemessen nach Stück")
        with ver_share:
            st.write(bar_position_dist_share(get_consors_df_to_merge()))
    col14, col15, col16, col17 = st.beta_columns(4)
    with col14:
        stk1 = st.beta_expander("Anteile Gesamt")
        with stk1:
            st.subheader(get_total_shares(get_consors_df_to_merge()))
    with col15:
        stk2 = st.beta_expander("Durschnitspreis pro Anteil")
        with stk2:
            st.subheader(convert_float_into_str(get_avrg_value_per_share(get_consors_df_to_merge())) + " €")
    with col16:
        stk3 = st.beta_expander("Durschnitsanstieg pro Aktie €")
        with stk3:
            st.subheader(convert_float_into_str(get_avrg_growth_per_share_abs(get_consors_df_to_merge())) + " €")
    with col17:
        stk4 = st.beta_expander("Durschnitsanstieg pro Aktie %")
        with stk4:
            st.subheader(convert_float_into_str(get_avrg_growth_per_share_per(get_consors_df_to_merge())) + " %")
    df = st.beta_expander("Datentabelle Anzeigen")
    with df:
        st.write(get_consors_df_to_merge())

if ing and (not consors) and (not comdirect):
    col1, col2, col3 = st.beta_columns(3)
    with col1:
        st.header("Depotwert")
        st.subheader(get_depot_value_total(get_ing_df_to_merge()) + " €")
    with col2:
        st.header("Depotentwicklung €")
        st.subheader(get_growth_abs_total(get_ing_df_to_merge()) + " €")
    with col3:
        st.header("Depotentwicklung %")
        st.subheader(get_growth_per_portfolio(get_ing_df_to_merge()) + " %")
    st.write("---")
    ba = st.beta_expander("Beste Aktien")
    with ba:
        col4, col5 = st.beta_columns(2)
        with col4:
            st.subheader(get_best_pos_val(get_ing_df_to_merge()))
        with col5:
            st.subheader(get_best_pos_per(get_ing_df_to_merge()))
    wa = st.beta_expander("Schlechteste Aktien")
    with wa:
        col6, col7 = st.beta_columns(2)
        with col6:
            st.subheader(get_worst_pos_val(get_ing_df_to_merge()))
        with col7:
            st.subheader(get_worst_pos_per(get_ing_df_to_merge()))
    col8, col9, col10, col11 = st.beta_columns(4)
    with col8:
        top10val = st.beta_expander("Beste 10 Aktien €")
        with top10val:
            for i in get_10best_pos_abs(get_ing_df_to_merge()):
                st.write(i)
    with col9:
        top10per = st.beta_expander("Beste 10 Aktien %")
        with top10per:
            for i in get_10best_pos_per(get_ing_df_to_merge()):
                st.write(i)
    with col10:
        bad10val = st.beta_expander("Schlechteste 10 Aktien €")
        with bad10val:
            for i in get_10worst_pos_abs(get_ing_df_to_merge()):
                st.write(i)
    with col11:
        bad10per = st.beta_expander("Schlechteste 10 Aktien %")
        with bad10per:
            for i in get_10worst_pos_per(get_ing_df_to_merge()):
                st.write(i)
    col12, col13 = st.beta_columns(2)
    with col12:
        ver_per = st.beta_expander("Anteil der Aktien am Gesamtdepot gemessen am Wert")
        with ver_per:
            st.write(pie_position_dist_per(get_ing_df_to_merge()))
    with col13:
        ver_share = st.beta_expander("Anteil der Aktien am Gesamtdepot gemessen nach Stück")
        with ver_share:
            st.write(bar_position_dist_share(get_ing_df_to_merge()))
    col14, col15, col16, col17 = st.beta_columns(4)
    with col14:
        stk1 = st.beta_expander("Anteile Gesamt")
        with stk1:
            st.subheader(get_total_shares(get_ing_df_to_merge()))
    with col15:
        stk2 = st.beta_expander("Durschnitspreis pro Anteil")
        with stk2:
            st.subheader(convert_float_into_str(get_avrg_value_per_share(get_ing_df_to_merge())) + " €")
    with col16:
        stk3 = st.beta_expander("Durschnitsanstieg pro Aktie €")
        with stk3:
            st.subheader(convert_float_into_str(get_avrg_growth_per_share_abs(get_ing_df_to_merge())) + " €")
    with col17:
        stk4 = st.beta_expander("Durschnitsanstieg pro Aktie %")
        with stk4:
            st.subheader(convert_float_into_str(get_avrg_growth_per_share_per(get_ing_df_to_merge())) + " %")
    df = st.beta_expander("Datentabelle Anzeigen")
    with df:
        st.write(get_ing_df_to_merge())


if comdirect and (not ing) and (not consors):
    col1, col2, col3 = st.beta_columns(3)
    with col1:
        st.header("Depotwert")
        st.subheader(get_depot_value_total(get_comdirect_df_to_merge()) + " €")
    with col2:
        st.header("Depotentwicklung €")
        st.subheader(get_growth_abs_total(get_comdirect_df_to_merge()) + " €")
    with col3:
        st.header("Depotentwicklung %")
        st.subheader(get_growth_per_portfolio(get_comdirect_df_to_merge()) + " %")
    st.write("---")
    ba = st.beta_expander("Beste Aktien")
    with ba:
        col4, col5 = st.beta_columns(2)
        with col4:
            st.subheader(get_best_pos_val(get_comdirect_df_to_merge()))
        with col5:
            st.subheader(get_best_pos_per(get_comdirect_df_to_merge()))
    wa = st.beta_expander("Schlechteste Aktien")
    with wa:
        col6, col7 = st.beta_columns(2)
        with col6:
            st.subheader(get_worst_pos_val(get_comdirect_df_to_merge()))
        with col7:
            st.subheader(get_worst_pos_per(get_comdirect_df_to_merge()))
    col8, col9, col10, col11 = st.beta_columns(4)
    with col8:
        top10val = st.beta_expander("Beste 10 Aktien €")
        with top10val:
            for i in get_10best_pos_abs(get_comdirect_df_to_merge()):
                st.write(i)
    with col9:
        top10per = st.beta_expander("Beste 10 Aktien %")
        with top10per:
            for i in get_10best_pos_per(get_comdirect_df_to_merge()):
                st.write(i)
    with col10:
        bad10val = st.beta_expander("Schlechteste 10 Aktien €")
        with bad10val:
            for i in get_10worst_pos_abs(get_comdirect_df_to_merge()):
                st.write(i)
    with col11:
        bad10per = st.beta_expander("Schlechteste 10 Aktien %")
        with bad10per:
            for i in get_10worst_pos_per(get_comdirect_df_to_merge()):
                st.write(i)
    col12, col13 = st.beta_columns(2)
    with col12:
        ver_per = st.beta_expander("Anteil der Aktien am Gesamtdepot gemessen am Wert")
        with ver_per:
            st.write(pie_position_dist_per(get_comdirect_df_to_merge()))
    with col13:
        ver_share = st.beta_expander("Anteil der Aktien am Gesamtdepot gemessen nach Stück")
        with ver_share:
            st.write(bar_position_dist_share(get_comdirect_df_to_merge()))
    col14, col15, col16, col17 = st.beta_columns(4)
    with col14:
        stk1 = st.beta_expander("Anteile Gesamt")
        with stk1:
            st.subheader(get_total_shares(get_comdirect_df_to_merge()))
    with col15:
        stk2 = st.beta_expander("Durschnitspreis pro Anteil")
        with stk2:
            st.subheader(convert_float_into_str(get_avrg_value_per_share(get_comdirect_df_to_merge())) + " €")
    with col16:
        stk3 = st.beta_expander("Durschnitsanstieg pro Aktie €")
        with stk3:
            st.subheader(convert_float_into_str(get_avrg_growth_per_share_abs(get_comdirect_df_to_merge())) + " €")
    with col17:
        stk4 = st.beta_expander("Durschnitsanstieg pro Aktie %")
        with stk4:
            st.subheader(convert_float_into_str(get_avrg_growth_per_share_per(get_comdirect_df_to_merge())) + " %")
    df = st.beta_expander("Datentabelle Anzeigen")
    with df:
        st.write(get_comdirect_df_to_merge())
