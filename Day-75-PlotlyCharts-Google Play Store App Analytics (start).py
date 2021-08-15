"""Analyzing Google Play Store Apps & Reviews dataset

This 'script' analyzes a Google Play Store Apps dataset to answer questions such as:
    Are paid or free apps more highly reviewed and which kind has more installations?
    Which categories of apps are the most popular?
    Which categories of apps are the highest grossing?
    Should you choose a competitive category to release an app?
The results of the data analysis are plotted using Plotly to create pie charts, bar charts, scatter plots, and box plots.

This script requires that 'pandas' and 'Plotly' be installed within the Python
environment you are running this script in.

"""

#!/usr/bin/env python
# coding: utf-8

# # Introduction
# 
# In this notebook, we will do a comprehensive analysis of the Android app market by comparing thousands of apps in the Google Play store.

# # About the Dataset of Google Play Store Apps & Reviews

# **Data Source:** <br>
# App and review data was scraped from the Google Play Store by Lavanya Gupta in 2018. Original files listed [here](
# https://www.kaggle.com/lava18/google-play-store-apps).

# # Import Statements

# In[1]:


import pandas as pd
import plotly.express as px


# # Notebook Presentation

# In[2]:


# Show numeric output in decimal format e.g., 2.15
pd.options.display.float_format = '{:,.2f}'.format


# # Read the Dataset

# In[3]:


df_apps = pd.read_csv('day75-data/apps.csv')


# # Data Cleaning

# **Challenge**: How many rows and columns does `df_apps` have? What are the column names? Look at a random sample of 5 different rows with [.sample()](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.sample.html).

# In[4]:


df_apps.sample(5)


# In[5]:


df_apps.shape


# In[6]:


df_apps.columns


# ### Drop Unused Columns
# 
# **Challenge**: Remove the columns called `Last_Updated` and `Android_Version` from the DataFrame. We will not use these columns. 

# In[7]:


df_apps.drop(axis=1, labels=['Android_Ver', 'Last_Updated'], inplace=True)
df_apps.head(3)


# ### Find and Remove NaN values in Ratings
# 
# **Challenge**: How may rows have a NaN value (not-a-number) in the Ratings column? Create DataFrame called `df_apps_clean` that does not include these rows. 

# In[8]:


df_apps.isna().sum()


# In[9]:


df_apps_clean = df_apps.dropna()


# ### Find and Remove Duplicates
# 
# **Challenge**: Are there any duplicates in data? Check for duplicates using the [.duplicated()](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.duplicated.html) function. How many entries can you find for the "Instagram" app? Use [.drop_duplicates()](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.drop_duplicates.html) to remove any duplicates from `df_apps_clean`. 
# 

# In[10]:


df_apps_clean[df_apps_clean.duplicated('App')]


# In[11]:


df_apps_clean[df_apps_clean['App'] == 'Instagram']


# In[12]:


df_apps_clean.drop_duplicates('App', keep='first', inplace=True)


# In[13]:


df_apps_clean.shape


# In[14]:


df_apps_clean.head()


# # Find Highest Rated Apps
# 
# **Challenge**: Identify which apps are the highest rated. What problem might you encounter if you rely exclusively on ratings alone to determine the quality of an app?

# In[15]:


df_apps_clean[['App', 'Rating', 'Reviews']].sort_values('Rating', ascending=False).head()


# # Find 5 Largest Apps in terms of Size (MBs)
# 
# **Challenge**: What's the size in megabytes (MB) of the largest Android apps in the Google Play Store. Based on the data, do you think there could be limit in place or can developers make apps as large as they please? 

# In[16]:


df_apps_clean[['App', 'Size_MBs']].sort_values('Size_MBs', ascending=False).head()


# # Find the 5 App with Most Reviews
# 
# **Challenge**: Which apps have the highest number of reviews? Are there any paid apps among the top 50?

# In[17]:


maskdf = df_apps_clean[['App', 'Reviews', 'Type']].sort_values('Reviews', ascending=False).head(50)['Type'] == 'Paid'
df_apps_clean[['App', 'Reviews', 'Type']].sort_values('Reviews', ascending=False).head(50)[maskdf]


# # Plotly Pie and Donut Charts - Visualise Categorical Data: Content Ratings

# In[18]:


ratings = df_apps_clean['Content_Rating'].value_counts()


# In[19]:


ratings.head()


# In[ ]:





# In[20]:


fig = px.pie(labels=ratings.index, values=ratings.values)
fig.show()


# In[21]:


fig = px.pie(labels=ratings.index,
             values=ratings.values,
             title='Content Rating',
             names=ratings.index,
             hole=0.1
            )
