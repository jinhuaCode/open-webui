<script lang="ts">
<<<<<<< HEAD
	import { toast } from 'svelte-sonner';
	import { v4 as uuidv4 } from 'uuid';
=======
	
	import { toast } from 'svelte-sonner';
	import { v4 as uuidv4 } from 'uuid';
	import { page } from '$app/stores';
	import ChatMenu from './Sidebar/ChatMenu.svelte';
	import { WEBUI_NAME, config, models as _models } from '$lib/stores';
>>>>>>> dfef03c8e (同步远程)

	import { goto } from '$app/navigation';
	import {
		user,
		chats,
		settings,
		showSettings,
<<<<<<< HEAD
=======
		userPreferences,
>>>>>>> dfef03c8e (同步远程)
		chatId,
		tags,
		showSidebar,
		mobile,
		showArchivedChats,
		pinnedChats,
		scrollPaginationEnabled,
		currentChatPage,
		temporaryChatEnabled,
<<<<<<< HEAD
		channels,
		socket,
		config,
		isApp
	} from '$lib/stores';
	import { onMount, getContext, tick, onDestroy } from 'svelte';

	const i18n = getContext('i18n');
=======
	} from '$lib/stores';
	import { onMount, getContext, tick, onDestroy } from 'svelte';
	import {
		createNewModel,
		deleteModelById,
		getModels as getWorkspaceModels,
		toggleModelById,
		updateModelById
	} from '$lib/apis/models/index';

	import { getModels } from '$lib/apis';
	const i18n = getContext('i18n');
	
