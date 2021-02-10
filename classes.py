import imports


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
        fig = imports.go.Figure(
            data=[imports.go.Pie(labels=lables, values=values)])
        return fig

    # creates a function that shows the number of shares of each position in a bar graph
    def fig_bar_positions_nr(self):
        df1 = self.new_df.replace_header_w_first_row(
            self.new_df.get_for_sorting())
        fig = imports.px.bar(data_frame=df1,
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
        df1 = imports.pd.concat(
            [self.get_pos_name(),
             self.get_post_wkn(), df3], axis=1)
        df1 = df1.rename(columns={'Depot': 'Name', 'Inhaber': 'WKN'})
        return df1


class Data_Frame_ING:
    pass
