from datetime import datetime, timedelta


def resolve_period(period: str | None):
    """Resolve a natural-language period into (start_date, end_date) datetimes."""
    if not period:
        return None, None

    now = datetime.now()
    today = now.replace(hour=0, minute=0, second=0, microsecond=0)
    key = period.lower().strip().replace(" ", "_").replace("-", "_")

    if key in ("today", "daily"):
        return today, now

    if key in ("yesterday",):
        start = today - timedelta(days=1)
        return start, start + timedelta(days=1) - timedelta(seconds=1)

    if key in ("last_week", "past_week", "this_week"):
        start = today - timedelta(days=7)
        return start, now

    if key in ("last_month", "past_month", "previous_month"):
        first_this_month = today.replace(day=1)
        end = first_this_month - timedelta(seconds=1)
        start = end.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        return start, end

    if key in ("this_month", "current_month"):
        start = today.replace(day=1)
        return start, now

    if key in ("last_quarter", "previous_quarter"):
        month = ((today.month - 1) // 3) * 3 + 1
        start_this_q = today.replace(month=month, day=1)
        end = start_this_q - timedelta(seconds=1)
        q_month = ((end.month - 1) // 3) * 3 + 1
        start = end.replace(month=q_month, day=1, hour=0, minute=0, second=0, microsecond=0)
        return start, end

    if key in ("this_quarter", "current_quarter"):
        q_month = ((today.month - 1) // 3) * 3 + 1
        start = today.replace(month=q_month, day=1)
        return start, now

    if key in ("q1", "quarter_1"):
        year = today.year
        return datetime(year, 1, 1), datetime(year, 3, 31, 23, 59, 59)

    if key in ("q2", "quarter_2"):
        year = today.year
        return datetime(year, 4, 1), datetime(year, 6, 30, 23, 59, 59)

    if key in ("q3", "quarter_3"):
        year = today.year
        return datetime(year, 7, 1), datetime(year, 9, 30, 23, 59, 59)

    if key in ("q4", "quarter_4"):
        year = today.year
        return datetime(year, 10, 1), datetime(year, 12, 31, 23, 59, 59)

    if key in ("last_6_months", "past_6_months", "six_months"):
        return today - timedelta(days=180), now

    if key in ("this_year", "current_year", "fiscal_year"):
        return datetime(today.year, 1, 1), now

    if key in ("last_year", "previous_year"):
        year = today.year - 1
        return datetime(year, 1, 1), datetime(year, 12, 31, 23, 59, 59)

    if key in ("august", "aug"):
        year = today.year
        return datetime(year, 8, 1), datetime(year, 8, 31, 23, 59, 59)

    if key in ("september", "sep"):
        year = today.year
        return datetime(year, 9, 1), datetime(year, 9, 30, 23, 59, 59)

    return None, None


def date_filter(start_date, end_date):
    """Build a MongoDB date range filter."""
    if not start_date and not end_date:
        return {}

    filt = {}
    if start_date:
        filt["$gte"] = start_date
    if end_date:
        filt["$lte"] = end_date
    return {"date": filt} if filt else {}
