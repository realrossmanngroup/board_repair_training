/* Grab all capacitors mentioned on forum*/

(SELECT DISTINCT TRIM(
    CASE
        WHEN CHAR_LENGTH(REGEXP_SUBSTR(message, '[Cc][0-9]{4}[^0-9]')) = 5
        THEN SUBSTRING(REGEXP_SUBSTR(message, '[Cc][0-9]{4}[^0-9]'), 1, 5)
        ELSE REGEXP_SUBSTR(message, '[Cc][0-9]{4}')
    END
    /* Grab all capacitors C#### format from posts. This means 'C' (upper or lower case)
       followed by four numbers. Any junk character after the pattern is removed. */
) FROM xf_post)
UNION
(SELECT DISTINCT TRIM(
    CASE
        WHEN CHAR_LENGTH(REGEXP_SUBSTR(title, '[Cc][0-9]{4}[^0-9]')) = 5
        THEN SUBSTRING(REGEXP_SUBSTR(title, '[Cc][0-9]{4}[^0-9]'), 1, 5)
        ELSE REGEXP_SUBSTR(title, '[Cc][0-9]{4}')
    END
    /* Grab all capacitors C#### format from thread titles. This means 'C' (upper or lower case)
       followed by four numbers. Any junk character after the pattern is removed. */
) FROM xf_thread)
INTO OUTFILE 'capacitors.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n';
