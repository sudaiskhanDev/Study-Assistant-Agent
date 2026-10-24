
import gradio as gr


def greet(name):
    if not name.strip():
        return "Please enter your name."

    return f"Welcome to AI Study Assistant, {name}!"


with gr.Blocks(title="AI Study Assistant") as demo:
    gr.Markdown("# 📚 AI Study Assistant")
    gr.Markdown("Upload notes, generate summaries, create quizzes, and study with flashcards.")

    name_input = gr.Textbox(
        label="Your Name",
        placeholder="Enter your name..."
    )

    greet_button = gr.Button("Test App")
    output = gr.Textbox(label="Output")

    greet_button.click(
        fn=greet,
        inputs=name_input,
        outputs=output
    )


if __name__ == "__main__":
    demo.launch()
