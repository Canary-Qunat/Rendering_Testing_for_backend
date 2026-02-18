from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database.database import get_db, init_db
from fastapi.templating import Jinja2Templates
from api.zerodha_client import Zerodha_Client
from fastapi.responses import RedirectResponse
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting Zerodha OAuth Backend (Single-User Mode)")
    init_db()
    print("Backend ready at http://127.0.0.1:8001")
    yield
    print("Shutting down")


FRONTEND_URL = "https://canary-qunat.github.io/Rendering_Testing_for_frontend/"

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

templates = Jinja2Templates(directory="templates")
client = Zerodha_Client()


@app.get('/')
def read_root():
    return {
        "status": "running",
        "message": "Zerodha OAuth Backend API (Single-User)",
        "endpoints": {
            "status": "/auth/status",
            "login": "/kite-login",
            "callback": "/auth/callback",
            "profile": "/api/profile",
            "dashboard": "/api/dashboard-data",
            "token_info": "/debug/token-info",
            "docs": "/docs"
        }
    }


@app.get('/auth/status')
def auth_status(db: Session = Depends(get_db)):
    """
    Check if ANY valid token exists in database (single-user system).
    Returns authenticated: true if valid token found, false otherwise.
    """
    print("\n Checking authentication status...")
    
    # Try to get profile using any valid token from database
    profile_data = client.get_profile(db)
    
    if profile_data:
        print(f" Valid token found! User: {profile_data.get('user_name', 'Unknown')}")
        return {
            "authenticated": True,
            "message": "Valid token found in database",
            "user": {
                "user_id": profile_data.get("user_id"),
                "user_name": profile_data.get("user_name"),
                "email": profile_data.get("email")
            }
        }
    else:
        print(" No valid token found in database")
        return {
            "authenticated": False,
            "message": "No valid token found. Please login."
        }


@app.get("/kite-login")
def kite_login():
    """Initiate Zerodha OAuth login"""
    try:
        print("\n Initiating Zerodha login...")
        login_url = client.get_login_url()
        print(f" Redirecting to: {login_url}")
        return RedirectResponse(url=login_url)
    except Exception as e:
        print(f" Error generating login URL: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/auth/callback")
def kite_callback(request_token: str, status: str = "success", db: Session = Depends(get_db)):
    """Handle OAuth callback from Zerodha"""
    print(f"\n Received OAuth callback: status={status}")
    
    if status != "success":
        print(f" Login failed with status: {status}")
        return RedirectResponse(url=f"{FRONTEND_URL}?auth=failed")
    
    try:
        print(f" Received request_token: {request_token[:10]}...")
        
        # Generate access token and save to database
        access_token = client.generate_access_token(request_token, db)
        
        if access_token:
            print(f" Access token generated and saved!")
            # Redirect to frontend with success
            return RedirectResponse(url=f"{FRONTEND_URL}?auth=success")
        else:
            print(f" Could not generate access token")
            return RedirectResponse(url=f"{FRONTEND_URL}?auth=error")

    except Exception as e:
        import traceback
        print(f" Callback error: {e}")
        print(traceback.format_exc()) # full stack traces in render log
        return RedirectResponse(url=f"{FRONTEND_URL}?auth=error&message={str(e)}")


@app.get('/api/profile')
def get_profile_api(db: Session = Depends(get_db)):
    """Get user profile using any valid token from database"""
    print("\n Fetching profile...")
    
    profile_data = client.get_profile(db)
    
    if not profile_data:
        print(" No valid token found")
        raise HTTPException(
            status_code=401,
            detail="Not authenticated. Please login at /kite-login"
        )
    
    print(f" Profile fetched: {profile_data.get('user_name', 'Unknown')}")
    return {"status": "success", "data": profile_data}


@app.get('/api/holdings')
def get_holdings_api(db: Session = Depends(get_db)):
    """Get holdings using any valid token from database"""
    print("\n Fetching holdings...")
    
    holdings = client.get_holdings(db)
    
    if holdings is None:
        print(" No valid token found")
        raise HTTPException(
            status_code=401,
            detail="Not authenticated. Please login at /kite-login"
        )
    
    print(f" Holdings fetched: {len(holdings)} items")
    return {"status": "success", "data": holdings}


