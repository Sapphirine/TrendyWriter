-- =================================================================================================
--                                  Find trending topic tool
-- =================================================================================================
--                      [USAGE] $ {pig} -x local -f topics_analysis.pig
-- -------------------------------------------------------------------------------------------------



-- Load data from local path into a table, which contains each line of the files(each topic).
-- Column name: line; Column type: chararray;
topics = LOAD '/Users/Marcus/Documents/PycharmProjects/TrendyWrite_api/topic/all_topics.txt' AS (line:chararray);
-- or [ $ topics = LOAD '/Users/Marcus/Desktop/all_topics.txt' ] , which provide the same result

-- Flatten each line(bag) into a collection words, which results in a bigger collection of words. 
words = FOREACH topics GENERATE FLATTEN(TOKENIZE(line)) AS word;
-- or [ $ words = FOREACH topics GENERATE FLATTEN(TOKENIZE((chararray)$0)) AS word; ] , which provide the same result  

-- Filter out empty words (just in case).
filtered_words = FILTER words BY word MATCHES '\\w+';

-- Create a group for each word, so that same words will group together.
word_groups = GROUP filtered_words BY word;

-- Count the entries in each group.
word_count = FOREACH word_groups GENERATE group AS word, COUNT(filtered_words) AS count;

-- Generate a new table which has three columns: word, word_len, count.
ordered_word_count_w_len = FOREACH word_count GENERATE word, SIZE(word) AS word_len, count;

-- Order the records by word_len in order to filter stop words.
ordered_word_len_w_count = ORDER ordered_word_count_w_len BY word_len;

-- Filter stop words (approximately).
filter_stopwords = FILTER ordered_word_count_w_len BY (int)word_len > 4;

-- Generate a new table which has two columns: word, count.
word_count2 = FOREACH filter_stopwords GENERATE word, count;

-- Order the records by count in order to filter unwanted words.
ordered_word_count2 = ORDER word_count2 BY count DESC;

-- Filter unwanted words.
filter_lesscountwords = FILTER ordered_word_count2 BY (int)count > 8;

-- Show current data.
DUMP filter_lesscountwords;

-- Store current data
STORE filter_lesscountwords INTO '/Users/Marcus/Documents/PycharmProjects/TrendyWrite_api/pig/trending_singleword';
