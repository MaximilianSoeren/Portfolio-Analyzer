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



# deffining the class needed
class DataFrame:
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

    def get_post_wkn(self):
        return self.new_df.iloc[6:, 1:2].dropna().head(-1)

    def get_pos_type(self):
        return self.new_df.iloc[6:, 2:3].dropna().head(-1)

    def get_pos_shares(self):
        return self.new_df.iloc[6:, 3:4].dropna().head(-1)

    def get_pos_value(self):
        return self.new_df.iloc[6:, 13:14].dropna().head(-1)

    def get_post_dev_abs(self):
        return self.new_df.iloc[6:, 14:15].dropna().head(-1)

    def get_post_dev_per(self):
        return self.new_df.iloc[6:, 16:17].dropna().head(-1)

    def get_for_sorting(self):
        return self.new_df.iloc[5:].dropna()

# importing CSV and reading it
expander = st.beta_expander
with expander:
    uploaded_file = st.file_uploader("", type=".csv", key=123)
df = DataFrame(pd.read_csv(uploaded_file, sep=';', thousands='.', decimal=',', encoding='utf-8'))
# Defining all functions used in this code


# This will delete the header and index of said dataframe AND convert it to a string.
def no_header_no_index(df):
    df_new = df.to_string(index=None, header=None)
    return df_new

# this will replace the header of the given Dataframe with the first row of said dataframe
def replace_header_w_first_row(df):
    new_df = df.rename(columns=df.iloc[0]).drop(df.index[0])
    return new_df

# this will turn any single value into a float type.
def turn_str_into_float_sd(func, col):
    df1 = func
    df2 = df1[col].apply(lambda x: x.replace('.', ''))
    df2 = df2.apply(lambda x: x.replace(',', '.'))
    df1[col] = df2
    df1[col] = df1[col].astype(float)
    return df1[col]

#this will turn a column of the dataframe into float type.
def turn_str_into_float(col):
    df1 = replace_header_w_first_row(df.get_for_sorting())
    df2 = df1[col].apply(lambda x: x.replace('.', ''))
    df2 = df2.apply(lambda x: x.replace(',', '.'))
    df1[col] = df2
    df1[col] = df1[col].astype(float)
    return df1[col]

# # this function returns the best position of the portfolio measured on asbolute value
def get_best_position_absolute():
    df1 = replace_header_w_first_row(df.get_for_sorting())
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
def get_best_position_percentage():
    df1 = replace_header_w_first_row(df.get_for_sorting())
    df2 = df1['Entwicklung prozentual'].apply(lambda x: x.replace('.', ''))
    df2 = df2.apply(lambda x: x.replace(',', '.'))
    df1['Entwicklung prozentual'] = df2
    df1['Entwicklung prozentual'] = df1['Entwicklung prozentual'].astype(float)
    df_sorted = df1.sort_values(['Entwicklung prozentual'], ascending=False)
    df_first = df_sorted.head(1)
    df_name = df_first['Name']
    df_att_percent = df_first['Entwicklung prozentual'].astype(str) + " %"
    df_att_abs = df_first['Entwicklung absolut'].astype(str) + " €"
    df_fixed = df_name + " | " + df_att_abs + " | " + df_att_percent
    return df_fixed
#
# this function will get the worst position in the portfolio depended on the absolute value (most € lost)
def get_worst_position_absolute():
    df1 = replace_header_w_first_row(df.get_for_sorting())
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
def get_worst_position_percentage():
    df1 = replace_header_w_first_row(df.get_for_sorting())
    df2 = df1['Entwicklung prozentual'].apply(lambda x: x.replace('.', ''))
    df2 = df2.apply(lambda x: x.replace(',', '.'))
    df1['Entwicklung prozentual'] = df2
    df1['Entwicklung prozentual'] = df1['Entwicklung prozentual'].astype(float)
    df_sorted = df1.sort_values(['Entwicklung prozentual'])
    df_first = df_sorted.head(1)
    df_name = df_first['Name']
    df_att_percent = df_first['Entwicklung prozentual'].astype(str) + " %"
    df_att_abs = df_first['Entwicklung absolut'].astype(str) + " €"
    df_fixed = df_name + " | " + df_att_abs + " | " + df_att_percent
    return df_fixed

