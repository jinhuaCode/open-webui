<script lang="ts">
	import { page } from '$app/stores';

	import Chat from '$lib/components/chat/Chat.svelte';
<<<<<<< HEAD
	import Help from '$lib/components/layout/Help.svelte';
</script>

<Help />
=======
</script>

>>>>>>> dfef03c8e (同步远程)
<Chat chatIdProp={$page.params.id} />