>>>>>>> dfef03c8e (同步远程)

	import {
		deleteChatById,
		getChatList,
		getAllTags,
		getChatListBySearchText,
		createNewChat,
		getPinnedChatList,
		toggleChatPinnedStatusById,
		getChatPinnedStatusById,
		getChatById,
		updateChatFolderIdById,
		importChat
	} from '$lib/apis/chats';
	import { createNewFolder, getFolders, updateFolderParentIdById } from '$lib/apis/folders';
	import { WEBUI_BASE_URL } from '$lib/constants';

	import ArchivedChatsModal from './Sidebar/ArchivedChatsModal.svelte';
	import UserMenu from './Sidebar/UserMenu.svelte';
	import ChatItem from './Sidebar/ChatItem.svelte';
	import Spinner from '../common/Spinner.svelte';
	import Loader from '../common/Loader.svelte';
	import AddFilesPlaceholder from '../AddFilesPlaceholder.svelte';
	import SearchInput from './Sidebar/SearchInput.svelte';
	import Folder from '../common/Folder.svelte';
	import Plus from '../icons/Plus.svelte';
	import Tooltip from '../common/Tooltip.svelte';
	import Folders from './Sidebar/Folders.svelte';
	import { getChannels, createNewChannel } from '$lib/apis/channels';
	import ChannelModal from './Sidebar/ChannelModal.svelte';
	import ChannelItem from './Sidebar/ChannelItem.svelte';
	import PencilSquare from '../icons/PencilSquare.svelte';
	import Home from '../icons/Home.svelte';
	import { log_softmax } from '@huggingface/transformers';

	const BREAKPOINT = 768;

	let navElement;
	let search = '';

	let shiftKey = false;

	let selectedChatId = null;
	let showDropdown = false;
	let showPinnedChat = true;

	let showCreateChannel = false;

	// Pagination variables
	let chatListLoading = false;
	let allChatsLoaded = false;

	let folders = {};

	const initFolders = async () => {
		const folderList = await getFolders(localStorage.token).catch((error) => {
			toast.error(`${error}`);
	let selectedChatId = null;
	let showDropdown = false;
	let showPinnedChat = true;
    let showgptmodel = true;
	// Pagination variables
	let chatListLoading = false;
	let allChatsLoaded = false;
let models=[];
let Allmodels=[];
let KITNModels='';
let NNITModels='';
let selectedModelIdx='';
let selfModel='';
let modelId='';
	let folders = {};
	// 存储过滤后的模型数据
	let sidebarModels = [];

	//响应式订阅模型数据
	$: {
		KITNModels = Allmodels.filter((model) => model.id=='kitn');
		NNITModels = Allmodels.filter((model) => model.id=='nnit-chatgpt');

		selfModel=Allmodels.filter((model) => model.id=='PersonalAssistant');
		sidebarModels = Allmodels.filter(model => $userPreferences.sidebarMasks.includes(model.id));
	}
	const handleModelClick = (modelId) => {
		console.log('handleModelClick:', modelId);
		// 先跳转到 /Masks/models 页面
	
		goto('/Apps/models');
		
		// 使用 setTimeout 延迟跳转到目标路由
		setTimeout(() => {
			// 在 /Masks/models 页面跳转后，再跳转到目标路由
			goto(`/g/${encodeURIComponent(modelId)}`);
		}, 100); // 设置适当的延迟（如100毫秒）
	};
	const initFolders = async () => {
		const folderList = await getFolders(localStorage.token).catch((error) => {
			toast.error(error);
			return [];
		});

		folders = {};

		// First pass: Initialize all folder entries
		for (const folder of folderList) {
			// Ensure folder is added to folders with its data
			folders[folder.id] = { ...(folders[folder.id] || {}), ...folder };
		}

		// Second pass: Tie child folders to their parents
		for (const folder of folderList) {
			if (folder.parent_id) {
				// Ensure the parent folder is initialized if it doesn't exist
				if (!folders[folder.parent_id]) {
					folders[folder.parent_id] = {}; // Create a placeholder if not already present
				}

				// Initialize childrenIds array if it doesn't exist and add the current folder id
				folders[folder.parent_id].childrenIds = folders[folder.parent_id].childrenIds
					? [...folders[folder.parent_id].childrenIds, folder.id]
					: [folder.id];

				// Sort the children by updated_at field
				folders[folder.parent_id].childrenIds.sort((a, b) => {
					return folders[b].updated_at - folders[a].updated_at;
				});
			}
		}
	};


>>>>>>> dfef03c8e (同步远程)
	const createFolder = async (name = 'Untitled') => {
		if (name === '') {
			toast.error($i18n.t('Folder name cannot be empty.'));
			return;
		}

		const rootFolders = Object.values(folders).filter((folder) => folder.parent_id === null);
		if (rootFolders.find((folder) => folder.name.toLowerCase() === name.toLowerCase())) {
			// If a folder with the same name already exists, append a number to the name
			let i = 1;
			while (
				rootFolders.find((folder) => folder.name.toLowerCase() === `${name} ${i}`.toLowerCase())
			) {
				i++;
			}

			name = `${name} ${i}`;
		}

		// Add a dummy folder to the list to show the user that the folder is being created
		const tempId = uuidv4();
		folders = {
			...folders,
			tempId: {
				id: tempId,
				name: name,
				created_at: Date.now(),
				updated_at: Date.now()
			}
		};

		const res = await createNewFolder(localStorage.token, name).catch((error) => {
			toast.error(`${error}`);
			return null;
		});

		if (res) {
			await initFolders();
		}
	};

	const initChannels = async () => {
		await channels.set(await getChannels(localStorage.token));
	};

	const initChatList = async () => {
		// Reset pagination variables
		tags.set(await getAllTags(localStorage.token));
		pinnedChats.set(await getPinnedChatList(localStorage.token));
		initFolders();

		currentChatPage.set(1);
		allChatsLoaded = false;

		if (search) {
			await chats.set(await getChatListBySearchText(localStorage.token, search, $currentChatPage));
		} else {
			await chats.set(await getChatList(localStorage.token, $currentChatPage));
		}

		// Enable pagination
		scrollPaginationEnabled.set(true);
	};

	const loadMoreChats = async () => {
		chatListLoading = true;

		currentChatPage.set($currentChatPage + 1);

		let newChatList = [];

		if (search) {
			newChatList = await getChatListBySearchText(localStorage.token, search, $currentChatPage);
		} else {
			newChatList = await getChatList(localStorage.token, $currentChatPage);
		}

		// once the bottom of the list has been reached (no results) there is no need to continue querying
		allChatsLoaded = newChatList.length === 0;
		await chats.set([...($chats ? $chats : []), ...newChatList]);

		chatListLoading = false;
	};

	let searchDebounceTimeout;

	const searchDebounceHandler = async () => {
		console.log('search', search);
		chats.set(null);

		if (searchDebounceTimeout) {
			clearTimeout(searchDebounceTimeout);
		}

		if (search === '') {
			await initChatList();
			return;
		} else {
			searchDebounceTimeout = setTimeout(async () => {
				allChatsLoaded = false;
				currentChatPage.set(1);
				await chats.set(await getChatListBySearchText(localStorage.token, search));

				if ($chats.length === 0) {
					tags.set(await getAllTags(localStorage.token));
				}
			}, 1000);
		}
	};

	const importChatHandler = async (items, pinned = false, folderId = null) => {
		console.log('importChatHandler', items, pinned, folderId);
		for (const item of items) {
			console.log(item);
			if (item.chat) {
				await importChat(localStorage.token, item.chat, item?.meta ?? {}, pinned, folderId);
			}
		}

		initChatList();
	};

	const inputFilesHandler = async (files) => {
		console.log(files);

		for (const file of files) {
			const reader = new FileReader();
			reader.onload = async (e) => {
				const content = e.target.result;

				try {
					const chatItems = JSON.parse(content);
					importChatHandler(chatItems);
				} catch {
					toast.error($i18n.t(`Invalid file format.`));
				}
			};

			reader.readAsText(file);
		}
	};

	const tagEventHandler = async (type, tagName, chatId) => {
		console.log(type, tagName, chatId);
		if (type === 'delete') {
			initChatList();
		} else if (type === 'add') {
			initChatList();
		}
	};

	let draggedOver = false;

	const onDragOver = (e) => {
		e.preventDefault();

		// Check if a file is being draggedOver.
		if (e.dataTransfer?.types?.includes('Files')) {
			draggedOver = true;
		} else {
			draggedOver = false;
		}
	};

	const onDragLeave = () => {
		draggedOver = false;
	};

	const onDrop = async (e) => {
		e.preventDefault();
		console.log(e); // Log the drop event

		// Perform file drop check and handle it accordingly
		if (e.dataTransfer?.files) {
			const inputFiles = Array.from(e.dataTransfer?.files);

			if (inputFiles && inputFiles.length > 0) {
				console.log(inputFiles); // Log the dropped files
				inputFilesHandler(inputFiles); // Handle the dropped files
			}
		}

		draggedOver = false; // Reset draggedOver status after drop
	};

	let touchstart;
	let touchend;
//角色模型在侧边栏的展示

	function checkDirection() {
		const screenWidth = window.innerWidth;
		const swipeDistance = Math.abs(touchend.screenX - touchstart.screenX);
		if (touchstart.clientX < 40 && swipeDistance >= screenWidth / 8) {
			if (touchend.screenX < touchstart.screenX) {
				showSidebar.set(false);
			}
			if (touchend.screenX > touchstart.screenX) {
				showSidebar.set(true);
			}
		}
	}

	const onTouchStart = (e) => {
		touchstart = e.changedTouches[0];
		console.log(touchstart.clientX);
	};

	const onTouchEnd = (e) => {
		touchend = e.changedTouches[0];
		checkDirection();
	};

	const onKeyDown = (e) => {
		if (e.key === 'Shift') {
			shiftKey = true;
		}
	};

	const onKeyUp = (e) => {
		if (e.key === 'Shift') {
			shiftKey = false;
		}
	};

	const onFocus = () => {};

	const onBlur = () => {
		shiftKey = false;
		selectedChatId = null;
	};
	let token = localStorage.token;  // 获取 token

	
	let selectedModelName = '';
		if (token) {
      try {
        // 获取工作区模型列表
        // 更新 store 中的模型数据
		await _models.set(await getModels(localStorage.token));
        Allmodels =  await getModels(localStorage.token);
		models = await getWorkspaceModels(localStorage.token);
		console.log("Allmodels:",Allmodels)

      } catch (error) {
        console.error('Error fetching models:', error);
      }
    }
	

	const modelsValue = new URLSearchParams($page.url.search).get('models');
    selectedModelName = modelsValue || '';
    console.log('初始化模型:', selectedModelName);

		showPinnedChat = localStorage?.showPinnedChat ? localStorage.showPinnedChat === 'true' : true;

		mobile.subscribe((e) => {
			if ($showSidebar && e) {
				showSidebar.set(false);
			}

			if (!$showSidebar && !e) {
				showSidebar.set(true);
			}
		});

		showSidebar.set(!$mobile ? localStorage.sidebar === 'true' : false);
		showSidebar.subscribe((value) => {
			localStorage.sidebar = value;
<<<<<<< HEAD

			// nav element is not available on the first render
			const navElement = document.getElementsByTagName('nav')[0];

			if (navElement) {
				if ($mobile) {
					if (!value) {
						navElement.style['-webkit-app-region'] = 'drag';
					} else {
						navElement.style['-webkit-app-region'] = 'no-drag';
					}
				} else {
					navElement.style['-webkit-app-region'] = 'drag';
				}
			}
		});

		await initChannels();
=======
		});

>>>>>>> dfef03c8e (同步远程)
		await initChatList();

		window.addEventListener('keydown', onKeyDown);
		window.addEventListener('keyup', onKeyUp);

		window.addEventListener('touchstart', onTouchStart);
		window.addEventListener('touchend', onTouchEnd);

		window.addEventListener('focus', onFocus);
<<<<<<< HEAD
		window.addEventListener('blur-sm', onBlur);
=======
		window.addEventListener('blur', onBlur);
>>>>>>> dfef03c8e (同步远程)

		const dropZone = document.getElementById('sidebar');

		dropZone?.addEventListener('dragover', onDragOver);
		dropZone?.addEventListener('drop', onDrop);
		dropZone?.addEventListener('dragleave', onDragLeave);
<<<<<<< HEAD
=======

		    // 读取已使用的模型信息


>>>>>>> dfef03c8e (同步远程)
	});

	onDestroy(() => {
		window.removeEventListener('keydown', onKeyDown);
		window.removeEventListener('keyup', onKeyUp);

		window.removeEventListener('touchstart', onTouchStart);
		window.removeEventListener('touchend', onTouchEnd);

		window.removeEventListener('focus', onFocus);
<<<<<<< HEAD
		window.removeEventListener('blur-sm', onBlur);
=======
		window.removeEventListener('blur', onBlur);
>>>>>>> dfef03c8e (同步远程)

		const dropZone = document.getElementById('sidebar');

		dropZone?.removeEventListener('dragover', onDragOver);
		dropZone?.removeEventListener('drop', onDrop);
		dropZone?.removeEventListener('dragleave', onDragLeave);
	});
