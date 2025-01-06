<!-- <script>
	import { onMount } from 'svelte';
	import { models } from '$lib/stores';
	import { getModels } from '$lib/apis';
	import Models from '$lib/components/GPTs/Models.svelte';
	import { goto } from '$app/navigation';
	import Chat from '$lib/components/chat/Chat.svelte';

</script>

<Chat /> -->
<script>
	import { toast } from 'svelte-sonner';
	import { goto } from '$app/navigation';

	import { onMount, getContext } from 'svelte';
	const i18n = getContext('i18n');

	import { page } from '$app/stores';
	import { models } from '$lib/stores';

	import { getModelById, updateModelById } from '$lib/apis/models/index';
	import Chat from '$lib/components/chat/Chat.svelte';

	import { getModels } from '$lib/apis';

	let model = null;

	onMount(async () => {
		const _id = $page.url.searchParams.get('model');
		if (_id) {
			model = await getModelById(localStorage.token, _id).catch((e) => {
				return null;
			});

			if (!model) {
				goto('/workspace/models');
			}
		} else {
			goto('/workspace/models');
		}
	});

</script>

{#if model}
	<Chat/>
{/if}

