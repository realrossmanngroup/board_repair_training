/* Grab all transistors mentioned on forum*/

(SELECT DISTINCT TRIM(
    CASE
        WHEN CHAR_LENGTH(REGEXP_SUBSTR(message, '[Qq][0-9]{4}[^0-9]')) = 5
        THEN SUBSTRING(REGEXP_SUBSTR(message, '[Qq][0-9]{4}[^0-9]'), 1, 5)
        ELSE REGEXP_SUBSTR(message, '[Qq][0-9]{4}')
    END
    /* Grab all transistors R#### format from posts. This means 'R' (upper or lower case)
       followed by four numbers. Any junk character after the pattern is removed. */
) FROM xf_post)
UNION
(SELECT DISTINCT TRIM(
    CASE
        WHEN CHAR_LENGTH(REGEXP_SUBSTR(title, '[Qq][0-9]{4}[^0-9]')) = 5
        THEN SUBSTRING(REGEXP_SUBSTR(title, '[Qq][0-9]{4}[^0-9]'), 1, 5)
        ELSE REGEXP_SUBSTR(title, '[Qq][0-9]{4}')
    END
    /* Grab all transistors R#### format from thread titles. This means 'Q' (upper or lower case)
       followed by four numbers. Any junk character after the pattern is removed. */
) FROM xf_thread)
INTO OUTFILE 'transistors.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n';
