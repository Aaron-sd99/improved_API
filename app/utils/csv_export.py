import csv
from io import StringIO
from fastapi import Response
def to_csv_response(rows: list[dict], filename: str = "export.csv") -> Response:
    buf = StringIO()
    if rows:
        writer = csv.DictWriter(buf, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    return Response(content=buf.getvalue(), media_type="text/csv",
                    headers={"Content-Disposition": f"attachment; filename={filename}"})
