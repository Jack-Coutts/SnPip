import mysql.connector
import pandas as pd
import plotly.express as px

mydb = mysql.connector.connect(host="localhost",
                               port="3366",
                               user="root",
                               password="my-secret-pw",
                               database="SnPip")

mycursor = mydb.cursor()

# NOTE: Start position and increment size of the graph
pos = 20000000
inc = 500000

# NOTE: Numbers for data to be selected based on position
start = (pos - inc)
finish = (pos + inc)

df = pd.read_sql(('SELECT POS, GENE, ID FROM snp WHERE POS BETWEEN %(dstart)s AND %(dfinish)s'), mydb,
                 params={"dstart": start, "dfinish": finish})

genes = list(df['GENE'].unique())
glist = [i for i in genes if i is not None]

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
             labels={'GENE': 'Gene',
                     'START': 'Start position',
                     'END': 'End position',
                     'SNP NUM': 'Number of SNPs'})

# NOTE: Configures the floating label
fig.update_traces(
    hovertemplate="<br>".join([
        "<b>%{y}</b><br>",
        "Start Position: %{customdata[0]:s}",
        "End Position: %{customdata[1]:s}",
        "Length (bp): %{customdata[2]}",
        "Number of SNPs: %{customdata[3]}"
    ])
)


# NOTE: Sets the title of the graph
fig.update_layout(
    title_text="Gene List")

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
