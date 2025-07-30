import streamlit as st
from team.dsa_team import get_dsa_team_and_docker
from config.docker_utils import start_docker_container, stop_docker_container
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.base import TaskResult
import asyncio
import json
from utils.visualization import plot_time_complexity, visualize_graph, plot_sorting_visualization
from utils.problem_templates import PROBLEM_CATEGORIES, get_problem_template
from streamlit_ace import st_ace
import time

# Initialize session state
if 'solutions' not in st.session_state:
    st.session_state.solutions = []
if 'current_problem' not in st.session_state:
    st.session_state.current_problem = ''
if 'show_code_editor' not in st.session_state:
    st.session_state.show_code_editor = False

# Page configuration
st.set_page_config(
    page_title="AlgoMentor AI - Your Personal DSA Guide",
    page_icon="📊",
    layout="wide"
)

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
    
    if st.button("📊 Visualize Data Structure", use_container_width=True):
        st.session_state.show_visualization = True
    
    if st.button("📝 Open Code Editor", use_container_width=True):
        st.session_state.show_code_editor = not st.session_state.show_code_editor

# Code Editor Section
if st.session_state.get('show_code_editor', False):
    st.markdown("### Code Editor")
    code = st_ace(
        language='python',
        theme='monokai',
        font_size=14,
        tab_size=4,
        show_gutter=True,
        key='code_editor',
        value='# Write your solution here\ndef solution():\n    pass',
        height=300
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

# Visualization Section
if st.session_state.get('show_visualization', False):
    st.markdown("### Data Structure Visualization")
    vis_type = st.selectbox(
        'Select visualization type',
        ['Graph', 'Time Complexity', 'Sorting']
    )
    
    if vis_type == 'Graph':
        st.markdown("Enter graph edges as tuples (e.g., (1,2), (2,3))")
        graph_input = st.text_area("Graph Input", value="(1,2), (2,3), (3,4), (4,1)")
        try:
            edges = eval(f'[{graph_input}]')
            fig = visualize_graph(edges)
            st.pyplot(fig)
        except Exception as e:
            st.error(f"Invalid graph input: {e}")
    
    elif vis_type == 'Time Complexity':
        st.markdown("Compare time complexities of different algorithms")
        algo1 = st.text_input("Algorithm 1", "Bubble Sort")
        time1 = st.text_input("Complexity (e.g., O(n^2))", "O(n^2)")
        
        algo2 = st.text_input("Algorithm 2", "Merge Sort")
        time2 = st.text_input("Complexity (e.g., O(n log n))", "O(n log n)")
        
        if st.button("Compare"):
            complexity_data = {algo1: time1, algo2: time2}
            fig = plot_time_complexity(complexity_data)
            st.pyplot(fig)
    
    elif vis_type == 'Sorting':
        st.markdown("Visualize sorting algorithms")
        array_input = st.text_area("Enter array (comma-separated)", "5,1,4,2,8,3,7,6")
        try:
            arr = [int(x.strip()) for x in array_input.split(',') if x.strip()]
            if arr:
                fig = plot_sorting_visualization(arr, "Sorting Visualization")
                st.pyplot(fig)
        except ValueError:
            st.error("Please enter valid integers separated by commas")

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
        # Clear previous messages
        if 'messages' not in st.session_state:
            st.session_state.messages = []
        
        # Add user message to chat
        user_msg = f"**Your Problem:** {task}"
        st.session_state.messages.append({"role": "user", "content": user_msg})
        
        # Create a status placeholder
        status_placeholder = st.empty()
        with status_placeholder.status("🧠 Analyzing your problem and generating solution..."):
            try:
                # Initialize team and docker
                team, docker = get_dsa_team_and_docker()
                
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
                        
                        elif isinstance(msg, TaskResult):
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