fig.update_traces(
    textposition='outside',
    textinfo='percent+label'
)
fig.show()


# # Numeric Type Conversion: Examine the Number of Installs
# 
# **Challenge**: How many apps had over 1 billion (that's right - BILLION) installations? How many apps just had a single install? 
# 
# Check the datatype of the Installs column.
# 
# Count the number of apps at each level of installations. 
# 
# Convert the number of installations (the Installs column) to a numeric data type. Hint: this is a 2-step process. You'll have make sure you remove non-numeric characters first. 

# In[22]:


df_apps_clean.head()


# In[23]:


type(df_apps_clean['Installs'][21])


# In[24]:


df_apps_clean['Installs'].value_counts().sort_index()


# In[25]:


df_apps_clean['Installs'] = df_apps_clean['Installs'].str.replace(',', '')


# In[26]:


df_apps_clean['Installs'] = df_apps_clean['Installs'].astype('int')


# In[27]:


df_apps_clean.info()


# In[28]:


df_apps_clean['Installs'].value_counts().sort_index()


# # Find the Most Expensive Apps, Filter out the Junk, and Calculate a (ballpark) Sales Revenue Estimate
# 
# Let's examine the Price column more closely.
# 
# **Challenge**: Convert the price column to numeric data. Then investigate the top 20 most expensive apps in the dataset.
# 
# Remove all apps that cost more than $250 from the `df_apps_clean` DataFrame.
# 
# Add a column called 'Revenue_Estimate' to the DataFrame. This column should hold the price of the app times the number of installs. What are the top 10 highest grossing paid apps according to this estimate? Out of the top 10 highest grossing paid apps, how many are games?
# 

# In[29]:


df_apps_clean['Price'] = df_apps_clean['Price'].str.replace('$', '').astype('float')


# ### The most expensive apps sub $250

# In[30]:


df_apps_clean = df_apps_clean[df_apps_clean['Price'] < 250]


# ### Highest Grossing Paid Apps (ballpark estimate)

# In[31]:


df_apps_clean['Revenue_Estimate'] = df_apps_clean['Price'] * df_apps_clean['Installs']


# In[32]:


df_apps_clean.sort_values('Revenue_Estimate', ascending=False).head(10)


# # Plotly Bar Charts & Scatter Plots: Analysing App Categories

# In[33]:


df_apps_clean['Category'].nunique()


# In[34]:


df_apps_clean['Category'].value_counts()


# In[35]:


top10_category = df_apps_clean['Category'].value_counts()[:10]


# In[ ]:





# ### Vertical Bar Chart - Highest Competition (Number of Apps)

# In[36]:


px.bar(
    x=top10_category.index,
    y=top10_category.values
)


# ### Horizontal Bar Chart - Most Popular Categories (Highest Downloads)

# In[37]:


category_installs = df_apps_clean.groupby('Category').agg({'Installs':'sum'}).sort_values('Installs', ascending=False)[:15]
category_installs.values


# In[38]:


bar = px.bar(
    x=category_installs['Installs'],
    y=category_installs.index,
    orientation='h'
)
bar.update_layout(
    xaxis_title='Number of Downloads',
    yaxis_title='Category'
)
bar.show()


# ### Category Concentration - Downloads vs. Competition
# 
# **Challenge**: 
# * First, create a DataFrame that has the number of apps in one column and the number of installs in another:
# 
# <img src=https://imgur.com/uQRSlXi.png width="350">
# 
# * Then use the [plotly express examples from the documentation](https://plotly.com/python/line-and-scatter/) alongside the [.scatter() API reference](https://plotly.com/python-api-reference/generated/plotly.express.scatter.html)to create scatter plot that looks like this. 
# 
# <img src=https://imgur.com/cHsqh6a.png>
# 
# *Hint*: Use the size, hover_name and color parameters in .scatter(). To scale the yaxis, call .update_layout() and specify that the yaxis should be on a log-scale like so: yaxis=dict(type='log') 

# In[39]:


popular_categories = df_apps_clean.groupby('Category').agg({'Installs':'sum', 'App':'count'}).sort_values('App', ascending=False)


# In[40]:


scatter = px.scatter(
    x=popular_categories['App'],
    y=popular_categories['Installs'],
    log_y=True,
    size=popular_categories['App'],
    color=popular_categories.index,
    hover_name=popular_categories.index
)
scatter.update_layout(
    xaxis_title='Number of Apps (Lower=More Concentrated)',
    yaxis_title='Installs'
)
scatter.show()


# # Extracting Nested Data from a Column
# 
# **Challenge**: How many different types of genres are there? Can an app belong to more than one genre? Check what happens when you use .value_counts() on a column with nested values? See if you can work around this problem by using the .split() function and the DataFrame's [.stack() method](https://pandas.pydata.org/pandas-docs/stable/reference/api/pandas.DataFrame.stack.html). 
# 

