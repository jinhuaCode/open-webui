<script>
	import { onMount } from 'svelte';
	import { models } from '$lib/stores';
	import { getModels } from '$lib/apis';
	import Models from '$lib/components/GPTs/Models.svelte';
	import { goto } from '$app/navigation';
	import Chat from '$lib/components/chat/Chat.svelte';

	onMount(async () => {

		await Promise.all([
			(async () => {
				models.set(await getModels(localStorage.token));

			})()
		]);
		goto(`/GPTs/models`);

	});
</script>

<Chat />

