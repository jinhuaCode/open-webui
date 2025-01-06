<script lang="ts">
	import { marked } from 'marked';

	import { toast } from 'svelte-sonner';
	import Sortable from 'sortablejs';
	import { WEBUI_VERSION , WEBUI_BASE_URL} from '$lib/constants';

	import fileSaver from 'file-saver';
	const { saveAs } = fileSaver;

	import { onMount, getContext, tick } from 'svelte';
	import { goto } from '$app/navigation';
	const i18n = getContext('i18n');

	import { userPreferences,WEBUI_NAME, config, mobile, models as _models, settings, user } from '$lib/stores';
	import {
		createNewModel,
		deleteModelById,
		getModels as getWorkspaceModels,
		toggleModelById,
		updateModelById,
	} from '$lib/apis/models/index';

	import { getModels } from '$lib/apis';

	import EllipsisHorizontal from '../icons/EllipsisHorizontal.svelte';
	import ModelMenu from './Models/ModelMenu.svelte';
	import ModelDeleteConfirmDialog from '../common/ConfirmDialog.svelte';
	import Tooltip from '../common/Tooltip.svelte';
	import GarbageBin from '../icons/GarbageBin.svelte';
	import Search from '../icons/Search.svelte';
	import Plus from '../icons/Plus.svelte';
	import ChevronRight from '../icons/ChevronRight.svelte';
	import Switch from '../common/Switch.svelte';
	import Spinner from '../common/Spinner.svelte';
	import { capitalizeFirstLetter } from '$lib/utils';

	let shiftKey = false;
	let importFiles;
	let modelsImportInputElement: HTMLInputElement;
	let loaded = false;

	let models = [];
	let mask = [];

	let filteredModels = [];
	let selectedModel = null;
	let showModelDeleteConfirm = false;
