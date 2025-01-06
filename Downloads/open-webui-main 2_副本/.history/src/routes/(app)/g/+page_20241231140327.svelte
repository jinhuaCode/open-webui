<script lang="ts">
	import { page } from '$app/stores';

	import Models from '$lib/components/GPTs/Models.svelte';
</script>

<Models chatIdProp={$page.params.id} />