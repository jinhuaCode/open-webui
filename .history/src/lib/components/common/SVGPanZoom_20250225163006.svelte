<script lang="ts">
<<<<<<< HEAD
	import fileSaver from 'file-saver';
	const { saveAs } = fileSaver;

	import { toast } from 'svelte-sonner';

	import panzoom, { type PanZoom } from 'panzoom';
	import DOMPurify from 'dompurify';

	import { onMount, getContext } from 'svelte';
	const i18n = getContext('i18n');

	import { copyToClipboard } from '$lib/utils';

	import DocumentDuplicate from '../icons/DocumentDuplicate.svelte';
	import Tooltip from './Tooltip.svelte';
	import Clipboard from '../icons/Clipboard.svelte';
	import Reset from '../icons/Reset.svelte';
	import ArrowDownTray from '../icons/ArrowDownTray.svelte';
=======
	import { onMount, getContext } from 'svelte';
	const i18n = getContext('i18n');

	import panzoom from 'panzoom';

	import DOMPurify from 'dompurify';
	import DocumentDuplicate from '../icons/DocumentDuplicate.svelte';
	import { copyToClipboard } from '$lib/utils';
	import { toast } from 'svelte-sonner';
	import Tooltip from './Tooltip.svelte';
	import Clipboard from '../icons/Clipboard.svelte';
>>>>>>> dfef03c8e (同步远程)

	export let className = '';
	export let svg = '';
	export let content = '';

<<<<<<< HEAD
	let instance: PanZoom;
=======
	let instance;
>>>>>>> dfef03c8e (同步远程)

	let sceneParentElement: HTMLElement;
	let sceneElement: HTMLElement;

	$: if (sceneElement) {
		instance = panzoom(sceneElement, {
			bounds: true,
			boundsPadding: 0.1,

			zoomSpeed: 0.065
		});
	}
<<<<<<< HEAD
	const resetPanZoomViewport = () => {
		instance.moveTo(0, 0);
		instance.zoomAbs(0, 0, 1);
		console.log(instance.getTransform());
	};

	const downloadAsSVG = () => {
		const svgBlob = new Blob([svg], { type: 'image/svg+xml' });
		saveAs(svgBlob, `diagram.svg`);
	};
=======
>>>>>>> dfef03c8e (同步远程)
</script>

<div bind:this={sceneParentElement} class="relative {className}">
	<div bind:this={sceneElement} class="flex h-full max-h-full justify-center items-center">
		{@html svg}
	</div>

	{#if content}
		<div class=" absolute top-1 right-1">
<<<<<<< HEAD
			<div class="flex gap-1">
				<Tooltip content={$i18n.t('Download as SVG')}>
					<button
						class="p-1.5 rounded-lg border border-gray-100 dark:border-none dark:bg-gray-850 hover:bg-gray-50 dark:hover:bg-gray-800 transition"
						on:click={() => {
							downloadAsSVG();
						}}
					>
						<ArrowDownTray className=" size-4" />
					</button>
				</Tooltip>

				<Tooltip content={$i18n.t('Reset view')}>
					<button
						class="p-1.5 rounded-lg border border-gray-100 dark:border-none dark:bg-gray-850 hover:bg-gray-50 dark:hover:bg-gray-800 transition"
						on:click={() => {
							resetPanZoomViewport();
						}}
					>
						<Reset className=" size-4" />
					</button>
				</Tooltip>

				<Tooltip content={$i18n.t('Copy to clipboard')}>
					<button
						class="p-1.5 rounded-lg border border-gray-100 dark:border-none dark:bg-gray-850 hover:bg-gray-50 dark:hover:bg-gray-800 transition"
						on:click={() => {
							copyToClipboard(content);
							toast.success($i18n.t('Copied to clipboard'));
						}}
					>
						<Clipboard className=" size-4" strokeWidth="1.5" />
					</button>
				</Tooltip>
			</div>
=======
			<Tooltip content={$i18n.t('Copy to clipboard')}>
				<button
					class="p-1.5 rounded-lg border border-gray-100 dark:border-none dark:bg-gray-850 hover:bg-gray-50 dark:hover:bg-gray-800 transition"
					on:click={() => {
						copyToClipboard(content);
						toast.success($i18n.t('Copied to clipboard'));
					}}
				>
					<Clipboard className=" size-4" strokeWidth="1.5" />
				</button>
			</Tooltip>
>>>>>>> dfef03c8e (同步远程)
		</div>
	{/if}
</div>
