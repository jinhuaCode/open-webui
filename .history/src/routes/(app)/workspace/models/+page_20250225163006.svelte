<script>
	import { onMount } from 'svelte';
<<<<<<< HEAD
	import { config, models, settings } from '$lib/stores';
=======
	import { models } from '$lib/stores';
>>>>>>> dfef03c8e (同步远程)
	import { getModels } from '$lib/apis';
	import Models from '$lib/components/workspace/Models.svelte';

	onMount(async () => {
		await Promise.all([
			(async () => {
<<<<<<< HEAD
				models.set(
					await getModels(
						localStorage.token,
						$config?.features?.enable_direct_connections && ($settings?.directConnections ?? null)
					)
				);
=======
				models.set(await getModels(localStorage.token));
>>>>>>> dfef03c8e (同步远程)
			})()
		]);
	});
</script>

{#if $models !== null}
	<Models />
{/if}