// 根据 searchValue（搜索值）对 models（模型列表）进行过滤，然后将过滤后的结果赋值给 filteredModels
	$: {
	  const sidebarMasks = $userPreferences.sidebarMasks; // 从本地存储获取偏好
	  if(models) {
		
		filteredModels = models.filter(
			(m) => 
			m.id !== 'kitn' &&
			m.id !== 'PersonalAssistant' &&
			(searchValue === '' || m.name.toLowerCase().includes(searchValue.toLowerCase()))
		);
		filteredModels.forEach(model => {
            model.is_showInSidebar = sidebarMasks.includes(model.id); 
			// 更新状态
        });
	}
	}

	let searchValue = '';

	const deleteModelHandler = async (model) => {
		const res = await deleteModelById(localStorage.token, model.id).catch((e) => {
			toast.error(e);
			return null;
		});

		if (res) {
			toast.success($i18n.t(`Deleted {{name}}`, { name: model.id }));
		}

		await _models.set(await getModels(localStorage.token));
		models = await getWorkspaceModels(localStorage.token);
	};

	const cloneModelHandler = async (model) => {
		sessionStorage.model = JSON.stringify({
			...model,
			id: `${model.id}-clone`,
			name: `${model.name} (Clone)`
		});
		goto('/GPTs/models/create');
	};

	const shareModelHandler = async (model) => {
		toast.success($i18n.t('Redirecting you to OpenWebUI Community'));

		const url = 'https://openwebui.com';

		const tab = await window.open(`${url}/models/create`, '_blank');

		// Define the event handler function
		const messageHandler = (event) => {
			if (event.origin !== url) return;
			if (event.data === 'loaded') {
				tab.postMessage(JSON.stringify(model), '*');

				// Remove the event listener after handling the message
				window.removeEventListener('message', messageHandler);
			}
		};

		window.addEventListener('message', messageHandler, false);
	};
	// 切换模型在侧边栏中的显示状态
	    // 更新 userPreferences 中 sidebarMasks 状态
  // 切换模型的显示状态（更新 sidebarMasks）
  function toggleSidebarState(modelId, isShow) {
        userPreferences.update(prefs => {
            let updatedSidebarMasks = [...prefs.sidebarMasks];
            if (isShow) {
                // 如果模型 ID 不在 sidebarMasks 中，才添加
                if (!updatedSidebarMasks.includes(modelId)) {
                    updatedSidebarMasks.push(modelId);
                    console.log('Added to sidebarMasks:', updatedSidebarMasks);
                }
            } else {
                // 如果模型 ID 在 sidebarMasks 中，才移除
        //         if (updatedSidebarMasks.includes(modelId)) {
        //             updatedSidebarMasks = updatedSidebarMasks.filter(id => id !== modelId);
        //             console.log('Removed from sidebarMasks:', updatedSidebarMasks);
        //         }
        //     }
		// 	//console.log('Updated sidebarMasks:', updatedSidebarMasks);

        //     prefs.sidebarMasks = updatedSidebarMasks;  // 更新偏好数据
        //     return prefs;
        // });
		const index = updatedSidebarMasks.indexOf(modelId);
                if (index !== -1) {
                    updatedSidebarMasks.splice(index, 1);
                }
            }
            return { ...prefs, sidebarMasks: updatedSidebarMasks };
        });
    }
	const hideModelHandler = async (model) => {
		let info = model.info;

		if (!info) {
			info = {
				id: model.id,
				name: model.name,
				meta: {
					suggestion_prompts: null
				},
				params: {}
			};
		}

		info.meta = {
			...info.meta,
			hidden: !(info?.meta?.hidden ?? false)
		};

		console.log(info);

		const res = await updateModelById(localStorage.token, info.id, info);

		if (res) {
			toast.success(
				$i18n.t(`GPTs {{name}} is now {{status}}`, {
					name: info.id,
					status: info.meta.hidden ? 'hidden' : 'visible'
				})
			);
		}

		await _models.set(await getModels(localStorage.token));
		models = await getWorkspaceModels(localStorage.token);
		mask = await getModels(localStorage.token);
		console.log("mask",mask)
	};

	const downloadModels = async (models) => {
		let blob = new Blob([JSON.stringify(models)], {
			type: 'application/json'
		});
		saveAs(blob, `models-export-${Date.now()}.json`);
	};

	const exportModelHandler = async (model) => {
		let blob = new Blob([JSON.stringify([model])], {
			type: 'application/json'
		});
		saveAs(blob, `${model.id}-${Date.now()}.json`);
	};

	onMount(async () => {
		models = await getWorkspaceModels(localStorage.token);
    const sidebarMasks = JSON.parse(localStorage.getItem('sidebarMasks')) || [];
    models.forEach(model => {
        model.is_showInSidebar = sidebarMasks.includes(model.id); // 本地同步状态
    });
		loaded = true;

		const onKeyDown = (event) => {
			if (event.key === 'Shift') {
				shiftKey = true;
			}
		};

		const onKeyUp = (event) => {
			if (event.key === 'Shift') {
				shiftKey = false;
			}
		};

		const onBlur = () => {
			shiftKey = false;
		};

		window.addEventListener('keydown', onKeyDown);
		window.addEventListener('keyup', onKeyUp);
		window.addEventListener('blur', onBlur);

		return () => {
			window.removeEventListener('keydown', onKeyDown);
			window.removeEventListener('keyup', onKeyUp);
			window.removeEventListener('blur', onBlur);
		};
	});
</script>


