# import pandas as pd
# import numpy as np
# import seaborn as sns
# import matplotlib.pyplot as plt
# from datetime import date, timedelta
# import datetime as dt
# import warnings
#
# warnings.filterwarnings("ignore")
#
#
# def count_retention(df, time):
#     """
#     Performs 2 steps to arrive at the daily user retention following signup day:
#
#     1) Performs a series of data wrangling steps to take care of missing values for \
#     users in the trip_count_summaries table. This is because these users have never taken a trip \
#     or deleted the app etc
#
#     2) Calculates daily retention for users signed up on provided date in "query" method
#     """
#
#     # Wrangling---------------
#
#     # Need to reset index
#     df = df.reset_index()
#
#     # User_ids with empty last_trip values
#     empty_here = np.where(df.end_time.isnull())
#
#     # Fill in with created_at date
#     df.end_time.loc[empty_here] = df.created_at.loc[empty_here]
#
#     # Convert datetime cols to datetime
#     for x in ['created_at', 'end_time']:
#         df[x] = pd.to_datetime(df[x]).dt.strftime('%m-%d-%Y')
#
#     if time == 'monthly':
#
#         # Get range of dates between min created_at date and max last_trip date
#         max_date = pd.to_datetime(df.end_time.max()).replace(month=pd.to_datetime(df.end_time.max()).month + 1)
#         min_date = pd.to_datetime(df.created_at.min())
#
#         # get dates in between interval
#         a = pd.Series(pd.date_range(start=min_date, end=max_date, freq='M')).apply(lambda x: x.replace(day=1))
#         #     print (max_date, min_date)
#
#         # Counting retention from here
#
#         # Empty Dataframe
#         df2 = pd.DataFrame(index=a, columns=[pd.to_datetime(a.min()).strftime('%m-%d-%Y')]).fillna(0)
#
#         for i in df.end_time:
#             #         print (pd.to_datetime(i).replace(month=pd.to_datetime(i).month+1))
#             df2.loc[pd.Series(pd.date_range(start=min_date.strftime('%m-%d-%Y'),
#                                             end=(pd.to_datetime(i).replace(month=pd.to_datetime(i).month + 1)),
#                                             freq='M')).apply(lambda x: x.replace(day=1))] += 1
#         return df2.transpose()
#
#     if time == 'weekly':
#
#         # Get range of dates between min created_at date and max last_trip date
#         max_date = pd.to_datetime(df.end_time.max())
#         min_date = pd.to_datetime(df.created_at.min())
#
#         # get dates in between interval
#         # delta = max_date - min_date
#         a = pd.date_range(start=min_date, end=max_date, freq='W-MON')
#
#         # Counting retention---------
#
#         # Empty Dataframe
#         df2 = pd.DataFrame(index=a, columns=[pd.to_datetime(a.min()).strftime('%m-%d-%Y')]).fillna(0)
#
#         for i in df.end_time:
#             #     print (i)
#             df2.loc[pd.date_range(start=min_date.strftime('%m-%d-%Y'), end=i, freq='W-MON')] += 1
#
#         return df2.transpose()
#
#     if time == 'daily':
#
#         # Get range of dates between min created_at date and max last_trip date
#         max_date = pd.to_datetime(df.end_time.max())
#         min_date = pd.to_datetime(df.created_at.min())
#
#         # get dates in between interval
#         # delta = max_date - min_date         # timedelta
#         a = pd.date_range(start=min_date, end=max_date)
#
#         # Counting retention
#
#         # Empty Dataframe
#         df2 = pd.DataFrame(index=a, columns=[pd.to_datetime(a.min()).strftime('%m-%d-%Y')]).fillna(0)
#
#         for i in df.end_time:
#             #     print (i)
#             df2.loc[pd.date_range(start=min_date.strftime('%m-%d-%Y'), end=i)] += 1
#
#         return df2.transpose()
#
#
# class CalculateRetention:
#
#     def __init__(self, data, time_period):
#         """
#
#         :param data: Pandas dataframe with 3 columns. \
#                     Column 1: 'user id' or some unique identifier
#                     Column 2: 'created_at': First date of user engaging in any activity
#                     Column 3: 'end_time': Last date of user engaging in any activity
#
#         """
#         self.data = data
#         self.output_consolidate_time = None
#         self.time_period = time_period
#
#     def consolidate_time(self):
#         """
#         Converts the columns in the dataframe to the appropriate datetimes \
#         depending on the `time_period` parameter fed in.
#
#         :return: Same Dataframe but with the `created_at` & 'end_time` columns changed into the first of the week or month
#         """
#         df = self.data
#         df = df.dropna()
#
#         # Column names to convert to datetime
#         column_names = ['created_at', 'end_time']
#
#         # Monthly
#
#         if self.time_period == 'monthly':
#             for x in column_names:
#                 df[x] = pd.to_datetime(df[x])
#                 df[x] = df[x].apply(lambda dt: pd.to_datetime(dt).replace(day=1))
#
#         if self.time_period == 'weekly':
#             for x in column_names:
#                 temp = pd.Series([(y - timedelta(days=y.weekday())) for y in pd.to_datetime(df[x])])
#                 df[x].update(temp)
#                 del temp
#
#         return df
#
#     def combine_queries(self):
#         """
#         Queries a list of users who have signed up between today and today - N days and groups by signup date
#
#         Return
#         -------
#         : A list where each value is a DataFrame (same columns as input) grouped by a certain `created_at` date
#         """
#         data = self.consolidate_time()
#
#         # Converting each datetime column to the right '2019-05-01' type format
#         data.created_at = pd.to_datetime(pd.to_datetime(data['created_at']).dt.strftime('%Y-%m-%d'))
#         data.end_time = pd.to_datetime(pd.to_datetime(data['end_time']).dt.strftime('%Y-%m-%d'))
#
#         # Creating the group by object
#         groupby_object = data.groupby('created_at')
#
#         # creating a list of all dataframes for each date!
#         data_list = [groupby_object.get_group(x) for x in np.unique(data.created_at)]
#         return data_list
#
#     def get_sample(self):
#         """
#         Calculate user retention for all unique `created_at` dates and store them into a list
#         """
#         compiled_list = self.combine_queries()
#
#         sample = [count_retention(x, time=self.time_period) for x in compiled_list]
#         return sample
#
#     def get_raw_retention(self):
#         """
#         Get matrix of all raw numbers from day 1 to day X where X is the longest running retention day.
#
#         :returns: Dataframe containing the raw retention
#
#         Example
#         ------
#         >>> obs = CalculateRetention(file, 'weekly')
#         >>> obs.get_raw_retention()
#         """
#
#         sample = self.get_sample()
#
#         # initialize empty dataframe
#         df1 = pd.DataFrame()
#
#         for s in sample[::-1]:
#             percentage_retention = ([x for x in s.sum()])
#             df = pd.DataFrame(percentage_retention).transpose().set_index(s.index)
#             df1 = pd.concat([df1, df], 0)
#
#         if self.time_period == 'monthly':
#             df1.columns = ['Month {}'.format(x) for x in range(0, df1.shape[1])]
#
#         if self.time_period == 'weekly':
#             df1.columns = ['Week {}'.format(x) for x in range(0, df1.shape[1])]
#
#         if self.time_period == 'daily':
#             df1.columns = ['Day {}'.format(x) for x in range(0, df1.shape[1])]
#
#         return df1.sort_index()
#
#     def compile_percentages(self):
#         """
#         Get matrix of all %s from day 1 to day X where X is the longest running retention day.
#
#         Example
#         ------
#         >>> obs = CalculateRetention(file, 'weekly')
#         >>> obs.compile_percentages()
#         """
#         sample = self.get_sample()
#
#         # Empty dataframe
#         df1 = pd.DataFrame()
#
#         # Calculate % retention for each day
#         for s in sample[::-1]:
#             percentage_retention = ([(x / s.sum()[0]) * 100 for x in s.sum()])
#             df = pd.DataFrame(percentage_retention).transpose().set_index(s.index)
#             df1 = pd.concat([df1, df], 0)
#
#         if self.time_period == 'monthly':
#             df1.columns = ['Month {}'.format(x) for x in range(0, df1.shape[1])]
#
#         if self.time_period == 'weekly':
#             df1.columns = ['Week {}'.format(x) for x in range(0, df1.shape[1])]
#
#         if self.time_period == 'daily':
#             df1.columns = ['Day {}'.format(x) for x in range(0, df1.shape[1])]
#
#         return df1.sort_index()
#
#     def plot_retention(self, plot_type):
#         """
#         Plot the cohort chart for all users signed up either weekly or monthly.
#
#         Parameters
#         -------
#         : plot_type: 'raw' or 'percentage
#
#         Example
#         -------
#         >>> obs = CalculateRetention(file, 'weekly')
#         >>> obs.plot_retention('percentage')
#         """
#
#         if plot_type == 'percentage':
#             df = self.compile_percentages()
#             divide_by = 100
#
#         if plot_type == 'raw':
#             df = self.get_raw_retention()
#             divide_by = 1
#
#         plt.figure(figsize=(20, 10))
#         plt.title('Cohort Analysis type: {}'.format(plot_type))
#
#         if self.time_period == 'weekly':
#             # Name of weeks for labels
#             cr_datetime = pd.to_datetime(df.sort_index().index)
#
#             xy_labels = ['{} to {}'.format(cr_datetime[x].strftime("%b %d"), \
#                                            (pd.to_datetime(cr_datetime[x]) + pd.Timedelta(days=6)).strftime("%b %d")) \
#                          for x, y in zip(range(len(cr_datetime)), range(1, len(cr_datetime)))]
#
#             xy_labels.append('{} to {}'.format(cr_datetime[len(cr_datetime) - 1].strftime("%b %d"),
#                                                (pd.to_datetime(cr_datetime[len(cr_datetime) - 1]) + pd.Timedelta(
#                                                    days=6)).strftime("%b %d")
#                                                ))
#
#         if self.time_period == 'monthly':
#             # Name of months for labels
#             xy_labels = [x.strftime("%B") for x in pd.to_datetime(df.index)]
#
#         sns.heatmap(df.sort_index() / divide_by, annot=True, cmap="YlGnBu", yticklabels=xy_labels)
