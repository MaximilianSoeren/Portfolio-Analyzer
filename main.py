"""
This application will create a localy hosted website that will let you interact with data taken from a csv-file
taken from your depot. And will allow you to interact and explore said data in different ways.
"""
# Importing all modules / files we need
import imports
import functions as fc

from classes import Data_Frame_Consors

darkmode = """
<style>
body {
  background-color: black;
  color: white;
}
</style>
"""
imports.st.markdown(darkmode, unsafe_allow_html=True)

# importing CSV and reading it
expander = imports.st.beta_expander(label="Upload")
with expander:
    col1, col2, col3 = imports.st.beta_columns(3)
    with col1:
        if imports.st.button("IGN", key=1):
            uploaded_file = imports.st.file_uploader("", type=".csv", key=1)
            try:
                fc.reading_csv_ing(uploaded_file)
            except:
                bank = 'Consors'
                print("Bitte lade eine CSV Datei von ING hoch.")
    with col2:
        if imports.st.button("CONSORS", key=2):
            uploaded_file = imports.st.file_uploader("", type=".csv", key=2)
            try:
                fc.reading_csv_consors(uploaded_file)
            except:
                bank = 'Consors'
                print("Bitte lade eine CSV Datei von Consors hoch.")
    with col3:
        if imports.st.button("COMDIRECT", key=3):
            uploaded_file = imports.st.file_uploader("", type=".csv", key=3)
            try:
                fc.reading_csv_comdirect(uploaded_file)
            except:
                bank = 'Consors'
                print("Bitte lade eine CSV Datei von Comdirect hoch.")

# Defining the structure of the website
header = imports.st.beta_container()
features1 = imports.st.beta_container()
features2 = imports.st.beta_container()
features3 = imports.st.beta_container()
features4 = imports.st.beta_container()
features5 = imports.st.beta_container()

# all of the below code is to build the landing page / page that comes up when Navigation -> Depot
with header:
    imports.st.title("Willkommen zu deinem Dashboard")
    imports.st.text("Hier kannst du alles wichtige zu deinem Portfolio sehen")
    imports.st.text(
        "Sobald du eine CSV Datei deines Portfolios bei der Consorsbank hochgeladen hast, kannst du hier"
        "alle wichtigen Informationen nachschauen.")
    imports.st.write("---")
# ----------------------------------------------------------------------------------------------------------------------
#     # this is the display functions for "Protfolioname / Gesamtdepotwert / Entwicklung...
with features1:
    col1, col2, col3 = imports.st.beta_columns(3)
    col1.header("Portfolioname")
    col1.subheader((fc.no_header_no_index(df.get_depot_name())))
    col2.header("Gesamtdepotwert")
    col2.subheader(fc.no_header_no_index(df.get_depot_value()) + " €")
    col3.header("Entwicklung Absolut / %")
    col3.subheader((fc.no_header_no_index(df.get_depot_dev_abs()) + " € | " +
                    fc.no_header_no_index(df.get_depot_dev_per()) + " %"))
    imports.st.write("---")
#     # ----------------------------------------------------------------------------------------------------------------------
#     # display functions for best / worst stock
with features2:
    col4, col5 = imports.st.beta_columns(2)
    best_share = col4.beta_expander("Beste Aktie")
    with best_share:
        imports.st.subheader(
            (fc.no_header_no_index(classes.get_best_position_absolute())))
        imports.st.subheader(
            (fc.no_header_no_index(df.get_best_position_percentage())))
    worst_share = col5.beta_expander("Schlechteste Aktie")
    with worst_share:
        imports.st.subheader(
            (fc.no_header_no_index(get_worst_position_absolute())))
        imports.st.subheader(
            (fc.no_header_no_index(get_worst_position_percentage())))
    col4.write("---")
    col5.write('---')
with features3:
    portfolio_per = col4.beta_expander("% der Position vom Portfolio")
    with portfolio_per:
        imports.st.plotly_chart(fig_pie_poisitions_per())
    portfolio_shares = col5.beta_expander("Stückanzahl pro Position")
    with portfolio_shares:
        imports.st.plotly_chart(fig_bar_positions_nr())
    col5.write('---')
    col4.write("---")
with features4:
    all_data = imports.st.beta_expander("Alles im Überblick")
    with all_data:
        imports.st.write(get_sorted_dataframe())
