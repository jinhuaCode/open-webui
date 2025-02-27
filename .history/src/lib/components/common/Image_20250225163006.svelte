<script lang="ts">
	import { WEBUI_BASE_URL } from '$lib/constants';
	import ImagePreview from './ImagePreview.svelte';

	export let src = '';
	export let alt = '';

<<<<<<< HEAD
	export let className = ' w-full outline-hidden focus:outline-hidden';
=======
	export let className = ' w-full';
>>>>>>> dfef03c8e (同步远程)
	export let imageClassName = 'rounded-lg';

	let _src = '';
	$: _src = src.startsWith('/') ? `${WEBUI_BASE_URL}${src}` : src;

	let showImagePreview = false;
</script>

<button
	class={className}
	on:click={() => {
		showImagePreview = true;
	}}
<<<<<<< HEAD
	type="button"
=======
>>>>>>> dfef03c8e (同步远程)
>
	<img src={_src} {alt} class={imageClassName} draggable="false" data-cy="image" />
</button>

<ImagePreview bind:show={showImagePreview} src={_src} {alt} />
