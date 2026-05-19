export default function AvatarChatPage() {
  return (
    <div className="min-h-screen bg-black text-white flex flex-col items-center justify-center p-6">
      <div className="w-full max-w-6xl grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Avatar Section */}
        <div className="bg-zinc-900 rounded-3xl p-4 shadow-2xl border border-zinc-800">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h1 className="text-2xl font-bold">AI Avatar</h1>
              <p className="text-zinc-400 text-sm">
                Real-time conversation with HeyGen LiveAvatar
              </p>
            </div>

            <div className="flex gap-2">
              <button
                className="px-4 py-2 rounded-xl bg-green-600 hover:bg-green-500 transition"
                onClick={() => alert("Connect avatar logic here")}
              >
                Start Session
              </button>

              <button
                className="px-4 py-2 rounded-xl bg-red-600 hover:bg-red-500 transition"
                onClick={() => alert("Disconnect avatar logic here")}
              >
                End Session
              </button>
            </div>
          </div>

          {/* Avatar Video */}
          <div className="relative rounded-2xl overflow-hidden bg-zinc-950 aspect-video border border-zinc-800">
            <video
              id="avatarVideo"
              autoPlay
              playsInline
              className="w-full h-full object-cover"
            />

            <div className="absolute bottom-4 left-4 bg-black/60 backdrop-blur px-3 py-2 rounded-xl text-sm">
              Avatar Stream
            </div>
          </div>
        </div>

        {/* Chat Section */}
        <div className="bg-zinc-900 rounded-3xl p-4 shadow-2xl border border-zinc-800 flex flex-col h-[700px]">
          <div className="mb-4">
            <h2 className="text-2xl font-bold">Chat</h2>
            <p className="text-zinc-400 text-sm">
              Talk with your AI avatar
            </p>
          </div>

          {/* Messages */}
          <div className="flex-1 overflow-y-auto space-y-4 pr-2">
            <div className="flex justify-end">
              <div className="bg-blue-600 px-4 py-3 rounded-2xl max-w-[80%]">
                Hello!
              </div>
            </div>

            <div className="flex justify-start">
              <div className="bg-zinc-800 px-4 py-3 rounded-2xl max-w-[80%]">
                Hi! I am your AI avatar assistant.
              </div>
            </div>
          </div>

          {/* Input */}
          <div className="mt-4 flex gap-3">
            <input
              type="text"
              placeholder="Type your message..."
              className="flex-1 bg-zinc-800 border border-zinc-700 rounded-2xl px-4 py-3 outline-none focus:ring-2 focus:ring-blue-500"
            />

            <button className="px-6 py-3 rounded-2xl bg-blue-600 hover:bg-blue-500 transition font-medium">
              Send
            </button>
          </div>

          {/* Voice Controls */}
          <div className="mt-4 flex gap-3">
            <button className="flex-1 bg-zinc-800 hover:bg-zinc-700 border border-zinc-700 rounded-2xl py-3 transition">
              🎤 Start Talking
            </button>

            <button className="flex-1 bg-zinc-800 hover:bg-zinc-700 border border-zinc-700 rounded-2xl py-3 transition">
              🔇 Mute
            </button>
          </div>
        </div>
      </div>

      {/* Setup Instructions */}
      <div className="w-full max-w-6xl mt-8 bg-zinc-900 border border-zinc-800 rounded-3xl p-6">
        <h3 className="text-xl font-bold mb-4">Setup</h3>

        <div className="space-y-3 text-zinc-300 text-sm">
          <p>1. Install SDK:</p>

          <pre className="bg-black rounded-xl p-4 overflow-x-auto">
{`npm install @heygen/liveavatar-web-sdk`}
          </pre>

          <p>2. Create backend endpoint to generate session token.</p>

          <p>3. Connect avatar stream to the video element.</p>

          <p>4. Connect OpenAI or another LLM for responses.</p>
        </div>
      </div>
    </div>
  );
}
