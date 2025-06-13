import datetime
import os, json, re
import requests
from jinja2 import Environment, FileSystemLoader
from openai import AzureOpenAI, OpenAI
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

from semantic_kernel.kernel import Kernel
from semantic_kernel.connectors.ai.open_ai.services.azure_chat_completion import AzureChatCompletion
from semantic_kernel.connectors.ai.open_ai.services.open_ai_chat_completion import OpenAIChatCompletion
from semantic_kernel.agents import AgentGroupChat, ChatCompletionAgent
from semantic_kernel.agents.strategies.selection.kernel_function_selection_strategy import (
    KernelFunctionSelectionStrategy,
)
from semantic_kernel.agents.strategies.termination.kernel_function_termination_strategy import (
    KernelFunctionTerminationStrategy,
)
from semantic_kernel.functions.kernel_function_from_prompt import KernelFunctionFromPrompt

from azure.identity import DefaultAzureCredential
from semantic_kernel.connectors.search_engine import BingConnector
from semantic_kernel.core_plugins import WebSearchEnginePlugin
from semantic_kernel.connectors.ai.function_choice_behavior import FunctionChoiceBehavior
from azure.core.exceptions import ClientAuthenticationError
from azure.identity import DefaultAzureCredential
from semantic_kernel.exceptions.function_exceptions import FunctionExecutionException
from semantic_kernel.functions import KernelArguments

from src.plugins.resume_screening import ResumeScreeningPlugin


class GeminiWrapper:
    """Wrapper class to make Gemini API compatible with OpenAI interface"""
    
    def __init__(self, api_key):
        genai.configure(api_key=api_key)
        self.chat = GeminiChatCompletions()


class GeminiChatCompletions:
    """Chat completions interface for Gemini"""
    
    def __init__(self):
        self.completions = self
    
    def create(self, model, messages, max_tokens=None, max_completion_tokens=None, **kwargs):
        # Convert OpenAI messages format to Gemini format
        gemini_model = genai.GenerativeModel(model)
        
        # Extract the user message (assuming simple user message for now)
        user_message = ""
        system_message = ""
        
        for message in messages:
            if message["role"] == "user":
                user_message = message["content"]
            elif message["role"] == "system":
                system_message = message["content"]
        
        # Combine system and user messages for Gemini
        final_message = f"{system_message}\n\n{user_message}" if system_message else user_message
        
        # Generate response
        try:
            response = gemini_model.generate_content(final_message)
            return GeminiResponse(response.text, model)
        except Exception as e:
            # If response is blocked, return a default message
            if "blocked" in str(e).lower():
                return GeminiResponse("I apologize, but I cannot process this request due to safety guidelines.", model)
            else:
                raise e


class GeminiResponse:
    """Response wrapper to match OpenAI response format"""
    
    def __init__(self, text, model):
        self.choices = [GeminiChoice(text)]
        self.model = model
    
    def model_dump_json(self):
        return json.dumps({
            "choices": [{"message": {"content": self.choices[0].message.content}}]
        })


class GeminiChoice:
    """Choice wrapper for Gemini response"""
    
    def __init__(self, text):
        self.message = GeminiMessage(text)


class GeminiMessage:
    """Message wrapper for Gemini response"""
    
    def __init__(self, text):
        self.content = text


class LocalLLMWrapper:
    """Wrapper class to make Local LLM API compatible with OpenAI interface"""
    
    def __init__(self, base_url="http://localhost:1234/v1"):
        self.base_url = base_url
        self.chat = LocalLLMChatCompletions(base_url)


