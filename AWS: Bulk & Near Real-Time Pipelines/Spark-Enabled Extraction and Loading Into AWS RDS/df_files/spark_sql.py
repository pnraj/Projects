

form_sql = '''
    SELECT a.`index` as Company_index , a.accessionNumber as `Acession_Number`, fd.filingDate as `Filling_Date`, ad.acceptanceDateTime as Acceptance_DateTime, act.act as Act, f.form as Form, fna.fileNumber as File_Number, fl.filmNumber as Film_Number, s.`size` as `Size`
    FROM accession_number a
    FULL OUTER JOIN filing_date fd
        ON a.`index` = fd.`index` AND a.accessionNumber_index = fd.filingDate_index
    FULL OUTER JOIN acceptance_date_time ad
        ON a.`index` = ad.`index` AND a.accessionNumber_index = ad.acceptanceDateTime_index
    FULL OUTER JOIN act_table act
        ON a.`index` = act.`index` AND a.accessionNumber_index = act.act_index
    FULL OUTER JOIN form_table f
        ON a.`index` = f.`index` AND a.accessionNumber_index = f.form_index
    FULL OUTER JOIN file_number fna
        ON a.`index` = fna.`index` AND a.accessionNumber_index = fna.fileNumber_index
    FULL OUTER JOIN film_number fl
        ON a.`index` = fl.`index` AND a.accessionNumber_index = fl.filmNumber_index
    FULL OUTER JOIN size_table s
        ON a.`index` = s.`index` AND a.accessionNumber_index = s.size_index
'''

