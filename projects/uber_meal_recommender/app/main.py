from fastapi import FastAPI, Depends
from fastapi.responses import HTMLResponse
from app.db.session import engine, SessionLocal
from app.db.base import Base
from app.models.order import Order
from app.seed import seed_orders

from app.prompts.openai_client import recommend_meal, ModelOutputError
from app.schemas.order import RecommendOrderRequest, RecommendOrderResponse
from fastapi import HTTPException 


app = FastAPI(title = "Uber Meal Recommender")

UI_HTML = """
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>Uber Meal Recommender</title>
    <style>
      :root {
        --bg: #0b0f1a;
        --panel: #121827;
        --panel-2: #0f1422;
        --accent: #f5c453;
        --accent-2: #7dd3fc;
        --text: #e5e7eb;
        --muted: #94a3b8;
        --border: #1f2a44;
      }
      * { box-sizing: border-box; }
      body {
        margin: 0;
        font-family: "Space Grotesk", "IBM Plex Sans", system-ui, sans-serif;
        color: var(--text);
        background:
          radial-gradient(900px 500px at 10% -10%, #1c2541 0%, transparent 60%),
          radial-gradient(700px 400px at 90% 10%, #11243a 0%, transparent 60%),
          var(--bg);
        min-height: 100vh;
        display: grid;
        place-items: center;
        padding: 32px 16px;
      }
      .shell {
        width: min(980px, 100%);
        display: grid;
        gap: 20px;
        grid-template-columns: 1.05fr 0.95fr;
      }
      @media (max-width: 880px) {
        .shell { grid-template-columns: 1fr; }
      }
      .card {
        background: linear-gradient(160deg, var(--panel), var(--panel-2));
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 12px 40px rgba(0,0,0,0.35);
      }
      h1 {
        font-size: clamp(28px, 3vw, 34px);
        margin: 0 0 8px;
        letter-spacing: 0.3px;
      }
      p.sub {
        margin: 0 0 22px;
        color: var(--muted);
        font-size: 0.95rem;
      }
      label {
        display: block;
        font-size: 0.85rem;
        color: var(--muted);
        margin-bottom: 6px;
      }
      input, select, textarea {
        width: 100%;
        padding: 12px 12px;
        border-radius: 10px;
        border: 1px solid var(--border);
        background: #0d1320;
        color: var(--text);
        outline: none;
        transition: border 120ms ease, box-shadow 120ms ease;
      }
      input:focus, select:focus, textarea:focus {
        border-color: var(--accent-2);
        box-shadow: 0 0 0 3px rgba(125, 211, 252, 0.15);
      }
      .row {
        display: grid;
        gap: 14px;
        grid-template-columns: repeat(2, 1fr);
      }
      @media (max-width: 520px) {
        .row { grid-template-columns: 1fr; }
      }
      .range {
        display: grid;
        gap: 6px;
      }
      .actions {
        display: flex;
        gap: 10px;
        align-items: center;
        margin-top: 8px;
      }
      button {
        background: linear-gradient(120deg, var(--accent), #ffd980);
        color: #141414;
        border: none;
        padding: 12px 18px;
        border-radius: 10px;
        font-weight: 600;
        cursor: pointer;
        transition: transform 120ms ease;
      }
      button:hover { transform: translateY(-1px); }
      .pill {
        font-size: 0.78rem;
        color: #0f172a;
        background: var(--accent-2);
        padding: 6px 10px;
        border-radius: 999px;
        font-weight: 600;
      }
      .result {
        display: grid;
        gap: 12px;
        min-height: 180px;
      }
      .result h2 {
        margin: 0;
        font-size: 1.1rem;
        color: var(--accent);
      }
      .result p {
        margin: 0;
        color: var(--text);
        line-height: 1.5;
      }
      .muted { color: var(--muted); }
      .error { color: #fca5a5; }
      .hint { font-size: 0.82rem; color: var(--muted); }
    </style>
  </head>
  <body>
    <div class="shell">
      <section class="card">
        <div class="pill">POST /recommend</div>
        <h1>Uber Meal Recommender</h1>
        <p class="sub">A minimal UI that sends your inputs to the FastAPI endpoint.</p>
        <form id="recommend-form">
          <div class="row">
            <div>
              <label for="phase_of_day">Phase of day</label>
              <select id="phase_of_day" name="phase_of_day" required>
                <option value="morning">morning</option>
                <option value="afternoon">afternoon</option>
                <option value="evening">evening</option>
              </select>
            </div>
            <div>
              <label for="mood">Mood (optional)</label>
              <input id="mood" name="mood" type="text" minlength="3" maxlength="80" placeholder="e.g. cozy, adventurous" />
            </div>
          </div>
          <div class="range">
            <label for="hungry">Hungry level: <span id="hungry-value">3</span></label>
            <input id="hungry" name="hungry" type="range" min="1" max="5" step="1" value="3" />
            <div class="hint">1 = snacky, 5 = starving</div>
          </div>
          <div class="actions">
            <button type="submit">Get recommendation</button>
            <span class="muted" id="status"></span>
          </div>
        </form>
      </section>
      <section class="card result">
        <h2>Recommended meal</h2>
        <p id="meal" class="muted">No recommendation yet.</p>
        <h2>Summary</h2>
        <p id="summary" class="muted">Fill the form and submit.</p>
        <p id="error" class="error"></p>
      </section>
    </div>
    <script>
      const form = document.getElementById("recommend-form");
      const status = document.getElementById("status");
      const mealEl = document.getElementById("meal");
      const summaryEl = document.getElementById("summary");
      const errorEl = document.getElementById("error");
      const hungry = document.getElementById("hungry");
      const hungryValue = document.getElementById("hungry-value");
      hungry.addEventListener("input", () => {
        hungryValue.textContent = hungry.value;
      });

      form.addEventListener("submit", async (event) => {
        event.preventDefault();
        status.textContent = "Sending...";
        errorEl.textContent = "";
        mealEl.textContent = "Waiting for response...";
        summaryEl.textContent = "";

        const payload = {
          phase_of_day: form.phase_of_day.value,
          hungry: Number(form.hungry.value),
        };
        if (form.mood.value.trim().length > 0) {
          payload.mood = form.mood.value.trim();
        }

        try {
          const res = await fetch("/recommend", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload),
          });
          const data = await res.json();
          if (!res.ok) {
            throw new Error(data.detail || "Request failed.");
          }
          mealEl.textContent = data.meal;
          summaryEl.textContent = data.summary;
          status.textContent = "Done.";
        } catch (err) {
          mealEl.textContent = "No recommendation yet.";
          summaryEl.textContent = "";
          errorEl.textContent = err.message || "Unexpected error.";
          status.textContent = "Error.";
        }
      });
    </script>
  </body>
</html>
"""


@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/", response_class=HTMLResponse)
def ui():
    return UI_HTML


@app.post("/recommend" , response_model=RecommendOrderResponse)
def recommend(request : RecommendOrderRequest):
    try:
        return recommend_meal(request=request)
    except ModelOutputError as e:
        raise HTTPException(status_code=502, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=502, detail="Unexpected error.")

# Temprorary create all
@app.on_event("startup")
def on_startup():
    # Create a tables.
    Base.metadata.create_all(bind = engine)

    # seed database.
    db = SessionLocal()
    try:
        seed_orders(db)
    finally:
        db.close()

    