class LocalLLMChatCompletions:
    """Chat completions interface for Local LLM"""
    
    def __init__(self, base_url):
        self.base_url = base_url
        self.completions = self
    
    def create(self, model, messages, max_tokens=None, max_completion_tokens=None, temperature=0.7, **kwargs):
        """Create a chat completion using the local LLM API"""
        # Prepare the request payload
        payload = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_completion_tokens or max_tokens or 1000,
            "stream": False
        }
        
        try:
            # Make request to local LLM server
            response = requests.post(
                f"{self.base_url}/chat/completions",
                headers={"Content-Type": "application/json"},
                json=payload,
                timeout=60
            )
            
            if response.status_code == 200:
                response_data = response.json()
                return LocalLLMResponse(response_data, model)
            else:
                raise Exception(f"Local LLM API error: {response.status_code} - {response.text}")
                
        except requests.exceptions.ConnectionError:
            raise Exception("Could not connect to local LLM server. Make sure it's running on http://localhost:1234")
        except requests.exceptions.Timeout:
            raise Exception("Local LLM request timed out. The model might be processing a complex request.")
        except Exception as e:
            raise Exception(f"Local LLM API error: {str(e)}")


class LocalLLMResponse:
    """Response wrapper to match OpenAI response format"""
    
    def __init__(self, response_data, model):
        self.choices = [LocalLLMChoice(choice) for choice in response_data.get('choices', [])]
        self.model = model
        self.usage = response_data.get('usage', {})
    
    def model_dump_json(self):
        return json.dumps({
            "choices": [{"message": {"content": choice.message.content}} for choice in self.choices],
            "model": self.model,
            "usage": self.usage
        })


class LocalLLMChoice:
    """Choice wrapper for Local LLM response"""
    
    def __init__(self, choice_data):
        self.message = LocalLLMMessage(choice_data.get('message', {}))
        self.index = choice_data.get('index', 0)
        self.finish_reason = choice_data.get('finish_reason', 'stop')


class LocalLLMMessage:
    """Message wrapper for Local LLM response"""
    
    def __init__(self, message_data):
        self.content = message_data.get('content', '')
        self.role = message_data.get('role', 'assistant')


def get_ai_service_config():
    """
    Determine which AI service to use based on AI_SERVICE environment variable.
    Returns a tuple of (service_type, client, model_name, model_orchestrator)
    """
    ai_service = os.getenv("AI_SERVICE", "").lower()
    
    if ai_service == "azure":
        # Azure OpenAI Configuration
        azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        azure_api_key = os.getenv("AZURE_OPENAI_API_KEY")
        azure_model = os.getenv("AZURE_OPENAI_MODEL", "gpt-4o-mini")
        azure_model_orchestrator = os.getenv("AZURE_OPENAI_MODEL_ORCHESTRATOR", "gpt-4o-mini")
        
        if not azure_endpoint or not azure_api_key or azure_api_key == "your-azure-openai-api-key-here":
            raise ValueError("Azure OpenAI selected but credentials are missing. Please check AZURE_OPENAI_ENDPOINT and AZURE_OPENAI_API_KEY in .env file.")
        
        try:
            client = AzureOpenAI(
                azure_endpoint=azure_endpoint,
                api_key=azure_api_key,
                api_version=os.getenv("AZURE_OPENAI_API_VERSION", "2024-12-01-preview")
            )
            print(f"✅ Using Azure OpenAI with model: {azure_model_orchestrator}")
            return ("azure", client, azure_model, azure_model_orchestrator)
        except Exception as e:
            raise ValueError(f"Failed to initialize Azure OpenAI: {str(e)}")
    
    elif ai_service == "openai":
        # OpenAI Configuration
        openai_api_key = os.getenv("OPENAI_API_KEY")
        openai_model = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        openai_model_orchestrator = os.getenv("OPENAI_MODEL_ORCHESTRATOR", "gpt-4o-mini")
        
        if not openai_api_key or openai_api_key == "sk-your-openai-api-key-here":
            raise ValueError("OpenAI selected but API key is missing. Please check OPENAI_API_KEY in .env file.")
        
        try:
            client = OpenAI(api_key=openai_api_key)
            print(f"✅ Using OpenAI with model: {openai_model_orchestrator}")
            return ("openai", client, openai_model, openai_model_orchestrator)
        except Exception as e:
            raise ValueError(f"Failed to initialize OpenAI: {str(e)}")
    
    elif ai_service == "gemini":
        # Gemini Configuration
        gemini_api_key = os.getenv("GEMINI_API_KEY")
        gemini_model = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
        gemini_model_orchestrator = os.getenv("GEMINI_MODEL_ORCHESTRATOR", "gemini-1.5-flash")
        
        if not gemini_api_key:
            raise ValueError("Gemini selected but API key is missing. Please check GEMINI_API_KEY in .env file.")
        
        try:
            client = GeminiWrapper(gemini_api_key)
            print(f"✅ Using Google Gemini with model: {gemini_model_orchestrator}")
            return ("gemini", client, gemini_model, gemini_model_orchestrator)
        except Exception as e:
            raise ValueError(f"Failed to initialize Gemini: {str(e)}")
    
    elif ai_service == "local":
        # Local LLM Configuration
        local_base_url = os.getenv("LOCAL_LLM_BASE_URL", "http://localhost:1234/v1")
        local_model = os.getenv("LOCAL_LLM_MODEL", "gemma-3-4b-it-qat")
        local_model_orchestrator = os.getenv("LOCAL_LLM_MODEL_ORCHESTRATOR", "gemma-3-4b-it-qat")
        
        try:
            client = LocalLLMWrapper(local_base_url)
            # Test connection by making a simple request
            test_response = client.chat.completions.create(
                model=local_model,
                messages=[{"role": "user", "content": "Hello"}],
                max_completion_tokens=10
            )
            print(f"✅ Using Local LLM at {local_base_url} with model: {local_model_orchestrator}")
            return ("local", client, local_model, local_model_orchestrator)
        except Exception as e:
            raise ValueError(f"Failed to connect to Local LLM at {local_base_url}: {str(e)}")
    
    else:
        raise ValueError(f"Invalid AI_SERVICE '{ai_service}'. Please set AI_SERVICE to 'azure', 'openai', 'gemini', or 'local' in your .env file.")


