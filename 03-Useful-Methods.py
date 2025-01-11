#!/usr/bin/env python
# coding: utf-8

# ___
# 
# <a href='http://www.pieriandata.com'><img src='../Pierian_Data_Logo.png'/></a>
# ___
# <center><em>Copyright by Pierian Data Inc.</em></center>
# <center><em>For more information, visit us at <a href='http://www.pieriandata.com'>www.pieriandata.com</a></em></center>

# # Useful Methods
# 
# Let's cover some useful methods and functions built in to pandas. This is actually just a small sampling of the functions and methods available in Pandas, but they are some of the most commonly used.
# The [documentation](https://pandas.pydata.org/pandas-docs/stable/reference/index.html) is a great resource to continue exploring more methods and functions (we will introduce more further along in the course).
# Here is a list of functions and methods we'll cover here (click on one to jump to that section in this notebook.):
# 
# * [apply() method](#apply_method)
# * [apply() with a function](#apply_function)
# * [apply() with a lambda expression](#apply_lambda)
# * [apply() on multiple columns](#apply_multiple)
# * [describe()](#describe)
# * [sort_values()](#sort)
# * [corr()](#corr)
# * [idxmin and idxmax](#idx)
# * [value_counts](#v_c)
# * [replace](#replace)
# * [unique and nunique](#uni)
# * [map](#map)
# * [duplicated and drop_duplicates](#dup)
# * [between](#bet)
# * [sample](#sample)
# * [nlargest](#n)
# 
# Make sure to view the video lessons to get the full explanation!

# <a id='apply_method'></a>
# 
# ## The .apply() method
# 
# Here we will learn about a very useful method known as **apply** on a DataFrame. This allows us to apply and broadcast custom functions on a DataFrame column

# In[1]:


import pandas as pd
import numpy as np


# In[2]:


df = pd.read_csv('tips.csv')


# In[3]:


df.head()


# <a id='apply_function'></a>
# ### apply with a function

# In[4]:


df.info()


# In[5]:


def last_four(num):
    return str(num)[-4:]


# In[6]:


df['CC Number'][0]


# In[7]:


last_four(3560325168603410)


# In[8]:


df['last_four'] = df['CC Number'].apply(last_four)


# In[9]:


df.head()


# ### Using .apply() with more complex functions

# In[10]:


df['total_bill'].mean()


# In[11]:


def yelp(price):
    if price < 10:
        return '$'
    elif price >= 10 and price < 30:
        return '$$'
    else:
        return '$$$'


# In[12]:


df['Expensive'] = df['total_bill'].apply(yelp)


# In[13]:


# df


# <a id='apply_lambda'></a>
# ### apply with lambda

# In[14]:


def simple(num):
    return num*2


# In[15]:


lambda num: num*2


# In[16]:


df['total_bill'].apply(lambda bill:bill*0.18)


# <a id='apply_multiple'></a>
# ## apply that uses multiple columns
# 
# Note, there are several ways to do this:
# 
# https://stackoverflow.com/questions/19914937/applying-function-with-multiple-arguments-to-create-a-new-pandas-column

# In[17]:


df.head()


# In[18]:


def quality(total_bill,tip):
    if tip/total_bill  > 0.25:
        return "Generous"
    else:
        return "Other"


# In[19]:


df['Tip Quality'] = df[['total_bill','tip']].apply(lambda df: quality(df['total_bill'],df['tip']),axis=1)


# In[20]:


df.head()


# In[21]:


import numpy as np


# In[22]:


df['Tip Quality'] = np.vectorize(quality)(df['total_bill'], df['tip'])


# In[23]:


df.head()


# So, which one is faster?

# In[24]:


import timeit 
  
# code snippet to be executed only once 
setup = '''
import numpy as np
import pandas as pd
df = pd.read_csv('tips.csv')
def quality(total_bill,tip):
    if tip/total_bill  > 0.25:
        return "Generous"
    else:
        return "Other"
'''
  
