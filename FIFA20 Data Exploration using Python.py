#!/usr/bin/env python
# coding: utf-8

# # WELCOME TO THE NOTEBOOK
# ------------------------------
# ## Task 1
# 
# ### Importing the modules

# In[1]:


import numpy as np 
import pandas as pd 
import plotly.graph_objects as go
import plotly.express as px
import plotly
import re
print('modules are imported')


# ### let's load the fifa 2020 dataset

# In[41]:


df_20 = pd.read_csv('C:/Users/Scoby/Desktop/FIFA20 project dataset/players_20.csv', error_bad_lines=False)


# let's check the dataset

# In[42]:


df_20.head()


# checking how many rows and columns we have

# In[43]:


df_20.shape


# let's check the columns

# In[44]:


cols = list(df_20.columns)
print(cols)


# ## Task 2:
# ### Data Preprocessin
# Dropping some useless columns

# In[45]:


useless_columns = ['dob','sofifa_id', 'player_url', 'long_name', 'body_type', 'real_face', 'loaned_from', 'nation_position', 'nation_jersey_number']


# Let's check the dataframe again

# In[46]:


df_20 = df_20.drop(useless_columns,axis=1)


# In[47]:


df_20.head()


# ### Calculating BMI 
# let's calculate body max index of each Player 

# In[48]:


df_20['BMI'] = df_20['weight_kg']/(df_20['height_cm']/100)**2


# In[49]:


df_20.head()


# ### Player's Position 
# Convert the categorical values in Player's Position column in integer values.

# In[50]:


df_20[['short_name','player_positions']]


# let's convert the column to integeral columns

# In[51]:


new_player_positions = df_20['player_positions'].str.get_dummies(sep = ', ').add_prefix('Position_')
new_player_positions.head()


# concatinating new_player_position dataframe to our dataframe

# In[52]:


df_20 = pd.concat([df_20, new_player_positions] , axis = 1)


# let's check the dataset again

# In[53]:


df_20.head()


# let's drop the original player_positions columns

# In[55]:


df_20 = df_20.drop('player_positions', axis=1)


# let's check the dataset again

# In[56]:


df_20.head()


# ## Task 3:
# ### Position Columns ratings
# Clean, Process and Assign the new attributes to columns listed below.

# In[61]:


columns = ['ls', 'st', 'rs', 'lw', 'lf', 'cf', 'rf', 'rw', 'lam', 'cam', 'ram',
       'lm', 'lcm', 'cm', 'rcm', 'rm', 'lwb', 'ldm', 'cdm', 'rdm', 'rwb', 'lb',
       'lcb', 'cb', 'rcb', 'rb']


# let's check what we have in these columns

# In[62]:


df_20[columns].head()


# let's omit the '+' sign

# In[64]:


for col in columns:
    df_20 [col] = df_20[col].str.split('+', n = 1, expand=True)[0]
df_20[columns]


# Let's Replace NaN values with 0 

# In[66]:


df_20[columns] = df_20[columns].fillna(0)


# Let's convert the columns to int 

# In[67]:


df_20[columns] = df_20[columns].astype(int)


# Checking the dataframe again

# In[70]:


df_20[columns].head()


# ### Filling Missing Values
# Let's fill <b>"dribbling", "defending", "physic", "passing", "shooting" and "pace" </b> missing values of these columns by median
# 

# In[72]:


columns = ["dribbling", "defending", "physic", "passing", "shooting", "pace"]
df_20[columns]


# At first let's check how many NaN values are there in these columuns

# In[73]:


df_20[columns].isnull().sum()


# now lets fill the NaN values with the median of the respective column

# In[76]:


for col in columns:
    df_20[col] = df_20[col].fillna(df_20[col].median())
df_20[columns]


# let's fill all NaN values in the dataframe with 0

# In[78]:


df_20 = df_20.fillna(0)


# let's count the NaN values again 

# In[79]:


df_20.isnull().sum()


# ## Task 4:
# ## Exploratory Data Analysis
# 
# #### 1- Scatter Plot (colored by Age) year 2020 - Overall Rating vs Value in Euros 

# In[83]:


fig = go.Figure(
data = go.Scatter(
    x= df_20['overall'],
    y= df_20['value_eur'],
    mode = 'markers',
    marker = dict(
    size = 10,
    color = df_20['age'],
    showscale = True
    ),
    text = df_20['short_name']

)

)

fig.update_layout(title='Scatter Plot (colored by age)year 2020 = overal ratings vs value in Euros'
                 , xaxis_title = 'Overall Rating',
                 yaxis_title = 'Value in Euros')

fig.show()


# #### 2- Pie chart proportion of right-foot players vs left-foot players

# In[85]:


fig = px.pie(df_20, names = 'preferred_foot', title = 'Percentage of plyers by preferred foot')
fig.show()


# #### 3- Histogram of Players Ages 

# In[86]:


fig = px.histogram(df_20, x = 'age', title = 'Histogram of Players Ages')
fig.show()


# #### 4- Scatterpolar plot to compare a player's grothw over time
# let's load the other datasets players from 2016 to 2019

# In[88]:


