def build_conversation_prompt(system_instruction, conversation_messages, user_input):
    """Build a text prompt from system instruction, a list of message dicts, and the current user input.

    Args:
        system_instruction (str): system-level instruction text
        conversation_messages (list[dict]): list of messages, each {'role':..., 'content':...}
        user_input (str): the current user input

    Returns:
        str: assembled prompt
    """
    if conversation_messages is None:
        conversation_messages = []

    formatted = []
    for msg in conversation_messages:
        role = msg.get("role", "user")
        content = msg.get("content", "")
        formatted.append(f"{role}: {content}")

    # append the current user input
    formatted.append(f"user: {user_input}")

    prompt = system_instruction + "\n\n" + "\n".join(formatted)
    return prompt
