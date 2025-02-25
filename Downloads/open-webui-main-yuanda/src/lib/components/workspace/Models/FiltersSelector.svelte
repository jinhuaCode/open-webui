<script lang="ts">
	import { getContext, onMount } from 'svelte';
	import Checkbox from '$lib/components/common/Checkbox.svelte';
	import Tooltip from '$lib/components/common/Tooltip.svelte';

	const i18n = getContext('i18n');

	export let filters = [];
	export let selectedFilterIds = [];
	let dropdownOpen = false; // 控制下拉框的显示状态

	let _filters = {};

	onMount(() => {
		_filters = filters.reduce((acc, filter) => {
			acc[filter.id] = {
				...filter,
				selected: selectedFilterIds.includes(filter.id)
			};

			return acc;
		}, {});
	});
	function toggleFilterSelection(FilterId) {
		if (_filters[FilterId].selected) {
			_filters[FilterId].selected = false;
			selectedFilterIds = selectedFilterIds.filter((id) => id !== FilterId);
		} else {
			_filters[FilterId].selected = true;
			selectedFilterIds = [...selectedFilterIds, FilterId];
		}
	}

	// 删除选中的工具
	function removeSelectedFilter(FilterId) {
		_filters[FilterId].selected = false;
		selectedFilterIds = selectedFilterIds.filter((id) => id !== FilterId);
	}
</script>
<style>
	.dropdown {
		position: relative;
		display: inline-block;
		width: 100%;
	}

	.dropdown-menu {
		position: absolute;
		top: 100%;
		left: 0;
		z-index: 10;
		background-color: white;
		border: 1px solid #ddd;
		border-radius: 0.5rem;
		width: 25%;
		max-height: 200px; /* 限制下拉框高度 */
		overflow-y: auto; /* 超出高度时显示滚动条 */
		box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
	}

	.dropdown-item {
		padding: 0.5rem 1rem;
		cursor: pointer;
		display: flex;
		align-items: center;
	}

	.dropdown-item:hover {
		background-color: #f5f5f5;
	}

	.button-container {
		display: flex;
		flex-wrap: wrap;
		gap: 0.5rem;
		margin-top: 0.5rem;
	}

	.selected-button {
		display: flex;
		align-items: center;
		background-color: #f0f0f0;
		border: 1px solid #ccc;
		padding: 0.3rem 0.6rem;
		border-radius: 999px;
		font-size: 0.875rem;
		cursor: default;
	}

	.selected-button .remove-icon {
		margin-left: 0.5rem;
		cursor: pointer;
		font-weight: bold;
		color: #555;
	}

	.selected-button .remove-icon:hover {
		color: red;
	}

	.dropdown-toggle {
		padding: 0rem 0rem;
		width: 25%;
		text-align: left;
		border: 1px solid #ddd;
		border-radius: 0.5rem;
		cursor: pointer;
		background-color: white;
		font-size: 0.875rem;
	}

	.dropdown.open .dropdown-menu {
		display: block; /* 显示下拉菜单 */
	}

	.dropdown.closed .dropdown-menu {
		display: none; /* 隐藏下拉菜单 */
	}
	.text-dark-red {
		color: #000000; 
		cursor: pointer; /* 鼠标移上去变为手型 */
	}

	.text-dark-red:hover {
		color: #8B0000; /* 悬停时的颜色变化，可以更亮一些 */
	}
</style>
<div class="dropdown {dropdownOpen ? 'open' : 'closed'}">
	<div class="flex w-full justify-between mb-1">
		<div class=" self-center text-sm font-semibold">{$i18n.t('Filters')}</div>
	</div>

	<div class=" text-xs dark:text-gray-500">
		{$i18n.t('To select filters here, add them to the "Functions" workspace first.')}
	</div>

	<div class="dropdown-toggle flex items-center mt-2 flex-wrap"
		on:click={() => (dropdownOpen = !dropdownOpen)}
	>
		{#if selectedFilterIds.length > 0}
			<div >
				{#each selectedFilterIds as FilterId}
					<button class=" px-2.5 py-1.5 font-medium hover:bg-black/5 dark:hover:bg-white/5 outline outline-1 outline-gray-100 dark:outline-gray-850 rounded-xl"
					type="button">
						{_filters[FilterId].name}
						
						<span
							class="remove-icon text-dark-red"
							on:click={() => removeSelectedFilter(FilterId)}
						>
							X
						</span>
						
					</button>
				{/each}
			</div>
		{:else}
		<button
		class=" px-3.5 py-1.5 font-medium hover:bg-black/5 dark:hover:bg-white/5 outline outline-1 outline-gray-100 dark:outline-gray-850 rounded-3xl"
		type="button">{$i18n.t('Select filters')}</button
	>
		{/if}
		
	</div>

	<!-- 下拉菜单 -->
	{#if dropdownOpen}
		<div class="dropdown-menu">
			{#each Object.keys(_filters) as FilterId}
				<div
					class="dropdown-item"
					on:click={() => toggleFilterSelection(FilterId)}
				>
					<input
						type="checkbox"
						bind:checked={_filters[FilterId].selected}
					/>
					<span class="ml-2">{_filters[FilterId].name}</span>
				</div>
			{/each}
		</div>
	{/if}
	
</div>