# In[41]:


genres = df_apps_clean['Genres'].str.split(';', expand=True).stack().value_counts()


# # Colour Scales in Plotly Charts - Competition in Genres

# **Challenge**: Can you create this chart with the Series containing the genre data? 
# 
# <img src=https://imgur.com/DbcoQli.png width=400>
# 
# Try experimenting with the built in colour scales in Plotly. You can find a full list [here](https://plotly.com/python/builtin-colorscales/). 
# 
# * Find a way to set the colour scale using the color_continuous_scale parameter. 
# * Find a way to make the color axis disappear by using coloraxis_showscale. 

# In[42]:


bar = px.bar(
    x=genres.index,
    y=genres.values,
    color=genres.values,
    color_continuous_scale=['#0d0887', '#f0f921'],
)
bar.update_layout(
    xaxis_title='Genre',
    yaxis_title='Number of Apps'
)

bar.show()


# # Grouped Bar Charts: Free vs. Paid Apps per Category

# In[44]:


df_apps_clean['Type'].value_counts()


# In[74]:


df_free_vs_paid = df_apps_clean.groupby(['Category', 'Type'], as_index=False).count().sort_values('App', ascending=False)
df_free_vs_paid.head()


# **Challenge**: Use the plotly express bar [chart examples](https://plotly.com/python/bar-charts/#bar-chart-with-sorted-or-ordered-categories) and the [.bar() API reference](https://plotly.com/python-api-reference/generated/plotly.express.bar.html#plotly.express.bar) to create this bar chart: 
# 
# <img src=https://imgur.com/LE0XCxA.png>
# 
# You'll want to use the `df_free_vs_paid` DataFrame that you created above that has the total number of free and paid apps per category. 
# 
# See if you can figure out how to get the look above by changing the `categoryorder` to 'total descending' as outlined in the documentation here [here](https://plotly.com/python/categorical-axes/#automatically-sorting-categories-by-name-or-total-value). 

# In[86]:


df_free_vs_paid[df_free_vs_paid['Type']=='Paid'].count()


# In[110]:


bar = px.bar(
    data_frame=df_free_vs_paid,
    x='Category',
    y='App',
    barmode='group',
    color='Type',
    log_y=True
)

bar.update_layout(
    yaxis_title='Number of Apps',
    xaxis_title='Category',
    xaxis={'categoryorder':'total descending'}
)
bar.show()


# # Plotly Box Plots: Lost Downloads for Paid Apps
# 
# **Challenge**: Create a box plot that shows the number of Installs for free versus paid apps. How does the median number of installations compare? Is the difference large or small?
# 
# Use the [Box Plots Guide](https://plotly.com/python/box-plots/) and the [.box API reference](https://plotly.com/python-api-reference/generated/plotly.express.box.html) to create the following chart. 
# 
# <img src=https://imgur.com/uVsECT3.png>
# 

# In[119]:


df_apps_clean.head()


# In[126]:


px.box(df_apps_clean, x='Type', y='Installs', log_y=True, points='all', color='Type', title='How many Downloads are Paid Apps Giving Up?')


# # Plotly Box Plots: Revenue by App Category
# 
# **Challenge**: See if you can generate the chart below: 
# 
# <img src=https://imgur.com/v4CiNqX.png>
# 
# Looking at the hover text, how much does the median app earn in the Tools category? If developing an Android app costs $30,000 or thereabouts, does the average photography app recoup its development costs?
# 
# Hint: I've used 'min ascending' to sort the categories. 

# In[130]:


box = px.box(
    df_apps_clean[df_apps_clean['Type']=='Paid'],
    x='Category',
    y='Revenue_Estimate',
    log_y=True,
)

box.update_layout(
    yaxis_title='Paid App BallPark Revenue',
    xaxis={'categoryorder':'min ascending'}
)


# # How Much Can You Charge? Examine Paid App Pricing Strategies by Category
# 
# **Challenge**: What is the median price price for a paid app? Then compare pricing by category by creating another box plot. But this time examine the prices (instead of the revenue estimates) of the paid apps. I recommend using `{categoryorder':'max descending'}` to sort the categories.

# In[134]:


df_apps_clean[df_apps_clean['Type'] == 'Paid']['Price'].describe()


# In[143]:


box = px.box(
    df_apps_clean[df_apps_clean['Type']=='Paid'],
    x='Category',
    y='Price',
    log_y=True,
    title='Price per paid app'
)

box.update_layout(
    xaxis={'categoryorder':'max descending'}
)


# In[ ]:




