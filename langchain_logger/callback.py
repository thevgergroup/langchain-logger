"""Callback Handler that prints to std out."""
from __future__ import annotations
from logging import Logger

from typing import TYPE_CHECKING, Any, Dict, List, Optional
from uuid import UUID

from langchain_core.callbacks.base import BaseCallbackHandler
from langchain_core.utils import print_text, get_colored_text

if TYPE_CHECKING:
    from langchain_core.agents import AgentAction, AgentFinish


class ChainOfThoughtCallbackHandler(BaseCallbackHandler):
    """Callback Handler that uses a logger to capture steps."""

    def __init__(self, color: Optional[str] = None, logger:Logger = None) -> None:
        """Initialize callback handler."""
        self.color = color
        self.logger = logger
        
    def on_llm_start(self, serialized: Dict[str, Any], prompts: List[str], *, 
                        run_id: UUID, parent_run_id: UUID | None = None, tags: List[str] | None = None, 
                        metadata: Dict[str, Any] | None = None, **kwargs: Any) -> Any:
        
        self.logger.info(">> Starting LLM")
        class_name = serialized.get("name", serialized.get("id", ["<unknown>"])[-1])
        self.logger.info(f"\n\n\033[1m> Entering new {class_name} LLM Start...\033[0m")
        for prompt in prompts:
            self.logger.info(get_colored_text(prompt, "blue"))
        
        #return super().on_llm_start(serialized, prompts, run_id=run_id, parent_run_id=parent_run_id, tags=tags, metadata=metadata, **kwargs)

    def on_llm_end(self, outputs: List[str], 
                   *, run_id: UUID, parent_run_id: UUID | None = None, 
                   tags: List[str] | None = None, 
                   metadata: Dict[str, Any] | None = None, **kwargs: Any) -> Any:
        
        self.logger.info(">> Ending LLM")
        for output in outputs:
            self.logger.info(get_colored_text(output, "green"))
        
        #self.logger.info(outputs)
        #return super().on_llm_end(outputs, run_id=run_id, parent_run_id=parent_run_id, tags=tags, metadata=metadata, **kwargs)
    
    def on_tool_start(self, serialized: Dict[str, Any], input_str: str, *, run_id: UUID, parent_run_id: UUID | None = None, tags: List[str] | None = None, metadata: Dict[str, Any] | None = None, inputs: Dict[str, Any] | None = None, **kwargs: Any) -> Any:
        self.logger.info(">> Starting Tool")
        self.logger.info(input_str)
        

    def on_chain_start(self, serialized: Dict[str, Any], inputs: Dict[str, Any], **kwargs: Any  ) -> None:
        """Print out that we are entering a chain."""
        class_name = serialized.get("name", serialized.get("id", ["<unknown>"])[-1])
        self.logger.info(f"\n\n\033[1m> Entering new {class_name} chain...\033[0m")

    def on_chain_end(self, outputs: Dict[str, Any], **kwargs: Any) -> None:
        """Print out that we finished a chain."""
        self.logger.info("\n\033[1m> Finished chain.\033[0m")

    def on_agent_action(
        self, action: AgentAction, color: Optional[str] = None, **kwargs: Any
    ) -> Any:
        """Run on agent action."""
        text = action.log
        text_to_print = get_colored_text(text, color) if color else text
        self.logger.info(text_to_print)

    def on_tool_end(
        self,
        output: str,
        color: Optional[str] = None,
        observation_prefix: Optional[str] = None,
        llm_prefix: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        """If not the final action, print out observation."""
        if observation_prefix is not None:
            #print_text(f"\n{observation_prefix}")
            self.logger.info(f"\n{observation_prefix}")
        #print_text(output, color=color or self.color)
        text_to_print = get_colored_text(output, color=color or self.color) 
        self.logger.info(text_to_print)
        if llm_prefix is not None:
            self.logger.info(f"\n{llm_prefix}")

    def on_text(
        self,
        text: str,
        color: Optional[str] = None,
        end: str = "",
        **kwargs: Any,
    ) -> None:
        """Run when agent ends."""
        text_to_print = get_colored_text(text, color=color or self.color, end=end)
        self.logger.info(text_to_print)

    def on_agent_finish(
        self, finish: AgentFinish, color: Optional[str] = None, **kwargs: Any
    ) -> None:
        """Run on agent end."""
        text_to_print = get_colored_text(finish.log, color=color or self.color)
        self.logger.info(text_to_print)
    
    