<script lang="ts">
	import { page } from '$app/stores';
	console.log($page.params.id)

	import Chat from '$lib/components/chat/Chat.svelte';
</script>

<Chat />
