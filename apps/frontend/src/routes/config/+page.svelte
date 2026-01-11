<script lang="ts">
  import { Copy, Edit2, Save, X } from 'lucide-svelte';
  import { writable } from 'svelte/store';

  let config = `# JAIson Configuration
model:
  type: "llama"
  name: "default"

server:
  host: "localhost"
  port: 7272
  debug: false

audio:
  sample_rate: 16000
  channels: 1
  format: "pcm_s16le"

prompts:
  character: "prompts/characters/default.txt"
  scene: "prompts/scenes/default.txt"
  instructions: "prompts/instructions/default.txt"

tts:
  engine: "tts_engine"
  voice: "default"
  speed: 1.0

stt:
  engine: "whisper"
  language: "en"

mcp:
  enabled: true
  tools: []`;

  let editMode = false;
  let editedConfig = config;

  function copyToClipboard() {
    navigator.clipboard.writeText(config);
    alert('Configuration copied to clipboard!');
  }

  function toggleEdit() {
    if (editMode) {
      editedConfig = config;
    }
    editMode = !editMode;
  }

  function saveConfig() {
    config = editedConfig;
    editMode = false;
    alert('Configuration saved (simulated - not persisted)');
  }
</script>

<div class="space-y-6">
  <div class="flex items-center justify-between">
    <h1 class="text-4xl font-bold">Configuration</h1>
    <div class="flex gap-2">
      {#if editMode}
        <button on:click={saveConfig} class="flex items-center gap-2 px-4 py-2 bg-green-600 hover:bg-green-700 rounded transition">
          <Save class="w-4 h-4" />
          Save
        </button>
        <button on:click={toggleEdit} class="flex items-center gap-2 px-4 py-2 bg-gray-600 hover:bg-gray-700 rounded transition">
          <X class="w-4 h-4" />
          Cancel
        </button>
      {:else}
        <button on:click={toggleEdit} class="flex items-center gap-2 px-4 py-2 bg-blue-600 hover:bg-blue-700 rounded transition">
          <Edit2 class="w-4 h-4" />
          Edit
        </button>
        <button on:click={copyToClipboard} class="flex items-center gap-2 px-4 py-2 bg-purple-600 hover:bg-purple-700 rounded transition">
          <Copy class="w-4 h-4" />
          Copy
        </button>
      {/if}
    </div>
  </div>

  <div class="bg-gray-800 rounded-lg border border-gray-700 overflow-hidden">
    {#if editMode}
      <textarea
        bind:value={editedConfig}
        class="w-full h-96 bg-gray-900 text-gray-100 p-4 font-mono text-sm border-none focus:outline-none"
      />
    {:else}
      <pre class="p-4 overflow-auto text-sm text-gray-300 font-mono h-96"><code>{config}</code></pre>
    {/if}
  </div>

  <div class="bg-blue-500/10 border border-blue-500/30 rounded-lg p-4 text-sm">
    <p class="text-blue-300">
      💡 Tip: This configuration file controls all aspects of your J.A.I.son instance. Changes typically require a server restart to take effect.
    </p>
  </div>

  <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
    <div class="bg-gray-800 rounded-lg p-4 border border-gray-700">
      <h3 class="font-semibold mb-2">Configuration Sections</h3>
      <ul class="text-sm space-y-1 text-gray-300">
        <li>• <span class="font-mono">model</span> - AI model configuration</li>
        <li>• <span class="font-mono">server</span> - Server settings</li>
        <li>• <span class="font-mono">audio</span> - Audio processing</li>
        <li>• <span class="font-mono">prompts</span> - AI personality files</li>
        <li>• <span class="font-mono">tts</span> - Text-to-Speech settings</li>
        <li>• <span class="font-mono">stt</span> - Speech-to-Text settings</li>
        <li>• <span class="font-mono">mcp</span> - Model Context Protocol</li>
      </ul>
    </div>

    <div class="bg-gray-800 rounded-lg p-4 border border-gray-700">
      <h3 class="font-semibold mb-2">Related Documentation</h3>
      <ul class="text-sm space-y-2">
        <li><a href="#" class="text-blue-400 hover:text-blue-300">Configuration Guide →</a></li>
        <li><a href="#" class="text-blue-400 hover:text-blue-300">Advanced Configuration →</a></li>
        <li><a href="#" class="text-blue-400 hover:text-blue-300">Environment Variables →</a></li>
        <li><a href="#" class="text-blue-400 hover:text-blue-300">Secrets Management →</a></li>
      </ul>
    </div>
  </div>
</div>
