import streamlit as st


def split_into_blocks(code: str) -> list[str]:
    # For now, just split by blank lines
    return [block.strip() for block in code.strip().split('\n\n') if block.strip()]

if __name__ == "__main__":
    uploaded_file = st.file_uploader("Upload a python file", type="py")
    if uploaded_file:
        code = uploaded_file.read().decode("utf-8")
        print(split_into_blocks(code))
