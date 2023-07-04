from pyspark.sql.functions import col,udf, posexplode_outer, to_date
from pyspark.sql.types import *
from pyspark.sql import Row
import datetime

from spark_sql import form_sql




def sec_fillings_df(jdf):
    filling_df = jdf.select(col("filings.recent.accessionNumber"), col("filings.recent.filingDate"),
                            col("filings.recent.acceptanceDateTime"), col("filings.recent.act"), 
                            col("filings.recent.form"), col("filings.recent.fileNumber"), 
                            col("filings.recent.filmNumber"), col("filings.recent.size"))

    ## Adding the index into the table

    filling_df1 = filling_df.rdd.zipWithIndex().map(lambda r: Row(*r[0], r[1])).toDF() 


    filling_df1 = filling_df1.select(col('_1').alias('accessionNumber'),col('_2').alias('filingDate'),
                                    col('_3').alias('acceptanceDateTime'),col('_4').alias('act'),
                                    col('_5').alias('form'),col('_6').alias('fileNumber'),
                                    col('_7').alias('filmNumber'),col('_8').alias('size'), col('_9').alias('index').cast(IntegerType()))


    return filling_df1

def convert_datetime(input_datetime):
    if input_datetime is None:
        return None

    datetime_obj = datetime.datetime.strptime(input_datetime, '%Y-%m-%dT%H:%M:%S.%fZ')
    mysql_datetime = datetime_obj.strftime('%Y-%m-%d %H:%M:%S')
    return mysql_datetime

# convertin the data from list type to column type and creating temp view
def form_table(filling_df1):

    accessionNumber = filling_df1.select(filling_df1.index,posexplode_outer(filling_df1.accessionNumber)
                                     .alias('accessionNumber_index','accessionNumber')).createOrReplaceTempView("accession_number")

    #-----------------------------------------------------------------------------------------------------------------------#
    filingDate = filling_df1.select(filling_df1.index,posexplode_outer(filling_df1.filingDate).alias('filingDate_index','filingDate'))

    filingDate = filingDate.withColumn('filingDate', to_date('filingDate', 'yyyy-MM-dd')).createOrReplaceTempView("filing_date") 
    
    #-----------------------------------------------------------------------------------------------------------------------#
    acceptanceDateTime = filling_df1.select(filling_df1.index,posexplode_outer(filling_df1.acceptanceDateTime)
                                            .alias('acceptanceDateTime_index','acceptanceDateTime'))
    
    # Register the UDF
    convert_datetime_udf = udf(convert_datetime, StringType())

    # Apply the UDF to the 'acceptanceDateTime' column
    acceptanceDateTime = acceptanceDateTime.withColumn('acceptanceDateTime', convert_datetime_udf('acceptanceDateTime')
                                                        .cast(TimestampType())).createOrReplaceTempView("acceptance_date_time")

    #-----------------------------------------------------------------------------------------------------------------------#
    act = filling_df1.select(filling_df1.index,posexplode_outer(filling_df1.act).alias('act_index','act'))

    act = act.select([col(c).cast(IntegerType()).alias(c) for c in act.columns]).createOrReplaceTempView("act_table")
    #-----------------------------------------------------------------------------------------------------------------------#

    form = filling_df1.select(filling_df1.index,posexplode_outer(filling_df1.form).alias('form_index','form')) \
                                    .createOrReplaceTempView("form_table")
    
    #-----------------------------------------------------------------------------------------------------------------------#

    fileNumber = filling_df1.select(filling_df1.index,posexplode_outer(filling_df1.fileNumber).alias('fileNumber_index','fileNumber')) \
                                                .createOrReplaceTempView("file_number")
    #-----------------------------------------------------------------------------------------------------------------------#

    filmNumber = filling_df1.select(filling_df1.index,posexplode_outer(filling_df1.filmNumber).alias('filmNumber_index','filmNumber')) 
    filmNumber = filmNumber.select([col(c).cast(IntegerType()).alias(c) for c in filmNumber.columns]).createOrReplaceTempView("film_number")                                            
    #-----------------------------------------------------------------------------------------------------------------------#
    size = filling_df1.select(filling_df1.index,posexplode_outer(filling_df1.size).alias('size_index','size'))

    size = size.select([col(c).cast(IntegerType()).alias(c) for c in size.columns]).createOrReplaceTempView("size_table")
    #-----------------------------------------------------------------------------------------------------------------------#

    fill_table_df = spark.sql(form_sql) #import from spark_sql.py

    fill_table_df.createOrReplaceTempView("Forms_table")
    rds_df = spark.sql("select * from Forms_table")

    return rds_df