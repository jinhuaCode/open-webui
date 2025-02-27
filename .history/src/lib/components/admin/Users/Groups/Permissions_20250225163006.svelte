<script lang="ts">
<<<<<<< HEAD
	import { getContext, onMount } from 'svelte';
=======
	import { getContext } from 'svelte';
>>>>>>> dfef03c8e (同步远程)
	const i18n = getContext('i18n');

	import Switch from '$lib/components/common/Switch.svelte';
	import Tooltip from '$lib/components/common/Tooltip.svelte';

<<<<<<< HEAD
	// Default values for permissions
	const defaultPermissions = {
=======
	export let permissions = {
>>>>>>> dfef03c8e (同步远程)
		workspace: {
			models: false,
			knowledge: false,
			prompts: false,
			tools: false
		},
<<<<<<< HEAD
		chat: {
			controls: true,
=======
	    // Masks:{
		// 	models:false
		// },
		chat: {
>>>>>>> dfef03c8e (同步远程)
			delete: true,
			edit: true,
			temporary: true,
			file_upload: true
<<<<<<< HEAD
		},
		features: {
			web_search: true,
			image_generation: true,
			code_interpreter: true
		}
	};

	export let permissions = {};

	// Reactive statement to ensure all fields are present in `permissions`
	$: {
		permissions = fillMissingProperties(permissions, defaultPermissions);
	}

	function fillMissingProperties(obj: any, defaults: any) {
		return {
			...defaults,
			...obj,
			workspace: { ...defaults.workspace, ...obj.workspace },
			chat: { ...defaults.chat, ...obj.chat },
			features: { ...defaults.features, ...obj.features }
		};
	}

	onMount(() => {
		permissions = fillMissingProperties(permissions, defaultPermissions);
	});
=======
		}
	};
>>>>>>> dfef03c8e (同步远程)
</script>

