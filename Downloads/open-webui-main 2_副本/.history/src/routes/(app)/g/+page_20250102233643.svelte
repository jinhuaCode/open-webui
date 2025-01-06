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
	let seletedmodel = null;
	onMount(async () => {
		const _id = $page.url.searchParams.get('models');
		console.log("id",_id);
		if (_id) {
			model = await getModelById(localStorage.token, _id).catch((e) => {
				console.log("model",model);
				return model;
			});

			if (!model) {
				goto('/workspace/models');
			}
			console.log("model",model);
		} else {
			goto('/workspace/models');
		}
	});

</script>

	<Chat {seletedmodel}/>

