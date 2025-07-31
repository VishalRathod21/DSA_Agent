import streamlit as st
import asyncio
import time
import os
from dotenv import load_dotenv
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.base import TaskResult
from utils.problem_templates import PROBLEM_CATEGORIES, get_problem_template
from config.docker_utils import start_docker_container, stop_docker_container

# Initialize session state
if 'solutions' not in st.session_state:
    st.session_state.solutions = []
if 'current_problem' not in st.session_state:
    st.session_state.current_problem = ''
if 'show_code_editor' not in st.session_state:
    st.session_state.show_code_editor = False
if 'api_key' not in st.session_state:
    # Try to get API key from environment variables first
    import os
    from dotenv import load_dotenv
    load_dotenv()
    st.session_state.api_key = os.getenv('GEMINI_API_KEY', '')
    st.session_state.agents_initialized = False

# Page configuration
st.set_page_config(
    page_title="AlgoMentor AI - Your Personal DSA Guide",
    page_icon="🔑",
    layout="wide"
)

# Sidebar for API Key input
with st.sidebar:
    st.title("🔑 API Key Setup")
    api_key = st.text_input(
        "Enter your Gemini API Key",
        type="password",
        placeholder="sk-...",
        help="Get your API key from https://makersuite.google.com/app/apikey"
    )
    
    if api_key:
        st.session_state.api_key = api_key
        st.success("✅ API Key saved!")
        
    st.markdown("---")
    st.markdown("### How to get your API key:")
    st.markdown("1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)")
    st.markdown("2. Sign in with your Google account")
    st.markdown("3. Click on 'Create API key'")
    st.markdown("4. Copy and paste the key above")
    
    if not st.session_state.get('api_key'):
        st.warning("⚠️ Please enter your Gemini API key to continue")

