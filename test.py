"""Generic template for calling an OpenAPI/HTTP endpoint."""

import json
import os
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen


def call_api(
	endpoint: str,
	method: str = "GET",
	payload: dict | None = None,
	api_key: str | None = None,
	timeout: int = 30,
) -> dict | list | str:
	"""Send a JSON request to an API and return its decoded response."""
	headers = {
		"Accept": "application/json",
		"Content-Type": "application/json",
	}
	if api_key:
		headers["Authorization"] = f"Bearer {api_key}"

	body = json.dumps(payload).encode("utf-8") if payload is not None else None
	request = Request(endpoint, data=body, headers=headers, method=method.upper())

	try:
		with urlopen(request, timeout=timeout) as response:
			text = response.read().decode("utf-8")
			return json.loads(text) if text else {}
	except HTTPError as error:
		details = error.read().decode("utf-8", errors="replace")
		raise RuntimeError(f"API returned HTTP {error.code}: {details}") from error
	except URLError as error:
		raise RuntimeError(f"Could not connect to API: {error.reason}") from error


if __name__ == "__main__":
	# Configure these values, or set API_URL/API_KEY in the environment.
	url = os.getenv("API_URL", "https://api.example.com/v1/resource")
	key = os.getenv("API_KEY")
	response = call_api(url, method="GET", api_key=key)
	print(json.dumps(response, indent=2))