# creating a function for plotly pie chat that shows the % of the Portfolio of the positions
def fig_pie_poisitions_per():
    lables = df.get_pos_name()
    df1 = replace_header_w_first_row(df.get_for_sorting())
    df2 = df1['Gesamtwert EUR'].apply(lambda x: x.replace('.', ''))
    df2 = df2.apply(lambda x: x.replace(',', '.'))
    df1['Gesamtwert EUR'] = df2
    df1['Gesamtwert EUR'] = df1['Gesamtwert EUR'].astype(float)
    values_of_pos = df1['Gesamtwert EUR']
    values = (values_of_pos / sum(values_of_pos)) * 100
    fig = go.Figure(data=[go.Pie(labels=lables, values=values)])
    return fig

# creates a function that shows the number of shares of each position in a bar graph
def fig_bar_positions_nr():
    df1 = replace_header_w_first_row(df.get_for_sorting())
    fig = px.bar(data_frame=df1, x=df1['Name'], y=df1['Stück/Nominal'])
    return fig

# is a function that shows the important bits of data from the whole DF. But in a way so you can sort it withint the dataframe.
def get_sorted_dataframe():
    df1 = replace_header_w_first_row(df.get_for_sorting())
    df2 = df1.apply(lambda x: x.str.replace('.', ''))
    df2 = df2[['Gesamtwert EUR','Stück/Nominal', 'Einstandskurs inkl. NK', 'Einstandswert', 'Veränderung Intraday', 'Entwicklung absolut', 'Entwicklung prozentual']].apply(lambda x: x.str.replace(',','.'))
    df3 = df2.astype('float', errors='ignore')
    df1 = pd.concat([df.get_pos_name(), df.get_post_wkn(), df3], axis=1)
    df1 = df1.rename(columns={'Depot': 'Name', 'Inhaber': 'WKN'})
    return df1


# Defining the structure of the website
header = st.beta_container()
features1 = st.beta_container()
features2 = st.beta_container()
features3 = st.beta_container()
features4 = st.beta_container()
features5 = st.beta_container()




# all of the below code is to build the landing page / page that comes up when Navigation -> Depot
with header:
    st.title("Willkommen zu deinem Dashboard")
    st.text("Hier kannst du alles wichtige zu deinem Portfolio sehen")
    st.text("Sobald du eine CSV Datei deines Portfolios bei der Consorsbank hochgeladen hast, kannst du hier"
            "alle wichtigen Informationen nachschauen.")
    st.write("---")
# ----------------------------------------------------------------------------------------------------------------------
#     # this is the display functions for "Protfolioname / Gesamtdepotwert / Entwicklung...
with features1:
    col1, col2, col3 = st.beta_columns(3)
    col1.header("Portfolioname")
    col1.subheader((no_header_no_index(df.get_depot_name())))
    col2.header("Gesamtdepotwert")
    col2.subheader(no_header_no_index(df.get_depot_value()) + " €")
    col3.header("Entwicklung Absolut / %")
    col3.subheader((no_header_no_index(df.get_depot_dev_abs()) + " € | " +
                    no_header_no_index(df.get_depot_dev_per()) + " %"))
    st.write("---")
#     # ----------------------------------------------------------------------------------------------------------------------
#     # display functions for best / worst stock
with features2:
    col4, col5 = st.beta_columns(2)
    best_share = col4.beta_expander("Beste Aktie")
    with best_share:
        st.subheader((no_header_no_index(get_best_position_absolute())))
        st.subheader((no_header_no_index(get_best_position_percentage())))
    worst_share = col5.beta_expander("Schlechteste Aktie")
    with worst_share:
        st.subheader((no_header_no_index(get_worst_position_absolute())))
        st.subheader((no_header_no_index(get_worst_position_percentage())))
    col4.write("---")
    col5.write('---')
with features3:
    portfolio_per = col4.beta_expander( "% der Position vom Portfolio")
    with portfolio_per:
        st.plotly_chart(fig_pie_poisitions_per())
    portfolio_shares = col5.beta_expander("Stückanzahl pro Position")
    with portfolio_shares:
        st.plotly_chart(fig_bar_positions_nr())
    col5.write('---')
    col4.write("---")
with features4:
    all_data = st.beta_expander("Alles im Überblick")
    with all_data:
        st.write(get_sorted_dataframe())
