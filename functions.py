import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import ipywidgets as widgets
from IPython.display import clear_output

def testme():
    return "khanh"
#df = pd.read_csv('new_taxonomy.csv')
new_taxonomy = pd.read_csv ('new_taxonomy.csv', header=[0])
# Section update count
sections = pd.DataFrame(new_taxonomy).groupby(by='subcategory', as_index=True, group_keys=True).count()

def instagram_complete_df():
    # complete taxonomy - will take some time to read in
    df_raw = pd.read_json("taxonomy_instagram_complete.json")
    raw_dict = {}
    for row in df_raw.sections_list:
        section_name = row['section_name']
        for content in row['section_content']:
            code = content['code']
            name = content['name']
            raw_dict[code] = content
    df = pd.DataFrame.from_dict(raw_dict)
    # Transpose axis - columns become rows and rows become columns
    df = df.T
    return df


def render_section_addition_counts():
    sections  = pd.DataFrame(new_taxonomy).groupby('subcategory').count()
    sections = sections.sort_values(by=["code_status"], ascending=False)
    
    sections_df = sections[['code_status']]
    sections_df = sections_df.rename(columns={"code_status": "count"})
    plt.figure(figsize=(18,6))
    plt.bar(sections_df.index, sections_df['count'])
    plt.xticks(rotation=90, fontsize=16)
    plt.ylabel('Count', fontsize=15)
    plt.title( " (" + str(len(sections)) + " total)", fontsize=30)
    display(  sections_df, plt.show() )
    
def return_colors_list(df):
    list = []
    for index, row in df.iterrows():
        list.append(row['color'])
    return list
    

ITEMS_MAX = 20
def render_graph(subcategory, df, new_taxonomy):
    plt.ioff()
    subcategory_df = new_taxonomy[(new_taxonomy['subcategory']==subcategory)]
    subcategory_df_count = len(subcategory_df)
    subcategory_df = subcategory_df.sort_values(by=["i_mean"], ascending=False)
    subcategory_df = subcategory_df.iloc[:ITEMS_MAX]
    subcategory_df['color'] = 'steelblue'
    subcategory_df_names = subcategory_df['name'].tolist()
    
    
    subcategory_existing_df = df[(df['subcategory']==subcategory)]
    subcategory_existing_df_count = subcategory_existing_df.shape[0]
    subcategory_existing_dfx = subcategory_existing_df[~subcategory_existing_df['name'].isin(subcategory_df_names)]
    subcategory_existing_df = subcategory_existing_dfx.sort_values(by=["i_mean"], ascending=False)
    subcategory_existing_df = subcategory_existing_df.iloc[:ITEMS_MAX]
    subcategory_existing_df['color'] = 'darkorange'
    
    addition_count = subcategory_existing_df_count - subcategory_df_count
    
    complete_df = pd.concat([subcategory_df, subcategory_existing_df])
    complete_df = complete_df.sort_values(by=["i_mean"], ascending=False)
    colors_list = return_colors_list(complete_df)
    
    plt.figure(figsize=(18,6))
    plt.bar(complete_df['name'], complete_df['i_mean'], color=colors_list)
    plt.xticks(rotation=90, fontsize=16, )
    plt.ylabel('i_mean', fontsize=15)
    plt.title("Added " +  str(addition_count) + " to " + subcategory  + " (" + str(subcategory_existing_df_count) + " total)", fontsize=30)
    plt.legend(handles=[Patch(facecolor='orange', edgecolor='darkorange',
                         label='Existing'),Patch(facecolor='steelblue', edgecolor='steelblue',
                         label='Newly Added')])
    plt.show()
    return plt






pd.options.display.max_rows = 200
pd.set_option('display.max_rows', 200)
def show_section_select():
    section_select = widgets.Dropdown(
        options=sections.index,
        description='Subcategories:',
        #value=selection,
        disabled=False,
        )
    
    section_select.observe(handle_section_selection, names='value')
    return section_select

def handle_section_selection(change):
    clear_output()
    section_selected = change['new']
    
    #h.update(section_selected)
    subcategory_df = new_taxonomy[(new_taxonomy['subcategory']==section_selected)].sort_values(by="i_mean", ascending=False)
    display( show_section_select(), subcategory_df, render_section_graph(section_selected) )
    
section_column_max = 40
def render_section_graph(subcategory):
    subcategory_df = new_taxonomy[(new_taxonomy['subcategory']==subcategory)]
    subcategory_df = subcategory_df.sort_values(by=["i_mean"], ascending=False)
    plt.figure(figsize=(18,6))
    plt.bar(subcategory_df['name'].iloc[:section_column_max], subcategory_df['i_mean'].iloc[:section_column_max])
    plt.xticks(rotation=90, fontsize=16)
    plt.ylabel('i_mean', fontsize=15)
    plt.title(subcategory + str(len(subcategory_df)), fontsize=30)
    plt.show()