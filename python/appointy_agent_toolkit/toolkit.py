"""Appointy Agent Toolkit."""

from typing import List, Optional
from pydantic import PrivateAttr

from .api import AppointyAPI
from .tools import tools
from .configuration import Configuration, is_tool_allowed
from .tool import AppointyTool


class AppointyAgentToolkit:
    _tools: List = PrivateAttr(default=[])

    def __init__(
        self, api_key: str, configuration: Optional[Configuration] = None
    ):
        super().__init__()

        context = configuration.get("context") if configuration else None

        appointy_api = AppointyAPI(api_key=api_key, context=context)

        filtered_tools = [
            tool for tool in tools if is_tool_allowed(tool, configuration)
        ]

        self._tools = [
            AppointyTool(
                name=tool["method"],
                description=tool["description"],
                method=tool["method"],
                appointy_api=appointy_api,
                args_schema=tool.get("args_schema", None),
            )
            for tool in filtered_tools
        ]

    def get_tools(self) -> List:
        """Get the tools in the toolkit."""
        return self._tools