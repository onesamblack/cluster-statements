import pathlib
import streamlit as st
import altair as alt
import pickle
import pandas
import numpy



def pickler(obj=None, filename: str= None, mode: str = 'pickle'):
  """
  pickles the file to filename, or 
  unpickles and returns the file

  (to save the result of long running calculations)

  Parameters
  ----------
  obj : 
    the object to pickle
  filename : str
    file to pickle to
  mode:
    one of 'pickle' or 'depickle'
  """
  unpickled = None
  
  if mode == 'pickle':
    pickle.dump(obj, open(filename,'wb'))

  elif mode == 'unpickle':
    unpickled = pickle.load(open(filename,'rb'))
  
  return unpickled


if __name__ == "__main__":
    all_viz_data = pickler(filename=pathlib.Path("assets/all_viz_data.pkl"), mode='unpickle')

    st.header("Clustered statements from the 2020 Presidential Debate")
    st.write("The chart below contains 2 dimensional representations of Biden's statements from the first Presidential debate of 2020")
    st.write("**Disclaimer**:the content of this analysis is not intended to portray any political affiliation. It was just interesting data")


    number_of_words = st.slider("number of words to include", min_value=5, max_value=100, value=10)
    number_of_clusters = st.slider("number of clusters to display", min_value=4, max_value=28, step=2, value=10)
    source_df = all_viz_data[number_of_clusters]
    
    source = source_df[source_df['word_count'] > number_of_words]
  

    chart = alt.Chart(source).mark_circle(size=60).encode(
        x='tsne_dim_1',
        y='tsne_dim_2',
        color=alt.Color('cluster_id', scale=alt.Scale(scheme='category20')) ,
        tooltip=['cluster_id','sentence']
    ).configure_axis(
        grid=False
    ).configure_view(
        strokeWidth=0
    ).properties(
        width=600,
        height=400,
    ).interactive()


    st.altair_chart(chart)
