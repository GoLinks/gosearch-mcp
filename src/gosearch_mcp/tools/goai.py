import re
from typing import Annotated

import httpx
from fastmcp import Context
from pydantic import BaseModel, Field

from gosearch_mcp.client import get_authorization_header, http_client


class Link(BaseModel):
    title: str = "Unknown source"
    url: str = ""
    service_name: str = "Unknown"


class Chat(BaseModel):
    type: str = ""
    message: str = ""
    links: list[Link] = []


class Completion(BaseModel):
    message: str = ""
    chat: Chat = Chat()


class GoAIResponse(BaseModel):
    completion: Completion = Completion()
    conversation_id: str | None = None


async def goai_response(
    prompt: Annotated[str, Field(description="The user's prompt to which the AI should respond.", min_length=1)],
    ephemeral: Annotated[bool, Field(description="If true, single response without creating a conversation.")] = True,
    ctx: Context | None = None,
) -> str:
    """Get an AI-generated response from GoAI, powered by the organization's knowledge base."""
    if ctx is None:
        raise PermissionError("Missing request context.")
    authorization = get_authorization_header(ctx)

    data = {"prompt": prompt, "ephemeral": ephemeral}

    try:
        response = await http_client.post(
            "/goai/response",
            data=data,
            headers={"Authorization": authorization},
        )
    except httpx.TimeoutException:
        raise TimeoutError("Request to GoSearch API timed out.")
    except httpx.ConnectError:
        raise ConnectionError("Failed to connect to GoSearch API.")

    if response.status_code == 401:
        raise PermissionError("Invalid or expired API token.")
    if response.status_code == 429:
        raise RuntimeError("Rate limit exceeded. Please try again later.")
    if response.status_code != 200:
        raise RuntimeError(f"GoSearch API returned status {response.status_code}.")

    return format_response(GoAIResponse.model_validate(response.json()))


def format_response(data: GoAIResponse) -> str:
    message = data.completion.chat.message or data.completion.message
    if not message:
        return "No response received."

    cited = {int(m) for m in re.findall(r"!\[(\d+)\]", message)}

    links = data.completion.chat.links
    if cited and links:
        sources = []
        for i in sorted(cited):
            if i <= len(links):
                link = links[i - 1]
                sources.append(f"  [{i}] {link.title}\n      Source: {link.service_name}\n      URL: {link.url}")
        return f"{message}\n\nSources:\n\n" + "\n\n".join(sources)

    return message
