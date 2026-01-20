"""
Fathom AI MCP Server

A Model Context Protocol server for interacting with the Fathom AI API.
Provides tools for accessing meeting recordings, summaries, transcripts,
teams, and webhooks.
"""

import os
from typing import Any, Optional
from datetime import datetime

import httpx
from fastmcp import FastMCP
from fastmcp.exceptions import ToolError
from pydantic import Field

# Initialize FastMCP server
mcp = FastMCP("Fathom AI")

# Constants
BASE_URL = "https://api.fathom.ai/external/v1"


def get_api_key() -> str:
    """Fetch the Fathom API key from the environment."""
    api_key = os.getenv("FATHOM_API_KEY", "").strip()
    if not api_key:
        raise ToolError(
            "FATHOM_API_KEY environment variable is required before calling Fathom tools."
        )
    return api_key


def get_headers() -> dict[str, str]:
    """Get headers for API requests."""
    return {
        "X-Api-Key": get_api_key(),
        "Content-Type": "application/json",
    }


async def make_request(
    method: str,
    endpoint: str,
    params: Optional[dict[str, Any]] = None,
    json_data: Optional[dict[str, Any]] = None,
) -> dict[str, Any]:
    """Make an HTTP request to the Fathom API."""
    url = f"{BASE_URL}{endpoint}"
    headers = get_headers()

    async with httpx.AsyncClient() as client:
        try:
            response = await client.request(
                method=method,
                url=url,
                headers=headers,
                params=params,
                json=json_data,
                timeout=30.0,
            )

            # Handle rate limiting
            if response.status_code == 429:
                rate_limit_reset = response.headers.get("RateLimit-Reset", "unknown")
                raise ToolError(
                    f"Rate limit exceeded. Reset in {rate_limit_reset} seconds."
                )

            # Handle authentication errors
            if response.status_code == 401:
                raise ToolError(
                    "Authentication failed. Please check your FATHOM_API_KEY."
                )

            # Handle not found errors
            if response.status_code == 404:
                raise ToolError("Resource not found.")

            # Handle bad request errors
            if response.status_code == 400:
                error_detail = response.text or "Invalid request parameters"
                raise ToolError(f"Bad request: {error_detail}")

            # Handle successful no-content responses (like DELETE)
            if response.status_code == 204:
                return {"success": True, "message": "Operation completed successfully"}

            response.raise_for_status()

            # Some endpoints return empty responses
            if not response.content:
                return {"success": True}

            return response.json()

        except httpx.HTTPError as e:
            raise ToolError(f"HTTP error occurred: {str(e)}")


# MEETINGS


@mcp.tool()
async def list_meetings(
    cursor: Optional[str] = None,
    calendar_invitees: Optional[list[str]] = Field(
        None, description="List of email addresses to filter by"
    ),
    calendar_invitees_domains: Optional[list[str]] = Field(
        None, description="List of company domains to filter by"
    ),
    calendar_invitees_domains_type: Optional[str] = Field(
        None, description="Filter by external/internal meetings: 'only_internal' or 'one_or_more_external'"
    ),
    created_after: Optional[str] = Field(
        None, description="ISO 8601 timestamp to filter meetings created after this date"
    ),
    created_before: Optional[str] = Field(
        None, description="ISO 8601 timestamp to filter meetings created before this date"
    ),
    recorded_by: Optional[list[str]] = Field(
        None, description="List of user emails who recorded the meetings"
    ),
    teams: Optional[list[str]] = Field(
        None, description="List of team names to filter by"
    ),
    include_action_items: bool = False,
    include_crm_matches: bool = False,
    include_summary: bool = False,
    include_transcript: bool = False,
) -> dict[str, Any]:
    """
    List meetings recorded by or shared with the authenticated user.

    Supports pagination via cursor and various filtering options including
    participants, date ranges, recording users, and teams. Can optionally
    include action items, CRM matches, summaries, and transcripts.
    """
    params = {}

    if cursor:
        params["cursor"] = cursor

    # Add array parameters
    if calendar_invitees:
        params["calendar_invitees[]"] = calendar_invitees
    if calendar_invitees_domains:
        params["calendar_invitees_domains[]"] = calendar_invitees_domains
    if calendar_invitees_domains_type:
        params["calendar_invitees_domains_type"] = calendar_invitees_domains_type
    if created_after:
        params["created_after"] = created_after
    if created_before:
        params["created_before"] = created_before
    if recorded_by:
        params["recorded_by[]"] = recorded_by
    if teams:
        params["teams[]"] = teams

    # Add include flags
    if include_action_items:
        params["include_action_items"] = "true"
    if include_crm_matches:
        params["include_crm_matches"] = "true"
    if include_summary:
        params["include_summary"] = "true"
    if include_transcript:
        params["include_transcript"] = "true"

    return await make_request("GET", "/meetings", params=params)


# RECORDINGS


@mcp.tool()
async def get_summary(
    recording_id: int = Field(..., description="The ID of the meeting recording"),
    destination_url: Optional[str] = Field(
        None, description="Optional URL for async summary delivery"
    ),
) -> dict[str, Any]:
    """
    Get the summary for a specific meeting recording.

    If destination_url is provided, the summary will be delivered asynchronously
    to that URL. Otherwise, the summary is returned directly.
    """
    params = {}
    if destination_url:
        params["destination_url"] = destination_url

    endpoint = f"/recordings/{recording_id}/summary"
    return await make_request("GET", endpoint, params=params)


