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
				// 先跳转到 /Masks/models 页面
		
		// 使用 setTimeout 延迟跳转到目标路由
		goto(`/Masks/models`);
		// goto(`/g/?models=${encodeURIComponent($page.params.model)}`);
		goto(`/g/${encodeURIComponent($page.params.model)}`);


      } catch (error) {
        console.error('Error fetching models:', error);
      }
    
	
	});
</script>
<Chat />

<!-- <Chat chatIdProp={$page.params.model}/> -->