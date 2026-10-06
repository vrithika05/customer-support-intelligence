import pandas as pd

REQUIRED_COLUMNS = {
    'customer_name', 'customer_email', 'subject', 'description', 'category',
    'sentiment', 'priority', 'status', 'csat', 'response_time_hours',
    'resolution_time_hours'
}


def clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    df = df.copy()
    df.columns = [str(c).strip().lower().replace(' ', '_') for c in df.columns]
    missing = REQUIRED_COLUMNS - set(df.columns)
    if missing:
        raise ValueError('Missing columns: ' + ', '.join(sorted(missing)))
    text_cols = ['customer_name', 'customer_email', 'subject', 'description', 'category', 'sentiment', 'priority', 'status']
    for col in text_cols:
        df[col] = df[col].fillna('').astype(str).str.strip()
    for col in ['csat', 'response_time_hours', 'resolution_time_hours']:
        df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
    return df


def kpis(tickets):
    total = len(tickets)
    resolved = sum(t.status.lower() == 'resolved' for t in tickets)
    csats = [t.csat for t in tickets if t.csat is not None and t.csat > 0]
    response = [t.response_time_hours for t in tickets]
    return {
        'total': total,
        'resolved': resolved,
        'resolution_rate': round((resolved / total) * 100, 1) if total else 0,
        'avg_csat': round(sum(csats) / len(csats), 2) if csats else 0,
        'avg_response': round(sum(response) / len(response), 2) if response else 0,
    }


def grouped_counts(tickets, attr):
    result = {}
    for t in tickets:
        value = getattr(t, attr) or 'Unknown'
        result[value] = result.get(value, 0) + 1
    return result
