import mysql.connector
import pandas as pd
import plotly.express as px

mydb = mysql.connector.connect(host="localhost",
                               port="3366",
                               user="root",
                               password="my-secret-pw",
                               database="SnPip")

mycursor = mydb.cursor()


# NOTE: Converts 1M to 1000000 e.t.c
def getVal(val):
    for i in val:
        if i == "k":
            pos = float(val.strip(i)) * 1000
            return pos
        elif i == "M":
            pos = float(val.strip(i)) * 1000000
            return pos


# NOTE: Start position and increment size of the graph
input = getVal('44.85M')
inc = 500000

# NOTE: Numbers for data to be selected based on position
start = (input - inc)
finish = (input + inc)

df = pd.read_sql(('SELECT POS, GENE, ID FROM snp WHERE POS BETWEEN %(dstart)s AND %(dfinish)s'), mydb,
                 params={"dstart": start, "dfinish": finish})

# NOTE: Gets the first and last positions of each gene in the imported df
first = dict(df.groupby('GENE')['POS'].first())
last = dict(df.groupby('GENE')['POS'].last())
num = df.value_counts('GENE').reset_index(name='NUM')  # NOTE: counts snp num

# NOTE: Creates a new df of each gene and their start and end positions
df2 = pd.DataFrame({'first': pd.Series(first), 'last': pd.Series(last)})
df2.reset_index(level=0, inplace=True)
df2.columns = ['GENE', 'START', 'END']
df2['length'] = df2['END'] - df2['START']

# NOTE: Creates a new df with the SNP numbers in it
df3 = pd.merge(df2, num, how='inner', on='GENE')
df3.columns = ['GENE', 'START', 'END', 'Length', 'SNP NUM']

# NOTE: Sorts the df by Start position
df4 = df3.sort_values(by=['START'])
print(df4)

# NOTE: Plots the graph
fig = px.bar(df4,
             x='Length',
             y='GENE',
             base='START',
             orientation='h',
             color='SNP NUM',
             custom_data=['START', 'END', 'Length', 'SNP NUM'],
             labels={'GENE': 'Genes',
                     'START': 'Start position',
                     'END': 'End position',
                     'SNP NUM': 'Number of SNPs'})

# NOTE: Configures the floating label
fig.update_traces(
    hovertemplate="<br>".join([
        "<b>%{y}</b><br>",
        "First SNP Position: %{customdata[0]:s}",
        "Last SNP Position: %{customdata[1]:s}",
        "Length betweem SNPs (bp): %{customdata[2]:s}",
        "Number of SNPs: %{customdata[3]:s}"
    ])
)


# NOTE: Sets the title & fonts of the graph
fig.update_layout(title={'text': "Gene Map",
                         'x':0.5,
                         'xanchor': 'center',
                         'yanchor': 'top'},
                  xaxis_title="Chromosome position (bp)",
                  yaxis_title="Genes",
                  font_family="Times New Roman",
                  font_color="Black",
                  title_font_family="Times New Roman",
                  title_font_color="Black")

# NOTE: Creates a range slider
fig.update_layout(
    xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=200000,
                     label="200000bp",
                     step="all",
                     stepmode="backward"),
                dict(count=400000,
                     label="400000bp",
                     step="all",
                     stepmode="backward"),
                dict(count=600000,
                     label="600000bp",
                     step="all",
                     stepmode="backward"),
                dict(count=800000,
                     label="800000bp",
                     step="all",
                     stepmode="backward"),
                dict(step="all")
            ])
        ),
        rangeslider=dict(
            visible=True
        ),
        type="linear"
    )
)

fig.show()
