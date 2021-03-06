## Duration Report
Duration report focuses on how the length of tracks changed over time in the 21st century.

The dataset used for this research was created by Yamac Eren Ay and released on the Kaggle website. It consists of around 600 thousand songs released on the Spotify US market between years of 1922 and 2021. It can be found by following the link: https://www.kaggle.com/yamaerenay/spotify-dataset-19212020-160k-tracks.

The dataset was reduced to only include the tracks between the years 2000 and 2021. The final csv file with the data is located in this folder. Our future plan is to develop an IMA database and use API calls to retrieve the data directly from it instead of using csv files.

Compressed csv file with all 600 thousand songs is also stored in the repository. To use it, first manually decompress it.

This folder also includes some notebooks used in the research stage and the notbook with the final visualisations used directly in the report.

- [visual_funtions](visual_functions.py) file contains functions used in notebooks for visualisations
- [duration_visual](duration_visual.ipynb) notebook has all of the final visualisations most of which are used in the final report
