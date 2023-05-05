import pandas as pd
import time

start_time = time.time()
# Load the data into Pandas dataframes
users = pd.read_csv("users.csv")
aliases = pd.read_csv("alias.csv")
events = pd.read_csv("events.csv")

# Define a function to recursively follow the aliases and return the final user ID
resolved_cache = {}
def resolve_alias(user_id):
    if user_id in resolved_cache:
        return resolved_cache[user_id]
    else:
        alias_row = aliases.loc[aliases['alias_user_id'] == user_id]
        if alias_row.empty:
            resolved_cache[user_id] = user_id
            return user_id
        else:
            resolved_id = resolve_alias(alias_row.iloc[0]['user_id'])
            resolved_cache[user_id] = resolved_id
            return resolved_id

# # Apply the resolve_alias function to the user IDs in the events table to get the final user IDs
events['user_id'] = events['user_id'].apply(resolve_alias)

# Compute the count of unique users for each feature key and variation using the transform method
events['user_count'] = events.groupby(['feature_key', 'feature_value'])['user_id'].transform('nunique')

# Drop duplicate rows and keep only the relevant columns
summary = events[['feature_key', 'feature_value', 'user_count']].drop_duplicates()

print (summary)

# output to file
summary.to_csv('output.csv')
 

