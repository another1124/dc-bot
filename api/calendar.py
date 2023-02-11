import sqlite3
from datetime import datetime, timedelta
from typing import List

from api.database import dbopen


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days + 1)):
        yield start_date + timedelta(n)


def update_calendar(date, hour, member, option="insert") -> None:
    """Update calendar (store every member's calendar) database

    Args:
        date (str): format: "YYYY-MM-DD"
        hour (str): "am" or "pm"
        member (str): member name
        option (str): "insert" or "delete"
    """
    with dbopen("calendar.db") as c:
        c.execute(
            """CREATE TABLE IF NOT EXISTS calendar
                (id INTEGER PRIMARY KEY,
                date DATE NOT NULL,
                hour TEXT NOT NULL,
                member TEXT NOT NULL,
                UNIQUE(date, hour, member))"""
        )
        if option == "insert":
            try:
                c.execute("INSERT INTO calendar (date, hour, member) VALUES (?, ?, ?)", (date, hour, member))
            except sqlite3.IntegrityError:
                print("The time is already booked")
        elif option == "delete":
            try:
                c.execute("DELETE FROM calendar WHERE start = ? AND end = ? AND member = ?", (date, hour, member))
            except sqlite3.IntegrityError:
                print("The time is not booked")
        else:
            raise ValueError("option should be 'insert' or 'delete'")


def schedule_meeting_time(start_date: str, end_date: str, members: List[str]) -> List[str]:
    """Find free meeting time for a group of members

    Args:
        start (str): start time, format: "YYYY-MM-DD"
        end (str): end time, format: "YYYY-MM-DD"
        members (List[str]): a list of member names

    Returns:
        List[str]: a list of free meeting time, format: "YYYY-MM-DD HH:MM:SS"
    """
    with dbopen("calendar.db") as c:
        c.execute("SELECT * from calendar")
        print(c.fetchall())
        c.execute(
            "SELECT date, hour FROM calendar WHERE member IN ({}) AND date BETWEEN ? AND ?".format(
                ",".join("?" * len(members))
            ),
            members + [start_date, end_date],
        )
        result = c.fetchall()

    busy_time = {}
    for date_hour in result:
        date_hour_str = date_hour[0] + " " + date_hour[1]
        busy_time[date_hour_str] = True

    free_time = []
    for single_date in daterange(
        datetime.strptime(start_date, "%Y-%m-%d").date(), datetime.strptime(end_date, "%Y-%m-%d").date()
    ):
        date_str = single_date.strftime("%Y-%m-%d")
        if date_str + " am" not in busy_time:
            free_time.append(date_str + " AM")
        if date_str + " pm" not in busy_time:
            free_time.append(date_str + " PM")

    return free_time
