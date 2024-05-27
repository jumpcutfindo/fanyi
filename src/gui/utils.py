def get_scaled_size(frame_width: int, frame_height: int, width: int, height: int):
    """Scales a given width and given height to the frame width and frame height specified"""
    ratio = min(frame_width / width, frame_height / height)
    return max(1, round(width * ratio)), max(1, round(height * ratio))
