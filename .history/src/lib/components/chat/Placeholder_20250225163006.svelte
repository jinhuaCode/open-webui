<script lang="ts">
	import { toast } from 'svelte-sonner';
	import { marked } from 'marked';

	import { onMount, getContext, tick, createEventDispatcher } from 'svelte';
	import { blur, fade } from 'svelte/transition';

	const dispatch = createEventDispatcher();

	import { config, user, models as _models, temporaryChatEnabled } from '$lib/stores';
	import { sanitizeResponseContent, findWordIndices } from '$lib/utils';
	import { WEBUI_BASE_URL } from '$lib/constants';

	import Suggestions from './Suggestions.svelte';
	import Tooltip from '$lib/components/common/Tooltip.svelte';
	import EyeSlash from '$lib/components/icons/EyeSlash.svelte';
<<<<<<< HEAD
	import MessageInput from './MessageInput.svelte';
=======
	import MessageInputTools from './MessageInputTools.svelte';
	import MessageInputSelf from './MessageInputSelf.svelte';
	import MessageInput from './MessageInput.svelte';
	import Form from './Form.svelte';
>>>>>>> dfef03c8e (同步远程)

	const i18n = getContext('i18n');

	export let transparentBackground = false;

	export let createMessagePair: Function;
	export let stopResponse: Function;

	export let autoScroll = false;

	export let atSelectedModel: Model | undefined;
	export let selectedModels: [''];

	export let history;

	export let prompt = '';
	export let files = [];

	export let selectedToolIds = [];
<<<<<<< HEAD
	export let imageGenerationEnabled = false;
	export let codeInterpreterEnabled = false;
	export let webSearchEnabled = false;

	let models = [];

=======
	export let webSearchEnabled = false;

	let models = [];
    const handleFormSubmit = async (event) => {
        const formData = event.detail;

        // 将表单数据发送到后端模型
        dispatch('submit', { type: 'form', data: formData });
    };
>>>>>>> dfef03c8e (同步远程)
	const selectSuggestionPrompt = async (p) => {
		let text = p;

		if (p.includes('{{CLIPBOARD}}')) {
			const clipboardText = await navigator.clipboard.readText().catch((err) => {
				toast.error($i18n.t('Failed to read clipboard contents'));
				return '{{CLIPBOARD}}';
			});

			text = p.replaceAll('{{CLIPBOARD}}', clipboardText);

			console.log('Clipboard text:', clipboardText, text);
		}

		prompt = text;

		console.log(prompt);
		await tick();

		const chatInputContainerElement = document.getElementById('chat-input-container');
		const chatInputElement = document.getElementById('chat-input');

		if (chatInputContainerElement) {
			chatInputContainerElement.style.height = '';
			chatInputContainerElement.style.height =
				Math.min(chatInputContainerElement.scrollHeight, 200) + 'px';
		}

		await tick();
		if (chatInputElement) {
			chatInputElement.focus();
			chatInputElement.dispatchEvent(new Event('input'));
		}

		await tick();
	};

	let selectedModelIdx = 0;

	$: if (selectedModels.length > 0) {
		selectedModelIdx = models.length - 1;
<<<<<<< HEAD
=======
		console.log("selectedModels",selectedModels)

>>>>>>> dfef03c8e (同步远程)
	}

	$: models = selectedModels.map((id) => $_models.find((m) => m.id === id));

<<<<<<< HEAD
	onMount(() => {});
</script>

