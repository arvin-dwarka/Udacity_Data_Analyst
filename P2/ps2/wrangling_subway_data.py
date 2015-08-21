import pandas
import pandasql
import csv
import datetime
import os


# ps2.1
def num_rainy_days(filename):
	'''
	This function converts a CSV file into a dataframe and runs a SQL query,
	returning a count of days when it rained.
    '''
	weather_data = pandas.read_csv(filename)

   	q = """
    SELECT count(*)
    FROM weather_data
    WHERE rain=1;
    """

    # Execute your SQL command against the pandas frame
	rainy_days = pandasql.sqldf(q.lower(), locals())
	return rainy_days

# ps2.2
def max_temp_aggregate_by_fog(filename):
	'''
    This function converts a CSV file into a dataframe and runs a SQL query,
    returning max temperatures on foggy and none foggy days.
    '''
 	weather_data = pandas.read_csv(filename)

	q = """
	SELECT fog, max(maxtempi)
	FROM weather_data
	GROUP BY fog;
	"""

	# Execute your SQL command against the pandas frame
	foggy_days = pandasql.sqldf(q.lower(), locals())
	return foggy_days

# ps2.3
def avg_weekend_temperature(filename):
	'''
	This function converts a CSV file into a dataframe and runs a SQL query, 
	returning average mean temperature on weekends.
	'''
	weather_data = pandas.read_csv(filename)

	q = """
	SELECT avg(meantempi)
	FROM weather_data
	WHERE cast (strftime('%w', date) as integer) = 0 or cast (strftime('%w', date) as integer) = 6;
	"""

	# Execute your SQL command against the pandas frame
	mean_temp_weekends = pandasql.sqldf(q.lower(), locals())
	return mean_temp_weekends

# ps2.4
def avg_min_temperature(filename):
	'''
	This function converts a CSV file into a dataframe and runs a SQL query, 
	returning the average minimunm temperature on rainy days.
	'''
	weather_data = pandas.read_csv(filename)

	q = """
	SELECT avg(mintempi)
	FROM weather_data
	WHERE mintempi > 55 and rain = 1;
	"""

	# Execute your SQL command against the pandas frame
	avg_min_temp_rainy = pandasql.sqldf(q.lower(), locals())
	return avg_min_temp_rainy

# ps2.5 - this was intense!!
def fix_turnstile_data(*filenames):
	'''
	This function fixes spagetti lines of data 
	by transforming the csv format from the input to the output example
	and prepends "updated_" to the filename.
	
	input example:
	A002,R051,02-00-00,05-21-11,00:00:00,REGULAR,
	003169391,001097585,05-21-11,04:00:00,REGULAR,
	003169415,001097588,05-21-11,08:00:00,REGULAR,
	003169431,001097607,05-21-11,12:00:00,REGULAR,
	003169506,001097686,05-21-11,16:00:00,REGULAR,
	003169693,001097734,05-21-11,20:00:00,REGULAR,
	003169998,001097769,05-22-11,00:00:00,REGULAR,
	003170119,001097792,05-22-11,04:00:00,REGULAR,003170146,001097801

	output example:
	A002,R051,02-00-00,05-21-11,00:00:00,REGULAR,003169391,001097585
	A002,R051,02-00-00,05-21-11,04:00:00,REGULAR,003169415,001097588
	A002,R051,02-00-00,05-21-11,08:00:00,REGULAR,003169431,001097607
	A002,R051,02-00-00,05-21-11,12:00:00,REGULAR,003169506,001097686
	A002,R051,02-00-00,05-21-11,16:00:00,REGULAR,003169693,001097734
	A002,R051,02-00-00,05-21-11,20:00:00,REGULAR,003169998,001097769
	A002,R051,02-00-00,05-22-11,00:00:00,REGULAR,003170119,001097792
	A002,R051,02-00-00,05-22-11,04:00:00,REGULAR,003170146,001097801 
	'''
	for name in filenames:
		output_data = []
		input_data = read_csv(name)
		for row in input_data:
			first_element = row.pop(0)
			second_element = row.pop(0)
			third_element = row.pop(0)
			while row:
				new_row = [first_element, second_element, third_element]
				for item in range(min(5,len(row))):
					new_row.append(row.pop(0).strip())
				output_data.append(new_row)
		write_csv('updated_'+name, output_data)

def read_csv(filename):
	'''
	This function reads a csv file and creates a workable csv_output list.
	'''
	csv_output = []
	with open(filename, 'rb') as csvfile:
		reader = csv.reader(csvfile, delimiter=',', quotechar='|')
		for row in reader:
			csv_output.append(row)
	return csv_output

