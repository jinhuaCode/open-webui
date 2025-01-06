<script lang="ts">
	import { page } from '$app/stores';

	import Chat from '$lib/components/chat/Chat.svelte';
	console.log($page.params.model.id)
</script>

<Chat chatIdProp={$page.params.id} />
