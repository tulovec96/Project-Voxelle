<script lang="ts">
  import { Activity, Cpu, HardDrive, Zap } from 'lucide-svelte';
  import { onMount } from 'svelte';

  let metrics = {
    cpu: 15,
    memory: 45,
    latency: 125,
    requestsPerSecond: 42,
    errors: 0,
    cpuHistory: [15, 18, 16, 20, 19, 22, 21] as number[],
    memoryHistory: [45, 46, 48, 47, 49, 50, 45] as number[]
  };

  onMount(() => {
    const interval = setInterval(() => {
      const newCpu = Math.max(5, Math.min(95, metrics.cpu + (Math.random() - 0.5) * 10));
      const newMemory = Math.max(20, Math.min(90, metrics.memory + (Math.random() - 0.5) * 5));
      
      metrics = {
        ...metrics,
        cpu: newCpu,
        memory: newMemory,
        latency: Math.max(50, Math.min(500, metrics.latency + (Math.random() - 0.5) * 20)),
        requestsPerSecond: Math.max(0, Math.min(100, metrics.requestsPerSecond + (Math.random() - 0.5) * 5)),
        cpuHistory: [...metrics.cpuHistory.slice(1), newCpu],
        memoryHistory: [...metrics.memoryHistory.slice(1), newMemory]
      };
    }, 2000);

    return () => clearInterval(interval);
  });

  function getColor(value: number, high: number = 80): string {
    if (value < high * 0.5) return 'text-green-500';
    if (value < high * 0.8) return 'text-yellow-500';
    return 'text-red-500';
  }
</script>

<div class="space-y-6">
  <h1 class="text-4xl font-bold">Performance Metrics</h1>

  <!-- Main Metrics -->
  <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
    <div class="bg-gray-800 rounded-lg p-6 border border-gray-700">
      <div class="flex items-center justify-between mb-4">
        <span class="text-sm text-gray-400">CPU Usage</span>
        <Cpu class="w-5 h-5 text-blue-500" />
      </div>
      <div class={`text-3xl font-bold ${getColor(metrics.cpu)}`}>{metrics.cpu.toFixed(1)}%</div>
      <div class="w-full bg-gray-700 rounded-full h-2 mt-4">
        <div class="bg-blue-500 h-2 rounded-full" style="width: {metrics.cpu}%" />
      </div>
      <div class="text-xs text-gray-400 mt-2">Last 14s</div>
    </div>

    <div class="bg-gray-800 rounded-lg p-6 border border-gray-700">
      <div class="flex items-center justify-between mb-4">
        <span class="text-sm text-gray-400">Memory Usage</span>
        <HardDrive class="w-5 h-5 text-purple-500" />
      </div>
      <div class={`text-3xl font-bold ${getColor(metrics.memory)}`}>{metrics.memory.toFixed(1)}%</div>
      <div class="w-full bg-gray-700 rounded-full h-2 mt-4">
        <div class="bg-purple-500 h-2 rounded-full" style="width: {metrics.memory}%" />
      </div>
      <div class="text-xs text-gray-400 mt-2">Last 14s</div>
    </div>

    <div class="bg-gray-800 rounded-lg p-6 border border-gray-700">
      <div class="flex items-center justify-between mb-4">
        <span class="text-sm text-gray-400">API Latency</span>
        <Zap class="w-5 h-5 text-yellow-500" />
      </div>
      <div class={`text-3xl font-bold ${getColor(metrics.latency, 300)}`}>{metrics.latency.toFixed(0)}ms</div>
      <div class="text-xs text-gray-400 mt-4">95th percentile</div>
    </div>

    <div class="bg-gray-800 rounded-lg p-6 border border-gray-700">
      <div class="flex items-center justify-between mb-4">
        <span class="text-sm text-gray-400">Requests/sec</span>
        <Activity class="w-5 h-5 text-green-500" />
      </div>
      <div class="text-3xl font-bold text-green-500">{metrics.requestsPerSecond.toFixed(1)}</div>
      <div class="text-xs text-gray-400 mt-4">Errors: {metrics.errors}</div>
    </div>
  </div>

  <!-- Detailed Charts -->
  <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
    <div class="bg-gray-800 rounded-lg p-6 border border-gray-700">
      <h3 class="font-semibold mb-4">CPU Usage (14s)</h3>
      <div class="h-32 flex items-end gap-1">
        {#each metrics.cpuHistory as value}
          <div 
            class="flex-1 bg-blue-500 rounded-t hover:bg-blue-400 transition" 
            style="height: {(value / 100) * 100}%"
            title={`${value.toFixed(1)}%`}
          />
        {/each}
      </div>
      <div class="flex justify-between text-xs text-gray-400 mt-2">
        <span>0%</span>
        <span>50%</span>
        <span>100%</span>
      </div>
    </div>

    <div class="bg-gray-800 rounded-lg p-6 border border-gray-700">
      <h3 class="font-semibold mb-4">Memory Usage (14s)</h3>
      <div class="h-32 flex items-end gap-1">
        {#each metrics.memoryHistory as value}
          <div 
            class="flex-1 bg-purple-500 rounded-t hover:bg-purple-400 transition" 
            style="height: {(value / 100) * 100}%"
            title={`${value.toFixed(1)}%`}
          />
        {/each}
      </div>
      <div class="flex justify-between text-xs text-gray-400 mt-2">
        <span>0%</span>
        <span>50%</span>
        <span>100%</span>
      </div>
    </div>
  </div>
</div>
