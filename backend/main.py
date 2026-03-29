from fastapi import FastAPI, UploadFile, File, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import pandas as pd
import hashlib

from database import SessionLocal, engine
import models

from pydantic import BaseModel

# 🔥 Create DB tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# 🔥 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 📦 DB dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# =========================
# 🔐 MODELS
# =========================

class UserCreate(BaseModel):
    email: str
    password: str

class LoginData(BaseModel):
    email: str
    password: str

# =========================
# 🔐 SIGNUP
# =========================

@app.post("/signup")
def signup(data: UserCreate, db: Session = Depends(get_db)):
    try:
        # 🔥 SHA256 hashing (no bcrypt issue)
        hashed = hashlib.sha256(data.password.encode()).hexdigest()

        user = models.User(email=data.email, password=hashed)
        db.add(user)
        db.commit()

        return {"message": "User created"}

    except Exception as e:
        return {"error": str(e)}

# =========================
# 🔐 LOGIN
# =========================

@app.post("/login")
def login(data: LoginData, db: Session = Depends(get_db)):
    try:
        user = db.query(models.User).filter(models.User.email == data.email).first()

        hashed = hashlib.sha256(data.password.encode()).hexdigest()

        if not user or user.password != hashed:
            return {"error": "Invalid credentials"}

        return {"message": "Login successful"}

    except Exception as e:
        return {"error": str(e)}

# =========================
# 📊 PORTFOLIO ANALYSIS
# =========================

@app.post("/portfolio")
async def analyze_portfolio(file: UploadFile = File(...)):
    try:
        df = pd.read_csv(file.file)

        total_invested = df["amount_invested"].sum()
        total_value = df["current_value"].sum()

        gain = total_value - total_invested
        xirr = (gain / total_invested) * 100 if total_invested else 0

        # 🔥 Allocation
        equity = df[df["category"] == "Equity"]["current_value"].sum()
        debt = df[df["category"] == "Debt"]["current_value"].sum()

        total = equity + debt if (equity + debt) else 1

        allocation = {
            "equity_percent": round((equity / total) * 100, 2),
            "debt_percent": round((debt / total) * 100, 2)
        }

        # 🔥 Overlap
        overlap_count = df["fund_name"].duplicated().sum()

        # 🔥 Expense drag
        avg_expense = df["expense_ratio"].mean()
        drag = avg_expense * total_value / 100

        # 🔥 Benchmark
        performance = "Outperforming" if xirr > 12 else "Underperforming"

        # 🔥 Suggestions
        suggestions = []

        if allocation["equity_percent"] > 70:
            suggestions.append("Reduce equity exposure, add debt funds")

        if avg_expense > 1.5:
            suggestions.append("Switch to low-cost index funds")

        if overlap_count > 0:
            suggestions.append("Remove duplicate fund exposure")

        if not suggestions:
            suggestions.append("Portfolio is well balanced 👍")

        return {
            "total_invested": int(total_invested),
            "total_value": int(total_value),
            "xirr": round(xirr, 2),
            "allocation": allocation,
            "overlap_count": int(overlap_count),
            "expense_drag": int(drag),
            "performance_vs_benchmark": performance,
            "suggestions": suggestions
        }

    except Exception as e:
        return {"error": str(e)}