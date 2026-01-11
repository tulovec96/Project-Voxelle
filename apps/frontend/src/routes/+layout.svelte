<script lang="ts">
	import * as Avatar from "$lib/components/ui/avatar";
	import {ModeWatcher, toggleMode} from "mode-watcher";
	import "../app.pcss";

	import { Button } from "$lib/components/ui/button";
	import { Sun, Moon, Server, Activity, AlertCircle, Menu, X, BarChart3, FileText, Settings } from "lucide-svelte";
	import { Toaster } from "$lib/components/ui/sonner";

	import { socket } from "./socketio"

	let isConnected = false;
	let sidebarOpen = false;

	socket.on("connect", () => {
		isConnected = true;
	});
	socket.on("disconnect", () => {
		isConnected = false;
	});

	function toggleSidebar() {
		sidebarOpen = !sidebarOpen;
	}
</script>
<svelte:head>
	<title>Neuro Control Panel</title>
	<link rel="preconnect" href="https://fonts.googleapis.com">
	<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
	<link href="https://fonts.googleapis.com/css2?family=Inter:wght@100..900&display=swap" rel="stylesheet">
</svelte:head>

<Toaster richColors/>
<ModeWatcher />

<div class="h-screen flex">
	<!-- Sidebar -->
	<aside class="hidden md:flex w-64 bg-gray-900 border-r border-gray-800 flex-col">
		<div class="p-6 border-b border-gray-800">
			<div class="flex items-center gap-2">
				<Server class="w-6 h-6 text-blue-500" />
				<h1 class="text-xl font-bold">J.A.I.son</h1>
			</div>
		</div>

		<nav class="flex-1 px-4 py-6 space-y-2">
			<Button variant="ghost" href="/" class="w-full justify-start gap-3">
				<Activity class="w-5 h-5" />
				Dashboard
			</Button>
			<Button variant="ghost" href="/metrics" class="w-full justify-start gap-3">
				<BarChart3 class="w-5 h-5" />
				Metrics
			</Button>
			<Button variant="ghost" href="/logs" class="w-full justify-start gap-3">
				<FileText class="w-5 h-5" />
				Logs
			</Button>
			<Button variant="ghost" href="/config" class="w-full justify-start gap-3">
				<Settings class="w-5 h-5" />
				Configuration
			</Button>
			<hr class="my-4 border-gray-800" />
			<Button variant="ghost" href="/lobotomy" class="w-full justify-start gap-3">Lobotomy</Button>
			<Button variant="ghost" href="/moderation" class="w-full justify-start gap-3">Moderation</Button>
			<Button variant="ghost" href="/memory" class="w-full justify-start gap-3">Memory</Button>
			<Button variant="ghost" href="/vtube" class="w-full justify-start gap-3">Vtube Studio</Button>
		</nav>

		<div class="p-4 border-t border-gray-800">
			<div class="flex items-center gap-2 px-4 py-2 rounded-lg transition" class:bg-green-900={isConnected} class:bg-red-900={!isConnected}>
				<div class={`w-2 h-2 rounded-full ${isConnected ? 'bg-green-500' : 'bg-red-500'}`} />
				<span class="text-sm">{isConnected ? 'Connected' : 'Disconnected'}</span>
			</div>
		</div>
	</aside>

	<!-- Main Content -->
	<div class="flex-1 flex flex-col overflow-hidden">
		<!-- Top Bar -->
		<nav class="w-full bg-gray-800 border-b border-gray-700 p-5 flex items-center justify-between">
			<div class="flex items-center gap-5">
				<button on:click={toggleSidebar} class="md:hidden p-2 hover:bg-gray-700 rounded-lg">
					{#if sidebarOpen}
						<X class="w-6 h-6" />
					{:else}
						<Menu class="w-6 h-6" />
					{/if}
				</button>
				<div class="flex items-center gap-3">
					<h1 class="text-2xl font-bold">J.A.I.son Control Panel</h1>
					<div class={`w-3 h-3 rounded-full ${isConnected ? 'bg-green-500' : 'bg-red-500'}`} />
				</div>
			</div>

			<div class="flex items-center gap-4">
				<Avatar.Root>
					<Avatar.Image src="https://www.kimjammer.com/icons/Logo.svg" alt="@jaison" />
					<Avatar.Fallback>JA</Avatar.Fallback>
				</Avatar.Root>

				<Button on:click={toggleMode} variant="outline" size="icon">
					<Sun class="h-[1.2rem] w-[1.2rem] rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0"/>
					<Moon class="absolute h-[1.2rem] w-[1.2rem] rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100"/>
				</Button>
			</div>
		</nav>

		<!-- Page Content -->
		<main class="flex-1 overflow-auto">
				<span class="sr-only">Toggle theme</span>
			</Button>
		</div>
	</nav>
	<slot></slot>
</div>