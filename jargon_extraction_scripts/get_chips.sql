/* Grab all chips from forum */

(SELECT DISTINCT TRIM(
    CASE
        WHEN CHAR_LENGTH(REGEXP_SUBSTR(message, '[Ii][Ss][Ll][0-9]{4}[^0-9a-zA-Z]')) = 8
        THEN SUBSTRING(REGEXP_SUBSTR(message, '[Ii][Ss][Ll][0-9]{4}[^0-9a-zA-Z]'), 1, 7)
        ELSE REGEXP_SUBSTR(message, '[Ii][Ss][Ll][0-9]{4}[^0-9a-zA-Z]')
    END
    /* Grab all chips in ISL-#### format from posts meaning intersil chips,
    as in ISL6259. This means four numbers, the fifth character NOT being
    a number, and the fifth character being removed so that the ) or , or .
    isn't in there as extra junk. */
) FROM xf_post)
UNION
(SELECT DISTINCT TRIM(
    CASE
        WHEN CHAR_LENGTH(REGEXP_SUBSTR(title, '[Ii][Ss][Ll][0-9]{4}[^0-9a-zA-Z]')) = 8
        THEN SUBSTRING(REGEXP_SUBSTR(title, '[Ii][Ss][Ll][0-9]{4}[^0-9a-zA-Z]'), 1, 7)
        ELSE REGEXP_SUBSTR(title, '[Ii][Ss][Ll][0-9]{4}[^0-9a-zA-Z]')
    END
) FROM xf_thread)
/* Grab all chips in ISL-#### format from titles meaning intersil chips*/
UNION

