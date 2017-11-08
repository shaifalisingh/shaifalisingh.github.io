# Hawaii Climate Analysis 

### This repository collects the following code pertaining to an analysis of temperature and precipitation readings in Hawaii.


![Surf](Surf.jpg)

### Data Engineering
* Code to create cleaned up CSV consisting of data with all NaN values. The reason why I removed the NaNs rather than substituted values is that I have no idea what the NaN values were originally supposed to be, therefore I decided not to make an assumption.

### Database Engineering
* Code to converted the cleaned CSV into a dataframe, and then uploaded them to a database using the SQLAlchemy ORM.

### Climate Analysis
* A jupyter notebook that consisted of many analysis of this data as below 
*Measurement of TOBS readings from one station over the course of the year charted in a histogram.*
*Measurement of Precipitation readings over the past year.*
*Measurement of the average temperatures, max temperatures, and minimum temperatures over a specified date.*

### App.py
* A Flask app that created a RESTFUL API through which a user could make several calls to access the data.