class Orchestrator:

    def __init__(self, screening_context, num_agents):
        self.service_type, self.client, self.model, self.model_orchestrator = get_ai_service_config()
        
        self.env = Environment(loader=FileSystemLoader(os.getenv('TEMPLATE_DIR_PROMPTS')))
        self.template = self.env.get_template(os.getenv('TEMPLATE_SYSTEM_ORCHESTRATOR'))
        self.screening_context = screening_context
        self.num_agents = num_agents
        
        print(f"Using {self.service_type.upper()} service with model: {self.model_orchestrator}")

    def get_response(self):
        response = self.client.chat.completions.create(
            model=self.model_orchestrator,
            messages=[
                {"role": "user", "content": self.template.render(
                    job_profile=self.screening_context['job_profile'],
                    num_resumes=self.screening_context['num_resumes'],
                    num_agents=self.num_agents
                )},
            ],
            max_completion_tokens=5000
        )
        return response

    def parse_response(self, response):
        json_response = json.loads(response.model_dump_json())
        json_response = json.loads(json_response['choices'][0]['message']['content'].replace('```json\n', '').replace('```', ''))
        return json_response

    def get_dynamic_agents(self, json_response):
        agents = []
        for agent_info in json_response.get('agents', []):
            agent = {
                'name': agent_info['name'],
                'role': agent_info['role'],
                'system_prompt': agent_info['system_prompt'],
            }
            agents.append(agent)
        return agents

    def run(self):
        response = self.get_response()
        json_response = self.parse_response(response)
        print(f'Creating dynamic agents who will be responsible for resume screening and matching analysis.')
        dynamic_agents = self.get_dynamic_agents(json_response)
        return dynamic_agents


class ApprovalTerminationStrategy(KernelFunctionTerminationStrategy):
    """A strategy for determining when an agent should terminate."""

    async def should_agent_terminate(self, agent, history):
        """Check if the agent should terminate."""
        return "approved" in history[-1].content.lower()


