import praw
import configparser
import sys
import re

# set up reddit connection
config = configparser.ConfigParser()
config.read('/home/jmyslinski/JOHNS_CONFIG_FILE_NO_TOUCH/config.John')
reddit = praw.Reddit(
        user_agent = config['REDDIT_API']['user_agent'],
        client_id = config['REDDIT_API']['client_id'],
        client_secret = config['REDDIT_API']['client_secret']
)

# handling arguments
assert len(sys.argv) == 4
url_id = sys.argv[1]
drink_name = sys.argv[2]
drink_category = sys.argv[3]

# hard coding arguments for testing purposes
url_id = 'knej2c'
drink_name = 'Oazacan Dead'
drink_category = 'Tiki'

# grabbing comment text
submission = reddit.submission(id = url_id)
for top_level_comment in submission.comments:
    if submission.author == top_level_comment.author:
        recipe = top_level_comment.body

# parser
end_words = {'tequila', 'rum', 'velvet falernum', 'mezcal', 'juice', 'syrup', 'grenadine', 'bitters'}
end_words_str = '|'.join(end_words)

measure_words = {'oz', 'tsp', 'dash'}
measure_words_str = '|'.join(measure_words)

regex_str = r'([0-9]|[0-9]\/[0-9])(.+)(' + measure_words_str + r')(.+)(' + end_words_str + r')'
recipe_parsed = re.findall(regex_str, recipe)
print(recipe_parsed)
print('-----------------')

# clean up regex results. maybe if regex didn't give me migraines I could make the regex do this.
recipe_final = []
for tup in recipe_parsed:
    # clean up regex results
    ls = [x.strip() for x in tup if x != ' ']

    # FRACTIONS
    if ls[1] not in measure_words:
        ls[0] = ls[0] + ls.pop(1)
    
    # deque would be faster?
    recipe_final.append(ls)

print(recipe_final)

