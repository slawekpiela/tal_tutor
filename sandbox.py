from airtable import Airtable
from configuration import base_id, table_dictionary, airtable_token
import pandas as pd
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode


new_words_list = {
  "records": [
    {
      "fields": {
        "keyword": "chris",
        "transcription": "krɪs",
        "translation": "Krzysiek",
        "study_status": "---",
        "translation_extended": "",
        "user": "slawek",
        "no_of_tries": 0,
        "group": "general"
      }
    },
    {
      "fields": {
        "keyword": "set off",
        "transcription": "sɛt ɔf",
        "translation": "wyruszyć",
        "study_status": "---",
        "translation_extended": "",
        "user": "slawek",
        "no_of_tries": 0,
        "group": "general"
      }
    },
    {
      "fields": {
        "keyword": "early",
        "transcription": "ˈɜrli",
        "translation": "wcześnie",
        "study_status": "---",
        "translation_extended": "",
        "user": "slawek",
        "no_of_tries": 0,
        "group": "general"
      }
    },
    {
      "fields": {
        "keyword": "in",
        "transcription": "ɪn",
        "translation": "w",
        "study_status": "---",
        "translation_extended": "",
        "user": "slawek",
        "no_of_tries": 0,
        "group": "general"
      }
    },
    {
      "fields": {
        "keyword": "morning",
        "transcription": "ˈmɔrnɪŋ",
        "translation": "ranek",
        "study_status": "---",
        "translation_extended": "",
        "user": "slawek",
        "no_of_tries": 0,
        "group": "general"
      }
    },
    {
      "fields": {
        "keyword": "towards",
        "transcription": "təˈwɔrdz",
        "translation": "w kierunku",
        "study_status": "---",
        "translation_extended": "",
        "user": "slawek",
        "no_of_tries": 0,
        "group": "general"
      }
    },
    {
      "fields": {
        "keyword": "the",
        "transcription": "ðə",
        "translation": "(przyimek określony)",
        "study_status": "---",
        "translation_extended": "",
        "user": "slawek",
        "no_of_tries": 0,
        "group": "general"
      }
    },
    {
      "fields": {
        "keyword": "moon",
        "transcription": "mun",
        "translation": "księżyc",
        "study_status": "---",
        "translation_extended": "",
        "user": "slawek",
        "no_of_tries": 0,
        "group": "general"
      }
    },
    {
      "fields": {
        "keyword": "he",
        "transcription": "hi",
        "translation": "on",
        "study_status": "---",
        "translation_extended": "",
        "user": "slawek",
        "no_of_tries": 0,
        "group": "general"
      }
    },
    {
      "fields": {
        "keyword": "knew",
        "transcription": "nju",
        "translation": "wiedział",
        "study_status": "---",
        "translation_extended": "",
        "user": "slawek",
        "no_of_tries": 0,
        "group": "general"
      }
    },
    {
      "fields": {
        "keyword": "that",
        "transcription": "ðæt",
        "translation": "że",
        "study_status": "---",
        "translation_extended": "",
        "user": "slawek",
        "no_of_tries": 0,
        "group": "general"
      }
    },
    {
      "fields": {
        "keyword": "going",
        "transcription": "ˈɡoʊɪŋ",
        "translation": "idąc",
        "study_status": "---",
        "translation_extended": "",
        "user": "slawek",
        "no_of_tries": 0,
        "group": "general"
      }
    },
    {
      "fields": {
        "keyword": "there",
        "transcription": "ˈðɛr",
        "translation": "tam",
        "study_status": "---",
        "translation_extended": "",
        "user": "slawek",
        "no_of_tries": 0,
        "group": "general"
      }
    },
    {
      "fields": {
        "keyword": "will",
        "transcription": "wɪl",
        "translation": "będzie",
        "study_status": "---",
        "translation_extended": "",
        "user": "slawek",
        "no_of_tries": 0,
        "group": "general"
      }
    },
    {
      "fields": {
        "keyword": "be",
        "transcription": "bi",
        "translation": "być",
        "study_status": "---",
        "translation_extended": "",
        "user": "slawek",
        "no_of_tries": 0,
        "group": "general"
      }
    },
    {
      "fields": {
        "keyword": "exciting",
        "transcription": "ɪkˈsaɪtɪŋ",
        "translation": "ekscytujące",
        "study_status": "---",
        "translation_extended": "",
        "user": "slawek",
        "no_of_tries": 0,
        "group": "general"
      }
    }
  ]
}
records_list = new_words_list['records']
original_dataframe = pd.DataFrame([record['fields'] for record in records_list])


# Function to display the editable grid and process updates
def display_editable_grid(dataframe):
  # Create a copy of the dataframe for the editable grid
  editable_dataframe = dataframe[['keyword', 'transcription', 'translation']].copy()

  # Configure the editable grid
  gb = GridOptionsBuilder.from_dataframe(editable_dataframe)
  gb.configure_grid_options(domLayout='normal')
  gb.configure_columns(['keyword', 'transcription', 'translation'], editable=True)
  grid_options = gb.build()

  # Display the editable AgGrid and return the grid response
  grid_response = AgGrid(
    editable_dataframe,
    gridOptions=grid_options,
    update_mode=GridUpdateMode.MODEL_CHANGED,
    fit_columns_on_grid_load=True
  )

  return grid_response


# Display the editable grid and capture the response
grid_response = display_editable_grid(original_dataframe)

# Add a 'Save' button to apply changes from the editable grid
if st.button('Save Changes'):
  # Extract the updated data from the grid response
  updated_data = pd.DataFrame(grid_response['data'])

  # Replace the original dataframe sections with the updated data
  for col in ['keyword', 'transcription', 'translation']:
    original_dataframe[col] = updated_data[col]

  st.success('Changes saved successfully!')
  # Display the updated DataFrame to confirm changes
  st.write('Updated Data:', original_dataframe)