<div>
	<!-- <div>
		<div class=" mb-2 text-sm font-medium">{$i18n.t('Model Permissions')}</div>

		<div class="mb-2">
			<div class="flex justify-between items-center text-xs pr-2">
				<div class=" text-xs font-medium">{$i18n.t('Model Filtering')}</div>

				<Switch bind:state={permissions.model.filter} />
			</div>
		</div>

		{#if permissions.model.filter}
			<div class="mb-2">
				<div class=" space-y-1.5">
					<div class="flex flex-col w-full">
						<div class="mb-1 flex justify-between">
							<div class="text-xs text-gray-500">{$i18n.t('Model IDs')}</div>
						</div>

						{#if model_ids.length > 0}
							<div class="flex flex-col">
								{#each model_ids as modelId, modelIdx}
									<div class=" flex gap-2 w-full justify-between items-center">
										<div class=" text-sm flex-1 rounded-lg">
											{modelId}
										</div>
<<<<<<< HEAD
										<div class="shrink-0">
=======
										<div class="flex-shrink-0">
>>>>>>> dfef03c8e (同步远程)
											<button
												type="button"
												on:click={() => {
													model_ids = model_ids.filter((_, idx) => idx !== modelIdx);
												}}
											>
												<Minus strokeWidth="2" className="size-3.5" />
											</button>
										</div>
									</div>
								{/each}
							</div>
						{:else}
							<div class="text-gray-500 text-xs text-center py-2 px-10">
								{$i18n.t('No model IDs')}
							</div>
						{/if}
					</div>
				</div>
				<hr class=" border-gray-100 dark:border-gray-700/10 mt-2.5 mb-1 w-full" />

				<div class="flex items-center">
					<select
						class="w-full py-1 text-sm rounded-lg bg-transparent {selectedModelId
							? ''
<<<<<<< HEAD
							: 'text-gray-500'} placeholder:text-gray-300 dark:placeholder:text-gray-700 outline-hidden"
=======
							: 'text-gray-500'} placeholder:text-gray-300 dark:placeholder:text-gray-700 outline-none"
>>>>>>> dfef03c8e (同步远程)
						bind:value={selectedModelId}
					>
						<option value="">{$i18n.t('Select a model')}</option>
						{#each $models.filter((m) => m?.owned_by !== 'arena') as model}
							<option value={model.id} class="bg-gray-50 dark:bg-gray-700">{model.name}</option>
						{/each}
					</select>

					<div>
						<button
							type="button"
							on:click={() => {
								if (selectedModelId && !permissions.model.model_ids.includes(selectedModelId)) {
									permissions.model.model_ids = [...permissions.model.model_ids, selectedModelId];
									selectedModelId = '';
								}
							}}
						>
							<Plus className="size-3.5" strokeWidth="2" />
						</button>
					</div>
				</div>
			</div>
		{/if}

		<div class=" space-y-1 mb-3">
			<div class="">
				<div class="flex justify-between items-center text-xs">
					<div class=" text-xs font-medium">{$i18n.t('Default Model')}</div>
				</div>
			</div>

			<div class="flex-1 mr-2">
				<select
<<<<<<< HEAD
					class="w-full bg-transparent outline-hidden py-0.5 text-sm"
=======
					class="w-full bg-transparent outline-none py-0.5 text-sm"
>>>>>>> dfef03c8e (同步远程)
					bind:value={permissions.model.default_id}
					placeholder="Select a model"
				>
					<option value="" disabled selected>{$i18n.t('Select a model')}</option>
					{#each permissions.model.filter ? $models.filter( (model) => filterModelIds.includes(model.id) ) : $models.filter((model) => model.id) as model}
						<option value={model.id} class="bg-gray-100 dark:bg-gray-700">{model.name}</option>
					{/each}
				</select>
			</div>
		</div>
	</div>

<<<<<<< HEAD
	<hr class=" border-gray-100 dark:border-gray-850 my-2" /> -->
=======
	<hr class=" border-gray-50 dark:border-gray-850 my-2" /> -->
>>>>>>> dfef03c8e (同步远程)

	<div>
		<div class=" mb-2 text-sm font-medium">{$i18n.t('Workspace Permissions')}</div>

		<div class="  flex w-full justify-between my-2 pr-2">
			<div class=" self-center text-xs font-medium">
				{$i18n.t('Models Access')}
			</div>
			<Switch bind:state={permissions.workspace.models} />
		</div>

		<div class="  flex w-full justify-between my-2 pr-2">
			<div class=" self-center text-xs font-medium">
				{$i18n.t('Knowledge Access')}
			</div>
			<Switch bind:state={permissions.workspace.knowledge} />
		</div>

		<div class="  flex w-full justify-between my-2 pr-2">
			<div class=" self-center text-xs font-medium">
				{$i18n.t('Prompts Access')}
			</div>
			<Switch bind:state={permissions.workspace.prompts} />
		</div>

		<div class=" ">
			<Tooltip
				className=" flex w-full justify-between my-2 pr-2"
				content={$i18n.t(
					'Warning: Enabling this will allow users to upload arbitrary code on the server.'
				)}
				placement="top-start"
			>
				<div class=" self-center text-xs font-medium">
					{$i18n.t('Tools Access')}
				</div>
				<Switch bind:state={permissions.workspace.tools} />
			</Tooltip>
		</div>
	</div>

<<<<<<< HEAD
	<hr class=" border-gray-100 dark:border-gray-850 my-2" />
=======
	<hr class=" border-gray-50 dark:border-gray-850 my-2" />
>>>>>>> dfef03c8e (同步远程)

	<div>
		<div class=" mb-2 text-sm font-medium">{$i18n.t('Chat Permissions')}</div>

		<div class="  flex w-full justify-between my-2 pr-2">
			<div class=" self-center text-xs font-medium">
<<<<<<< HEAD
				{$i18n.t('Allow Chat Controls')}
			</div>

			<Switch bind:state={permissions.chat.controls} />
		</div>

		<div class="  flex w-full justify-between my-2 pr-2">
			<div class=" self-center text-xs font-medium">
=======
>>>>>>> dfef03c8e (同步远程)
				{$i18n.t('Allow File Upload')}
			</div>

			<Switch bind:state={permissions.chat.file_upload} />
		</div>

		<div class="  flex w-full justify-between my-2 pr-2">
			<div class=" self-center text-xs font-medium">
				{$i18n.t('Allow Chat Delete')}
			</div>

			<Switch bind:state={permissions.chat.delete} />
		</div>

		<div class="  flex w-full justify-between my-2 pr-2">
			<div class=" self-center text-xs font-medium">
				{$i18n.t('Allow Chat Edit')}
			</div>

			<Switch bind:state={permissions.chat.edit} />
		</div>

		<div class="  flex w-full justify-between my-2 pr-2">
			<div class=" self-center text-xs font-medium">
				{$i18n.t('Allow Temporary Chat')}
			</div>

			<Switch bind:state={permissions.chat.temporary} />
		</div>
	</div>
<<<<<<< HEAD

	<hr class=" border-gray-100 dark:border-gray-850 my-2" />

	<div>
		<div class=" mb-2 text-sm font-medium">{$i18n.t('Features Permissions')}</div>

		<div class="  flex w-full justify-between my-2 pr-2">
			<div class=" self-center text-xs font-medium">
				{$i18n.t('Web Search')}
			</div>

			<Switch bind:state={permissions.features.web_search} />
		</div>

		<div class="  flex w-full justify-between my-2 pr-2">
			<div class=" self-center text-xs font-medium">
				{$i18n.t('Image Generation')}
			</div>

			<Switch bind:state={permissions.features.image_generation} />
		</div>

		<div class="  flex w-full justify-between my-2 pr-2">
			<div class=" self-center text-xs font-medium">
				{$i18n.t('Code Interpreter')}
			</div>

			<Switch bind:state={permissions.features.code_interpreter} />
		</div>
	</div>
=======
>>>>>>> dfef03c8e (同步远程)
</div>
