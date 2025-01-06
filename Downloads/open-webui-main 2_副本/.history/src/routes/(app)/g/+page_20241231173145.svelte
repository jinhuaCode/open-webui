<!-- <script lang="ts">
	import { page } from '$app/stores';

	import Chat from '$lib/components/chat/Chat.svelte';
	
</script>

<Chat /> -->
<script lang="ts">
	import { goto } from '$app/navigation';
	import { onMount } from 'svelte';
	import { page } from '$app/stores';

	onMount(() => {
		goto('/GPTs/models');
		
		// 使用 setTimeout 延迟跳转到目标路由
			goto(`/g/?models=${encodeURIComponent($page.params.model)}`);
	});
</script>
<!-- <Chat chatIdProp={$page.params.model}/> -->