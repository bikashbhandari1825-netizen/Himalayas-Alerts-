from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from database import get_db_connection

app = FastAPI(title="Nepal Suraksha Backend", version="1.0")

class DisasterReport(BaseModel):
    type: str
    description: str
    latitude: float
    longitude: float
    reported_by: int
    location_name: str = ""
    district: str = ""
    province: str = ""


@app.post("/api/v1/report")
def create_report(report: DisasterReport):
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed!")
    try:
        cursor = conn.cursor()
        # डेटाबेसमा नयाँ स्तम्भहरू (location_name, district, province) थप्ने SQL query
        query = "INSERT INTO incidents (type, description, latitude, longitude, reported_by, location_name, district, province, status) VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'Pending');"
        cursor.execute(query, (
            report.type, 
            report.description, 
            report.latitude, 
            report.longitude, 
            report.reported_by, 
            report.location_name, 
            report.district, 
            report.province
        ))
        conn.commit()
        incident_id = cursor.lastrowid
        conn.close()
        return {"status": "success", "incident_id": incident_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/api/v1/reports")
def get_all_reports():
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed!")
    cursor = conn.cursor()
    # डेटाबेसबाट नयाँ स्तम्भहरू पनि तानेर ल्याउने
    cursor.execute("SELECT id, type, description, latitude, longitude, status, reported_by, location_name, district, province FROM incidents ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    
    reports = []
    for row in rows:
        reports.append({
            "id": row[0],
            "type": row[1],
            "description": row[2],
            "latitude": row[3],
            "longitude": row[4],
            "status": row[5],
            "reported_by": row[6],
            "location_name": row[7],
            "district": row[8],
            "province": row[9]
        })
    return {"status": "success", "data": reports}

@app.post("/api/v1/calculate-risk")
def calculate_risk(rainfall_mm: float, river_level_m: float, population_high: bool):
    score = 0
    if rainfall_mm > 100: score += 40
    elif rainfall_mm > 50: score += 20
    if river_level_m > 7.0: score += 40
    elif river_level_m > 4.0: score += 20
    if population_high: score += 20
    
    if score >= 81: level = "Critical 🔴"
    elif score >= 61: level = "High 🟠"
    elif score >= 31: level = "Moderate 🟡"
    else: level = "Low 🟢"
    
    return {
        "risk_score": score,
        "risk_level": level,
        "recommendation": "Evacuate immediately" if score >= 61 else "Monitor closely"
    }

@app.get("/", response_class=HTMLResponse)
async def read_index():
    with open("index.html", "r", encoding="utf-8") as f:
        return f.read()