import pandas as pd
import json
import matplotlib.pyplot as plt
import seaborn as sns
import argparse
from datetime import datetime
from tabulate import tabulate
import numpy as np
import re

def getUserID(x):
    if x == None:
        return None
    return str(x["user_id"])

def createChannel(file):
    with open(file, encoding="utf8") as f:
        channel_json = json.load(f)

    data = channel_json["data"]
    cols = channel_json["columns"]

    df = pd.DataFrame(data=data,columns=cols)
    df["UserID"] = df["ID"].apply(getUserID)

    df["Datetime"] = pd.to_datetime(df["Timestamp"])

    return df

def postingTimeChart(df,save=False):
    df["Datetime_Hour"] = df["Datetime"].dt.hour
    
    plt.figure(figsize=(10, 5))
    g = sns.countplot(x="Datetime_Hour", data=df, color="green", order=range(24))
    g.set_xlabel("Hour")
    g.set_title("Messages per hour")

    if save:
        plt.savefig("postingTimeChart.png")

    return g

def messagesPerWeekday(df,save=False):
    df["Datetime_Weekday"] = df["Datetime"].dt.day_name()

    plt.figure(figsize=(10, 5))
    order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    g = sns.countplot(x="Datetime_Weekday", data=df, color="green", order=order)
    g.set_xlabel("Weekday")
    g.set_title("Messages")

    if save:
        plt.savefig("messagesPerWeekday.png")

    return g

def heatmapDayHours(df,users=None,save=False):

    if users:
        df = df[df["UserID"].isin(users)]

    df["Datetime_Hour"] = df["Datetime"].dt.hour
    df["Datetime_Weekday"] = df["Datetime"].dt.day_name()

    data = df.groupby(["Datetime_Weekday", "Datetime_Hour"])["message ID"].count().reset_index().rename(columns = {"message ID": "Nr_Messages"})
    
    # missing days
    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    available_days = list(data["Datetime_Weekday"].unique())
    
    adding = []
    
    for day in days:
        if day not in available_days:
            print(f"{day} not in data")
            n = {"Datetime_Weekday" : day, "Datetime_Hour" : 0, "Nr_Messages" : np.NaN}
            data = data.append(n, ignore_index = True)
            
    heat = data.pivot(index="Datetime_Weekday", columns="Datetime_Hour", values="Nr_Messages").reset_index().set_index("Datetime_Weekday")

    ## fill up missing hours
    hours = list(range(24))
    for x in hours:
        if x not in heat.columns:
            heat[x] = np.NaN

    # rearrange columns and transpose, then rearrange again
    heat = heat[range(24)]
    heat = heat.transpose()
    heat = heat[days]

    plt.figure(figsize=(14, 12))
    g = sns.heatmap(heat,annot=True,fmt=".0f")
    g.set_xlabel("Day",fontsize=15)
    g.set_ylabel("Hour",fontsize=15)
    g.set_title("Most active hours per weekday",fontsize=20)

    if save:
        plt.savefig("heatmap_Days_Hours.png")

    return g

def getNMostActiveUser(df,n=None):
    mostActive = df.groupby("UserID").count()["message ID"].sort_values(ascending=False).reset_index().rename(columns={"message ID": "Messages"})

    if n:
        mostActive = mostActive.head(n)

    mostActive = mostActive.merge(df[["UserID", "Name"]], how="left").drop_duplicates()
    mostActive = mostActive[["Name", "UserID", "Messages"]]

    return mostActive


def getStatistics(df):

    minDate = df["Datetime"].dt.date.min()
    maxDate = df["Datetime"].dt.date.max()
    daysInData = (maxDate - minDate).days + 1
    messages = len(df)
    meanNrOfMessages = round(df.groupby(df["Datetime"].dt.date)["message ID"].count().mean(), 2)
    members = df["UserID"].nunique()
    channel = df["Chat name"].unique()[0]

    dic = {"Channel": channel,
           "Active Members": members, 
           "Messages": messages, "First date": minDate,
           "Last date": maxDate, 
           "Days in data": daysInData, 
           "Mean # messages per day": meanNrOfMessages}
    
    return pd.DataFrame.from_dict(dic,orient="index",columns=["Value"]).reset_index().rename(columns={"index" : "Parameter"})

def isPositiveValue(input):
    try:
        value = int(input)
    except ValueError:
        raise argparse.ArgumentTypeError("invalid value: must be a positive int")

    if value <= 0:
        raise argparse.ArgumentTypeError("invalid value: must be a positive int")

    return value

def main():
    parser = argparse.ArgumentParser(description="Analyse a Telegram JSON file. Simply read the file in and create insights.")

    parser.add_argument("file", help="JSON file containing the telegram data")
    parser.add_argument("-t", "--time", action="store_true", help="Create chart of posting times")
    parser.add_argument("-dh", "--daysHours", default=[None], action="store", nargs="*", type=str, metavar="UserID",
                        help="Create heatmap of posting days vs. times for all users or certain UserIDs")

    parser.add_argument("-w", "--weekday", action="store_true", help="Create chart of messages per weekday")

    parser.add_argument("-s", "--statistics", action="store_true",
                        help = "Show statistics (#members, #messages, #mean nr of messages etc.)")

    parser.add_argument("-ma", "--mostActive", type=isPositiveValue, metavar="n",
                        help = "Show the top n members by messages and their message count. Need to pass n > 0 as input")            

    args = parser.parse_args()

    df = createChannel(args.file)

    if args.time:
        postingTimeChart(df,save=True)

    if args.daysHours != [None]:
        users = args.daysHours
        heatmapDayHours(df, users,save=True)

    if args.weekday:
        messagesPerWeekday(df,save=True)

    if args.statistics:
        stats = getStatistics(df)
        print(tabulate(stats, tablefmt='psql', showindex=False))

    if args.mostActive:
        nrUsers = args.mostActive
        most_active = getNMostActiveUser(df,nrUsers)
        print(tabulate(most_active, headers="keys", tablefmt='psql', showindex=False))

if __name__ == "__main__":
        main()