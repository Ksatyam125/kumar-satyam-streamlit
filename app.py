{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 3,
   "id": "9ba047e4",
   "metadata": {},
   "outputs": [],
   "source": [
    "# import all the app dependencies\n",
    "import pandas as pd\n",
    "import numpy as np\n",
    "import sklearn\n",
    "import streamlit as st\n",
    "import joblib\n",
    "import matplotlib\n",
    "from IPython import get_ipython\n",
    "from PIL import Image\n",
    "\n",
    "# load the encoder and model object\n",
    "model = joblib.load(\"rta_model_deploy3.joblib\")\n",
    "encoder = joblib.load(\"ordinal_encoder2.joblib\")\n",
    "\n",
    "st.set_option('deprecation.showPyplotGlobalUse', False)\n",
    "\n",
    "# 1: serious injury, 2: Slight injury, 0: Fatal Injury\n",
    "\n",
    "st.set_page_config(page_title=\"Accident Severity Prediction App\",\n",
    "        page_icon=\"🚧\", layout=\"wide\")\n",
    "\n",
    "#creating option list for dropdown menu\n",
    "options_day = ['Sunday', \"Monday\", \"Tuesday\", \"Wednesday\", \"Thursday\", \"Friday\", \"Saturday\"]\n",
    "options_age = ['18-30', '31-50', 'Over 51', 'Unknown', 'Under 18']\n",
    "\n",
    "# number of vehicle involved: range of 1 to 7\n",
    "# number of casualties: range of 1 to 8\n",
    "# hour of the day: range of 0 to 23\n",
    "\n",
    "options_types_collision = ['Vehicle with vehicle collision','Collision with roadside objects',\n",
    "              'Collision with pedestrians','Rollover','Collision with animals',\n",
    "              'Unknown','Collision with roadside-parked vehicles','Fall from vehicles',\n",
    "              'Other','With Train']\n",
    "\n",
    "options_sex = ['Male','Female','Unknown']\n",
    "\n",
    "options_education_level = ['Junior high school','Elementary school','High school',\n",
    "              'Unknown','Above high school','Writing & reading','Illiterate']\n",
    "\n",
    "options_services_year = ['Unknown','2-5yrs','Above 10yr','5-10yrs','1-2yr','Below 1yr']\n",
    "\n",
    "options_acc_area = ['Other', 'Office areas', 'Residential areas', ' Church areas',\n",
    "    ' Industrial areas', 'School areas', ' Recreational areas',\n",
    "    ' Outside rural areas', ' Hospital areas', ' Market areas',\n",
    "    'Rural village areas', 'Unknown', 'Rural village areasOffice areas',\n",
    "    'Recreational areas']\n",
    "\n",
    "# features list\n",
    "features = ['Number_of_vehicles_involved','Number_of_casualties','Hour_of_Day','Type_of_collision','Age_band_of_driver','Sex_of_driver',\n",
    "    'Educational_level','Service_year_of_vehicle','Day_of_week','Area_accident_occured']"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "id": "eb9fd3ee",
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "Defaulting to user installation because normal site-packages is not writeable\n",
      "Collecting streamlit\n",
      "  Downloading streamlit-1.22.0-py2.py3-none-any.whl (8.9 MB)\n",
      "     ---------------------------------------- 8.9/8.9 MB 1.4 MB/s eta 0:00:00\n",
      "Collecting cachetools>=4.0\n",
      "  Downloading cachetools-5.3.0-py3-none-any.whl (9.3 kB)\n",
      "Requirement already satisfied: watchdog in c:\\programdata\\anaconda3\\lib\\site-packages (from streamlit) (2.1.6)\n",
      "Requirement already satisfied: typing-extensions>=3.10.0.0 in c:\\programdata\\anaconda3\\lib\\site-packages (from streamlit) (4.3.0)\n",
      "Collecting gitpython!=3.1.19\n",
      "  Downloading GitPython-3.1.31-py3-none-any.whl (184 kB)\n",
      "     -------------------------------------- 184.3/184.3 kB 1.2 MB/s eta 0:00:00\n",
      "Collecting altair<5,>=3.2.0\n",
      "  Downloading altair-4.2.2-py3-none-any.whl (813 kB)\n",
      "     -------------------------------------- 813.6/813.6 kB 2.0 MB/s eta 0:00:00\n",
      "Collecting validators>=0.2\n",
      "  Downloading validators-0.20.0.tar.gz (30 kB)\n",
      "  Preparing metadata (setup.py): started\n",
      "  Preparing metadata (setup.py): finished with status 'done'\n",
      "Collecting tzlocal>=1.1\n",
      "  Downloading tzlocal-5.0.1-py3-none-any.whl (20 kB)\n",
      "Requirement already satisfied: click>=7.0 in c:\\programdata\\anaconda3\\lib\\site-packages (from streamlit) (8.0.4)\n",
      "Requirement already satisfied: tenacity<9,>=8.0.0 in c:\\programdata\\anaconda3\\lib\\site-packages (from streamlit) (8.0.1)\n",
      "Collecting rich>=10.11.0\n",
      "  Downloading rich-13.3.5-py3-none-any.whl (238 kB)\n",
      "     -------------------------------------- 238.7/238.7 kB 1.8 MB/s eta 0:00:00\n",
      "Requirement already satisfied: numpy in c:\\programdata\\anaconda3\\lib\\site-packages (from streamlit) (1.21.5)\n",
      "Collecting pydeck>=0.1.dev5\n",
      "  Downloading pydeck-0.8.1b0-py2.py3-none-any.whl (4.8 MB)\n",
      "     ---------------------------------------- 4.8/4.8 MB 3.6 MB/s eta 0:00:00\n",
      "Requirement already satisfied: pandas<3,>=0.25 in c:\\programdata\\anaconda3\\lib\\site-packages (from streamlit) (1.4.4)\n",
      "Requirement already satisfied: python-dateutil in c:\\programdata\\anaconda3\\lib\\site-packages (from streamlit) (2.8.2)\n",
      "Requirement already satisfied: requests>=2.4 in c:\\programdata\\anaconda3\\lib\\site-packages (from streamlit) (2.28.1)\n",
      "Collecting pyarrow>=4.0\n",
      "  Downloading pyarrow-12.0.0-cp39-cp39-win_amd64.whl (21.5 MB)\n",
      "     ---------------------------------------- 21.5/21.5 MB 2.7 MB/s eta 0:00:00\n",
      "Requirement already satisfied: packaging>=14.1 in c:\\programdata\\anaconda3\\lib\\site-packages (from streamlit) (21.3)\n",
      "Requirement already satisfied: importlib-metadata>=1.4 in c:\\programdata\\anaconda3\\lib\\site-packages (from streamlit) (4.11.3)\n",
      "Collecting protobuf<4,>=3.12\n",
      "  Downloading protobuf-3.20.3-cp39-cp39-win_amd64.whl (904 kB)\n",
      "     -------------------------------------- 904.2/904.2 kB 4.1 MB/s eta 0:00:00\n",
      "Requirement already satisfied: toml in c:\\programdata\\anaconda3\\lib\\site-packages (from streamlit) (0.10.2)\n",
      "Requirement already satisfied: tornado>=6.0.3 in c:\\programdata\\anaconda3\\lib\\site-packages (from streamlit) (6.1)\n",
      "Collecting blinker>=1.0.0\n",
      "  Downloading blinker-1.6.2-py3-none-any.whl (13 kB)\n",
      "Collecting pympler>=0.9\n",
      "  Downloading Pympler-1.0.1-py3-none-any.whl (164 kB)\n",
      "     -------------------------------------- 164.8/164.8 kB 1.1 MB/s eta 0:00:00\n",
      "Requirement already satisfied: pillow>=6.2.0 in c:\\programdata\\anaconda3\\lib\\site-packages (from streamlit) (9.2.0)\n",
      "Requirement already satisfied: jsonschema>=3.0 in c:\\programdata\\anaconda3\\lib\\site-packages (from altair<5,>=3.2.0->streamlit) (4.16.0)\n",
      "Requirement already satisfied: jinja2 in c:\\programdata\\anaconda3\\lib\\site-packages (from altair<5,>=3.2.0->streamlit) (2.11.3)\n",
      "Requirement already satisfied: entrypoints in c:\\programdata\\anaconda3\\lib\\site-packages (from altair<5,>=3.2.0->streamlit) (0.4)\n",
      "Requirement already satisfied: toolz in c:\\programdata\\anaconda3\\lib\\site-packages (from altair<5,>=3.2.0->streamlit) (0.11.2)\n",
      "Requirement already satisfied: colorama in c:\\programdata\\anaconda3\\lib\\site-packages (from click>=7.0->streamlit) (0.4.5)\n",
      "Collecting gitdb<5,>=4.0.1\n",
      "  Downloading gitdb-4.0.10-py3-none-any.whl (62 kB)\n",
      "     ---------------------------------------- 62.7/62.7 kB 3.3 MB/s eta 0:00:00\n",
      "Requirement already satisfied: zipp>=0.5 in c:\\programdata\\anaconda3\\lib\\site-packages (from importlib-metadata>=1.4->streamlit) (3.8.0)\n",
      "Requirement already satisfied: pyparsing!=3.0.5,>=2.0.2 in c:\\programdata\\anaconda3\\lib\\site-packages (from packaging>=14.1->streamlit) (3.0.9)\n",
      "Requirement already satisfied: pytz>=2020.1 in c:\\programdata\\anaconda3\\lib\\site-packages (from pandas<3,>=0.25->streamlit) (2022.1)\n",
      "Requirement already satisfied: six>=1.5 in c:\\programdata\\anaconda3\\lib\\site-packages (from python-dateutil->streamlit) (1.16.0)\n",
      "Requirement already satisfied: idna<4,>=2.5 in c:\\programdata\\anaconda3\\lib\\site-packages (from requests>=2.4->streamlit) (3.3)\n",
      "Requirement already satisfied: certifi>=2017.4.17 in c:\\programdata\\anaconda3\\lib\\site-packages (from requests>=2.4->streamlit) (2022.9.14)\n",
      "Requirement already satisfied: charset-normalizer<3,>=2 in c:\\programdata\\anaconda3\\lib\\site-packages (from requests>=2.4->streamlit) (2.0.4)\n",
      "Requirement already satisfied: urllib3<1.27,>=1.21.1 in c:\\programdata\\anaconda3\\lib\\site-packages (from requests>=2.4->streamlit) (1.26.11)\n",
      "Collecting pygments<3.0.0,>=2.13.0\n",
      "  Downloading Pygments-2.15.1-py3-none-any.whl (1.1 MB)\n",
      "     ---------------------------------------- 1.1/1.1 MB 1.5 MB/s eta 0:00:00\n",
      "Collecting markdown-it-py<3.0.0,>=2.2.0\n",
      "  Downloading markdown_it_py-2.2.0-py3-none-any.whl (84 kB)\n",
      "     ---------------------------------------- 84.5/84.5 kB 2.4 MB/s eta 0:00:00\n",
      "Collecting tzdata\n",
      "  Using cached tzdata-2023.3-py2.py3-none-any.whl (341 kB)\n",
      "Requirement already satisfied: decorator>=3.4.0 in c:\\programdata\\anaconda3\\lib\\site-packages (from validators>=0.2->streamlit) (5.1.1)\n",
      "Collecting smmap<6,>=3.0.1\n",
      "  Downloading smmap-5.0.0-py3-none-any.whl (24 kB)\n",
      "Requirement already satisfied: MarkupSafe>=0.23 in c:\\programdata\\anaconda3\\lib\\site-packages (from jinja2->altair<5,>=3.2.0->streamlit) (2.0.1)\n",
      "Requirement already satisfied: attrs>=17.4.0 in c:\\programdata\\anaconda3\\lib\\site-packages (from jsonschema>=3.0->altair<5,>=3.2.0->streamlit) (21.4.0)\n",
      "Requirement already satisfied: pyrsistent!=0.17.0,!=0.17.1,!=0.17.2,>=0.14.0 in c:\\programdata\\anaconda3\\lib\\site-packages (from jsonschema>=3.0->altair<5,>=3.2.0->streamlit) (0.18.0)\n",
      "Collecting mdurl~=0.1\n",
      "  Downloading mdurl-0.1.2-py3-none-any.whl (10.0 kB)\n",
      "Building wheels for collected packages: validators\n",
      "  Building wheel for validators (setup.py): started\n",
      "  Building wheel for validators (setup.py): finished with status 'done'\n",
      "  Created wheel for validators: filename=validators-0.20.0-py3-none-any.whl size=19579 sha256=6c77eca2ac57ad7d5fa656e7b23399a2f4cc9ccba001afc56634feff9efdf87f\n",
      "  Stored in directory: c:\\users\\kumar satyam\\appdata\\local\\pip\\cache\\wheels\\2d\\f0\\a8\\1094fca7a7e5d0d12ff56e0c64675d72aa5cc81a5fc200e849\n",
      "Successfully built validators\n",
      "Installing collected packages: validators, tzdata, smmap, pympler, pygments, pyarrow, protobuf, mdurl, cachetools, blinker, tzlocal, pydeck, markdown-it-py, gitdb, rich, gitpython, altair, streamlit\n",
      "Successfully installed altair-4.2.2 blinker-1.6.2 cachetools-5.3.0 gitdb-4.0.10 gitpython-3.1.31 markdown-it-py-2.2.0 mdurl-0.1.2 protobuf-3.20.3 pyarrow-12.0.0 pydeck-0.8.1b0 pygments-2.15.1 pympler-1.0.1 rich-13.3.5 smmap-5.0.0 streamlit-1.22.0 tzdata-2023.3 tzlocal-5.0.1 validators-0.20.0\n",
      "Note: you may need to restart the kernel to use updated packages.\n"
     ]
    },
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "  WARNING: The script pygmentize.exe is installed in 'C:\\Users\\KUMAR SATYAM\\AppData\\Roaming\\Python\\Python39\\Scripts' which is not on PATH.\n",
      "  Consider adding this directory to PATH or, if you prefer to suppress this warning, use --no-warn-script-location.\n",
      "  WARNING: The script markdown-it.exe is installed in 'C:\\Users\\KUMAR SATYAM\\AppData\\Roaming\\Python\\Python39\\Scripts' which is not on PATH.\n",
      "  Consider adding this directory to PATH or, if you prefer to suppress this warning, use --no-warn-script-location.\n",
      "  WARNING: The script streamlit.exe is installed in 'C:\\Users\\KUMAR SATYAM\\AppData\\Roaming\\Python\\Python39\\Scripts' which is not on PATH.\n",
      "  Consider adding this directory to PATH or, if you prefer to suppress this warning, use --no-warn-script-location.\n",
      "ERROR: pip's dependency resolver does not currently take into account all the packages that are installed. This behaviour is the source of the following dependency conflicts.\n",
      "spyder 5.2.2 requires pyqt5<5.13, which is not installed.\n",
      "spyder 5.2.2 requires pyqtwebengine<5.13, which is not installed.\n"
     ]
    }
   ],
   "source": [
    "pip install streamlit"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 6,
   "id": "c7f9a9a2",
   "metadata": {},
   "outputs": [
    {
     "name": "stderr",
     "output_type": "stream",
     "text": [
      "2023-05-16 10:48:19.632 \n",
      "  \u001b[33m\u001b[1mWarning:\u001b[0m to view this Streamlit app on a browser, run it with the following\n",
      "  command:\n",
      "\n",
      "    streamlit run C:\\ProgramData\\Anaconda3\\lib\\site-packages\\ipykernel_launcher.py [ARGUMENTS]\n"
     ]
    }
   ],
   "source": [
    "# Give a title to web app using html syntax\n",
    "st.markdown(\"<h1 style='text-align: center;'>Accident Severity Prediction App 🚧</h1>\", unsafe_allow_html=True)\n",
    "\n",
    "# define a main() function to take inputs from user in form based approach\n",
    "def main():\n",
    "    with st.form(\"road_traffic_severity_form\"):\n",
    "       st.subheader(\"Please enter the following inputs:\")\n",
    "        \n",
    "       No_vehicles = st.slider(\"Number of vehicles involved:\",1,7, value=0, format=\"%d\")\n",
    "       No_casualties = st.slider(\"Number of casualties:\",1,8, value=0, format=\"%d\")\n",
    "       Hour = st.slider(\"Hour of the day:\", 0, 23, value=0, format=\"%d\")\n",
    "       collision = st.selectbox(\"Type of collision:\",options=options_types_collision)\n",
    "       Age_band = st.selectbox(\"Driver age group?:\", options=options_age)\n",
    "       Sex = st.selectbox(\"Sex of the driver:\", options=options_sex)\n",
    "       Education = st.selectbox(\"Education of driver:\",options=options_education_level)\n",
    "       service_vehicle = st.selectbox(\"Service year of vehicle:\", options=options_services_year)\n",
    "       Day_week = st.selectbox(\"Day of the week:\", options=options_day)\n",
    "       Accident_area = st.selectbox(\"Area of accident:\", options=options_acc_area)\n",
    "        \n",
    "       submit = st.form_submit_button(\"Predict\")\n",
    "\n",
    "# encode using ordinal encoder and predict\n",
    "    if submit:\n",
    "       input_array = np.array([collision,\n",
    "                  Age_band,Sex,Education,service_vehicle,\n",
    "                  Day_week,Accident_area], ndmin=2)\n",
    "        \n",
    "       encoded_arr = list(encoder.transform(input_array).ravel())\n",
    "        \n",
    "       num_arr = [No_vehicles,No_casualties,Hour]\n",
    "       pred_arr = np.array(num_arr + encoded_arr).reshape(1,-1)        \n",
    "      \n",
    "# predict the target from all the input features\n",
    "       prediction = model.predict(pred_arr)\n",
    "        \n",
    "       if prediction == 0:\n",
    "           st.write(f\"The severity prediction is fatal injury⚠\")\n",
    "       elif prediction == 1:\n",
    "           st.write(f\"The severity prediction is serious injury\")\n",
    "       else:\n",
    "           st.write(f\"The severity prediction is slight injury\")\n",
    "        \n",
    "       st.write(\"Developed By: Avi kumar Talaviya\")\n",
    "       st.markdown(\"\"\"Reach out to me on: [Twitter](https://twitter.com/avikumart_) |\n",
    "       [Linkedin](https://www.linkedin.com/in/avi-kumar-talaviya-739153147/) |\n",
    "       [Kaggle](https://www.kaggle.com/avikumart) \n",
    "       \"\"\")"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 8,
   "id": "bc3fd94b",
   "metadata": {},
   "outputs": [],
   "source": [
    "a,b,c = st.columns([0.2,0.6,0.2])\n",
    "with b:\n",
    " st.image(\"banner-picture.jpeg\", use_column_width=True)\n",
    "\n",
    "\n",
    "# description about the project and code files       \n",
    "st.subheader(\"🧾Description:\")\n",
    "st.text(\"\"\"This data set is collected from Addis Ababa Sub-city police departments for master's research work. \n",
    "The data set has been prepared from manual records of road traffic accidents of the year 2017-20. \n",
    "All the sensitive information has been excluded during data encoding and finally it has 32 features and 12316 instances of the accident.\n",
    "Then it is preprocessed and for identification of major causes of the accident by analyzing it using different machine learning classification algorithms.\n",
    "\"\"\")\n",
    "\n",
    "st.markdown(\"Source of the dataset: [Click Here](https://www.narcis.nl/dataset/RecordID/oai%3Aeasy.dans.knaw.nl%3Aeasy-dataset%3A191591)\")\n",
    "\n",
    "st.subheader(\"🧭 Problem Statement:\")\n",
    "st.text(\"\"\"The target feature is Accident_severity which is a multi-class variable. \n",
    "The task is to classify this variable based on the other 31 features step-by-step by going through each day's task. \n",
    "The metric for evaluation will be f1-score\n",
    "\"\"\")\n",
    "\n",
    "st.markdown(\"Please find GitHub repository link of project: [Click Here](https://github.com/avikumart/Road-Traffic-Severity-Classification-Project)\")          \n",
    "  \n",
    "# run the main function        \n",
    "if __name__ == '__main__':\n",
    "  main()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "id": "c90773db",
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.9.13"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 5
}
