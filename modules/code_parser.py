def split_into_blocks(code: str) -> list[str]:
    # For now, just split by blank lines
    return [block.strip() for block in code.strip().split('\n\n') if block.strip()]