<<<<<<< HEAD
=======

>>>>>>> dfef03c8e (同步远程)
</script>

<ArchivedChatsModal
	bind:show={$showArchivedChats}
	on:change={async () => {
		await initChatList();
	}}
/>

<<<<<<< HEAD
<ChannelModal
	bind:show={showCreateChannel}
	onSubmit={async ({ name, access_control }) => {
		const res = await createNewChannel(localStorage.token, {
			name: name,
			access_control: access_control
		}).catch((error) => {
			toast.error(`${error}`);
			return null;
		});

		if (res) {
			$socket.emit('join-channels', { auth: { token: $user.token } });
			await initChannels();
			showCreateChannel = false;
		}
	}}
/>

=======
>>>>>>> dfef03c8e (同步远程)
<!-- svelte-ignore a11y-no-static-element-interactions -->

{#if $showSidebar}
	<div
<<<<<<< HEAD
		class=" {$isApp
			? ' ml-[4.5rem] md:ml-0'
			: ''} fixed md:hidden z-40 top-0 right-0 left-0 bottom-0 bg-black/60 w-full min-h-screen h-screen flex justify-center overflow-hidden overscroll-contain"
=======
		class=" fixed md:hidden z-40 top-0 right-0 left-0 bottom-0 bg-black/60 w-full min-h-screen h-screen flex justify-center overflow-hidden overscroll-contain"
>>>>>>> dfef03c8e (同步远程)
		on:mousedown={() => {
			showSidebar.set(!$showSidebar);
		}}
	/>
{/if}

<div
	bind:this={navElement}
	id="sidebar"
	class="h-screen max-h-[100dvh] min-h-screen select-none {$showSidebar
		? 'md:relative w-[260px] max-w-[260px]'
<<<<<<< HEAD
		: '-translate-x-[260px] w-[0px]'} {$isApp
		? `ml-[4.5rem] md:ml-0 `
		: 'transition-width duration-200 ease-in-out'}  shrink-0 bg-gray-50 text-gray-900 dark:bg-gray-950 dark:text-gray-200 text-sm fixed z-50 top-0 left-0 overflow-x-hidden
=======
		: '-translate-x-[260px] w-[0px]'} bg-gray-50 text-gray-900 dark:bg-gray-950 dark:text-gray-200 text-sm transition fixed z-50 top-0 left-0 overflow-x-hidden
>>>>>>> dfef03c8e (同步远程)
        "
	data-state={$showSidebar}
>
	<div
		class="py-2 my-auto flex flex-col justify-between h-screen max-h-[100dvh] w-[260px] overflow-x-hidden z-50 {$showSidebar
			? ''
			: 'invisible'}"
	>
<<<<<<< HEAD
		<div class="px-1.5 flex justify-between space-x-1 text-gray-600 dark:text-gray-400">
