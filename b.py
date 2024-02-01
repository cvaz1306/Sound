def push_into_buffer(buffer, new_item, buffer_size):
    """
    Push a new item into an array buffer, maintaining the buffer size.

    Parameters:
    - buffer: List, the current array buffer.
    - new_item: Any, the new item to be pushed into the buffer.
    - buffer_size: int, the maximum size of the buffer.

    Returns:
    - List, the updated array buffer.
    """
    # Add the new item to the front of the buffer
    buffer.insert(0, new_item)

    # Trim the buffer to the specified size
    buffer = buffer[:buffer_size]

    return buffer