class MultiAgent:
    def __init__(self):
        self.service_type, self.client, self.model, self.model_orchestrator = get_ai_service_config()
        
        # Initialize Bing connector only if API key is available
        bing_api_key = os.getenv("BING_API_KEY")
        if bing_api_key and bing_api_key != "your-bing-api-key-here":
            try:
                self.bing_connector = BingConnector(bing_api_key)
                self.has_bing = True
                print("✅ Bing Search enabled")
            except Exception as e:
                print(f"⚠️ Bing Search disabled: {str(e)}")
                self.bing_connector = None
                self.has_bing = False
        else:
            print("⚠️ Bing Search disabled: No API key provided")
            self.bing_connector = None
            self.has_bing = False
        
        self.env = Environment(loader=FileSystemLoader(os.getenv('TEMPLATE_DIR_PROMPTS')))
        self.template_termination = self.env.get_template(os.getenv('TEMPLATE_TERMINATION'))
        self.template_selection = self.env.get_template(os.getenv('TEMPLATE_SELECTION'))
    
    def _create_kernel_with_chat_completion(self, service_id: str, deployment_name: str) -> Kernel:
        kernel = Kernel()
        if self.service_type == "azure":
            kernel.add_service(AzureChatCompletion(service_id=service_id, 
                                                   deployment_name=deployment_name))
        elif self.service_type == "openai":
            kernel.add_service(OpenAIChatCompletion(service_id=service_id, 
                                                    ai_model_id=deployment_name))
        else:  # Gemini - create a minimal kernel without chat completion service
            # For Gemini, we'll use a simplified approach that doesn't require OpenAI
            # We'll handle the chat completion directly with Gemini API
            pass  # Don't add any chat completion service for Gemini
        return kernel
    
    def _standardize_string(self, input_string: str) -> str:
        return re.sub(r'[^0-9A-Za-z_-]', '_', input_string)
    
    def create_agents(self, dynamic_agents):
        expert_agents = []
        
        if self.service_type == "gemini":
            # For Gemini, create proper agent objects
            for agent in dynamic_agents:
                agent_name = self._standardize_string(agent['name'])
                # Create a proper GeminiAgent object
                expert_agent = GeminiAgent(
                    agent_id=agent_name,
                    name=agent_name,
                    instructions=agent['system_prompt'],
                    client=self.client,
                    model=self.model
                )
                expert_agents.append(expert_agent)
                print(f"Created Gemini agent: {agent_name}")
            return expert_agents
        
        elif self.service_type == "local":
            # For Local LLM, create simple agent objects similar to Gemini
            for agent in dynamic_agents:
                agent_name = self._standardize_string(agent['name'])
                # Create a LocalLLMAgent object
                expert_agent = LocalLLMAgent(
                    agent_id=agent_name,
                    name=agent_name,
                    instructions=agent['system_prompt'],
                    client=self.client,
                    model=self.model
                )
                expert_agents.append(expert_agent)
                print(f"Created Local LLM agent: {agent_name}")
            return expert_agents
        
        # For Azure/OpenAI, use the existing Semantic Kernel approach
        for agent in dynamic_agents:

            agent_name = self._standardize_string(agent['name'])
            kernel = self._create_kernel_with_chat_completion(agent_name, self.model)            
        
            # Configure the function choice behavior to auto invoke kernel functions
            settings = kernel.get_prompt_execution_settings_from_service_id(service_id=agent_name)
            settings.function_choice_behavior = FunctionChoiceBehavior.Auto()

            # Add WebSearch plugin only if Bing is available
            if self.has_bing:
                kernel.add_plugin(WebSearchEnginePlugin(self.bing_connector), "WebSearch")
            
            kernel.add_plugin(ResumeScreeningPlugin(), "ResumeScreening")
           
            expert = ChatCompletionAgent(id=agent_name,
                                         kernel=kernel,
                                         name=agent_name,
                                         instructions=agent['system_prompt'],
                                         arguments=KernelArguments(settings=settings),         
                                        )
            expert_agents.append(expert)

            print(f"Created agent: {expert.name}, agent ID: {expert.id} ")
        return expert_agents
    
    def create_selection_function(self, expert_agents):
        if self.service_type == "gemini" or self.service_type == "local":
            # For Gemini and Local LLM, we'll use a simplified selection approach
            # Convert agent objects to names for the template
            agent_names = [agent.name for agent in expert_agents]
            selection_function = KernelFunctionFromPrompt(function_name="selection",
                                                          prompt=self.template_selection.render(expert_agents=agent_names,
                                                                                                history=f"{{{{$history}}}}"))
        else:
            # For Azure/OpenAI, use the existing approach
            selection_function = KernelFunctionFromPrompt(function_name="selection",
                                                          prompt=self.template_selection.render(expert_agents=expert_agents,
                                                                                                history=f"{{{{$history}}}}"))
        return selection_function
    
    def create_termination_function(self, termination_keyword):
        selection_function = KernelFunctionFromPrompt(function_name="termination",
                                                      prompt=self.template_termination.render(termination_keyword=termination_keyword,
                                                                                              history=f"{{{{$history}}}}"))
              
        return selection_function

    def create_chat_group(self, expert_agents, selection_function, termination_function, termination_keyword):
        if self.service_type == "gemini":
            # For Gemini, create a simplified chat group that doesn't use Semantic Kernel
            return GeminiChatGroup(expert_agents, termination_keyword)
        elif self.service_type == "local":
            # For Local LLM, create a simplified chat group similar to Gemini
            return LocalLLMChatGroup(expert_agents, termination_keyword)
        
        # For Azure/OpenAI, use the existing Semantic Kernel approach
        group = AgentGroupChat(agents=expert_agents,
                               selection_strategy=KernelFunctionSelectionStrategy(
                                    function=selection_function,
                                    kernel=self._create_kernel_with_chat_completion("selection", self.model),
                                    result_parser=lambda result: str(result.value[0]) if result.value is not None else expert_agents[-1].name,
                                    agent_variable_name="agents",
                                    history_variable_name="history",
                                ),
                                termination_strategy=KernelFunctionTerminationStrategy(
                                    agents=[expert_agents[-1]],
                                    function=termination_function,
                                    kernel=self._create_kernel_with_chat_completion("termination", self.model),
                                    result_parser=lambda result: termination_keyword in str(result.value[0]).lower(),
                                    history_variable_name="history",
                                    maximum_iterations=2,
                                ),
                        )
          
        return group


    def auth_callback_factory(self, scope):
        auth_token = None
        async def auth_callback() -> str:
            """Auth callback for the SessionsPythonTool.
            This is a sample auth callback that shows how to use Azure's DefaultAzureCredential
            to get an access token.
            """
            nonlocal auth_token
            current_utc_timestamp = int(datetime.datetime.now(datetime.timezone.utc).timestamp())

            if not auth_token or auth_token.expires_on < current_utc_timestamp:
                credential = DefaultAzureCredential()

                try:
                    auth_token = credential.get_token(scope)
                except ClientAuthenticationError as cae:
                    err_messages = getattr(cae, "messages", [])
                    raise FunctionExecutionException(
                        f"Failed to retrieve the client auth token with messages: {' '.join(err_messages)}"
                    ) from cae

            return auth_token.token
        
        return auth_callback