<div class="m-auto w-full max-w-6xl px-2 @2xl:px-20 translate-y-6 py-24 text-center">
	{#if $temporaryChatEnabled}
=======
// 	let currentModel=null;
// 	$: currentModel = models[selectedModelIdx];
// console.log("models",models)
	onMount(() => {});
</script>

<div class="m-auto w-full max-w-6xl px-2 xl:px-20 translate-y-6 py-24 text-center">
	<!-- {#if $temporaryChatEnabled}
>>>>>>> dfef03c8e (同步远程)
		<Tooltip
			content="This chat won't appear in history and your messages will not be saved."
			className="w-full flex justify-center mb-0.5"
			placement="top"
		>
			<div class="flex items-center gap-2 text-gray-500 font-medium text-lg my-2 w-fit">
				<EyeSlash strokeWidth="2.5" className="size-5" /> Temporary Chat
			</div>
		</Tooltip>
<<<<<<< HEAD
	{/if}
=======
	{/if} -->
>>>>>>> dfef03c8e (同步远程)

	<div
		class="w-full text-3xl text-gray-800 dark:text-gray-100 font-medium text-center flex items-center gap-4 font-primary"
	>
		<div class="w-full flex flex-col justify-center items-center">
<<<<<<< HEAD
			<div class="flex flex-row justify-center gap-3 @sm:gap-3.5 w-fit px-5">
				<div class="flex shrink-0 justify-center">
=======
			<div class="flex flex-row justify-center gap-3 sm:gap-3.5 w-fit px-5">
				<div class="flex flex-shrink-0 justify-center">
>>>>>>> dfef03c8e (同步远程)
					<div class="flex -space-x-4 mb-0.5" in:fade={{ duration: 100 }}>
						{#each models as model, modelIdx}
							<Tooltip
								content={(models[modelIdx]?.info?.meta?.tags ?? [])
									.map((tag) => tag.name.toUpperCase())
									.join(', ')}
								placement="top"
							>
								<button
									on:click={() => {
										selectedModelIdx = modelIdx;
									}}
								>
									<img
										crossorigin="anonymous"
										src={model?.info?.meta?.profile_image_url ??
											($i18n.language === 'dg-DG'
												? `/doge.png`
												: `${WEBUI_BASE_URL}/static/favicon.png`)}
<<<<<<< HEAD
										class=" size-9 @sm:size-10 rounded-full border-[1px] border-gray-200 dark:border-none"
=======
										class=" size-9 sm:size-10 rounded-md border-gray-200 dark:border-none"
>>>>>>> dfef03c8e (同步远程)
										alt="logo"
										draggable="false"
									/>
								</button>
							</Tooltip>
						{/each}
					</div>
				</div>

<<<<<<< HEAD
				<div class=" text-3xl @sm:text-4xl line-clamp-1" in:fade={{ duration: 100 }}>
=======
				<div class=" text-3xl sm:text-4xl line-clamp-1" in:fade={{ duration: 100 }}>
>>>>>>> dfef03c8e (同步远程)
					{#if models[selectedModelIdx]?.name}
						{models[selectedModelIdx]?.name}
					{:else}
						{$i18n.t('Hello, {{name}}', { name: $user.name })}
					{/if}
				</div>
			</div>

			<div class="flex mt-1 mb-2">
				<div in:fade={{ duration: 100, delay: 50 }}>
					{#if models[selectedModelIdx]?.info?.meta?.description ?? null}
						<Tooltip
							className=" w-fit"
							content={marked.parse(
								sanitizeResponseContent(models[selectedModelIdx]?.info?.meta?.description ?? '')
							)}
							placement="top"
						>
							<div
								class="mt-0.5 px-2 text-sm font-normal text-gray-500 dark:text-gray-400 line-clamp-2 max-w-xl markdown"
							>
								{@html marked.parse(
									sanitizeResponseContent(models[selectedModelIdx]?.info?.meta?.description)
								)}
							</div>
						</Tooltip>

						{#if models[selectedModelIdx]?.info?.meta?.user}
							<div class="mt-0.5 text-sm font-normal text-gray-400 dark:text-gray-500">
								By
								{#if models[selectedModelIdx]?.info?.meta?.user.community}
									<a
										href="https://openwebui.com/m/{models[selectedModelIdx]?.info?.meta?.user
											.username}"
										>{models[selectedModelIdx]?.info?.meta?.user.name
											? models[selectedModelIdx]?.info?.meta?.user.name
											: `@${models[selectedModelIdx]?.info?.meta?.user.username}`}</a
									>
								{:else}
									{models[selectedModelIdx]?.info?.meta?.user.name}
								{/if}
							</div>
						{/if}
					{/if}
				</div>
			</div>

<<<<<<< HEAD
			<div class="text-base font-normal @md:max-w-3xl w-full py-3 {atSelectedModel ? 'mt-2' : ''}">
				<MessageInput
					{history}
					{selectedModels}
					bind:files
					bind:prompt
					bind:autoScroll
					bind:selectedToolIds
					bind:imageGenerationEnabled
					bind:codeInterpreterEnabled
					bind:webSearchEnabled
					bind:atSelectedModel
					{transparentBackground}
					{stopResponse}
					{createMessagePair}
					placeholder={$i18n.t('How can I help you today?')}
					on:upload={(e) => {
						dispatch('upload', e.detail);
					}}
					on:submit={(e) => {
						dispatch('submit', e.detail);
					}}
				/>
=======
			<div
				class="text-base font-normal xl:translate-x-6 md:max-w-3xl w-full py-3 {atSelectedModel
					? 'mt-2'
					: ''}"
			>
			{#if models[selectedModelIdx]?.info?.meta?.capabilities.uploader ?? true }
			{#if  models[selectedModelIdx]?.id === "root-cause-analysis-form"}
    <!-- <form >
        <div>
            <label for="input1">Input 1:</label>
            <input type="text" id="input1"  required />
        </div>
        <div>
            <label for="input2">Input 2:</label>
            <input type="text" id="input2" required />
        </div>
        <button type="submit">Submit</button>
    </form> -->
	<Form
	on:submit={handleFormSubmit}
	></Form>
		{:else}
			<MessageInput
		{history}
		{selectedModels}
		bind:files
		bind:prompt
		bind:autoScroll
		bind:selectedToolIds
		bind:webSearchEnabled
		bind:atSelectedModel
		{transparentBackground}
		{stopResponse}
		{createMessagePair}
		placeholder={$i18n.t('How can I help you today?')}
		on:upload={(e) => {
			dispatch('upload', e.detail);
		}}
		on:submit={(e) => {
            dispatch('submit', { type: 'message', data: e.detail });
		}}
	/>
	{/if}
<!-- {:else if models[selectedModelIdx]?info?.meta?.capabilities?.uploader ?? true}// && models[selectedModelIdx]?.id === "PersonalAssistant" )|| models[selectedModelIdx]?.id === "flowchart" }
	<MessageInput
		{history}
		{selectedModels}
		bind:files
		bind:prompt
		bind:autoScroll
		bind:selectedToolIds
		bind:webSearchEnabled
		bind:atSelectedModel
		{transparentBackground}
		{stopResponse}
		{createMessagePair}
		placeholder={$i18n.t('How can I help you today?')}
		on:upload={(e) => {
			dispatch('upload', e.detail);
		}}
		on:submit={(e) => {
			dispatch('submit', e.detail);
		}}
	/> -->
{:else}
	<MessageInputTools
		{history}
		{selectedModels}
		bind:files
		bind:prompt
		bind:autoScroll
		bind:selectedToolIds
		bind:webSearchEnabled
		bind:atSelectedModel
		{transparentBackground}
		{stopResponse}
		{createMessagePair}
		placeholder={$i18n.t('How can I help you today?')}
		on:upload={(e) => {
			dispatch('upload', e.detail);
		}}
		on:submit={(e) => {
            dispatch('submit', { type: 'message', data: e.detail });
		}}
	/>
{/if}

>>>>>>> dfef03c8e (同步远程)
			</div>
		</div>
	</div>
	<div class="mx-auto max-w-2xl font-primary" in:fade={{ duration: 200, delay: 200 }}>
		<div class="mx-5">
			<Suggestions
				suggestionPrompts={models[selectedModelIdx]?.info?.meta?.suggestion_prompts ??
					$config?.default_prompt_suggestions ??
					[]}
<<<<<<< HEAD
				inputValue={prompt}
=======
>>>>>>> dfef03c8e (同步远程)
				on:select={(e) => {
					selectSuggestionPrompt(e.detail);
				}}
			/>
		</div>
<<<<<<< HEAD
	</div>
=======
	</div>	
</div>
<div class="fixed bottom-4 right-4">
	<img
		crossorigin="anonymous"
		src="{WEBUI_BASE_URL}/static/favicon1.png"
		class="w-24 h-7"
		alt="logo"
	/>
>>>>>>> dfef03c8e (同步远程)
</div>
