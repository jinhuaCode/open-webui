<script>
	import { onMount } from 'svelte';
	import { models } from '$lib/stores';
	import { getModels } from '$lib/apis';
	import Models from '$lib/components/GPTs/Models.svelte';
	import { goto } from '$app/navigation';
	import Chat from '$lib/components/chat/Chat.svelte';

	onMount(async () => {

		await Promise.all([
			(async () => {
				models.set(await getModels(localStorage.token));

			})()
		]);


	});
</script>

<!-- <Chat /> -->
<div class="flex gap-4 mt-0.5 mb-0.5">
	<div class=" w-[44px]">
		<div
			class=" rounded-full object-cover {model.is_active
				? ''
				: 'opacity-50 dark:opacity-50'} "
		>
			<img
				src={model?.meta?.profile_image_url ?? '/static/favicon.png'}
				alt="modelfile profile"
				class=" rounded-md w-full h-full object-cover"
			/>
		</div>
	</div>


		<div class=" flex-1 self-center {model.is_active ? '' : 'text-gray-500'}">
			<Tooltip
				content={marked.parse(model?.meta?.description ?? model.id)}
				className=" w-fit"
				placement="top-start"
			>
				<div class=" font-semibold line-clamp-1">{model.name}</div>
			</Tooltip>

			<div class="flex gap-1 text-xs overflow-hidden">
				<div class="line-clamp-1">
					{#if (model?.meta?.description ?? '').trim()}
						{model?.meta?.description}
					{:else}
						{model.id}
					{/if}
				</div>
			</div>
		</div>

		
	</a>
</div>

