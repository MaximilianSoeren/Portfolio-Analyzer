
# # setting up pandas to import and make our/ csv usable
# import imports
# # ----------------------------------------------------------------------------------------
# #  defining functions that will collect just the usefull data depending on what we want.
# # ----------------------------------------------------------------------------------------

# # This will delete the header and index of said dataframe AND convert it to a string.
# def no_header_no_index(df):
#     df_new = df.to_string(index=None, header=None)
#     return df_new

# # this will replace the header of the given Dataframe with the first row of said dataframe
# def replace_header_w_first_row(df):
#     new_df = df.rename(columns=df.iloc[0]).drop(df.index[0])
#     return new_df

# # this will turn any single value into a float type.
# def turn_str_into_float_sd(func, col):
#     df1 = func
#     df2 = df1[col].apply(lambda x: x.replace('.', ''))
#     df2 = df2.apply(lambda x: x.replace(',', '.'))
#     df1[col] = df2
#     df1[col] = df1[col].astype(float)
#     return df1[col]

# #this will turn a column of the dataframe into float type.
# def turn_str_into_float(col):
#     df1 = replace_header_w_first_row(imports.DataFrame.df.get_for_sorting())
#     df2 = df1[col].apply(lambda x: x.replace('.', ''))
#     df2 = df2.apply(lambda x: x.replace(',', '.'))
#     df1[col] = df2
#     df1[col] = df1[col].astype(float)
#     return df1[col]

# # # this function returns the best position of the portfolio measured on asbolute value
# def get_best_position_absolute():
#     df1 = replace_header_w_first_row(imports.main.df.get_for_sorting())
#     df2 = df1['Entwicklung absolut'].apply(lambda x: x.replace('.', ''))
#     df2 = df2.apply(lambda x: x.replace(',', '.'))
#     df1['Entwicklung absolut'] = df2
#     df1['Entwicklung absolut'] = df1['Entwicklung absolut'].astype(float)
#     df_sorted = df1.sort_values(['Entwicklung absolut'], ascending=False)
#     df_first = df_sorted.head(1)
#     df_name = df_first['Name']
#     df_att_percent = df_first['Entwicklung prozentual'].astype(str) + " %"
#     df_att_abs = df_first['Entwicklung absolut'].astype(str) + " €"
#     df_fixed = df_name + " | " + df_att_abs + " | " + df_att_percent
#     return df_fixed


# # this is horrible, please future me, find a better solution.
# def get_best_position_percentage():
#     df1 = replace_header_w_first_row(imports.main.df.get_for_sorting())
#     df2 = df1['Entwicklung prozentual'].apply(lambda x: x.replace('.', ''))
#     df2 = df2.apply(lambda x: x.replace(',', '.'))
#     df1['Entwicklung prozentual'] = df2
#     df1['Entwicklung prozentual'] = df1['Entwicklung prozentual'].astype(float)
#     df_sorted = df1.sort_values(['Entwicklung prozentual'], ascending=False)
#     df_first = df_sorted.head(1)
#     df_name = df_first['Name']
#     df_att_percent = df_first['Entwicklung prozentual'].astype(str) + " %"
#     df_att_abs = df_first['Entwicklung absolut'].astype(str) + " €"
#     df_fixed = df_name + " | " + df_att_abs + " | " + df_att_percent
#     return df_fixed
# #
# # this function will get the worst position in the portfolio depended on the absolute value (most € lost)
# def get_worst_position_absolute():
#     df1 = replace_header_w_first_row(imports.main.df.get_for_sorting())
#     df2 = df1['Entwicklung absolut'].apply(lambda x: x.replace('.', ''))
#     df2 = df2.apply(lambda x: x.replace(',', '.'))
#     df1['Entwicklung absolut'] = df2
#     df1['Entwicklung absolut'] = df1['Entwicklung absolut'].astype(float)
#     df_sorted = df1.sort_values(['Entwicklung absolut'])
#     df_first = df_sorted.head(1)
#     df_name = df_first['Name']
#     df_att_percent = df_first['Entwicklung prozentual'].astype(str) + " %"
#     df_att_abs = df_first['Entwicklung absolut'].astype(str) + " €"
#     df_fixed = df_name + " | " + df_att_abs + " | " + df_att_percent
#     return df_fixed

# # this function will get the worst position in the portfolio depended on the percentage value (most % lost)
# def get_worst_position_percentage():
#     df1 = replace_header_w_first_row(imports.main.df.get_for_sorting())
#     df2 = df1['Entwicklung prozentual'].apply(lambda x: x.replace('.', ''))
#     df2 = df2.apply(lambda x: x.replace(',', '.'))
#     df1['Entwicklung prozentual'] = df2
#     df1['Entwicklung prozentual'] = df1['Entwicklung prozentual'].astype(float)
#     df_sorted = df1.sort_values(['Entwicklung prozentual'])
#     df_first = df_sorted.head(1)
#     df_name = df_first['Name']
#     df_att_percent = df_first['Entwicklung prozentual'].astype(str) + " %"
#     df_att_abs = df_first['Entwicklung absolut'].astype(str) + " €"
#     df_fixed = df_name + " | " + df_att_abs + " | " + df_att_percent
#     return df_fixed

# # creating a function for plotly pie chat that shows the % of the Portfolio of the positions
# def fig_pie_poisitions_per():
#     lables = imports.main.df.get_pos_name()
#     df1 = replace_header_w_first_row(imports.main.df.get_for_sorting())
#     df2 = df1['Gesamtwert EUR'].apply(lambda x: x.replace('.', ''))
#     df2 = df2.apply(lambda x: x.replace(',', '.'))
#     df1['Gesamtwert EUR'] = df2
#     df1['Gesamtwert EUR'] = df1['Gesamtwert EUR'].astype(float)
#     values_of_pos = df1['Gesamtwert EUR']
#     values = (values_of_pos / sum(values_of_pos)) * 100
#     fig = imports.go.Figure(data=[imports.go.Pie(labels=lables, values=values)])
#     return fig

# # creates a function that shows the number of shares of each position in a bar graph
# def fig_bar_positions_nr():
#     df1 = replace_header_w_first_row(imports.main.df.get_for_sorting())
#     fig = imports.px.bar(data_frame=df1, x=df1['Name'], y=df1['Stück/Nominal'])
#     return fig

# # is a function that shows the important bits of data from the whole DF. But in a way so you can sort it withint the dataframe.
# def get_sorted_dataframe():
#     df1 = replace_header_w_first_row(imports.main.df.get_for_sorting())
#     df2 = df1.apply(lambda x: x.str.replace('.', ''))
#     df2 = df2[['Gesamtwert EUR','Stück/Nominal', 'Einstandskurs inkl. NK', 'Einstandswert', 'Veränderung Intraday', 'Entwicklung absolut', 'Entwicklung prozentual']].apply(lambda x: x.str.replace(',','.'))
#     df3 = df2.astype('float', errors='ignore')
#     df1 = imports.pd.concat([imports.main.df.get_pos_name(), imports.main.df.get_post_wkn(), df3], axis=1)
#     df1 = df1.rename(columns={'Depot': 'Name', 'Inhaber': 'WKN'})
#     return df1