@mcp.tool()
async def get_transcript(
    recording_id: int = Field(..., description="The ID of the meeting recording"),
    destination_url: Optional[str] = Field(
        None, description="Optional URL for async transcript delivery"
    ),
) -> dict[str, Any]:
    """
    Get the transcript for a specific meeting recording.

    If destination_url is provided, the transcript will be delivered asynchronously
    to that URL. Otherwise, the transcript is returned directly. The transcript
    includes speaker information, text, and timestamps.
    """
    params = {}
    if destination_url:
        params["destination_url"] = destination_url

    endpoint = f"/recordings/{recording_id}/transcript"
    return await make_request("GET", endpoint, params=params)


# TEAMS


@mcp.tool()
async def list_teams(
    cursor: Optional[str] = Field(None, description="Cursor for pagination"),
) -> dict[str, Any]:
    """
    List all teams accessible to the authenticated user.

    Returns a paginated list of teams with their names and creation dates.
    """
    params = {}
    if cursor:
        params["cursor"] = cursor

    return await make_request("GET", "/teams", params=params)


# TEAM MEMBERS


@mcp.tool()
async def list_team_members(
    cursor: Optional[str] = Field(None, description="Cursor for pagination"),
    team: Optional[str] = Field(None, description="Team name to filter by"),
) -> dict[str, Any]:
    """
    List team members accessible to the authenticated user.

    Can be filtered by team name. Returns member names, emails, and creation dates.
    """
    params = {}
    if cursor:
        params["cursor"] = cursor
    if team:
        params["team"] = team

    return await make_request("GET", "/team_members", params=params)


# WEBHOOKS


@mcp.tool()
async def create_webhook(
    destination_url: str = Field(
        ..., description="The URL where webhook events will be sent"
    ),
    triggered_for: list[str] = Field(
        ...,
        description="Array of recording types that trigger this webhook. Options: 'my_recordings', 'shared_external_recordings', 'my_shared_with_team_recordings', 'shared_team_recordings'",
    ),
    include_action_items: bool = False,
    include_crm_matches: bool = False,
    include_summary: bool = False,
    include_transcript: bool = False,
) -> dict[str, Any]:
    """
    Create a new webhook for receiving meeting notifications.

    At least one of the include_* flags must be true. The webhook will be triggered
    for the specified recording types and will include the requested content.

    Returns the webhook ID, URL, secret (for signature verification), and configuration.
    """
    # Validate that at least one include flag is set
    if not any([
        include_action_items,
        include_crm_matches,
        include_summary,
        include_transcript,
    ]):
        raise ToolError(
            "At least one of include_action_items, include_crm_matches, "
            "include_summary, or include_transcript must be true"
        )

    # Validate triggered_for values
    valid_triggers = {
        "my_recordings",
        "shared_external_recordings",
        "my_shared_with_team_recordings",
        "shared_team_recordings",
    }
    invalid_triggers = set(triggered_for) - valid_triggers
    if invalid_triggers:
        raise ToolError(
            f"Invalid triggered_for values: {invalid_triggers}. "
            f"Valid options are: {valid_triggers}"
        )

    json_data = {
        "destination_url": destination_url,
        "triggered_for": triggered_for,
        "include_action_items": include_action_items,
        "include_crm_matches": include_crm_matches,
        "include_summary": include_summary,
        "include_transcript": include_transcript,
    }

    return await make_request("POST", "/webhooks", json_data=json_data)


@mcp.tool()
async def delete_webhook(
    webhook_id: str = Field(..., description="The ID of the webhook to delete"),
) -> dict[str, Any]:
    """
    Delete a webhook by its ID.

    Returns a success message if the webhook was deleted successfully.
    """
    endpoint = f"/webhooks/{webhook_id}"
    return await make_request("DELETE", endpoint)


# RESOURCES - Provide easy access to API documentation and status


@mcp.resource("fathom://api/info")
def get_api_info() -> str:
    """Get information about the Fathom API."""
    return """# Fathom AI API Information

Base URL: https://api.fathom.ai/external/v1
Rate Limit: 60 requests per 60 seconds

## Available Endpoints:

### Meetings
- list_meetings: List meetings with filtering and pagination

### Recordings
- get_summary: Get meeting summary
- get_transcript: Get meeting transcript

### Teams
- list_teams: List accessible teams

### Team Members
- list_team_members: List team members with optional team filter

### Webhooks
- create_webhook: Create webhook for meeting notifications
- delete_webhook: Delete a webhook by ID

## Authentication
All requests require FATHOM_API_KEY environment variable to be set.
"""


@mcp.resource("fathom://api/rate-limits")
def get_rate_limits() -> str:
    """Get information about API rate limits."""
    return """# Fathom API Rate Limits

Global rate limit: 60 API calls per 60-second window

Rate-limited calls return HTTP 429 status code with headers:
- RateLimit-Limit: Maximum requests allowed
- RateLimit-Remaining: Remaining requests in current window
- RateLimit-Reset: Time left in current window (seconds)

Best practices:
- Implement exponential backoff for 429 responses
- Monitor rate limit headers in responses
- Batch requests where possible
- Cache responses when appropriate
"""


if __name__ == "__main__":
    mcp.run()