class GeminiAgent:
    """Simple agent class for Gemini"""
    
    def __init__(self, agent_id, name, instructions, client, model):
        self.id = agent_id
        self.name = name
        self.instructions = instructions
        self.client = client
        self.model = model


class GeminiChatGroup:
    """Simplified chat group for Gemini agents"""
    
    def __init__(self, agents, termination_keyword):
        self.agents = agents
        self.termination_keyword = termination_keyword
        self.is_complete = False
        self.history = []
    
    async def add_chat_message(self, message):
        """Add a message to the chat history"""
        self.history.append(message)
    
    async def invoke(self):
        """Invoke the chat group to process messages"""
        if not self.history:
            return
        
        # Get the last message
        last_message = self.history[-1]
        
        # Process with each agent
        for agent in self.agents:
            # Create a prompt combining the agent's instructions with the user message
            prompt = f"""
            You are {agent.name}. Your role: {agent.instructions}
            
            User request: {last_message.content}
            
            Please provide your analysis and recommendations based on your role.
            """
            
            try:
                # Generate response using Gemini
                response = agent.client.chat.completions.create(
                    model=agent.model,
                    messages=[{"role": "user", "content": prompt}],
                    max_completion_tokens=1000
                )
                
                # Parse the response
                response_text = response.choices[0].message.content
                
                # Create a mock response object similar to Semantic Kernel's format
                mock_response = type('MockResponse', (), {
                    'role': 'assistant',
                    'name': agent.name,
                    'content': response_text
                })()
                
                yield mock_response
                
                # Check for termination
                if self.termination_keyword.lower() in response_text.lower():
                    self.is_complete = True
                    break
                    
            except Exception as e:
                # Handle errors gracefully
                error_response = type('ErrorResponse', (), {
                    'role': 'assistant',
                    'name': agent.name,
                    'content': f"I apologize, but I encountered an error while processing your request: {str(e)}"
                })()
                yield error_response
    
    async def invoke_stream(self):
        """Streaming version of invoke - alias for invoke since we already yield responses"""
        async for response in self.invoke():
            yield response
    
    async def reset(self):
        """Reset the chat group"""
        self.history = []
        self.is_complete = False