# code snippet whose execution time is to be measured 
stmt_one = ''' 
df['Tip Quality'] = df[['total_bill','tip']].apply(lambda df: quality(df['total_bill'],df['tip']),axis=1)
'''

stmt_two = '''
df['Tip Quality'] = np.vectorize(quality)(df['total_bill'], df['tip'])
'''
  


# In[25]:


timeit.timeit(setup = setup, 
                    stmt = stmt_one, 
                    number = 1000) 


# In[26]:


timeit.timeit(setup = setup, 
                    stmt = stmt_two, 
                    number = 1000) 


# Wow! Vectorization is much faster! Keep **np.vectorize()** in mind for the future.
# 
# Full Details:
# https://docs.scipy.org/doc/numpy/reference/generated/numpy.vectorize.html

# <a id='describe'></a>
# ### df.describe for statistical summaries

# In[27]:


df.describe()


# In[28]:


df.describe().transpose()


# <a id='sort'></a>
# ### sort_values()

# In[29]:


df.sort_values('tip')


# In[31]:


# Helpful if you want to reorder after a sort
# https://stackoverflow.com/questions/13148429/how-to-change-the-order-of-dataframe-columns
df.sort_values(['tip','size'])


# <a id='corr'></a>
# ## df.corr() for correlation checks
# 
# [Wikipedia on Correlation](https://en.wikipedia.org/wiki/Correlation_and_dependence)

# In[29]:


df.corr()


# In[30]:


df[['total_bill','tip']].corr()


# <a id='idx'></a>
# ### idxmin and idxmax

# In[31]:


df.head()


# In[32]:


df['total_bill'].max()


# In[33]:


df['total_bill'].idxmax()


# In[34]:


df['total_bill'].idxmin()


# In[35]:


df.iloc[67]


# In[36]:


df.iloc[170]


# <a id='v_c'></a>
# ### value_counts
# 
# Nice method to quickly get a count per category. Only makes sense on categorical columns.

# In[37]:


df.head()


# In[38]:


df['sex'].value_counts()


# <a id='replace'></a>
# 
# ### replace
# 
# Quickly replace values with another one.

# In[39]:


df.head()


# In[40]:


df['Tip Quality'].replace(to_replace='Other',value='Ok')


# In[41]:


df['Tip Quality'] = df['Tip Quality'].replace(to_replace='Other',value='Ok')


# In[42]:


df.head()


# <a id='uni'></a>
# ### unique

# In[59]:


df['size'].unique()


# In[60]:


df['size'].nunique()


# In[57]:


df['time'].unique()


# <a id='map'></a>
# ### map

# In[45]:


my_map = {'Dinner':'D','Lunch':'L'}


# In[46]:


df['time'].map(my_map)


# In[48]:


df.head()


# <a id='dup'></a>
# ## Duplicates
# 
# ### .duplicated() and .drop_duplicates()

# In[50]:


# Returns True for the 1st instance of a duplicated row
df.duplicated()


# In[51]:


simple_df = pd.DataFrame([1,2,2],['a','b','c'])


# In[52]:


simple_df


# In[53]:


simple_df.duplicated()


# In[54]:


simple_df.drop_duplicates()


# <a id='bet'></a>
# ## between
# 
# left: A scalar value that defines the left boundary
# right: A scalar value that defines the right boundary
# inclusive: A Boolean value which is True by default. If False, it excludes the two passed arguments while checking.

# In[64]:


df['total_bill'].between(10,20,inclusive=True)


# In[65]:


df[df['total_bill'].between(10,20,inclusive=True)]


# <a id='sample'></a>
# ## sample

# In[68]:


df.sample(5)


# In[69]:


df.sample(frac=0.1)


# <a id='n'></a>
# ## nlargest and nsmallest

# In[71]:


df.nlargest(10,'tip')


# ----
