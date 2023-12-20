/* Grab all Macbook logic board numbers from forum posts */

(SELECT DISTINCT TRIM(
    CASE
        WHEN CHAR_LENGTH(REGEXP_SUBSTR(message, '820-[0-9]{4}[^0-9]')) = 9
        THEN SUBSTRING(REGEXP_SUBSTR(message, '820-[0-9]{4}[^0-9]'), 1, 8)
        ELSE REGEXP_SUBSTR(message, '820-[0-9]{4}[^0-9]')
    END
    /* Grab all board numbers in 820-#### format from posts. This means 4 numbers,
       the fifth character NOT being a number, and the fifth character being
       removed so that the ) or , or . isn't in there as extra junk. */
) FROM xf_post)
UNION
(SELECT DISTINCT TRIM(
    CASE
        WHEN CHAR_LENGTH(REGEXP_SUBSTR(title, '820-[0-9]{4}[^0-9]')) = 9
        THEN SUBSTRING(REGEXP_SUBSTR(title, '820-[0-9]{4}[^0-9]'), 1, 8)
        ELSE REGEXP_SUBSTR(title, '820-[0-9]{4}[^0-9]')
    END
) FROM xf_thread)
/* Grab all board numbers in 820-#### format from titles */
UNION
(SELECT DISTINCT TRIM(
    CASE
        WHEN CHAR_LENGTH(REGEXP_SUBSTR(message, '820-[0-9]{5}[^0-9]')) = 10
        THEN SUBSTRING(REGEXP_SUBSTR(message, '820-[0-9]{5}[^0-9]'), 1, 9)
        ELSE REGEXP_SUBSTR(message, '820-[0-9]{5}[^0-9]')
    END
    /* Grab all board numbers in 820-##### format from posts. This means 5 numbers,
       the fifth character NOT being a number, and the sixth character being
       removed so that the ) or , or . isn't in there as extra junk. */
) FROM xf_post)
UNION
(SELECT DISTINCT TRIM(
    CASE
        WHEN CHAR_LENGTH(REGEXP_SUBSTR(title, '820-[0-9]{5}[^0-9]')) = 10
        THEN SUBSTRING(REGEXP_SUBSTR(title, '820-[0-9]{5}[^0-9]'), 1, 9)
        ELSE REGEXP_SUBSTR(title, '820-[0-9]{5}[^0-9]')
    END
) FROM xf_thread)
/* Grab all board numbers in 820-##### format from titles */
INTO OUTFILE 'macbook_board_models.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n';
