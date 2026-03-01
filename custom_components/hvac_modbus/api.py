"""API Client for HVAC Backend."""

import asyncio
import logging
from typing import Any, Optional

import aiohttp
from aiohttp import ClientError, ClientResponseError

from .const import API_ENDPOINTS, DEFAULT_PORT

_LOGGER = logging.getLogger(__name__)


class HVACApiError(Exception):
    """Exception for HVAC API errors."""
    pass


class HVACApiClient:
    """Client to communicate with HVAC Backend API."""

    def __init__(
        self,
        host: str,
        port: int = DEFAULT_PORT,
        api_key: Optional[str] = None,
        session: Optional[aiohttp.ClientSession] = None,
    ):
        """Initialize the API client."""
        self._host = host
        self._port = port
        self._api_key = api_key
        self._session = session
        self._own_session = session is None
        self._base_url = f"http://{host}:{port}"

    async def _get_session(self) -> aiohttp.ClientSession:
        """Get or create aiohttp session."""
        if self._session is None:
            self._session = aiohttp.ClientSession()
            self._own_session = True
        return self._session

    async def close(self) -> None:
        """Close the aiohttp session if we own it."""
        if self._own_session and self._session is not None:
            await self._session.close()
            self._session = None

    def _get_headers(self) -> dict[str, str]:
        """Get request headers."""
        headers = {"Content-Type": "application/json"}
        if self._api_key:
            headers["Authorization"] = f"Bearer {self._api_key}"
        return headers

    async def _request(
        self,
        method: str,
        endpoint: str,
        data: Optional[dict] = None,
        retries: int = 3,
        timeout: int = 10,
    ) -> dict[str, Any]:
        """Make an HTTP request with retry logic."""
        session = await self._get_session()
        url = f"{self._base_url}{endpoint}"
        
        for attempt in range(retries):
            try:
                async with asyncio.timeout(timeout):
                    if method == "GET":
                        async with session.get(
                            url, headers=self._get_headers()
                        ) as response:
                            response.raise_for_status()
                            return await response.json()
                    elif method == "PUT":
                        async with session.put(
                            url, headers=self._get_headers(), json=data
                        ) as response:
                            response.raise_for_status()
                            return await response.json()
                    elif method == "POST":
                        async with session.post(
                            url, headers=self._get_headers(), json=data
                        ) as response:
                            response.raise_for_status()
                            return await response.json()
            except asyncio.TimeoutError:
                _LOGGER.warning(
                    "Timeout on attempt %d/%d for %s", attempt + 1, retries, url
                )
                if attempt == retries - 1:
                    raise HVACApiError(f"Timeout after {retries} attempts")
            except ClientResponseError as err:
                _LOGGER.error("HTTP error %d: %s", err.status, err.message)
                raise HVACApiError(f"HTTP error {err.status}: {err.message}")
            except ClientError as err:
                _LOGGER.error("Client error: %s", str(err))
                if attempt == retries - 1:
                    raise HVACApiError(f"Connection error: {str(err)}")
            
            await asyncio.sleep(1 * (attempt + 1))
        
        raise HVACApiError("Unknown error")

    async def get_rooms(self) -> list[dict[str, Any]]:
        """Get all rooms data."""
        return await self._request("GET", API_ENDPOINTS["rooms"])

    async def get_room(self, room_id: str) -> dict[str, Any]:
        """Get single room data."""
        return await self._request("GET", f"{API_ENDPOINTS['rooms']}/{room_id}")

    async def set_room_setpoint(self, room_id: str, temperature: float) -> dict[str, Any]:
        """Set room temperature setpoint."""
        return await self._request(
            "PUT",
            f"{API_ENDPOINTS['rooms']}/{room_id}",
            data={"temp": temperature},
        )

    async def get_system(self) -> dict[str, Any]:
        """Get system control data."""
        return await self._request("GET", API_ENDPOINTS["system"])

    async def set_system(
        self,
        power: Optional[bool] = None,
        home_mode: Optional[bool] = None,
        run_mode: Optional[int] = None,
        fan_speed: Optional[int] = None,
    ) -> dict[str, Any]:
        """Set system control parameters."""
        data = {}
        if power is not None:
            data["power"] = power
        if home_mode is not None:
            data["home_mode"] = home_mode
        if run_mode is not None:
            data["run_mode"] = run_mode
        if fan_speed is not None:
            data["fan_speed"] = fan_speed
        return await self._request("PUT", API_ENDPOINTS["system"], data=data)

    async def get_grouped_registers(self) -> dict[str, Any]:
        """Get all registers grouped by category."""
        return await self._request("GET", API_ENDPOINTS["registers"])

    async def get_status(self) -> dict[str, Any]:
        """Get connection status."""
        return await self._request("GET", API_ENDPOINTS["status"])

    async def write_register(self, address: int, value: float) -> dict[str, Any]:
        """Write to a register by address."""
        return await self._request(
            "POST",
            "/api/registers/write",
            data={"address": address, "value": value},
        )

    async def test_connection(self) -> bool:
        """Test if the connection to the backend is working."""
        try:
            status = await self.get_status()
            return status.get("connected", False)
        except HVACApiError:
            return False