def write_csv(filename, array):
	'''
	This function writes an array to a csv file.
	'''
	with open(filename, 'wb') as csvfile:
		writer = csv.writer(csvfile, delimiter=',')
		for row in array:
			writer.writerow(row)

# ps2.6
def create_master_turnstile_file(filenames, output_file):
	'''
	This function will merge two files that have the same column structure 
	and no headers into one output file with a header.
	'''
	with open(output_file, 'w') as master_file:
		master_file.write('C/A,UNIT,SCP,DATEn,TIMEn,DESCn,ENTRIESn,EXITSn\n')
		for filename in filenames:
			with open(filename, 'r') as input_file:
				for line in input_file:
					master_file.write(line)

# ps2.7
def filter_by_regular(filename):
    '''
    This function reads the csv file located at filename into a pandas dataframe,
    and filter the dataframe to only rows 
    where the 'DESCn' column has the value 'REGULAR'.
    
    For example, if the pandas dataframe is as follows:
    ,C/A,UNIT,SCP,DATEn,TIMEn,DESCn,ENTRIESn,EXITSn
    0,A002,R051,02-00-00,05-01-11,00:00:00,REGULAR,3144312,1088151
    1,A002,R051,02-00-00,05-01-11,04:00:00,DOOR,3144335,1088159
    2,A002,R051,02-00-00,05-01-11,08:00:00,REGULAR,3144353,1088177
    3,A002,R051,02-00-00,05-01-11,12:00:00,DOOR,3144424,1088231
    
    The dataframe will look like below after filtering to only rows where DESCn column
    has the value 'REGULAR':
    0,A002,R051,02-00-00,05-01-11,00:00:00,REGULAR,3144312,1088151
    2,A002,R051,02-00-00,05-01-11,08:00:00,REGULAR,3144353,1088177
    '''
    df = pandas.read_csv(filename)
    turnstile_data = df[df['DESCn'] == 'REGULAR']
    return turnstile_data

# ps2.8
def get_hourly_entries(df):
	'''
	This function:
		1) Create a new column called ENTRIESn_hourly
	    2) Assign to the column the difference between ENTRIESn of the current row 
          and the previous row. If there is any NaN, fill/replace it with 1.
	'''
	df['ENTRIESn_hourly'] = df['ENTRIESn'] - df['ENTRIESn'].shift(periods=1)
	df = df.fillna(1)
	return df

# ps2.9
def get_hourly_exits(df):
	'''
	This function:
       1) Create a new column called EXITSn_hourly
       2) Assign to the column the difference between EXITSn of the current row 
          and the previous row. If there is any NaN, fill/replace it with 0.
	'''
	df['EXITSn_hourly'] = df['EXITSn'] - df['EXITSn'].shift(periods=1)
	df = df.fillna(0)
	return df

# ps2.10
def time_to_hour(time):
	'''
	This function returns the hour part from an input variable time.
	'''
	hour = int(time.split(':')[0])
	return hour

# ps2.11
def reformat_subway_dates(date):
	'''
	This function takes an input date and returns the date in year-month-day
	'''
	subway_date = time.strptime(date, "%m-%d-%y")
	date_formatted = datetime.datetime(*subway_date[:6])
	return date_formatted.strftime("%Y-%m-%d")

if __name__ == '__main__':
	'''
	This calls the functions above.
	'''
	os.system('clear')

	print "Number of rainy days:"
	print num_rainy_days('weather_underground.csv')
	raw_input("Press Enter to continue...")
	os.system('clear')

	print "Maximum temperature aggregate by fog:"
	print max_temp_aggregate_by_fog('weather_underground.csv')
	raw_input("Press Enter to continue...")
	os.system('clear')

	print "Average minimum temperature:"
	print avg_min_temperature('weather_underground.csv')
	raw_input("Press Enter to continue...")
	os.system('clear')

	print "Fixed turnstile data:"
	fix_turnstile_data('turnstile_110528.txt')
	print open('updated_turnstile_110528.txt').read()
	raw_input("Press Enter to continue...")
	os.system('clear')

	print "Filter by regular:"
	df = filter_by_regular('turnstile_data.csv')
	print df
	raw_input("Press Enter to continue...")

	print "Hourly entries:"
	df = pandas.read_csv('turnstile_data.csv')
	print get_hourly_entries(df)
	raw_input("Press Enter to continue...")
	os.system('clear')

	print "Hourly exits:"
	df = pandas.read_csv('turnstile_data.csv')
	print get_hourly_exits(df)
	os.system('clear')
