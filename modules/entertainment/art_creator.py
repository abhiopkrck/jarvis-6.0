import eel
import webbrowser
from bytez import Bytez

# ==== CONFIG ====
BYTEZ_API_KEY = "your api key "
BYTEZ_MODEL = "Lykon/absolute-reality-1.6525"

# Initialize Bytez SDK once
sdk = Bytez(BYTEZ_API_KEY)
model = sdk.model(BYTEZ_MODEL)

# ==== EXPOSE FUNCTION TO JS ====
@eel.expose
def generate_image(prompt: str):
    """
    Generate image from Bytez and open it directly.
    Returns the URL (for frontend display/logs).
    """
    try:
        result = model.run(prompt)
        if result and hasattr(result, "output") and result.output:
            image_url = result.output
            webbrowser.open(image_url)  # Open image directly
            return image_url
        else:
            return None
    except Exception as e:
        print("Error generating image:", e)
        return None
