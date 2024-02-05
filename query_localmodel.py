import llama_cpp
#CUDA
#llm = llama_cpp.Llama(model_path="/Users/slawekpiela/llama/llama-2-7b-chat.Q5_K_M.gguf", n_gpu_layers=40, n_ctx=4000)
#MAC
n_ctx=4000 #define size of the context window (for llama2 max is 4098. Affects speed of inference.
llm = llama_cpp.Llama(model_path="/Users/slawekpiela/llama/llama-2-7b-chat.Q5_K_M.gguf",device='mps',n_ctx=n_ctx)
def query(prompt):
    print("start l_query)")
    #llm = llama_cpp.Llama(model_path="/Users/slawekpiela/llama/llama-2-7b-chat.Q5_K_M.gguf", n_gpu_layers=40, n_ctx=n_ctx)
    llm = llama_cpp.Llama(model_path="/Users/slawekpiela/llama/llama-2-7b-chat.Q5_K_M.gguf", device='mps', n_ctx=n_ctx)
    output = llm(
        prompt,  # Prompt
        temperature=0.4,
        max_tokens = 50,  # Generate up to 32 tokens
        #stop = ["Q:", "\n"],  # Stop generating just before the model would generate a new question

    )
    print("Prompt in query: ", prompt, "\n")
    print("\nResult: ", output, "\n")
    return output



