<script lang="ts">
	import { createEventDispatcher } from 'svelte';

	const dispatch = createEventDispatcher();
	import RecursiveFolder from './RecursiveFolder.svelte';
	export let folders = {};

	let folderList = [];
	// Get the list of folders that have no parent, sorted by name alphabetically
	$: folderList = Object.keys(folders)
		.filter((key) => folders[key].parent_id === null)
		.sort((a, b) =>
			folders[a].name.localeCompare(folders[b].name, undefined, {
				numeric: true,
				sensitivity: 'base'
			})
		);
</script>

{#each folderList as folderId (folderId)}
	<RecursiveFolder
<<<<<<< HEAD
		className=""
=======
		className="px-2"
>>>>>>> dfef03c8e (同步远程)
		{folders}
		{folderId}
		on:import={(e) => {
			dispatch('import', e.detail);
		}}
		on:update={(e) => {
			dispatch('update', e.detail);
		}}
		on:change={(e) => {
			dispatch('change', e.detail);
		}}
	/>
{/each}