(SELECT DISTINCT TRIM(
    CASE
        WHEN CHAR_LENGTH(REGEXP_SUBSTR(message, '[Ll][Pp][0-9]{4}[^0-9a-zA-Z]')) = 7
        THEN SUBSTRING(REGEXP_SUBSTR(message, '[Ll][Pp][0-9]{4}[^0-9a-zA-Z]'), 1, 6)
        ELSE REGEXP_SUBSTR(message, '[Ll][Pp][0-9]{4}[^0-9a-zA-Z]')
    END
    /* Grab all chips in LP-#### format from posts meaning TI chips,
    as in LP8550. This means four numbers, the fifth character NOT being
    a number, and the fifth character being removed so that the ) or , or .
    isn't in there as extra junk. */
) FROM xf_post)
UNION
(SELECT DISTINCT TRIM(
    CASE
        WHEN CHAR_LENGTH(REGEXP_SUBSTR(title, '[Ll][Pp][0-9]{4}[^0-9a-zA-Z]')) = 7
        THEN SUBSTRING(REGEXP_SUBSTR(title, '[Ll][Pp][0-9]{4}[^0-9a-zA-Z]'), 1, 6)
        ELSE REGEXP_SUBSTR(title, '[Ll][Pp][0-9]{4}[^0-9a-zA-Z]')
    END
) FROM xf_thread)
/* Grab all chips in LP-#### format from titles meaning TI chips*/
UNION
(SELECT DISTINCT TRIM(
    CASE
        WHEN CHAR_LENGTH(REGEXP_SUBSTR(message, '[Cc][Dd][0-9]{4}[^0-9a-zA-Z]')) = 7
        THEN SUBSTRING(REGEXP_SUBSTR(message, '[Cc][Dd][0-9]{4}[^0-9a-zA-Z]'), 1, 6)
        ELSE REGEXP_SUBSTR(message, '[Cc][Dd][0-9]{4}[^0-9a-zA-Z]')
    END
    /* Grab all chips in CD-#### format from posts meaning TI chips,
    as in CD3215. This means four numbers, the fifth character NOT being
    a number, and the fifth character being removed so that the ) or , or .
    isn't in there as extra junk. */
) FROM xf_post)
UNION
(SELECT DISTINCT TRIM(
    CASE
        WHEN CHAR_LENGTH(REGEXP_SUBSTR(title, '[Cc][Dd][0-9]{4}[^0-9a-zA-Z]')) = 7
        THEN SUBSTRING(REGEXP_SUBSTR(title, '[Cc][Dd][0-9]{4}[^0-9a-zA-Z]'), 1, 6)
        ELSE REGEXP_SUBSTR(title, '[Cc][Dd][0-9]{4}[^0-9a-zA-Z]')
    END
) FROM xf_thread)
/* Grab all chips in CD-#### format from titles meaning TI chips*/
UNION
(SELECT DISTINCT TRIM(
    CASE
        WHEN CHAR_LENGTH(REGEXP_SUBSTR(message, '[Ii][Ss][Ll][0-9]{5}[^0-9a-zA-Z]')) = 9
        THEN SUBSTRING(REGEXP_SUBSTR(message, '[Ii][Ss][Ll][0-9]{5}[^0-9a-zA-Z]'), 1, 8)
        ELSE REGEXP_SUBSTR(message, '[Ii][Ss][Ll][0-9]{5}[^0-9a-zA-Z]')
    END
    /* Grab all chips in ISL-##### format from posts meaning intersil chips,
    as in ISL95870. This means four numbers, the fifth character NOT being
    a number, and the fifth character being removed so that the ) or , or .
    isn't in there as extra junk. */
) FROM xf_post)
UNION
(SELECT DISTINCT TRIM(
    CASE
       WHEN CHAR_LENGTH(REGEXP_SUBSTR(title, '[Ii][Ss][Ll][0-9]{5}[^0-9a-zA-Z]')) = 9
        THEN SUBSTRING(REGEXP_SUBSTR(title, '[Ii][Ss][Ll][0-9]{5}[^0-9a-zA-Z]'), 1, 8)
        ELSE REGEXP_SUBSTR(title, '[Ii][Ss][Ll][0-9]{5}[^0-9a-zA-Z]')
    END
) FROM xf_thread)
/* Grab all chips in ISL-##### format from titles*/
UNION
(SELECT DISTINCT TRIM(
    CASE
        WHEN CHAR_LENGTH(REGEXP_SUBSTR(message, '[Tt][Pp][Ss][0-9]{5}[^0-9a-zA-Z]')) = 9
        THEN SUBSTRING(REGEXP_SUBSTR(message, '[Tt][Pp][Ss][0-9]{5}[^0-9a-zA-Z]'), 1, 8)
        ELSE REGEXP_SUBSTR(message, '[Tt][Pp][Ss][0-9]{5}[^0-9a-zA-Z]')
    END
    /* Grab all chips in TPS-##### format from posts meaning TI chips,
    as in ISL95870. This means four numbers, the fifth character NOT being
    a number, and the fifth character being removed so that the ) or , or .
    isn't in there as extra junk. */
) FROM xf_post)
UNION
(SELECT DISTINCT TRIM(
    CASE
       WHEN CHAR_LENGTH(REGEXP_SUBSTR(title, '[Tt][Pp][Ss][0-9]{5}[^0-9a-zA-Z]')) = 9
        THEN SUBSTRING(REGEXP_SUBSTR(title, '[Tt][Pp][Ss][0-9]{5}[^0-9a-zA-Z]'), 1, 8)
        ELSE REGEXP_SUBSTR(title, '[Tt][Pp][Ss][0-9]{5}[^0-9a-zA-Z]')
    END
) FROM xf_thread)
/* Grab all chips in TPS-##### format from titles*/
UNION
(SELECT DISTINCT TRIM(
    CASE
        WHEN CHAR_LENGTH(REGEXP_SUBSTR(message, '[Uu][0-9]{4}[^0-9]')) = 5
        THEN SUBSTRING(REGEXP_SUBSTR(message, '[Uu][0-9]{4}[^0-9]'), 1, 5)
        ELSE REGEXP_SUBSTR(message, '[Uu][0-9]{4}')
    END
    /* Grab all chips U#### format from posts. This means 'U' (upper or lower case)
       followed by four numbers. Any junk character after the pattern is removed. */
) FROM xf_post)
UNION
(SELECT DISTINCT TRIM(
    CASE
        WHEN CHAR_LENGTH(REGEXP_SUBSTR(title, '[Uu][0-9]{4}[^0-9]')) = 5
        THEN SUBSTRING(REGEXP_SUBSTR(title, '[Uu][0-9]{4}[^0-9]'), 1, 5)
        ELSE REGEXP_SUBSTR(title, '[Uu][0-9]{4}')
    END
    /* Grab all chips U#### format from thread titles. This means 'U' (upper or lower case)
       followed by four numbers. Any junk character after the pattern is removed. */
) FROM xf_thread)
INTO OUTFILE 'chips.csv'
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n';
