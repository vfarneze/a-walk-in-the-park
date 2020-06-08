# -*- coding: utf-8 -*-
"""PySpark_DataFrame.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1kuO_D-mxEmhxqggBhC_35-j7gqID96Ol

## Install JDK
## Install Spark
## Set Environment variables
## Create a Spark Session
"""

!apt-get install openjdk-8-jdk-headless -qq > /dev/null
!wget -q https://archive.apache.org/dist/spark/spark-2.4.3/spark-2.4.3-bin-hadoop2.6.tgz
!tar -xvf spark-2.4.3-bin-hadoop2.6.tgz
!pip install -q findspark
import os
os.environ["JAVA_HOME"] = "/usr/lib/jvm/java-8-openjdk-amd64"
os.environ["SPARK_HOME"] = "/content/spark-2.4.3-bin-hadoop2.6"
import findspark
findspark.init()
from pyspark.sql import SparkSession
spark = SparkSession.builder.master("local[*]").getOrCreate()

"""## Test Spark"""

df = spark.createDataFrame([{"Google": "Colab","Spark": "Scala"} ,{"Google": "Dataproc","Spark":"Python"}])
df.show()

"""## Copy a data file to your local Colab environment"""

!wget https://raw.githubusercontent.com/futurexskill/bidata/master/retailstore.csv

"""## Check if the file is copied"""

!ls

"""# DataFrame

## Read the CSV file into a DataFrame
"""

customerDF = spark.read.csv("retailstore.csv",header=True)

type(customerDF)

"""## Print the dataset"""

customerDF.show()

customerDF.show(5)

"""## Get Statistical Summary of the DataFrame"""

customerDF.describe().show()

"""## Select a particular column"""

customerDF.select("country").show()

"""## View count group by country"""

customerDF.groupBy("country").count().show()

"""## View count group by gender"""

customerDF.groupBy("gender").count().show()

"""# Running SQL Queries Programmatically

## Create a temporary table
"""

customerDF.createOrReplaceTempView("customer")

"""## Fetch all records from the table using a SQL query"""

results = spark.sql("select * from customer")

type(results)

"""## Show the result fetched"""

results.show()

"""## Get the list of customers with age greater than 22"""

new_results = spark.sql("select * from customer where age>22").show()

"""## Display the salary of customers with age greater than 22"""

new_results = spark.sql("select * from customer where age>22").select("salary").show()

"""## List of people earning more than 30000 with Spark DataFrame"""

customerDF.filter("salary > 30000").show()

"""## List of people earning more than 200K with Spark SQL"""

spark.sql("select * from customer where salary > 30000").show()

"""## Group By gender find average salary and max age"""

customerDF.groupBy("gender").agg({"salary": "avg", "age": "max"}).show()

"""## Fetch Multiple Columns"""

customerDF.select(["age","salary"]).show()

"""## Adding a new column"""

customerDF.withColumn('doublesalary',customerDF['salary']*2).show()

"""## Renaming a column"""

customerDF.withColumnRenamed('salary', 'income').show()

"""## Age of people earning more than 30000"""

customerDF.filter("salary > 30000").select('age').show()

"""## Age & country of people earning more than 200K"""

customerDF.filter("salary > 30000").select('age','country').show()

"""## Fetching data with Python comparision operator"""

customerDF.filter(customerDF['salary'] > 30000).show()

customerDF.filter(customerDF['salary'] > 30000).select('age','country').show()

"""## Applying multiple Filter conditions"""

customerDF.filter((customerDF['salary'] > 30000) & (customerDF['age'] < 25)).show()

"""## ~ is a not operation"""

customerDF.filter((customerDF['salary'] > 30000) & ~(customerDF['age'] < 22)).show()

"""## Count Distrinct, Average and Standard Deviation"""

from pyspark.sql.functions import countDistinct, avg,stddev

"""## count distinct countries"""

customerDF.select(countDistinct("country")).show()

"""## Use alias"""

customerDF.select(countDistinct("country").alias("Distinct Countries")).show()

"""## Calculate avergage income"""

customerDF.select(avg('salary')).show()

"""## Calculate avergage age"""

customerDF.select(avg('age')).show()

"""## Calculate standard deviation"""

customerDF.select(stddev("salary")).show()

customerDF.select(stddev("age")).show()

"""## format number"""

from pyspark.sql.functions import format_number

salary_std = customerDF.select(stddev("salary").alias('std'))

salary_std.show()

salary_std.select(format_number('std',2)).show()

"""## Order By

Order By Ascending
"""

customerDF.orderBy("salary").show()

"""Order by descending"""

customerDF.orderBy(customerDF["salary"].desc()).show()

"""## drop any row that contains null data"""

customerDF.na.drop().show()

"""## Replace missing values"""

customerDF.na.fill('NEW VALUE').show()
