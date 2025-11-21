// renderer.js
// This file talks to Python via Eel.

function $(id) { return document.getElementById(id); }

const chatDisplay = $("chat-display");
const inputEntry = $("input-entry");
const sendBtn = $("send-btn");
const stopBtn = $("stop-speech-btn");
const clearBtn = $("clear-chat-btn");
const openLogsBtn = $("open-logs-btn");
const voiceModeBtn = $("voice-mode-btn");
const exitBtn = $("exit-btn");
const statusLabel = $("status");

function addMessage(sender, text) {
  const el = document.createElement("div");
  el.classList.add("message");
  if (sender === "You") el.classList.add("msg-user");
  else if (sender === "Jarvis") el.classList.add("msg-jarvis");
  else el.classList.add("msg-system");
  const ts = new Date().toLocaleTimeString();
  el.innerHTML = `<strong>[${ts}] ${sender}:</strong><div>${escapeHtml(text)}</div>`;
  chatDisplay.appendChild(el);
  chatDisplay.scrollTop = chatDisplay.scrollHeight;
}

function escapeHtml(unsafe) {
  return unsafe
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;");
}

// Hook up send
sendBtn.addEventListener("click", doSend);
inputEntry.addEventListener("keydown", (e) => {
  if (e.key === "Enter") doSend();
});

async function doSend() {
  const q = inputEntry.value.trim();
  if (!q) return;
  inputEntry.value = "";
  addMessage("You", q);
  setStatus("Processing your command...");
  try {
    const res = await eel.py_send_query(q)();
    if (res.ok) {
      addMessage("Jarvis", res.response);
      setStatus("Ready | Command executed");
    } else {
      addMessage("system", "Error: " + (res.error || "Unknown error"));
      setStatus("Error occurred");
    }
  } catch (err) {
    addMessage("system", "Connection error: " + err);
    setStatus("Error occurred");
  }
}

// stop speech
stopBtn.addEventListener("click", async () => {
  const res = await eel.py_stop_speech()();
  if (res.stopped) {
    addMessage("system", "🗣️ Speech stopped by user");
    setStatus("Speech stopped | Ready");
  } else {
    addMessage("system", "No active speech to stop");
    setStatus("No speech active");
  }
});

// clear chat (frontend only)
clearBtn.addEventListener("click", () => {
  chatDisplay.innerHTML = "";
  addMessage("system", "Chat history cleared");
  setStatus("Chat cleared | Ready");
  eel.py_clear_chat(); // optional
});

// open logs
openLogsBtn.addEventListener("click", async () => {
  const res = await eel.py_open_logs()();
  if (!res.ok) {
    addMessage("system", "Unable to open logs (file not found).");
  } else {
    addMessage("system", "Logs opened.");
  }
});

// voice mode
voiceModeBtn.addEventListener("click", async () => {
  setStatus("Listening for voice command...");
  addMessage("system", "Voice mode activated — listening...");
  await eel.py_activate_voice_mode()();
});
 // Stop voice mode
    document.getElementById('stop-voice-btn').addEventListener('click', () => {
        eel.py_stop_voice_mode()(function(res){
            console.log(res.message);
            document.getElementById('voice-status').innerText = "Status: Inactive";
        });
    });

// Exit button
exitBtn.addEventListener("click", async () => {
    setStatus("Exiting Jarvis...");
    try {
        await eel.py_exit_app()();
        // Close the frontend window manually just in case
        window.close();
    } catch (e) {
        console.log("Error exiting:", e);
    }
});

exitBtn.addEventListener("click", async () => {
    try {
        await eel.py_exit_app()();
    } catch (e) {
        console.log("Exit error:", e);
    }
});

// status helper
function setStatus(text) {
  statusLabel.textContent = "🔹 " + text;
}
// Show image generation modal
document.getElementById("image-gen-btn").addEventListener("click", () => {
    document.getElementById("image-gen-panel").style.display = "flex";
});

// Call Python backend via Eel
async function generateImage() {
    const prompt = document.getElementById("image-prompt").value.trim();
    if(!prompt) return alert("Enter an image prompt!");

    const resultDiv = document.getElementById("image-result");
    resultDiv.innerText = "Generating image...";

    try {
        const imageUrl = await eel.generate_image(prompt)(); // Call Python function
        if(imageUrl){
            resultDiv.innerHTML = `<img src="${imageUrl}" style="max-width:100%;border:2px solid #fff;margin-top:10px;" />`;
        } else {
            resultDiv.innerText = "Failed to generate image.";
        }
    } catch(err) {
        console.error(err);
        resultDiv.innerText = "Error generating image.";
    }
}
// small clock update
async function updateClock() {
  try {
    const t = await eel.py_get_time()();
    $("date").textContent = t.date;
    $("time").textContent = t.time;
    $("day").textContent = t.day;
  } catch (e) {
    // ignore
  }
}
setInterval(updateClock, 1000);
updateClock();
// Called by Python to add Jarvis message
function js_add_jarvis_message(msg) {
    const chatDisplay = document.getElementById("chat-display");
    const message = document.createElement("div");
    message.className = "message msg-jarvis";
    const ts = new Date().toLocaleTimeString();
    message.innerHTML = `<strong>[${ts}] Jarvis:</strong> ${msg}`;
    chatDisplay.appendChild(message);
    chatDisplay.scrollTop = chatDisplay.scrollHeight;
}
eel.expose(js_add_jarvis_message);

// Called by Python to add system message
function js_add_system_message(msg) {
    const chatDisplay = document.getElementById("chat-display");
    const message = document.createElement("div");
    message.className = "message msg-system";
    const ts = new Date().toLocaleTimeString();
    message.innerHTML = `<strong>[${ts}] SYSTEM:</strong> ${msg}`;
    chatDisplay.appendChild(message);
    chatDisplay.scrollTop = chatDisplay.scrollHeight;
}
eel.expose(js_add_system_message);
