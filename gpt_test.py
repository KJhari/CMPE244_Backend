import openai

def query_gpt_3_5_turbo(prompt, model_id, api_key):
    """
    Query the GPT-3.5 Turbo model with a given prompt.

    :param prompt: The prompt to send to the model.
    :param model_id: The ID of your fine-tuned model.
    :param api_key: Your OpenAI API key.
    :return: The response from the GPT-3.5 Turbo model.
    """
    openai.api_key = api_key
    try:
        response = openai.ChatCompletion.create(
            model=model_id,
            messages=[{"role": "system", "content": "You are the support assistant for the IoT Motor Control project."},
                      {"role": "user", "content": prompt}],
            temperature=0  # Adjust temperature if needed
        )
        return response.choices[0].message["content"]
    except Exception as e:
        return str(e)

# Example usage

# prompt = "can you do a demo of the project for me"

# response = query_gpt_3_5_turbo(prompt, model_id, api_key)
# print(response)