import pandas
import pandasql


#ps2.1
def num_rainy_days(filename):
	'''
    This function converts a CSV file into a dataframe and runs a SQL query, 
    returning a count of days when it rained.
    '''
 weather_data = pandas.read_csv(filename)

    q = """
    SELECT count(*)
    FROM weather_data
    WHERE rain = 1;
    """
    
    #Execute your SQL command against the pandas frame
    rainy_days = pandasql.sqldf(q.lower(), locals())
    return rainy_days