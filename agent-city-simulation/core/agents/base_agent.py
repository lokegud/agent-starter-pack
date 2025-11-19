"""Base Agent class for all Agent City agents"""

import os
import logging
from typing import Dict, Any, Optional, List
from anthropic import Anthropic
from dotenv import load_dotenv
import yaml

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(
    level=os.getenv('LOG_LEVEL', 'INFO'),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class BaseAgent:
    """Base class for all Agent City agents"""

    def __init__(
        self,
        agent_type: str,
        agent_id: Optional[str] = None,
        personality: Optional[Dict] = None,
        config_path: str = "agent-city-simulation/config.yaml"
    ):
        """
        Initialize base agent

        Args:
            agent_type: Type of agent (scout, evaluator, designer, etc.)
            agent_id: Unique identifier for this agent instance
            personality: Personality traits dict (risk_tolerance, etc.)
            config_path: Path to configuration file
        """
        self.agent_type = agent_type
        self.agent_id = agent_id or f"{agent_type}_{os.urandom(4).hex()}"
        self.personality = personality or {"risk_tolerance": 0.5}

        # Load configuration
        self.config = self._load_config(config_path)

        # Initialize Claude client
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key or api_key == "your-anthropic-key-here":
            logger.warning(f"[{self.agent_type}] Anthropic API key not set. Please update .env file.")
            self.client = None
        else:
            self.client = Anthropic(api_key=api_key)

        # Get model from config
        self.model = self.config.get('anthropic', {}).get('model', 'claude-3-5-sonnet-20241022')
        self.max_tokens = self.config.get('anthropic', {}).get('max_tokens', 4096)
        self.temperature = self.config.get('anthropic', {}).get('temperature', 0.7)

        logger.info(f"[{self.agent_id}] Initialized {agent_type} agent")

    def _load_config(self, config_path: str) -> Dict:
        """Load configuration from YAML file"""
        try:
            with open(config_path, 'r') as f:
                return yaml.safe_load(f)
        except FileNotFoundError:
            logger.warning(f"Config file not found: {config_path}. Using defaults.")
            return {}

    async def think(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None
    ) -> str:
        """
        Call Claude API to process a task

        Args:
            prompt: The user prompt
            system_prompt: Optional system prompt (defaults to agent type)
            temperature: Optional temperature override

        Returns:
            Claude's response text
        """
        if not self.client:
            raise RuntimeError("Anthropic API client not initialized. Check your API key in .env")

        try:
            logger.info(f"[{self.agent_id}] Thinking about task...")

            messages = [{"role": "user", "content": prompt}]

            response = self.client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                temperature=temperature or self.temperature,
                system=system_prompt or f"You are a {self.agent_type} agent in Agent City.",
                messages=messages
            )

            result = response.content[0].text
            logger.info(f"[{self.agent_id}] Task completed ({len(result)} chars)")
            return result

        except Exception as e:
            logger.error(f"[{self.agent_id}] Error: {e}")
            raise

    def log_task(
        self,
        task: str,
        status: str,
        output: Any = None,
        error: Optional[str] = None
    ):
        """
        Log agent activity

        Args:
            task: Description of the task
            status: Status (started, completed, failed)
            output: Optional output data
            error: Optional error message
        """
        log_msg = f"[{self.agent_id}] Task: {task} | Status: {status}"

        if status == "failed" and error:
            logger.error(f"{log_msg} | Error: {error}")
        elif status == "completed":
            logger.info(log_msg)
            if output:
                logger.debug(f"[{self.agent_id}] Output: {output}")
        else:
            logger.info(log_msg)

    def get_personality_trait(self, trait: str, default: float = 0.5) -> float:
        """
        Get a personality trait value

        Args:
            trait: Trait name (risk_tolerance, analytical, etc.)
            default: Default value if trait not set

        Returns:
            Trait value (0.0 to 1.0)
        """
        return self.personality.get(trait, default)
