from bytez import Bytez
import time

key = "ea0e20284203b535479c427e0d609c77"
sdk = Bytez(key)

# NEW working stable model
model = sdk.model("ali-vilab/text-to-video-ms-1.7b-legacy")

def generate(prompt: str):
    print("🎥 Generating video…")

    try:
        # Use new 1-object response (your SDK)
        response = model.run(prompt)

        # These 3 attributes ALWAYS exist
        output = getattr(response, "output", None)
        error = getattr(response, "error", None)
        meta = getattr(response, "metadata", None)

        if error:
            print("❌ Bytez Error:", error)
            return None

        # output is ALWAYS a string or dict or list
        print("RAW OUTPUT:", output)

        video_url = None

        # Case 1: if string is returned
        if isinstance(output, str):
            if output.startswith("http"):
                video_url = output

        # Case 2: if dict
        if isinstance(output, dict):
            video_url = output.get("video") or output.get("url")

        # Case 3: if list
        if isinstance(output, list) and len(output) > 0:
            if isinstance(output[0], dict):
                video_url = output[0].get("video") or output[0].get("url")

        print("🎬 Video URL:", video_url)
        return video_url

    except Exception as e:
        print("❌ Exception:", e)
        return None
