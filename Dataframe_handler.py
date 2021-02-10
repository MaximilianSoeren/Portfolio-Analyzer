from main import df


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


#  This is to render the upload CSV data and make it a variable called DF used through the programm