class LocalLLMAgent:
    """Simple agent class for Local LLM"""
    
    def __init__(self, agent_id, name, instructions, client, model):
        self.id = agent_id
        self.name = name
        self.instructions = instructions
        self.client = client
        self.model = model


class LocalLLMChatGroup:
    """Simplified chat group for Local LLM agents"""
    
    def __init__(self, agents, termination_keyword):
        self.agents = agents
        self.termination_keyword = termination_keyword
        self.is_complete = False
        self.history = []
    
    async def add_chat_message(self, message):
        """Add a message to the chat history"""
        self.history.append(message)
    
    async def invoke(self):
        """Invoke the chat group to process messages"""
        if not self.history:
            return
        
        # Get the last message
        last_message = self.history[-1]
        
        # Process with each agent
        for agent in self.agents:
            # Create a prompt combining the agent's instructions with the user message
            prompt = f"""
            You are {agent.name}. Your role: {agent.instructions}
            
            User request: {last_message.content}
            
            Please provide your analysis and recommendations based on your role.
            """
            
            try:
                # Generate response using Local LLM
                response = agent.client.chat.completions.create(
                    model=agent.model,
                    messages=[{"role": "user", "content": prompt}],
                    max_completion_tokens=1000,
                    temperature=0.7
                )
                
                # Parse the response
                response_text = response.choices[0].message.content
                
                # Create a mock response object similar to Semantic Kernel's format
                mock_response = type('MockResponse', (), {
                    'role': 'assistant',
                    'name': agent.name,
                    'content': response_text
                })()
                
                yield mock_response
                
                # Check for termination
                if self.termination_keyword.lower() in response_text.lower():
                    self.is_complete = True
                    break
                    
            except Exception as e:
                # Handle errors gracefully
                error_response = type('ErrorResponse', (), {
                    'role': 'assistant',
                    'name': agent.name,
                    'content': f"I apologize, but I encountered an error while processing your request: {str(e)}"
                })()
                yield error_response
    
    async def invoke_stream(self):
        """Streaming version of invoke - alias for invoke since we already yield responses"""
        async for response in self.invoke():
            yield response
    
    async def reset(self):
        """Reset the chat group"""
        self.history = []
        self.is_complete = False
