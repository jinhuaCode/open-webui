<!-- <script lang="ts">
	import { getContext, onMount } from 'svelte';
	import Checkbox from '$lib/components/common/Checkbox.svelte';
	import Tooltip from '$lib/components/common/Tooltip.svelte';

	const i18n = getContext('i18n');

	export let actions = [];
	export let selectedActionIds = [];

	let _actions = {};

	onMount(() => {
		_actions = actions.reduce((acc, action) => {
			acc[action.id] = {
				...action,
				selected: selectedActionIds.includes(action.id)
			};

			return acc;
		}, {});
	});
</script>

<div>
	<div class="flex w-full justify-between mb-1">
		<div class=" self-center text-sm font-semibold">{$i18n.t('Actions')}</div>
	</div>

	<div class=" text-xs dark:text-gray-500">
		{$i18n.t('To select actions here, add them to the "Functions" workspace first.')}
	</div>

	<div class="flex flex-col">
		{#if actions.length > 0}
			<div class=" flex items-center mt-2 flex-wrap">
				{#each Object.keys(_actions) as action, actionIdx}
					<div class=" flex items-center gap-2 mr-3">
						<div class="self-center flex items-center">
							<Checkbox
								state={_actions[action].selected ? 'checked' : 'unchecked'}
								on:change={(e) => {
									_actions[action].selected = e.detail === 'checked';
									selectedActionIds = Object.keys(_actions).filter((t) => _actions[t].selected);
								}}
							/>
						</div>

						<div class=" py-0.5 text-sm w-full capitalize font-medium">
							<Tooltip content={_actions[action].meta.description}>
								{_actions[action].name}
							</Tooltip>
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

	export let actions = []; // 工具列表
	export let selectedActionIds = []; // 选中的工具 ID 列表

	let dropdownOpen = false; // 控制下拉框的显示状态

	// 初始化工具数据
	let _actions = {};

	onMount(() => {
		_actions = actions.reduce((acc, action) => {
			acc[action.id] = {
				...action,
				selected: selectedActionIds.includes(action.id)
			};
			return acc;
		}, {});
	});

	// 切换选项状态
// 切换选项状态
function toggleActionSelection(actionId) {
		if (_actions[actionId].selected) {
			_actions[actionId].selected = false;
			selectedActionIds = selectedActionIds.filter((id) => id !== actionId);
		} else {
			_actions[actionId].selected = true;
			selectedActionIds = [...selectedActionIds, actionId];
		}
	}

	// 删除选中的工具
	function removeSelectedAction(actionId) {
		_actions[actionId].selected = false;
		selectedActionIds = selectedActionIds.filter((id) => id !== actionId);
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
		<div class=" self-center text-sm font-semibold">{$i18n.t('Tools')}</div>
	</div>

	<div class=" text-xs dark:text-gray-500">
		{$i18n.t('To select toolkits here, add them to the "Tools" workspace first.')}
	</div>
	<!-- 触发按钮 -->
	<div class="dropdown-toggle"
		on:click={() => (dropdownOpen = !dropdownOpen)}
	>

		{#if selectedActionIds.length > 0}
			<div >
				{#each selectedActionIds as actionId}
					<button class=" px-2.5 py-1.5 font-medium hover:bg-black/5 dark:hover:bg-white/5 outline outline-1 outline-gray-100 dark:outline-gray-850 rounded-3xl"
					type="button">
						{_actions[actionId].name}
						
						<span
							class="remove-icon text-dark-red"
							on:click={() => removeSelectedAction(actionId)}
						>
							X
						</span>
						
					</button>
				{/each}
			</div>
		{:else}
		<button
		class=" px-3.5 py-1.5 font-medium hover:bg-black/5 dark:hover:bg-white/5 outline outline-1 outline-gray-100 dark:outline-gray-850 rounded-3xl"
		type="button">{$i18n.t('Select Tools')}</button
	>
		{/if}
		
	</div>

	<!-- 下拉菜单 -->
	{#if dropdownOpen}
		<div class="dropdown-menu">
			{#each Object.keys(_actions) as actionId}
				<div
					class="dropdown-item"
					on:click={() => toggleActionSelection(actionId)}
				>
					<input
						type="checkbox"
						bind:checked={_actions[actionId].selected}
					/>
					<span class="ml-2">{_actions[actionId].name}</span>
				</div>
			{/each}
		</div>
	{/if}
	
</div>
