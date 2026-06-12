from agentic_chatbot_tool_backend import chatbot, get_all_threads
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage, ToolMessage
import streamlit as st
import uuid 

# Generate a unique thread ID for each new conversation
def generate_thread_id():
    return str(uuid.uuid4())



# Add a new thread ID to the conversation list
def add_thread(thread_id):

    # Prevent the same thread from being added multiple times
    if thread_id not in st.session_state["chat_threads"]:
        st.session_state["chat_threads"].append(thread_id)

    

# Create a completely new chat conversation
def reset_chat():

    # Generate and assign a new thread ID
    st.session_state["thread_id"] = generate_thread_id()

    # Clear the current chat messages from the UI
    st.session_state["message_history"] = []

    # Add the new thread to the conversation list
    add_thread(st.session_state["thread_id"])



# Load a previous conversation from the LangGraph checkpointer
def load_conversation(thread_id):

    # Get the saved state for the selected thread
    state = chatbot.get_state(
        config={
            "configurable": {
                "thread_id": thread_id
            }
        }
    )

    # Return saved messages
    # Return an empty list if no messages are available
    return state.values.get("messages", [])



# Display the main application title
st.title("Agentic Chatbot with LangGraph")


# Create message_history when the app runs for the first time
if "message_history" not in st.session_state:
    st.session_state["message_history"] = []


# Create a thread ID when the app runs for the first time
if "thread_id" not in st.session_state:
    st.session_state["thread_id"] = generate_thread_id()


# Create a list for storing all conversation thread IDs
if "chat_threads" not in st.session_state:
    st.session_state["chat_threads"] = get_all_threads()



# Add the current thread to the conversation list
add_thread(st.session_state["thread_id"])


# ========================= Sidebar threading feature =========================

# Display the sidebar title
st.sidebar.title("My Conversations")


# Create a button for starting a new conversation
if st.sidebar.button("New Chat"):

    # Reset the current chat and create a new thread
    reset_chat()

    # Rerun the Streamlit app to update the interface
    st.rerun()




# Display all conversation threads in reverse order
# This shows the newest conversation first
for thread_id in st.session_state["chat_threads"][::-1]:

    # Create one sidebar button for every conversation
    if st.sidebar.button(
        str(thread_id),
        key=thread_id
    ):

        # Set the selected thread as the current thread
        st.session_state["thread_id"] = thread_id

        # Load the messages saved under the selected thread
        messages = load_conversation(thread_id)

        # Temporary list for converting LangChain messages
        # into Streamlit's required message format
        temp_messages = []


        # Loop through all saved messages
        for message in messages:

            # Check whether the message was sent by the user
            if isinstance(message, HumanMessage):
                role = "user"

            # Check whether the message was sent by the AI
            elif isinstance(message, AIMessage):
                role = "assistant"

            # Ignore other message types, such as ToolMessage
            else:
                continue


            # Convert the LangChain message into a dictionary
            temp_messages.append({
                "role": role,
                "content": message.content
            })


        # Replace the current UI history with the selected conversation
        st.session_state["message_history"] = temp_messages

        # Rerun the application to display the loaded messages
        st.rerun()



# ========================= Main chat interface =========================

# Display all messages from the currently selected conversation
for message in st.session_state["message_history"]:

    # Create either a user chat bubble or assistant chat bubble
    with st.chat_message(message["role"]):

        # Display the message content
        st.text(message["content"])



# Create the chat input box
user_input = st.chat_input("Type here")


# Run this block after the user submits a message
if user_input:

    # Save the user's message in Streamlit session state
    st.session_state["message_history"].append({
        "role": "user",
        "content": user_input
    })


    # Display the user's message in the chat interface
    with st.chat_message("user"):
        st.text(user_input)


    # Pass the current thread ID to LangGraph
    # LangGraph uses this ID to save and retrieve conversation memory

    CONFIG = {
        "configurable": {"thread_id": st.session_state["thread_id"]},
        "metadata": {
            "thread_id": st.session_state["thread_id"]
        },
        "run_name": "chat_trace",
    }



    # Assistant streaming block
    with st.chat_message("assistant"):
        # Use a mutable holder so the generator can set/modify it
        status_holder = {"box": None}

        def ai_only_stream():
            for message_chunk, metadata in chatbot.stream(
                {"messages": [HumanMessage(content=user_input)]},
                config=CONFIG,
                stream_mode="messages",
            ):
                # Lazily create & update the SAME status container when any tool runs
                if isinstance(message_chunk, ToolMessage):
                    tool_name = getattr(message_chunk, "name", "tool")
                    if status_holder["box"] is None:
                        status_holder["box"] = st.status(
                            f"🔧 Using `{tool_name}` …", expanded=True
                        )
                    else:
                        status_holder["box"].update(
                            label=f"🔧 Using `{tool_name}` …",
                            state="running",
                            expanded=True,
                        )

                # Stream ONLY assistant tokens
                if isinstance(message_chunk, AIMessage):
                    yield message_chunk.content

        ai_message = st.write_stream(ai_only_stream())

        # Finalize only if a tool was actually used
        if status_holder["box"] is not None:
            status_holder["box"].update(
                label="✅ Tool finished", state="complete", expanded=False
            )


    # Save the complete assistant response in Streamlit session state
    st.session_state["message_history"].append({
        "role": "assistant",
        "content": ai_message
    })