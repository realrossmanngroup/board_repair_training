/* Grab all signal names mentioned on the forum */

(SELECT DISTINCT TRIM(
    CASE
        WHEN CHAR_LENGTH(REGEXP_SUBSTR(message, '[A-Za-z0-9]+_[A-Za-z0-9]+')) >= 3
        THEN REGEXP_SUBSTR(message, '[A-Za-z0-9]+_[A-Za-z0-9]+')
    END
    /* Grab all signal names in the format "XXXX_XXXX" from posts.
       This means random letters/numbers connected by an underscore. */
) FROM xf_post)
UNION
(SELECT DISTINCT TRIM(
    CASE
        WHEN CHAR_LENGTH(REGEXP_SUBSTR(title, '[A-Za-z0-9]+_[A-Za-z0-9]+')) >= 3
        THEN REGEXP_SUBSTR(title, '[A-Za-z0-9]+_[A-Za-z0-9]+')
    END
    /* Grab all signal names in the format "XXXX_XXXX" from thread titles.
       This means random letters/numbers connected by an underscore. */
) FROM xf_thread);

/*
INTO OUTFILE 'signal_names.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n';
*/