# Custom CSS for better styling
st.markdown("""
    <style>
        .main {
            padding: 2rem;
        }
        .stTextInput>div>div>input {
            padding: 12px !important;
            border-radius: 10px !important;
        }
        .stButton>button {
            width: 100%;
            border-radius: 10px;
            padding: 10px 24px;
            font-weight: 600;
            background: linear-gradient(45deg, #4e54c8, #8f94fb);
            color: white;
            border: none;
            transition: all 0.3s ease;
        }
        .stButton>button:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }
        .stMarkdown h1 {
            color: #4e54c8;
        }
    </style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.title("📊 AlgoMentor AI")
    st.markdown("---")
    st.markdown("### About")
    st.markdown("Your intelligent guide to mastering Data Structures and Algorithms. Get personalized, step-by-step solutions to complex coding problems.")
    st.markdown("---")
    st.markdown("### How to use")
    st.markdown("1. Enter your DSA problem or question")
    st.markdown("2. Click 'Generate Solution'")
    st.markdown("3. View the step-by-step solution")

# Main content
col1, col2 = st.columns([2, 1])

with col1:
    st.title("AlgoMentor AI")
    st.markdown("### Your Personal DSA Guide")
    
    # Problem category selection
    selected_category = st.selectbox(
        'Select Problem Category',
        ['-- Select a category --'] + list(PROBLEM_CATEGORIES.keys())
    )
    
    # Problem selection based on category
    problem_options = []
    if selected_category != '-- Select a category --':
        problem_options = PROBLEM_CATEGORIES[selected_category]
    
    selected_problem = st.selectbox(
        'Or select a common problem',
        ['-- Select a problem --'] + problem_options
    )
    
    # Get problem template if a common problem is selected
    if selected_problem != '-- Select a problem --':
        template = get_problem_template(selected_problem)
        st.session_state.current_problem = selected_problem
        st.markdown(f"**Description:** {template['description']}")
        st.markdown(f"**Example:**\n```\n{template['example']}\n```")
        st.markdown("**Constraints:**")
        for constraint in template['constraints']:
            st.markdown(f"- {constraint}")
        
        task = st.text_area(
            "Or describe your own problem:",
            value=template['description'],
            height=100,
            help="Modify the problem statement as needed"
        )
    else:
        task = st.text_area(
            "Describe your DSA problem:",
            value='',
            height=150,
            help="Be as specific as possible for better assistance"
        )

with col2:
    st.markdown("### Quick Actions")
    if st.button("📋 View Solution History", use_container_width=True):
        st.session_state.show_solution_history = True
    
    if st.button("📝 Open Code Editor", use_container_width=True):
        st.session_state.show_code_editor = not st.session_state.show_code_editor

# Code Editor Section
if st.session_state.get('show_code_editor', False):
    st.markdown("### Code Editor")
    code = st.text_area(
        'Enter your Python code here',
        height=300,
        key='code_editor',
        help='Write or paste your Python code here',
        placeholder='def solve():\n    # Your solution here\n    pass'
    )
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("▶️ Run Code", use_container_width=True):
            st.session_state.run_code = True
    with col2:
        if st.button("💾 Save Solution", use_container_width=True):
            if st.session_state.current_problem and code.strip():
                solution = {
                    'problem': st.session_state.current_problem or 'Custom Problem',
                    'code': code,
                    'timestamp': time.strftime("%Y-%m-%d %H:%M:%S")
                }
                st.session_state.solutions.append(solution)
                st.success("Solution saved to history!")


async def run(team,docker,task):
    try:
        await start_docker_container(docker)
        async for message in team.run_stream(task=task):
            if isinstance(message, TextMessage):
                print(msg:= f"{message.source} : {message.content}")
                yield msg
            elif isinstance(message, TaskResult):
                print(msg:= f"Stop Reason: {message.stop_reason}")
                yield msg
        print("Task Completed")
    except Exception as e:
        print(f"Error: {e}")
        yield f"Error: {e}"
    finally:
        await stop_docker_container(docker)


# Add some spacing
st.markdown("---")

# Create two columns for the button with some spacing
col1, col2 = st.columns([1, 2])
with col1:
    if st.button("🚀 Generate Solution", use_container_width=True, type="primary"):
        if not st.session_state.get('api_key'):
            st.error("Please enter your Gemini API key in the sidebar")
        else:
            # Get the task from the input
            task = st.session_state.get('current_problem', '')
            if not task:
                st.error("Please enter a problem to solve")
            else:
                with st.spinner('Initializing agents...'):
                    try:
                        # Import the team only when needed
                        from team.dsa_team import get_dsa_team_and_docker
                        from autogen_agentchat.base import TaskResult
                        
                        # Clear previous messages
                        if 'messages' not in st.session_state:
                            st.session_state.messages = []
                        
                        # Add user message to chat
                        user_msg = f"**Your Problem:** {task}"
                        st.session_state.messages.append({"role": "user", "content": user_msg})
                        
                        # Create a status placeholder
                        status_placeholder = st.empty()
                        with status_placeholder.status("🧠 Analyzing your problem and generating solution..."):
                            # Initialize the team and docker
                            team, docker = get_dsa_team_and_docker()
                            st.session_state.agents_initialized = True
                            
                            # Create a placeholder for the chat
                            chat_placeholder = st.container()
                            
                            # Display chat messages
                            with chat_placeholder:
                                for message in st.session_state.messages:
                                    with st.chat_message(message["role"]):
                                        st.markdown(message["content"])
                            
                            # Process the task
                            async def process_task():
                                async for msg in run(team, docker, task):
                                    if isinstance(msg, str):
                                        role = "assistant"
                                        avatar = "🤖"
                                        if msg.startswith("user"):
                                            role = "user"
                                            avatar = "👤"
                                        elif msg.startswith('DSA_Problem_Solver_Agent'):
                                            avatar = "🧑‍💻"
                                        
                                        # Add to messages if not already there
                                        if msg not in [m["content"] for m in st.session_state.messages]:
                                            st.session_state.messages.append({"role": role, "content": msg})
                                            
                                            # Update the chat display
                                            with chat_placeholder:
                                                with st.chat_message(role, avatar=avatar):
                                                    st.markdown(msg)
                                    
                                    elif hasattr(msg, 'result'):  # Check if it's a TaskResult-like object
                                        completion_msg = f"✅ **Task Completed!** {msg.result}"
                                        st.session_state.messages.append({"role": "assistant", "content": completion_msg})
                                        with chat_placeholder:
                                            with st.chat_message("assistant", avatar="✅"):
                                                st.markdown(completion_msg)
                            
                            # Run the async task
                            asyncio.run(process_task())
                    
                    except Exception as e:
                        error_msg = f"❌ **Error:** {str(e)}"
                        st.error(error_msg)
                        if 'messages' in st.session_state:
                            st.session_state.messages.append({"role": "error", "content": error_msg})
                    finally:
                        # Clear the status
                        if 'status_placeholder' in locals():
                            status_placeholder.empty()

# Display previous messages if any
if 'messages' in st.session_state and st.session_state.messages:
    st.markdown("---")
    st.markdown("### Solution")
    for message in st.session_state.messages:
        avatar = "🤖"
        if message["role"] == "user":
            avatar = "👤"
        elif message["role"] == "error":
            avatar = "❌"
        
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])