@app.get('/api/positions')
def get_positions_api(db: Session = Depends(get_db)):
    """Get positions using any valid token from database"""
    print("\n Fetching positions...")
    
    positions = client.get_positions(db)
    
    if positions is None:
        print(" No valid token found")
        raise HTTPException(
            status_code=401,
            detail="Not authenticated. Please login at /kite-login"
        )
    
    net_positions = positions.get("net", []) if positions else []
    print(f" Positions fetched: {len(net_positions)} items")
    
    return {"status": "success", "data": net_positions}


@app.get('/api/dashboard-data')
def get_dashboard_data_api(db: Session = Depends(get_db)):
    """
    Get complete dashboard data using any valid token from database.
    This is a single-user system - uses the most recent valid token.
    """
    print("\n Fetching dashboard data...")
    
    # Check if we have a valid token by trying to get profile
    profile_data = client.get_profile(db)
    
    if not profile_data:
        print(" No valid token found in database")
        raise HTTPException(
            status_code=401,
            detail="Not authenticated. Please login at /kite-login"
        )
    
    print(f" Valid token found! Fetching all data...")
    
    # Fetch all data
    holdings = client.get_holdings(db)
    positions = client.get_positions(db)

    # Calculate net positions
    net_positions = positions.get("net", []) if positions else []

    # Calculate portfolio summary
    total_holdings_value = 0
    total_holdings_pnl = 0

    for holding in holdings:
        last_price = holding.get('last_price', 0)
        qty = holding.get('quantity', 0)
        average_price = holding.get('average_price', 0)
        
        current_value = last_price * qty
        invested_value = average_price * qty
        
        total_holdings_value += current_value
        total_holdings_pnl += (current_value - invested_value)

    total_positions_pnl = sum(pos.get('pnl', 0) for pos in net_positions)
    
    portfolio_summary = {
        'total_value': round(total_holdings_value, 2),
        'total_pnl': round(total_holdings_pnl + total_positions_pnl, 2),
        'holdings_pnl': round(total_holdings_pnl, 2),
        'positions_pnl': round(total_positions_pnl, 2),
        'holdings_count': len(holdings),
        'positions_count': len(net_positions)
    }
    
    print(f" Dashboard data complete!")
    print(f"   Holdings: {len(holdings)} | Positions: {len(net_positions)}")
    print(f"   Total Value: ₹{portfolio_summary['total_value']:,.2f}")
    print(f"   Total P&L: ₹{portfolio_summary['total_pnl']:,.2f}")
    
    return {
        "status": "success",
        "data": {
            "profile": profile_data,
            "holdings": holdings,
            "positions": net_positions,
            "summary": portfolio_summary
        }
    }


# Debug endpoint to check token status
@app.get('/debug/token-info')
def debug_token_info(db: Session = Depends(get_db)):
    """
    Debug endpoint to check token status in database.
    Use this to diagnose authentication issues.
    """
    from database.database import get_token_info
    
    info = get_token_info(db)
    
    return {
        "status": "success",
        "token_info": info,
        "help": "If is_valid=false, you need to login again at /kite-login"
    }


# Legacy HTML dashboard endpoint
@app.get('/dashboard')
def dashboard(request: Request, db: Session = Depends(get_db)):
    """HTML dashboard (legacy)"""
    profile_data = client.get_profile(db)
    
    if not profile_data:
        return RedirectResponse(url="/kite-login")
    
    holdings = client.get_holdings(db)
    positions = client.get_positions(db)
    net_positions = positions.get("net", []) if positions else []

    total_holdings_value = 0
    total_holdings_pnl = 0

    for holding in holdings:
        last_price = holding.get('last_price', 0)
        qty = holding.get('quantity', 0)
        average_price = holding.get('average_price', 0)
        
        current_value = last_price * qty
        invested_value = average_price * qty
        
        total_holdings_value += current_value
        total_holdings_pnl += (current_value - invested_value)

    total_positions_pnl = sum(pos.get('pnl', 0) for pos in net_positions)
    
    portfolio_summary = {
        'total_value': round(total_holdings_value, 2),
        'total_pnl': round(total_holdings_pnl + total_positions_pnl, 2),
        'holdings_pnl': round(total_holdings_pnl, 2),
        'positions_pnl': round(total_positions_pnl, 2),
        'holdings_count': len(holdings),
        'positions_count': len(net_positions)
    }
    
    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "profile": profile_data,
        "holdings": holdings,
        "positions": net_positions,
        "summary": portfolio_summary

    })


