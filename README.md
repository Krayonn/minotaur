# Minotaur
A webapp containing an API to retrieve compound and related assay result data, and an interactive dashboard to view the compound and related assay result data

## Setup
To setup the project up you will need to have python 3 installed on your machine, and it is encouraged to use virtual environments.

To install the requirements for this project, use
`pip install -r requirements.txt`

To start the webapp on your localhost, please navigate to the django_api, then use
`python manage.py runserver`

In your browser then go to [http://localhost:8000/](http://localhost:8000/) to view the webapp.

## Pages
### Home page
Here you find some basic information on the project, as well as links to the other pages.

### Api page
Here will be a button that can be used to reload the compounds.json file found under minotaur/compounds/fixtures into the django database. It will also display the data currently loaded into the database in json format.
To use the Api itself, use the following paths
* */compounds* - to retrieve a list of all the compounds in the database.
* */compounds/1234* - to retrieve the compound with the given compound ID.
* */compounds/123/assays* - to retrieve only the list of assay results of the compound with the given compound id.
* */compounds/123/assays/456* - to retrieve the assay result with the given assay result idea.

### Dashboard
The dashboard page contains an *interactive graph* to view the compound and assay result data. Use the drop down menus to select what you would like to be on the x and y axis to display the data. When you hover over the datapoints the surrounding components will then update to according to what datapoint you are hovered over. The components are a data table containing the properties of the compound, the structure of the compound and below a list of the assay results for that compound showing the target and what has been measured.
If the graph does not load or the components aren't changing for some reason, please try refreshing the page.
