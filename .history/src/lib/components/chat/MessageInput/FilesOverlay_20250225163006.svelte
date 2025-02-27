<script lang="ts">
	import { showSidebar } from '$lib/stores';
	import AddFilesPlaceholder from '$lib/components/AddFilesPlaceholder.svelte';

	export let show = false;
	let overlayElement = null;

	$: if (show && overlayElement) {
		document.body.appendChild(overlayElement);
		document.body.style.overflow = 'hidden';
	} else if (overlayElement) {
		document.body.removeChild(overlayElement);
		document.body.style.overflow = 'unset';
	}
</script>

{#if show}
	<div
		bind:this={overlayElement}
		class="fixed {$showSidebar
			? 'left-0 md:left-[260px] md:w-[calc(100%-260px)]'
<<<<<<< HEAD
			: 'left-0'}  fixed top-0 right-0 bottom-0 w-full h-full flex z-9999 touch-none pointer-events-none"
=======
			: 'left-0'}  fixed top-0 right-0 bottom-0 w-full h-full flex z-[9999] touch-none pointer-events-none"
>>>>>>> dfef03c8e (同步远程)
		id="dropzone"
		role="region"
		aria-label="Drag and Drop Container"
	>
<<<<<<< HEAD
		<div class="absolute w-full h-full backdrop-blur-sm bg-gray-800/40 flex justify-center">
=======
		<div class="absolute w-full h-full backdrop-blur bg-gray-800/40 flex justify-center">
>>>>>>> dfef03c8e (同步远程)
			<div class="m-auto pt-64 flex flex-col justify-center">
				<div class="max-w-md">
					<AddFilesPlaceholder />
				</div>
			</div>
		</div>
	</div>
{/if}
