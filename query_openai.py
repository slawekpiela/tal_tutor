import time
from openai import OpenAI
from configuration import api_key, assistant_id, assistant_id3, assistant_id4, Models
import os

#api-key=os.getenv("api-key")
# Assuming other configurations (api_key, etc.) are set correctly.
client = OpenAI(api_key=api_key)

def query_model(prompt, instructions, assistant, thread_id):
    print("Thread ID provided to query_model: ", thread_id)

    try:
        # Create a new thread if no thread ID is provided
        if thread_id is None:
            thread = client.beta.threads.create()
            thread_id = thread.id

        # Send the prompt as a message to the thread (for both new and existing threads)
        client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=prompt
        )

        # Create a run
        run = client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=assistant,
            instructions=instructions
            # tools=[{"type": "retrieval"}]  # Uncomment if needed
        )

        # Wait for the run to complete
        status = "start"
        # st.write(status)

        count = 0
        while status != "completed":
         result = client.beta.threads.runs.retrieve(
                thread_id=thread_id,
                run_id=run.id)
         status = result.status
         print(f'\rstatus', end='')
         time.sleep(1)


        # Retrieve messages after run is complete
        messages = client.beta.threads.messages.list(thread_id=thread_id)
        result_role = role = messages.data[0].role

        result_text = messages.data[0].content[0].text.value  # Extract text from completion
        full_result = messages
        print("Thread ID returned by query_model: ", thread_id)
        return result_text, result_role,full_result, thread_id

    except Exception as e:
        print("Error in query_model:", e)
        return None, None, None

# Usage example
# result, full_result, new_thread_id = query_model("Your prompt here", "Your instructions here", assistant_id, None)
