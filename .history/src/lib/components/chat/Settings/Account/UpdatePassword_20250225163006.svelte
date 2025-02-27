<script lang="ts">
	import { getContext } from 'svelte';
	import { toast } from 'svelte-sonner';
	import { updateUserPassword } from '$lib/apis/auths';

	const i18n = getContext('i18n');

	let show = false;
	let currentPassword = '';
	let newPassword = '';
	let newPasswordConfirm = '';

	const updatePasswordHandler = async () => {
		if (newPassword === newPasswordConfirm) {
			const res = await updateUserPassword(localStorage.token, currentPassword, newPassword).catch(
				(error) => {
<<<<<<< HEAD
					toast.error(`${error}`);
=======
					toast.error(error);
>>>>>>> dfef03c8e (同步远程)
					return null;
				}
			);

			if (res) {
				toast.success($i18n.t('Successfully updated.'));
			}

			currentPassword = '';
			newPassword = '';
			newPasswordConfirm = '';
		} else {
			toast.error(
				`The passwords you entered don't quite match. Please double-check and try again.`
			);
			newPassword = '';
			newPasswordConfirm = '';
		}
	};
</script>

<form
	class="flex flex-col text-sm"
	on:submit|preventDefault={() => {
		updatePasswordHandler();
	}}
>
	<div class="flex justify-between items-center text-sm">
		<div class="  font-medium">{$i18n.t('Change Password')}</div>
		<button
			class=" text-xs font-medium text-gray-500"
			type="button"
			on:click={() => {
				show = !show;
			}}>{show ? $i18n.t('Hide') : $i18n.t('Show')}</button
		>
	</div>

	{#if show}
		<div class=" py-2.5 space-y-1.5">
			<div class="flex flex-col w-full">
				<div class=" mb-1 text-xs text-gray-500">{$i18n.t('Current Password')}</div>

				<div class="flex-1">
					<input
<<<<<<< HEAD
						class="w-full bg-transparent dark:text-gray-300 outline-hidden placeholder:opacity-30"
						type="password"
						bind:value={currentPassword}
						placeholder={$i18n.t('Enter your current password')}
=======
						class="w-full rounded py-2 px-4 text-sm dark:text-gray-300 dark:bg-gray-800 outline-none"
						type="password"
						bind:value={currentPassword}
>>>>>>> dfef03c8e (同步远程)
						autocomplete="current-password"
						required
					/>
				</div>
			</div>

			<div class="flex flex-col w-full">
				<div class=" mb-1 text-xs text-gray-500">{$i18n.t('New Password')}</div>

				<div class="flex-1">
					<input
<<<<<<< HEAD
						class="w-full bg-transparent text-sm dark:text-gray-300 outline-hidden placeholder:opacity-30"
						type="password"
						bind:value={newPassword}
						placeholder={$i18n.t('Enter your new password')}
=======
						class="w-full rounded py-2 px-4 text-sm dark:text-gray-300 dark:bg-gray-800 outline-none"
						type="password"
						bind:value={newPassword}
>>>>>>> dfef03c8e (同步远程)
						autocomplete="new-password"
						required
					/>
				</div>
			</div>

			<div class="flex flex-col w-full">
				<div class=" mb-1 text-xs text-gray-500">{$i18n.t('Confirm Password')}</div>

				<div class="flex-1">
					<input
<<<<<<< HEAD
						class="w-full bg-transparent text-sm dark:text-gray-300 outline-hidden placeholder:opacity-30"
						type="password"
						bind:value={newPasswordConfirm}
						placeholder={$i18n.t('Confirm your new password')}
=======
						class="w-full rounded py-2 px-4 text-sm dark:text-gray-300 dark:bg-gray-800 outline-none"
						type="password"
						bind:value={newPasswordConfirm}
>>>>>>> dfef03c8e (同步远程)
						autocomplete="off"
						required
					/>
				</div>
			</div>
		</div>

		<div class="mt-3 flex justify-end">
			<button
<<<<<<< HEAD
				class="px-3.5 py-1.5 text-sm font-medium bg-black hover:bg-gray-900 text-white dark:bg-white dark:text-black dark:hover:bg-gray-100 transition rounded-full"
=======
				class=" px-4 py-2 text-xs bg-gray-800 hover:bg-gray-900 dark:bg-gray-700 dark:hover:bg-gray-800 text-gray-100 transition rounded-md font-medium"
>>>>>>> dfef03c8e (同步远程)
			>
				{$i18n.t('Update password')}
			</button>
		</div>
	{/if}
</form>
