# SQLalchemy challenge
This is my SQLalchemy challenge submission. All code in this repository is my own.
## Climate Analysis
The climate_starter ipynb file contains the climate analysis. The data utilized is from the Hawaii.sqlite database in the resources folder. The analysis includes a bar chart of total precipitation for the last year, the summary statistics for precipitation, and a temperature frequency histogram. 
## flask app
The app.py file contains a flask app to retrieve and return jsonified weather data from the Hawaii.sqlite file. The import statements at the top of the code contain the necessary imports to run flask and SQLalchemy. When the file is run, it creates a server, and posts the link to access it in the terminal. Clicking on the server ip in the terminal will open a window in chrome for the application to run. The different pages can be accessed by pasting the API routes into the search bar at the top of chrome. 
## Additional info
The resources folder contains CSV files of both of the tables for convienence. Both the climate analysis and flask app code make use of the Python DateTime library. The necessary import statements to utilize this library are included in both files. 
