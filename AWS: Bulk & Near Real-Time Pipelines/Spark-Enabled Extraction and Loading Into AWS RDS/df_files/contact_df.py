from pyspark.sql.functions import col,struct, udf
from pyspark.sql.types import *
from pyspark.sql import Row
import re




# UDF to remove none in street 2 from contact dataframe
def str_merge(street1, street2):
    if street1 is not None and street2 is not None:
        return street2 + ',' + street1
    elif street1 is not None:
        return street1
    elif street2 is not None:
        return street2
    else:
        return None

# UDF to remove extra characters from phone numbers
def clean_phone_number(phone):
    # Remove all non-digit characters from the phone number
    cleaned_phone = re.sub(r'\D', '', phone)
    return cleaned_phone

def contacts_df(jdf):

    # convertin the dict to separated columns
    mailing_df = jdf.select(struct(col("addresses.mailing.*")).alias("mailing_data")).select("mailing_data.*")

    # removing rows with all null values
    mailing_df = mailing_df.dropna(how='all')

    # Create A UDF
    str_merge_udf = udf(str_merge, StringType())

    # Apply the UDF to create a new column

    mailing_df = mailing_df.withColumn('Address', str_merge_udf(col('street1'), col('street2'))).withColumnRenamed('stateOrCountry', 'State') \
                            .drop('street1', 'street2', 'stateOrCountryDescription')

    mailing_df = mailing_df.rdd.zipWithIndex().map(lambda r: Row(*r[0], r[1])).toDF()

    # renaming the column after adding index
    mailing_df = mailing_df.select(col('_1').alias('City'),col('_2').alias('State'),
                                col('_3').alias('Zipcode').cast(IntegerType()),col('_4').alias('Address'),
                                col('_5').alias('index').cast(IntegerType()))
    
    return mailing_df

def contact_table(mailing_df,company_table):

    address_df = mailing_df.join(company_table.select(col('Phone_Number'), col('index')),on='index',how='left')

    clean_phone_number_udf = udf(clean_phone_number)

    contact_table = address_df.withColumn("Phone_Number", clean_phone_number_udf(col("Phone_Number"))) \
                            .withColumn("Phone_Number", col("Phone_Number").cast(IntegerType()))

    contact_table = contact_table.select('Address', 'Phone_Number', 'City', 'State', 'ZipCode', col('index').alias('company_index')) 

    contact_table.createOrReplaceTempView("Contact_Table")
    cont_df = spark.sql("select * from Contact_Table")

    return cont_df