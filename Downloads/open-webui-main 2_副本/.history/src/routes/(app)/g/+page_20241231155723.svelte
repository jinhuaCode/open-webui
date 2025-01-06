<script lang="ts">
	import { page } from '$app/stores';
	console.log($page.params.model.id)

	import Chat from '$lib/components/chat/Chat.svelte';
</script>

<Chat chatIdProp={$page.params.id} />