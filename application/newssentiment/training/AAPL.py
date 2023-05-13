#!/usr/bin/env python
# coding: utf-8

# In[50]:


import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


# ## Sentiment

# In[51]:


sentiment = pd.read_csv("AAPL-sentiment.csv", parse_dates=['date'])


# In[52]:


sentiment.describe()


# In[53]:


sentiment.head()


# In[54]:


plt.hist(sentiment.ts_polarity)
plt.show()


# ## Stock

# In[55]:


stock = pd.read_csv("AAPL-stock.csv", parse_dates=['date'])


# In[56]:


stock.head()


# ## Merge data

# In[57]:


df = pd.merge(sentiment, stock, how='inner', on='date')


# In[58]:


df.head()


# In[59]:


df.tail()


# In[60]:


plt.plot(df.date, df.close)
plt.gcf().autofmt_xdate()
plt.show()


# In[61]:


df.corr(numeric_only=True)


# ## Model

# In[62]:


def window_data(df, window, feature_cols: tuple[str], target_col):
    X_feat = [[] for _ in feature_cols]

    y = []
    for i in range(len(df) - window):
        for feat_id, feature_col_name in enumerate(feature_cols):
            feat_value = df.iloc[i:(i + window), df.columns.get_loc(feature_col_name)]
            X_feat[feat_id].append(feat_value)

        target = df.iloc[(i + window), df.columns.get_loc(target_col)] # j + 1
        y.append(target)
        
    return np.hstack(X_feat), np.array(y).reshape(-1, 1)


# In[63]:


# Predict j+1 target using a "window_size"-day window of previous closing prices
window_size = 1

X, y = window_data(df, window_size, ("ts_polarity", "twitter_volume", "close"), "close")


# We take the features of n days to make a prediction at j + 1 after those n days

# In[64]:


df.head()


# ```
# So for 3 days we have X[0] = [ts_polarity[0], ts_polarity[1], ts_polarity[2],
#                               twitter_vol[0], twitter_vol[1], twitter_vol[2],
#                               ...
#                               close[0], close[1], close[2]]
# 
# And y[0] = close[3]
# ```

# In[65]:


X[0]


# In[66]:


y[0]


# ### Training

# In[67]:


from sklearn.model_selection import train_test_split

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.33, random_state=0, shuffle=False)


# In[68]:


from sklearn.preprocessing import MinMaxScaler

# Use the MinMaxScaler to scale data between 0 and 1.
x_train_scaler = MinMaxScaler()
x_test_scaler = MinMaxScaler()
y_train_scaler = MinMaxScaler()
y_test_scaler = MinMaxScaler()

# Fit the scaler for the Training Data
x_train_scaler.fit(X_train)
y_train_scaler.fit(y_train)

# Scale the training data
X_train = x_train_scaler.transform(X_train)
y_train = y_train_scaler.transform(y_train)

# Fit the scaler for the Testing Data
x_test_scaler.fit(X_test)
y_test_scaler.fit(y_test)

# Scale the y_test data
X_test = x_test_scaler.transform(X_test)
y_test = y_test_scaler.transform(y_test)


# In[69]:


from xgboost import XGBRegressor

# Create the XG Boost regressor instance
model = XGBRegressor(objective='reg:squarederror', n_estimators=1000)


# In[70]:


model.fit(X_train, y_train)


# ## Performance

# In[71]:


from sklearn import metrics


# In[72]:


# Make some predictions
predicted = model.predict(X_test)


# In[73]:


# Evaluating the model
print('Root Mean Squared Error:', np.sqrt(metrics.mean_squared_error(y_test, predicted)))
print('R-squared :', metrics.r2_score(y_test, predicted))


# In[74]:


# Recover the original prices instead of the scaled version
predicted_prices = y_train_scaler.inverse_transform(predicted.reshape(-1, 1))
real_prices = y_train_scaler.inverse_transform(y_test.reshape(-1, 1))


# In[75]:


# Create a DataFrame of Real and Predicted values
stocks = pd.DataFrame({
    "Real": real_prices.ravel(),
    "Predicted": predicted_prices.ravel()
}, index = df.index[-len(real_prices): ]) 
stocks.head()


# In[76]:


# Plot the real vs predicted values as a line chart
#plt.plot(y_train, label="Train")
plt.plot(stocks.Real, label="Real")
plt.plot(stocks.Predicted, label="Predicted")
plt.xlabel("Day")
plt.ylabel("Price")
plt.legend()
plt.show()


# ## Export model

# In[77]:


import joblib


# In[78]:


joblib.dump(model, 'stock_prediction.joblib')
joblib.dump(y_train_scaler, 'stock_prediction_y_scaler.joblib')
joblib.dump(x_train_scaler, 'stock_prediction_x_scaler.joblib')

