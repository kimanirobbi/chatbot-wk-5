# robbi - Chatbot

Minimal Streamlit chatbot using Hugging Face transformers.

## Requirements

This project requires Python 3.8+ and the packages listed in `requirements.txt`.

To install dependencies (PowerShell):

```powershell
python -m pip install --upgrade pip
pip install -r .\requirements.txt
```

## Run the app (PowerShell)

```powershell
streamlit run .\chatbot.py
```

This will start a Streamlit server and open the app in your browser.

## Notes

- The default model is `gpt2` (small) to keep downloads and memory usage reasonable. Replace the model name in `chatbot.py` if you want a different Hugging Face model (be aware of memory and token limits).
- If using models from the Hugging Face Hub that require authentication or have large checkpoints, follow Hugging Face docs to login (`huggingface-cli login`) and ensure you have enough RAM/VRAM.
- If you see slow startup or OOM errors, consider using a smaller model or running on a machine with a GPU.

## Troubleshooting

- If Streamlit does not open automatically, copy the provided local URL from the terminal into your browser.
- If transformers complain about missing tokenizer pad token, the code sets `pad_token` to `eos_token` automatically.

---

If you'd like, I can also add a simple `requirements-dev.txt` or a Dockerfile for reproducible runs.