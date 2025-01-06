<!-- <script lang="ts">
	import { page } from '$app/stores';
	console.log($page.params.model)
	import { onMount, getContext, tick, onDestroy } from 'svelte';
	import { goto } from '$app/navigation';
	import Chat from '$lib/components/chat/Chat.svelte';

	// onMount(async () => {
		
    //   try {
    //     // 获取工作区模型列表
    //     // 更新 store 中的模型数据
	// 			// 先跳转到 /Masks/models 页面
		
	// 	// 使用 setTimeout 延迟跳转到目标路由
	// 	goto(`/GPTs/models`);
	goto(`/g/?models=${encodeURIComponent($page.params.model)}`);
	// 	goto(`/g/${encodeURIComponent($page.params.model)}`);


    //   } catch (error) {
    //     console.error('Error fetching models:', error);
    //   }
	// });
</script> -->

<!-- <Chat chatIdProp={$page.params.model}/> -->
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
		const _id =$page.params.model
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