<!-- <Chat chatIdProp={$page.params.model}/> -->	
 <div class=" my-2 mb-5 gap-2 grid lg:grid-cols-2 xl:grid-cols-3" id="model-list">
		<div
			class=" flex flex-col cursor-pointer w-full px-3 py-2 dark:hover:bg-white/5 hover:bg-black/5 rounded-xl transition"
			id="model-item-{model.id}"
		>
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

				<a
					class=" flex flex-1 cursor-pointer w-full"
					href={`/g/?models=${encodeURIComponent(model.id)}`}

				>
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

			<div class="flex justify-between items-center -mb-0.5 px-0.5">
				<div class=" text-xs mt-0.5">
					<Tooltip
						content={model?.user?.email ?? $i18n.t('Deleted User')}
						className="flex shrink-0"
						placement="top-start"
					>
						<div class="shrink-0 text-gray-500">
							{$i18n.t('By {{name}}', {
								name: capitalizeFirstLetter(
									model?.user?.name ?? model?.user?.email ?? $i18n.t('Anonymous')
								)
							})}
						</div>
					</Tooltip>
				</div>

				<div class="flex flex-row gap-0.5 items-center">
					{#if shiftKey}
						<Tooltip content={$i18n.t('Delete')}>
							<button
								class="self-center w-fit text-sm px-2 py-2 dark:text-gray-300 dark:hover:text-white hover:bg-black/5 dark:hover:bg-white/5 rounded-xl"
								type="button"
								on:click={() => {
									deleteModelHandler(model);
								}}
							>
								<GarbageBin />
							</button>
						</Tooltip>
					{:else}
						{#if model.user_id === $user?.id}
							<a
								class="self-center w-fit text-sm px-2 py-2 dark:text-gray-300 dark:hover:text-white hover:bg-black/5 dark:hover:bg-white/5 rounded-xl"
								type="button"
								href={`/GPTs/models/edit?id=${encodeURIComponent(model.id)}`}
							>
								<svg
									xmlns="http://www.w3.org/2000/svg"
									fill="none"
									viewBox="0 0 24 24"
									stroke-width="1.5"
									stroke="currentColor"
									class="w-4 h-4"
								>
									<path
										stroke-linecap="round"
										stroke-linejoin="round"
										d="m16.862 4.487 1.687-1.688a1.875 1.875 0 1 1 2.652 2.652L6.832 19.82a4.5 4.5 0 0 1-1.897 1.13l-2.685.8.8-2.685a4.5 4.5 0 0 1 1.13-1.897L16.863 4.487Zm0 0L19.5 7.125"
									/>
								</svg>
							</a>
						{/if}

						<!-- <ModelMenu
							user={$user}
							{model}
							shareHandler={() => {
								shareModelHandler(model);
							}}
							cloneHandler={() => {
								cloneModelHandler(model);
							}}
							exportHandler={() => {
								exportModelHandler(model);
							}}
							hideHandler={() => {
								hideModelHandler(model);
							}}
							deleteHandler={() => {
								selectedModel = model;
								showModelDeleteConfirm = true;
							}}
							onClose={() => {}}
						>
							<button
								class="self-center w-fit text-sm p-1.5 dark:text-gray-300 dark:hover:text-white hover:bg-black/5 dark:hover:bg-white/5 rounded-xl"
								type="button"
							>
								<EllipsisHorizontal className="size-5" />
							</button>
						</ModelMenu> -->
<!-- 
						<div class="ml-1">
							<Tooltip content={model.is_active ? $i18n.t('Enabled') : $i18n.t('Disabled')}>
								<Switch
									bind:state={model.is_active}
									on:change={async (e) => {
										toggleModelById(localStorage.token, model.id);
										_models.set(await getModels(localStorage.token));
									}}
								/>
							</Tooltip>
						</div> -->
						<div class="ml-1">
							<Tooltip content={model.is_showInSidebar ? $i18n.t('Enabled in Sidebar') : $i18n.t('Disabled in Sidebar')}>
								<Switch
								
								state={model.is_showInSidebar}
								on:change={(e) => toggleSidebarState(model.id, e.detail)}
							/>
								<!-- bind:state={model.is_showInSidebar}
									on:change={(e) => toggleSidebarState(model.id, e.detail)}
									 -->
									<!-- on:change={(e) => toggleSidebarState(model.id, e.detail)} 
								checked={model.is_showInSidebar}  -->
							</Tooltip>
						</div>
					{/if}
				</div>
			</div>
		</div>
</div>