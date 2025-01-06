<!-- <script lang="ts">
	import { page } from '$app/stores';
	console.log($page.params.id)

	import Chat from '$lib/components/chat/Chat.svelte';
</script>

<Chat chatIdProp={$page.params.id}/> -->
<script lang="ts">
	import { page } from '$app/stores';
	console.log($page.params.model)
	import { onMount, getContext, tick, onDestroy } from 'svelte';
	import { goto } from '$app/navigation';

	import Chat from '$lib/components/chat/Chat.svelte';
	onMount(async () => {
		
      try {
        // 获取工作区模型列表
        // 更新 store 中的模型数据
		goto(`/g/?models=${encodeURIComponent($page.params.model)}`);


      } catch (error) {
        console.error('Error fetching models:', error);
      }
    
	
	});
</script>

<!-- <Chat chatIdProp={$page.params.model}/> -->