=======
	
		<div class="px-1.5 flex justify-between space-x-1 text-gray-800 dark:text-gray-200">
			<a
				id="sidebar-new-chat-button"
				class="flex flex-1 rounded-lg px-1 py-[7px] h-full hover:bg-gray-100 dark:hover:bg-gray-900 transition"
				href="/"
				draggable="false"
				on:click={async () => {
					selectedChatId = null;
					await goto('/');
					const newChatButton = document.getElementById('new-chat-button');
					setTimeout(() => {
						newChatButton?.click();
						if ($mobile) {
							showSidebar.set(false);
						}
					}, 0);
				}}
			>
				<div class="self-center mx-1.5">
						<svg
							xmlns="http://www.w3.org/2000/svg"
							fill="none"
							viewBox="0 0 24 24"
							stroke-width="2"
							stroke="currentColor"
							class="size-[1.1rem]"
						>
						
							<path
							 
								d="m16.862 4.487 1.687-1.688a1.875 1.875 0 1 1 2.652 2.652L10.582 16.07a4.5 4.5 0 0 1-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 0 1 1.13-1.897l8.932-8.931Zm0 0L19.5 7.125M18 14v4.75A2.25 2.25 0 0 1 15.75 21H5.25A2.25 2.25 0 0 1 3 18.75V8.25A2.25 2.25 0 0 1 5.25 6H10"
								/>
						</svg>
				</div>
				 <!-- <div class=" self-center font-medium text-sm text-gray-850 dark:text-white font-primary">
					{$i18n.t('New Chat')}
				</div> -->
				<div class="flex self-center">
					<div class=" self-center font-medium text-sm font-primary">{$i18n.t('New Chat')}</div>
				</div>
			</a>

				<!-- <a
				class="flex-grow flex space-x-3 rounded-lg px-2 py-[7px] hover:bg-gray-100 dark:hover:bg-gray-900 transition"
				href="javascript:void(0);"  
				on:click={() => handleModelClick(NNITModels[0]?.id)}  
				>
				<div class="self-center">
					<button on:click={() => { selectedModelIdx = modelIdx; }}>
						<img
						crossorigin="anonymous"
						src={NNITModels[0]?.info?.meta?.profile_image_url ??
							($i18n.language === 'dg-DG'
							  ? `/doge.png`
							  : `${WEBUI_BASE_URL}/static/favicon.png`)}
						class="rounded-full border-[1px] border-gray-200 dark:border-none"
						alt="logo"
						draggable="false"
						width="15" 
						height="15"
					  /> 
					</button>
				  </div>
					<div class="flex self-center">
						<div class=" self-center font-medium text-sm font-primary">{$i18n.t('New Chat')}</div>
					</div>
				</a> -->


>>>>>>> dfef03c8e (同步远程)
			<button
				class=" cursor-pointer p-[7px] flex rounded-xl hover:bg-gray-100 dark:hover:bg-gray-900 transition"
				on:click={() => {
					showSidebar.set(!$showSidebar);
				}}
			>
				<div class=" m-auto self-center">
					<svg
						xmlns="http://www.w3.org/2000/svg"
						fill="none"
						viewBox="0 0 24 24"
						stroke-width="2"
						stroke="currentColor"
						class="size-5"
					>
						<path
							stroke-linecap="round"
							stroke-linejoin="round"
							d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25H12"
						/>
					</svg>
				</div>
			</button>
