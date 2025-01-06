<!-- <script lang="ts">
	import { page } from '$app/stores';

	import Chat from '$lib/components/chat/Chat.svelte';
	
</script>

<Chat /> -->
<script lang="ts">
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';

	onMount(() => {
		goto('/GPTs/models');
	});
</script>
<!-- <Chat chatIdProp={$page.params.model}/> -->