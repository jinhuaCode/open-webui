<!-- <script lang="ts">
	import Checkbox from '$lib/components/common/Checkbox.svelte';
	import { getContext, onMount } from 'svelte';

	export let tools = [];

	let _tools = {};

	export let selectedToolIds = [];

	const i18n = getContext('i18n');

	onMount(() => {
		_tools = tools.reduce((acc, tool) => {
			acc[tool.id] = {
				...tool,
				selected: selectedToolIds.includes(tool.id)
			};

			return acc;
		}, {});
	});
</script>

<div>
	<div class="flex w-full justify-between mb-1">
		<div class=" self-center text-sm font-semibold">{$i18n.t('Tools')}</div>
	</div>

	<div class=" text-xs dark:text-gray-500">
		{$i18n.t('To select toolkits here, add them to the "Tools" workspace first.')}
	</div>

	<div class="flex flex-col">
		{#if tools.length > 0}
			<div class=" flex items-center mt-2 flex-wrap">
				{#each Object.keys(_tools) as tool, toolIdx}
					<div class=" flex items-center gap-2 mr-3">
						<div class="self-center flex items-center">
							<Checkbox
								state={_tools[tool].selected ? 'checked' : 'unchecked'}
								on:change={(e) => {
									_tools[tool].selected = e.detail === 'checked';
									selectedToolIds = Object.keys(_tools).filter((t) => _tools[t].selected);
								}}
							/>
						</div>

						<div class=" py-0.5 text-sm w-full capitalize font-medium">
							{_tools[tool].name}
						</div>
					</div>
				{/each}
			</div>
		{/if}
	</div>
</div> -->
<script lang="ts">
	import Checkbox from '$lib/components/common/Checkbox.svelte';
	import { getContext, onMount } from 'svelte';

	const i18n = getContext('i18n');

	export let tools = []; // 工具列表
	export let selectedToolIds = []; // 选中的工具 ID 列表

	let dropdownOpen = false; // 控制下拉框的显示状态

	// 初始化工具数据
	let _tools = {};

	onMount(() => {
		_tools = tools.reduce((acc, tool) => {
			acc[tool.id] = {
				...tool,
				selected: selectedToolIds.includes(tool.id)
			};
			return acc;
		}, {});
	});

	// 切换选项状态
// 切换选项状态
function toggleToolSelection(toolId) {
		if (_tools[toolId].selected) {
			_tools[toolId].selected = false;
			selectedToolIds = selectedToolIds.filter((id) => id !== toolId);
		} else {
			_tools[toolId].selected = true;
			selectedToolIds = [...selectedToolIds, toolId];
		}
	}

	// 删除选中的工具
	function removeSelectedTool(toolId) {
		_tools[toolId].selected = false;
		selectedToolIds = selectedToolIds.filter((id) => id !== toolId);
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
<!-- 下拉框 -->
<div class="dropdown {dropdownOpen ? 'open' : 'closed'}">
	<div class="flex w-full justify-between mb-1">
		<div class=" self-center text-sm font-semibold">{$i18n.t('Actions')}</div>
	</div>

	<div class=" text-xs dark:text-gray-500">
		{$i18n.t('To select toolkits here, add them to the "Tools" workspace first.')}
	</div>
	<!-- 触发按钮 -->
	<div class="dropdown-toggle"
		on:click={() => (dropdownOpen = !dropdownOpen)}
	>

		{#if selectedToolIds.length > 0}
			<div >
				{#each selectedToolIds as toolId}
					<button class=" px-2.5 py-1.5 font-medium hover:bg-black/5 dark:hover:bg-white/5 outline outline-1 outline-gray-100 dark:outline-gray-850 rounded-3xl"
					type="button">
						{_tools[toolId].name}
						
						<span
							class="remove-icon text-dark-red"
							on:click={() => removeSelectedTool(toolId)}
						>
							X
						</span>
						
					</button>
				{/each}
			</div>
		{:else}
		<button
		class=" px-3.5 py-1.5 font-medium hover:bg-black/5 dark:hover:bg-white/5 outline outline-1 outline-gray-100 dark:outline-gray-850 rounded-3xl"
		type="button">{$i18n.t('Select Actions')}</button
	>
		{/if}
		
	</div>

	<!-- 下拉菜单 -->
	{#if dropdownOpen}
		<div class="dropdown-menu">
			{#each Object.keys(_tools) as toolId}
				<div
					class="dropdown-item"
					on:click={() => toggleToolSelection(toolId)}
				>
					<input
						type="checkbox"
						bind:checked={_tools[toolId].selected}
					/>
					<span class="ml-2">{_tools[toolId].name}</span>
				</div>
			{/each}
		</div>
	{/if}
	
</div>