<<<<<<< HEAD

			<a
				id="sidebar-new-chat-button"
				class="flex justify-between items-center flex-1 rounded-lg px-2 py-1 h-full text-right hover:bg-gray-100 dark:hover:bg-gray-900 transition no-drag-region"
				href="/"
				draggable="false"
				on:click={async () => {
					selectedChatId = null;
					await goto('/');
					const newChatButton = document.getElementById('new-chat-button');
					setTimeout(() => {
						newChatButton?.click();
						if ($mobile) {
							showSidebar.set(false);
						}
					}, 0);
				}}
			>
				<div class="flex items-center">
					<div class="self-center mx-1.5">
						<img
							crossorigin="anonymous"
							src="{WEBUI_BASE_URL}/static/favicon.png"
							class=" size-5 -translate-x-1.5 rounded-full"
							alt="logo"
						/>
					</div>
					<div class=" self-center font-medium text-sm text-gray-850 dark:text-white font-primary">
						{$i18n.t('New Chat')}
					</div>
				</div>

				<div>
					<PencilSquare className=" size-5" strokeWidth="2" />
				</div>
			</a>
		</div>

		<!-- {#if $user?.role === 'admin'}
			<div class="px-1.5 flex justify-center text-gray-800 dark:text-gray-200">
				<a
					class="grow flex items-center space-x-3 rounded-lg px-2 py-[7px] hover:bg-gray-100 dark:hover:bg-gray-900 transition"
					href="/home"
					on:click={() => {
						selectedChatId = null;
						chatId.set('');

						if ($mobile) {
							showSidebar.set(false);
						}
					}}
					draggable="false"
				>
					<div class="self-center">
						<Home strokeWidth="2" className="size-[1.1rem]" />
					</div>

					<div class="flex self-center translate-y-[0.5px]">
						<div class=" self-center font-medium text-sm font-primary">{$i18n.t('Home')}</div>
					</div>
				</a>
			</div>
		{/if} -->

		{#if $user?.role === 'admin' || $user?.permissions?.workspace?.models || $user?.permissions?.workspace?.knowledge || $user?.permissions?.workspace?.prompts || $user?.permissions?.workspace?.tools}
			<div class="px-1.5 flex justify-center text-gray-800 dark:text-gray-200">
				<a
					class="grow flex items-center space-x-3 rounded-lg px-2 py-[7px] hover:bg-gray-100 dark:hover:bg-gray-900 transition"
=======
		</div>

		{#if $user?.role === 'admin' }
			<div class="px-1.5 flex justify-center text-gray-800 dark:text-gray-200">
				<a
					class="flex-grow flex space-x-3 rounded-lg px-2 py-[7px] hover:bg-gray-100 dark:hover:bg-gray-900 transition"
>>>>>>> dfef03c8e (同步远程)
					href="/workspace"
					on:click={() => {
						selectedChatId = null;
						chatId.set('');

						if ($mobile) {
							showSidebar.set(false);
						}
					}}
					draggable="false"
				>
					<div class="self-center">
						<svg
							xmlns="http://www.w3.org/2000/svg"
							fill="none"
							viewBox="0 0 24 24"
							stroke-width="2"
							stroke="currentColor"
							class="size-[1.1rem]"
						>
							<path
<<<<<<< HEAD
								stroke-linecap="round"
								stroke-linejoin="round"
=======
							 
>>>>>>> dfef03c8e (同步远程)
								d="M13.5 16.875h3.375m0 0h3.375m-3.375 0V13.5m0 3.375v3.375M6 10.5h2.25a2.25 2.25 0 0 0 2.25-2.25V6a2.25 2.25 0 0 0-2.25-2.25H6A2.25 2.25 0 0 0 3.75 6v2.25A2.25 2.25 0 0 0 6 10.5Zm0 9.75h2.25A2.25 2.25 0 0 0 10.5 18v-2.25a2.25 2.25 0 0 0-2.25-2.25H6a2.25 2.25 0 0 0-2.25 2.25V18A2.25 2.25 0 0 0 6 20.25Zm9.75-9.75H18a2.25 2.25 0 0 0 2.25-2.25V6A2.25 2.25 0 0 0 18 3.75h-2.25A2.25 2.25 0 0 0 13.5 6v2.25a2.25 2.25 0 0 0 2.25 2.25Z"
							/>
						</svg>
					</div>

<<<<<<< HEAD
					<div class="flex self-center translate-y-[0.5px]">
=======
					<div class="flex self-center">
>>>>>>> dfef03c8e (同步远程)
						<div class=" self-center font-medium text-sm font-primary">{$i18n.t('Workspace')}</div>
					</div>
				</a>
			</div>
		{/if}
<<<<<<< HEAD

=======
			{#if sidebarModels.length > 0}
				{#each sidebarModels as model}
				{#if !model?.info?.meta?.knowledge}
				<div class="px-1.5 flex justify-center text-gray-800 dark:text-gray-200">
					<a
				class="flex-grow flex space-x-3 rounded-lg px-2 py-[7px] hover:bg-gray-100 dark:hover:bg-gray-900 transition"
				href="javascript:void(0);"  
				on:click={() => handleModelClick(model.id)}  
				>
					<div class="self-center">
						<button on:click={() => handleModelClick(model.id)}>
							<img
							crossorigin="anonymous"
							src={model?.info?.meta?.profile_image_url ??
								($i18n.language === 'dg-DG'
								  ? `/doge.png`
								  : `${WEBUI_BASE_URL}/static/favicon.png`)}
							class="rounded-md border-gray-200 dark:border-none"
							alt="logo"
							draggable="false"
							width="20" 
							height="20"
						  /> 
						</button>
					  </div>
						<div class="flex self-center">
							<div class=" self-center font-medium text-sm font-primary">{model.name}</div>
						</div>
					</a>
				</div>
				{/if}
				{/each}
			{/if}
		<!-- {#each gptsModels as model,modelIdx}	
		<div class="px-1.5 flex justify-center text-gray-800 dark:text-gray-200">
				<a
					class="flex-grow flex space-x-3 rounded-lg px-2 py-[7px] hover:bg-gray-100 dark:hover:bg-gray-900 transition"
					href={`/?models=${encodeURIComponent(model.id)}`}
				>
				<div class="self-center">
					<button on:click={() => { selectedModelIdx = modelIdx; }}>
						<img
						crossorigin="anonymous"
						src={model?.info?.meta?.profile_image_url ??
							($i18n.language === 'dg-DG'
							  ? `/doge.png`
							  : `${WEBUI_BASE_URL}/static/favicon.png`)}
						class="rounded-full border-[1px] border-gray-200 dark:border-none"
						alt="logo"
						draggable="false"
						width="15" 
						height="15"
					  /> 
					</button>
				  </div>
					<div class="flex self-center">
						<div class=" self-center font-medium text-sm font-primary">{model.name}</div>
					</div>
				</a>
			</div>
			{/each} -->
			<div class="px-1.5 flex justify-center text-gray-800 dark:text-gray-200">
				<a
					class="flex-grow flex space-x-3 rounded-lg px-2 py-[7px] hover:bg-gray-100 dark:hover:bg-gray-900 transition"
					href="/Apps"
					on:click={() => {
						selectedChatId = null;
						chatId.set('');
	
						if ($mobile) {
							showSidebar.set(false);
						}
					}}
					draggable="false"
				>
					<div class="self-center">
						<!-- <svg
	
							xmlns="http://www.w3.org/2000/svg"
							fill="none"
							viewBox="0 0 24 24"
							stroke-width="2"
							stroke="currentColor"
							class="size-[1.1rem]"
						>
						
							<path
							 
								d="M13.5 16.875h3.375m0 0h3.375m-3.375 0V13.5m0 3.375v3.375M6 10.5h2.25a2.25 2.25 0 0 0 2.25-2.25V6a2.25 2.25 0 0 0-2.25-2.25H6A2.25 2.25 0 0 0 3.75 6v2.25A2.25 2.25 0 0 0 6 10.5Zm0 9.75h2.25A2.25 2.25 0 0 0 10.5 18v-2.25a2.25 2.25 0 0 0-2.25-2.25H6a2.25 2.25 0 0 0-2.25 2.25V18A2.25 2.25 0 0 0 6 20.25Zm9.75-9.75H18a2.25 2.25 0 0 0 2.25-2.25V6A2.25 2.25 0 0 0 18 3.75h-2.25A2.25 2.25 0 0 0 13.5 6v2.25a2.25 2.25 0 0 0 2.25 2.25Z"
							/>
						</svg> -->
						<svg t="1736389078604" class="icon" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" p-id="2091" width="20" height="20"><path d="M307.41504 180.224l-23.12704-73.55904L265.216 180.224l-7.20896 27.73504-3.584 13.77792-89.81504 32.68608-15.27296 5.54496 15.27296 4.608 54.56896 16.42496 36.992 11.136 1.83808 5.84704 26.32192 83.75296 7.38304 23.59808 6.144-23.59808 23.72096-91.47392 25.472-9.26208 4.43904-1.664 75.17696-27.30496-75.17696-22.61504-31.65696-9.51296-12.416-39.68z m319.05792 506.28096l56.45312-16.04096 104.96-29.74208 19.02592-5.376 89.088-25.21088L806.912 583.68l-123.98592-36.69504-55.38304-16.512-1.96608-6.09792-37.376-116.608-29.22496-91.09504-8.23296-25.55904-4.48-13.824-4.52608 13.824-39.24992 116.65408-39.21408 116.608-1.664 5.12-26.624 7.552-124.07296 35.11296-118.912 33.70496 117.84704 34.85696 1.06496 0.34304 124.07296 36.77696 25.6 7.552 22.99904 71.63904 37.20704 116.31104 20.90496 65.32096 17.28-51.2 4.69504-14.12096 39.08096-116.27008 23.72096-70.6048v0.03584z" p-id="2092"></path></svg>
					</div>
	
					<div class="flex self-center">
						<div class=" self-center font-medium text-sm font-primary">{$i18n.t('Apps')}</div>
					</div>
				</a>
			</div>
			<div class="divider">
				<span class="divider-text"></span>
			</div>
			
			<div class="px-1.5 flex justify-center text-gray-800 dark:text-gray-200">
				
				<a
				class="flex-grow flex space-x-3 rounded-lg px-2 py-[7px] hover:bg-gray-100 dark:hover:bg-gray-900 transition"
				href="javascript:void(0);"  
				on:click={() => handleModelClick(KITNModels[0]?.id)}  
				>
				<div class="self-center">
					<button on:click={() => { selectedModelIdx = modelIdx; }}>
						<img
						crossorigin="anonymous"
						src={KITNModels[0]?.info?.meta?.profile_image_url ??
							($i18n.language === 'dg-DG'
							  ? `/doge.png`
							  : `${WEBUI_BASE_URL}/static/favicon.png`)}
						class="rounded-md border-gray-200 dark:border-none"
						alt="logo"
						draggable="false"
						width="20" 
						height="20"
					  /> 
					</button>
				  </div>
					<div class="flex self-center">
						<div class=" self-center font-medium text-sm font-primary">{CGE-SEEKS}</div>
					</div>
				</a>
			</div>
<!-- 个人助手 -->
			<div class="px-1.5 flex justify-center text-gray-800 dark:text-gray-200">
				
				<a
				class="flex-grow flex space-x-3 rounded-lg px-2 py-[7px] hover:bg-gray-100 dark:hover:bg-gray-900 transition"
				href="javascript:void(0);"  
				on:click={() => handleModelClick(selfModel[0]?.id)}  
				>
				<div class="self-center">
					<button on:click={() => { selectedModelIdx = modelIdx; }}>
						<img
						crossorigin="anonymous"
						src={selfModel[0]?.info?.meta?.profile_image_url ??
							($i18n.language === 'dg-DG'
							  ? `/doge.png`
							  : `${WEBUI_BASE_URL}/static/favicon.png`)}
						class="rounded-md border-gray-200 dark:border-none"
						alt="logo"
						draggable="false"
						width="20" 
						height="20"
					  /> 
					</button>
				  </div>
					<div class="flex self-center">
						<div class=" self-center font-medium text-sm font-primary">{selfModel[0]?.name}</div>
					</div>
				</a>
			</div>
			{#if sidebarModels.length > 0}
				{#each sidebarModels as model}
				{#if model?.info?.meta?.knowledge}
				<div class="px-1.5 flex justify-center text-gray-800 dark:text-gray-200">
					<a
				class="flex-grow flex space-x-3 rounded-lg px-2 py-[7px] hover:bg-gray-100 dark:hover:bg-gray-900 transition"
				href="javascript:void(0);"  
				on:click={() => handleModelClick(model.id)}  
				>
					<div class="self-center">
						<button on:click={() => handleModelClick(model.id)}>
							<img
							crossorigin="anonymous"
							src={model?.info?.meta?.profile_image_url ??
								($i18n.language === 'dg-DG'
								  ? `/doge.png`
								  : `${WEBUI_BASE_URL}/static/favicon.png`)}
							class="rounded-md border-gray-200 dark:border-none"
							alt="logo"
							draggable="false"
							width="20" 
							height="20"
						  /> 
						</button>
					  </div>
						<div class="flex self-center">
							<div class=" self-center font-medium text-sm font-primary">{model.name}</div>
						</div>
					</a>
				</div>
				{/if}
				{/each}
			{/if}
>>>>>>> dfef03c8e (同步远程)
		<div class="relative {$temporaryChatEnabled ? 'opacity-20' : ''}">
			{#if $temporaryChatEnabled}
				<div class="absolute z-40 w-full h-full flex justify-center"></div>
			{/if}

			<SearchInput
				bind:value={search}
				on:input={searchDebounceHandler}
				placeholder={$i18n.t('Search')}
			/>
<<<<<<< HEAD
		</div>

		<div
			class="relative flex flex-col flex-1 overflow-y-auto overflow-x-hidden {$temporaryChatEnabled
				? 'opacity-20'
				: ''}"
		>
			{#if $config?.features?.enable_channels && ($user.role === 'admin' || $channels.length > 0) && !search}
				<Folder
					className="px-2 mt-0.5"
					name={$i18n.t('Channels')}
					dragAndDrop={false}
					onAdd={async () => {
						if ($user.role === 'admin') {
							await tick();

							setTimeout(() => {
								showCreateChannel = true;
							}, 0);
						}
					}}
					onAddLabel={$i18n.t('Create Channel')}
				>
					{#each $channels as channel}
						<ChannelItem
							{channel}
							onUpdate={async () => {
								await initChannels();
							}}
						/>
					{/each}
				</Folder>
			{/if}

			<Folder
				collapsible={!search}
				className="px-2 mt-0.5"
				name={$i18n.t('Chats')}
				onAdd={() => {
					createFolder();
				}}
				onAddLabel={$i18n.t('New Folder')}
				on:import={(e) => {
					importChatHandler(e.detail);
				}}
				on:drop={async (e) => {
					const { type, id, item } = e.detail;

					if (type === 'chat') {
						let chat = await getChatById(localStorage.token, id).catch((error) => {
							return null;
						});
						if (!chat && item) {
							chat = await importChat(localStorage.token, item.chat, item?.meta ?? {});
						}

						if (chat) {
							console.log(chat);
							if (chat.folder_id) {
								const res = await updateChatFolderIdById(localStorage.token, chat.id, null).catch(
									(error) => {
										toast.error(`${error}`);
										return null;
									}
								);
							}

							if (chat.pinned) {
								const res = await toggleChatPinnedStatusById(localStorage.token, chat.id);
							}

							initChatList();
						}
					} else if (type === 'folder') {
						if (folders[id].parent_id === null) {
							return;
						}

						const res = await updateFolderParentIdById(localStorage.token, id, null).catch(
							(error) => {
								toast.error(`${error}`);
								return null;
							}
						);

						if (res) {
							await initFolders();
						}
					}
				}}
			>
				{#if $temporaryChatEnabled}
					<div class="absolute z-40 w-full h-full flex justify-center"></div>
				{/if}

				{#if !search && $pinnedChats.length > 0}
					<div class="flex flex-col space-y-1 rounded-xl">
						<Folder
							className=""
							bind:open={showPinnedChat}
							on:change={(e) => {
								localStorage.setItem('showPinnedChat', e.detail);
								console.log(e.detail);
							}}
							on:import={(e) => {
								importChatHandler(e.detail, true);
							}}
							on:drop={async (e) => {
								const { type, id, item } = e.detail;

								if (type === 'chat') {
									let chat = await getChatById(localStorage.token, id).catch((error) => {
										return null;
									});
									if (!chat && item) {
										chat = await importChat(localStorage.token, item.chat, item?.meta ?? {});
									}

									if (chat) {
										console.log(chat);
										if (chat.folder_id) {
											const res = await updateChatFolderIdById(
												localStorage.token,
												chat.id,
												null
											).catch((error) => {
												toast.error(`${error}`);
												return null;
											});
										}

										if (!chat.pinned) {
											const res = await toggleChatPinnedStatusById(localStorage.token, chat.id);
										}

										initChatList();
									}
								}
							}}
							name={$i18n.t('Pinned')}
						>
							<div
								class="ml-3 pl-1 mt-[1px] flex flex-col overflow-y-auto scrollbar-hidden border-s border-gray-100 dark:border-gray-900"
							>
								{#each $pinnedChats as chat, idx}
									<ChatItem
										className=""
										id={chat.id}
										title={chat.title}
										{shiftKey}
										selected={selectedChatId === chat.id}
										on:select={() => {
											selectedChatId = chat.id;
										}}
										on:unselect={() => {
											selectedChatId = null;
										}}
										on:change={async () => {
											initChatList();
										}}
										on:tag={(e) => {
											const { type, name } = e.detail;
											tagEventHandler(type, name, chat.id);
										}}
									/>
								{/each}
							</div>
						</Folder>
					</div>
				{/if}

=======

			<!-- <div class="absolute z-40 right-3.5 top-1">
				<Tooltip content={$i18n.t('New folder')}>
					<button
						class="p-1 rounded-lg bg-gray-50 hover:bg-gray-100 dark:bg-gray-950 dark:hover:bg-gray-900 transition"
						on:click={() => {
							createFolder();
						}}
					>
						<Plus />
					</button>
				</Tooltip>
			</div> -->
		</div>

		<div
			class="relative flex flex-col flex-1 overflow-y-auto {$temporaryChatEnabled
				? 'opacity-20'
				: ''}"
		>
			{#if $temporaryChatEnabled}
				<div class="absolute z-40 w-full h-full flex justify-center"></div>
			{/if}

			{#if !search && $pinnedChats.length > 0}
				<div class="flex flex-col space-y-1 rounded-xl">
					<Folder
						className="px-2"
						bind:open={showPinnedChat}
						on:change={(e) => {
							localStorage.setItem('showPinnedChat', e.detail);
							console.log(e.detail);
						}}
						on:import={(e) => {
							importChatHandler(e.detail, true);
						}}
						on:drop={async (e) => {
							const { type, id, item } = e.detail;

							if (type === 'chat') {
								let chat = await getChatById(localStorage.token, id).catch((error) => {
									return null;
								});
								if (!chat && item) {
									chat = await importChat(localStorage.token, item.chat, item?.meta ?? {});
									console.log("chat:",chat);

								}

								if (chat) {
									console.log("chat:",chat);
									if (chat.folder_id) {
										const res = await updateChatFolderIdById(
											localStorage.token,
											chat.id,
											null
										).catch((error) => {
											toast.error(error);
											return null;
										});
									}

									if (!chat.pinned) {
										const res = await toggleChatPinnedStatusById(localStorage.token, chat.id);
									}

									initChatList();
								}
							}
						}}
						name={$i18n.t('Pinned')}
					>
						<div
							class="ml-3 pl-1 mt-[1px] flex flex-col overflow-y-auto scrollbar-hidden border-s border-gray-100 dark:border-gray-900"
						>
							{#each $pinnedChats as chat, idx}
								<ChatItem
									className=""
									id={chat.id}
									title={chat.title}
									{shiftKey}
									selected={selectedChatId === chat.id}
									on:select={() => {
										selectedChatId = chat.id;
									}}
									on:unselect={() => {
										selectedChatId = null;
									}}
									on:change={async () => {
										initChatList();
									}}
									on:tag={(e) => {
										const { type, name } = e.detail;
										tagEventHandler(type, name, chat.id);
									}}
								/>
							{/each}
						</div>
					</Folder>
				</div>
			{/if}

			<div class=" flex-1 flex flex-col overflow-y-auto scrollbar-hidden">
>>>>>>> dfef03c8e (同步远程)
				{#if !search && folders}
					<Folders
						{folders}
						on:import={(e) => {
							const { folderId, items } = e.detail;
							importChatHandler(items, false, folderId);
						}}
						on:update={async (e) => {
							initChatList();
						}}
						on:change={async () => {
							initChatList();
						}}
					/>
				{/if}

<<<<<<< HEAD
				<div class=" flex-1 flex flex-col overflow-y-auto scrollbar-hidden">
					<div class="pt-1.5">
						{#if $chats}
							{#each $chats as chat, idx}
=======
				<Folder
					collapsible={!search}
					className="px-2 mt-0.5"
					name={$i18n.t('All chats')}
					on:import={(e) => {
						importChatHandler(e.detail);
					}}
					on:drop={async (e) => {
						const { type, id, item } = e.detail;

						if (type === 'chat') {
							let chat = await getChatById(localStorage.token, id).catch((error) => {
								return null;
							});
							if (!chat && item) {
								chat = await importChat(localStorage.token, item.chat, item?.meta ?? {});
							}

							if (chat) {
								console.log(chat);
								if (chat.folder_id) {
									const res = await updateChatFolderIdById(localStorage.token, chat.id, null).catch(
										(error) => {
											toast.error(error);
											return null;
										}
									);
								}

								if (chat.pinned) {
									const res = await toggleChatPinnedStatusById(localStorage.token, chat, id);
								}

								initChatList();
							}
						} else if (type === 'folder') {
							if (folders[id].parent_id === null) {
								return;
							}

							const res = await updateFolderParentIdById(localStorage.token, id, null).catch(
								(error) => {
									toast.error(error);
									return null;
								}
							);

							if (res) {
								await initFolders();
							}
						}
					}}
				>
					<div class="pt-1.5">
						{#if $chats}
							{#each $chats as chat, idx}
							
>>>>>>> dfef03c8e (同步远程)
								{#if idx === 0 || (idx > 0 && chat.time_range !== $chats[idx - 1].time_range)}
									<div
										class="w-full pl-2.5 text-xs text-gray-500 dark:text-gray-500 font-medium {idx ===
										0
											? ''
											: 'pt-5'} pb-1.5"
									>
										{$i18n.t(chat.time_range)}
										<!-- localisation keys for time_range to be recognized from the i18next parser (so they don't get automatically removed):
							{$i18n.t('Today')}
							{$i18n.t('Yesterday')}
							{$i18n.t('Previous 7 days')}
							{$i18n.t('Previous 30 days')}
							{$i18n.t('January')}
							{$i18n.t('February')}
							{$i18n.t('March')}
							{$i18n.t('April')}
							{$i18n.t('May')}
							{$i18n.t('June')}
							{$i18n.t('July')}
							{$i18n.t('August')}
							{$i18n.t('September')}
							{$i18n.t('October')}
							{$i18n.t('November')}
							{$i18n.t('December')}
							-->
									</div>
								{/if}
<<<<<<< HEAD

								<ChatItem
=======
								
								<ChatItem
								
>>>>>>> dfef03c8e (同步远程)
									className=""
									id={chat.id}
									title={chat.title}
									{shiftKey}
									selected={selectedChatId === chat.id}
									on:select={() => {
										selectedChatId = chat.id;
									}}
									on:unselect={() => {
										selectedChatId = null;
									}}
									on:change={async () => {
										initChatList();
									}}
									on:tag={(e) => {
										const { type, name } = e.detail;
										tagEventHandler(type, name, chat.id);
									}}
								/>
							{/each}

							{#if $scrollPaginationEnabled && !allChatsLoaded}
								<Loader
									on:visible={(e) => {
										if (!chatListLoading) {
											loadMoreChats();
										}
									}}
								>
									<div
										class="w-full flex justify-center py-1 text-xs animate-pulse items-center gap-2"
									>
										<Spinner className=" size-4" />
										<div class=" ">Loading...</div>
									</div>
								</Loader>
							{/if}
						{:else}
							<div class="w-full flex justify-center py-1 text-xs animate-pulse items-center gap-2">
								<Spinner className=" size-4" />
								<div class=" ">Loading...</div>
							</div>
						{/if}
					</div>
<<<<<<< HEAD
				</div>
			</Folder>
=======
				</Folder>
			</div>
>>>>>>> dfef03c8e (同步远程)
		</div>

		<div class="px-2">
			<div class="flex flex-col font-primary">
				{#if $user !== undefined}
					<UserMenu
						role={$user.role}
						on:show={(e) => {
							if (e.detail === 'archived-chat') {
								showArchivedChats.set(true);
							}
						}}
					>
						<button
							class=" flex items-center rounded-xl py-2.5 px-2.5 w-full hover:bg-gray-100 dark:hover:bg-gray-900 transition"
							on:click={() => {
								showDropdown = !showDropdown;
							}}
						>
							<div class=" self-center mr-3">
								<img
									src={$user.profile_image_url}
									class=" max-w-[30px] object-cover rounded-full"
									alt="User profile"
								/>
							</div>
							<div class=" self-center font-medium">{$user.name}</div>
						</button>
					</UserMenu>
				{/if}
			</div>
		</div>
	</div>
</div>

<style>
	.scrollbar-hidden:active::-webkit-scrollbar-thumb,
	.scrollbar-hidden:focus::-webkit-scrollbar-thumb,
	.scrollbar-hidden:hover::-webkit-scrollbar-thumb {
		visibility: visible;
	}
	.scrollbar-hidden::-webkit-scrollbar-thumb {
		visibility: hidden;
	}
<<<<<<< HEAD
=======
.divider {
    display: flex;
    align-items: center;
    margin: 1px 0;
    width: 100%;
}

.divider::before,
.divider::after {
    content: '';
    flex: 1;
    height: 1px;
    background: #ddd;
}

.divider-text {
    color: #888;
    font-size: 10px;
    padding: 0 2px;
}

>>>>>>> dfef03c8e (同步远程)
</style>