df_16 = pd.read_csv('C:/Users/Scoby/Desktop/FIFA20 project dataset/players_16.csv', error_bad_lines=False)
df_17 = pd.read_csv('C:/Users/Scoby/Desktop/FIFA20 project dataset/players_17.csv', error_bad_lines=False)
df_18 = pd.read_csv('C:/Users/Scoby/Desktop/FIFA20 project dataset/players_18.csv', error_bad_lines=False)
df_19 = pd.read_csv('C:/Users/Scoby/Desktop/FIFA20 project dataset/players_19.csv', error_bad_lines=False)


# player attributes column names

# In[89]:


attributes = ['Pace','Shooting','Passing','Dribbling','Defending','Physic','Overall'] 


# Creating a method to compare a Players growth over Time

# In[94]:


def player_growth(name):
    data20 = df_20[df_20.short_name.str.startswith(name)]
    data19 = df_19[df_19.short_name.str.startswith(name)]
    data18 = df_18[df_18.short_name.str.startswith(name)]
    data17 = df_17[df_17.short_name.str.startswith(name)]
    data16 = df_16[df_16.short_name.str.startswith(name)]

    attributes = ['pace', 'shooting', 'passing', 'dribbling', 'defending', 'physic', 'overall']

    trace0 = go.Scatterpolar(
        r=[data20['pace'].values[0], data20['shooting'].values[0], data20['passing'].values[0],
           data20['dribbling'].values[0], data20['defending'].values[0], data20['physic'].values[0],
           data20['overall'].values[0]],
        theta=attributes,
        fill='toself',
        name='2020'
    )

    trace1 = go.Scatterpolar(
        r=[data19['pace'].values[0], data19['shooting'].values[0], data19['passing'].values[0],
           data19['dribbling'].values[0], data19['defending'].values[0], data19['physic'].values[0],
           data19['overall'].values[0]],
        theta=attributes,
        fill='toself',
        name='2019'
    )

    trace2 = go.Scatterpolar(
        r=[data18['pace'].values[0], data18['shooting'].values[0], data18['passing'].values[0],
           data18['dribbling'].values[0], data18['defending'].values[0], data18['physic'].values[0],
           data18['overall'].values[0]],
        theta=attributes,
        fill='toself',
        name='2018'
    )

    trace3 = go.Scatterpolar(
        r=[data17['pace'].values[0], data17['shooting'].values[0], data17['passing'].values[0],
           data17['dribbling'].values[0], data17['defending'].values[0], data17['physic'].values[0],
           data17['overall'].values[0]],
        theta=attributes,
        fill='toself',
        name='2017'
    )

    trace4 = go.Scatterpolar(
        r=[data16['pace'].values[0], data16['shooting'].values[0], data16['passing'].values[0],
           data16['dribbling'].values[0], data16['defending'].values[0], data16['physic'].values[0],
           data16['overall'].values[0]],
        theta=attributes,
        fill='toself',
        name='2016'
    )

    data = [trace0, trace1, trace2, trace3, trace4]
    layout = go.Layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )
        ),
        showlegend=True,
        title='Stats related to {} from 2016'.format(name)
    )

    fig = go.Figure(data=data, layout=layout)
    fig.show()
                            


# Let's check the growth of Neymar over time 

# In[95]:


player_growth('Neymar')


# what about cristiano Ronaldo

# In[96]:


player_growth('Cristiano Ronaldo')


# ## Task 5:
# #### 6- Pie chart Describing the Percentage of Players in different Attacker positions

# In[101]:


attack = ['RW', 'LW', 'ST', 'CF', 'LS', 'RS', 'RF', 'LF']

sample = df_20.query('team_position in @attack')
fig = px.pie(sample, names = 'team_position', color_discrete_sequence= px.colors.sequential.Magma_r,
            title = 'Percentage of Players in different Attacker positions')
fig.show()


# #### 7- Pie chart Describing the Percentage of Players in different Midfielder positions

# In[100]:


mid = ['CAM', 'RCM', 'CDM', 'LDM', 'RM', 'LCM', 'LM', 'RDM', 'RAM','CM', 'LAM']
sample = df_20.query('team_position in @mid')
fig = px.pie(sample, names = 'team_position', color_discrete_sequence= px.colors.sequential.Magma_r,
            title = 'Percentage of Players in different Mid positions')
fig.show()


# #### 8- Pie chart Describing the Percentage of Players in different Defender positions

# In[102]:


defence = ['LCB', 'RCB', 'LB', 'RB', 'CB', 'RWB', 'LWB']
sample = df_20.query('team_position in @defence')
fig = px.pie(sample, names = 'team_position', color_discrete_sequence= px.colors.sequential.Magma_r,
            title = 'Percentage of Players in different Def positions')
fig.show()


# ### Pick Top 5 Players per Position
# Creating a method to pick top 5 player based on a the player position and the player value in euro

# In[105]:


def pick_top_players(pos, value):
    column = str('Position_')+str.upper(pos)
    target_players = df_20[(df_20[column] == 1) & (df_20['value_eur'] <= value)][['short_name', 'age','overall'
                                                                                    ,'value_eur']].head(5)
    return target_players                                                   


# In[108]:


#top5 left back within 34 mil Euros budget
pick_top_players('lb',34000000)


# In[109]:


#top5 Strikers within 55 mil Euros budget
pick_top_players('st',55000000)

