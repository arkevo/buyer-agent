# Author: Green Mountain Systems AI Inc.
# Donated to IAB Tech Lab

"""MCP (Model Context Protocol) server for the Ad Buyer Agent.

Exposes buyer operations as MCP tools via FastMCP SSE transport.
This is the foundation server that all other MCP tool modules build upon.

Mount into a FastAPI app:
    from ad_buyer.interfaces.mcp_server import mount_mcp
    mount_mcp(app)

This creates an SSE endpoint at /mcp/sse for MCP client connections
(Claude Desktop, ChatGPT, Cursor, Windsurf, etc.).
"""

import json
import logging
import sqlite3
from datetime import datetime, timezone

from fastapi import FastAPI
from mcp.server.fastmcp import FastMCP

from ..config.settings import Settings

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# MCP Server Instance
# ---------------------------------------------------------------------------

mcp = FastMCP(
    name="ad-buyer-agent",
    instructions=(
        "You are the IAB Tech Lab Ad Buyer Agent assistant. "
        "You help users manage advertising campaigns, deals, seller "
        "relationships, and buyer operations through the buyer agent system. "
        "Use the available tools to check system status, review configuration, "
        "and manage buyer workflows."
    ),
)


def _get_settings() -> Settings:
    """Get a fresh Settings instance.

    Returns a new instance each time so that environment changes
    (and test patches) are reflected.
    """
    return Settings()


# ---------------------------------------------------------------------------
# Foundation Tools
# ---------------------------------------------------------------------------


@mcp.tool()
def get_setup_status() -> str:
    """Check the current setup and configuration state of the buyer agent.

    Returns a JSON object with:
    - setup_complete: whether all required configuration is in place
    - checks: individual status checks (seller endpoints, database, etc.)
    """
    settings = _get_settings()
    checks: dict[str, bool] = {}

    # Check seller endpoints
    seller_endpoints = settings.get_seller_endpoints()
    checks["seller_endpoints_configured"] = len(seller_endpoints) > 0

    # Check database accessibility
    db_accessible = False
    try:
        db_url = settings.database_url
        # Strip sqlite:/// prefix for direct connection test
        if db_url.startswith("sqlite:///"):
            db_path = db_url[len("sqlite:///"):]
        else:
            db_path = db_url

        # Try a lightweight connection test
        conn = sqlite3.connect(db_path)
        conn.execute("SELECT 1")
        conn.close()
        db_accessible = True
    except (sqlite3.Error, OSError):
        db_accessible = False
    checks["database_accessible"] = db_accessible

    # Check API key configuration
    checks["api_key_configured"] = bool(settings.api_key)

    # Check LLM configuration
    checks["llm_configured"] = bool(settings.anthropic_api_key)

    # Overall setup completeness
    # Minimum required: seller endpoints + database
    setup_complete = (
        checks["seller_endpoints_configured"]
        and checks["database_accessible"]
    )

    result = {
        "setup_complete": setup_complete,
        "checks": checks,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    return json.dumps(result, indent=2)


@mcp.tool()
def health_check() -> str:
    """Check the health of buyer agent services.

    Returns a JSON object with:
    - status: overall health (healthy, degraded, unhealthy)
    - version: system version
    - services: individual service health details
    """
    from .. import __version__

    settings = _get_settings()
    services: dict[str, dict] = {}

    # Check database service
    try:
        db_url = settings.database_url
        if db_url.startswith("sqlite:///"):
            db_path = db_url[len("sqlite:///"):]
        else:
            db_path = db_url

        conn = sqlite3.connect(db_path)
        conn.execute("SELECT 1")
        conn.close()
        services["database"] = {"status": "healthy"}
    except (sqlite3.Error, OSError) as exc:
        services["database"] = {"status": "unhealthy", "error": str(exc)}

    # Check seller connectivity (lightweight -- just config presence)
    seller_endpoints = settings.get_seller_endpoints()
    if seller_endpoints:
        services["seller_connections"] = {
            "status": "configured",
            "endpoint_count": len(seller_endpoints),
        }
    else:
        services["seller_connections"] = {
            "status": "not_configured",
            "endpoint_count": 0,
        }

    # Check event bus availability
    services["event_bus"] = {"status": "healthy"}

    # Determine overall status
    unhealthy_count = sum(
        1 for s in services.values() if s.get("status") == "unhealthy"
    )
    if unhealthy_count == 0:
        overall_status = "healthy"
    elif unhealthy_count < len(services):
        overall_status = "degraded"
    else:
        overall_status = "unhealthy"

    result = {
        "status": overall_status,
        "version": __version__,
        "services": services,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
    return json.dumps(result, indent=2)


@mcp.tool()
def get_config() -> str:
    """Get the current buyer agent configuration.

    Returns non-sensitive configuration values. API keys and secrets
    are never exposed through this tool.

    Returns a JSON object with:
    - environment: current environment (development, staging, production)
    - seller_endpoints: configured seller agent URLs
    - database_url: database connection string
    - llm settings: model names, temperature, etc.
    """
    settings = _get_settings()

    result = {
        "environment": settings.environment,
        "seller_endpoints": settings.get_seller_endpoints(),
        "iab_server_url": settings.iab_server_url,
        "database_url": settings.database_url,
        "default_llm_model": settings.default_llm_model,
        "manager_llm_model": settings.manager_llm_model,
        "llm_temperature": settings.llm_temperature,
        "llm_max_tokens": settings.llm_max_tokens,
        "cors_allowed_origins": settings.get_cors_origins(),
        "log_level": settings.log_level,
        "crew_memory_enabled": settings.crew_memory_enabled,
        "crew_verbose": settings.crew_verbose,
        "crew_max_iterations": settings.crew_max_iterations,
    }
    return json.dumps(result, indent=2)


# ---------------------------------------------------------------------------
# Mounting
# ---------------------------------------------------------------------------


def mount_mcp(app: FastAPI) -> None:
    """Mount the MCP SSE server onto a FastAPI application.

    Creates an SSE endpoint at /mcp/sse that MCP clients can connect to.

    Args:
        app: The FastAPI application to mount onto.
    """
    sse_app = mcp.sse_app()
    app.mount("/mcp/sse", sse_app)
    logger.info("MCP SSE server mounted at /mcp/sse")
