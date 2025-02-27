<script lang="ts">
	import DOMPurify from 'dompurify';
	import { createEventDispatcher, onMount, getContext } from 'svelte';
	const i18n = getContext('i18n');

	import fileSaver from 'file-saver';
	const { saveAs } = fileSaver;

	import { marked, type Token } from 'marked';
<<<<<<< HEAD
	import { unescapeHtml } from '$lib/utils';
=======
	import { revertSanitizedResponseContent, unescapeHtml } from '$lib/utils';
>>>>>>> dfef03c8e (同步远程)

	import { WEBUI_BASE_URL } from '$lib/constants';

	import CodeBlock from '$lib/components/chat/Messages/CodeBlock.svelte';
	import MarkdownInlineTokens from '$lib/components/chat/Messages/Markdown/MarkdownInlineTokens.svelte';
	import KatexRenderer from './KatexRenderer.svelte';
	import Collapsible from '$lib/components/common/Collapsible.svelte';
	import Tooltip from '$lib/components/common/Tooltip.svelte';
	import ArrowDownTray from '$lib/components/icons/ArrowDownTray.svelte';

	const dispatch = createEventDispatcher();

	export let id: string;
	export let tokens: Token[];
	export let top = true;
<<<<<<< HEAD
	export let attributes = {};

	export let save = false;

	export let onTaskClick: Function = () => {};
=======

	export let save = false;
>>>>>>> dfef03c8e (同步远程)
	export let onSourceClick: Function = () => {};

	const headerComponent = (depth: number) => {
		return 'h' + depth;
	};

	const exportTableToCSVHandler = (token, tokenIdx = 0) => {
		console.log('Exporting table to CSV');

<<<<<<< HEAD
		// Extract header row text and escape for CSV.
		const header = token.header.map((headerCell) => `"${headerCell.text.replace(/"/g, '""')}"`);

		// Create an array for rows that will hold the mapped cell text.
		const rows = token.rows.map((row) =>
			row.map((cell) => {
				// Map tokens into a single text
				const cellContent = cell.tokens.map((token) => token.text).join('');
				// Escape double quotes and wrap the content in double quotes
				return `"${cellContent.replace(/"/g, '""')}"`;
			})
		);

		// Combine header and rows
		const csvData = [header, ...rows];

		// Join the rows using commas (,) as the separator and rows using newline (\n).
		const csvContent = csvData.map((row) => row.join(',')).join('\n');

		// Log rows and CSV content to ensure everything is correct.
		console.log(csvData);
=======
		// Create an array for rows that will hold the mapped cell text.
		const rows = token.rows.map((row) =>
			row.map((cell) => cell.tokens.map((token) => token.text).join(''))
		);

		// Join the rows using commas (,) as the separator and rows using newline (\n).
		const csvContent = rows.map((row) => row.join(',')).join('\n');

		// Log rows and CSV content to ensure everything is correct.
		console.log(rows);
>>>>>>> dfef03c8e (同步远程)
		console.log(csvContent);

		// To handle Unicode characters, you need to prefix the data with a BOM:
		const bom = '\uFEFF'; // BOM for UTF-8

		// Create a new Blob prefixed with the BOM to ensure proper Unicode encoding.
		const blob = new Blob([bom + csvContent], { type: 'text/csv;charset=UTF-8' });

		// Use FileSaver.js's saveAs function to save the generated CSV file.
		saveAs(blob, `table-${id}-${tokenIdx}.csv`);
	};
</script>

<!-- {JSON.stringify(tokens)} -->
{#each tokens as token, tokenIdx (tokenIdx)}
	{#if token.type === 'hr'}
<<<<<<< HEAD
		<hr class=" border-gray-100 dark:border-gray-850" />
	{:else if token.type === 'heading'}
		<svelte:element this={headerComponent(token.depth)} dir="auto">
=======
		<hr class=" border-gray-50 dark:border-gray-850" />
	{:else if token.type === 'heading'}
		<svelte:element this={headerComponent(token.depth)}>
>>>>>>> dfef03c8e (同步远程)
			<MarkdownInlineTokens id={`${id}-${tokenIdx}-h`} tokens={token.tokens} {onSourceClick} />
		</svelte:element>
	{:else if token.type === 'code'}
		{#if token.raw.includes('```')}
			<CodeBlock
				id={`${id}-${tokenIdx}`}
				{token}
				lang={token?.lang ?? ''}
<<<<<<< HEAD
				code={token?.text ?? ''}
				{attributes}
=======
				code={revertSanitizedResponseContent(token?.text ?? '')}
>>>>>>> dfef03c8e (同步远程)
				{save}
				on:code={(e) => {
					dispatch('code', e.detail);
				}}
				on:save={(e) => {
					dispatch('update', {
						raw: token.raw,
						oldContent: token.text,
						newContent: e.detail
					});
				}}
			/>
		{:else}
			{token.text}
		{/if}
	{:else if token.type === 'table'}
		<div class="relative w-full group">
			<div class="scrollbar-hidden relative overflow-x-auto max-w-full rounded-lg">
				<table
					class=" w-full text-sm text-left text-gray-500 dark:text-gray-400 max-w-full rounded-xl"
				>
					<thead
						class="text-xs text-gray-700 uppercase bg-gray-50 dark:bg-gray-850 dark:text-gray-400 border-none"
					>
						<tr class="">
							{#each token.header as header, headerIdx}
								<th
									scope="col"
<<<<<<< HEAD
									class="px-3! py-1.5! cursor-pointer border border-gray-100 dark:border-gray-850"
									style={token.align[headerIdx] ? '' : `text-align: ${token.align[headerIdx]}`}
								>
									<div class="flex flex-col gap-1.5 text-left">
										<div class="shrink-0 break-normal">
=======
									class="!px-3 !py-1.5 cursor-pointer select-none border border-gray-50 dark:border-gray-850"
									style={token.align[headerIdx] ? '' : `text-align: ${token.align[headerIdx]}`}
								>
									<div class="flex flex-col gap-1.5 text-left">
										<div class="flex-shrink-0 break-normal">
>>>>>>> dfef03c8e (同步远程)
											<MarkdownInlineTokens
												id={`${id}-${tokenIdx}-header-${headerIdx}`}
												tokens={header.tokens}
												{onSourceClick}
											/>
										</div>
									</div>
								</th>
							{/each}
						</tr>
					</thead>
					<tbody>
						{#each token.rows as row, rowIdx}
							<tr class="bg-white dark:bg-gray-900 dark:border-gray-850 text-xs">
								{#each row ?? [] as cell, cellIdx}
									<td
<<<<<<< HEAD
										class="px-3! py-1.5! text-gray-900 dark:text-white w-max border border-gray-100 dark:border-gray-850"
=======
										class="!px-3 !py-1.5 text-gray-900 dark:text-white w-max border border-gray-50 dark:border-gray-850"
>>>>>>> dfef03c8e (同步远程)
										style={token.align[cellIdx] ? '' : `text-align: ${token.align[cellIdx]}`}
									>
										<div class="flex flex-col break-normal">
											<MarkdownInlineTokens
												id={`${id}-${tokenIdx}-row-${rowIdx}-${cellIdx}`}
												tokens={cell.tokens}
												{onSourceClick}
											/>
										</div>
									</td>
								{/each}
							</tr>
						{/each}
					</tbody>
				</table>
			</div>

			<div class=" absolute top-1 right-1.5 z-20 invisible group-hover:visible">
				<Tooltip content={$i18n.t('Export to CSV')}>
					<button
						class="p-1 rounded-lg bg-transparent transition"
						on:click={(e) => {
							e.stopPropagation();
							exportTableToCSVHandler(token, tokenIdx);
						}}
					>
						<ArrowDownTray className=" size-3.5" strokeWidth="1.5" />
					</button>
				</Tooltip>
			</div>
		</div>
	{:else if token.type === 'blockquote'}
<<<<<<< HEAD
		<blockquote dir="auto">
			<svelte:self id={`${id}-${tokenIdx}`} tokens={token.tokens} {onTaskClick} {onSourceClick} />
=======
		<blockquote>
			<svelte:self id={`${id}-${tokenIdx}`} tokens={token.tokens} />
>>>>>>> dfef03c8e (同步远程)
		</blockquote>
	{:else if token.type === 'list'}
		{#if token.ordered}
			<ol start={token.start || 1}>
				{#each token.items as item, itemIdx}
<<<<<<< HEAD
					<li dir="auto" class="text-start">
						{#if item?.task}
							<input
								class=" translate-y-[1px] -translate-x-1"
								type="checkbox"
								checked={item.checked}
								on:change={(e) => {
									onTaskClick({
										id: id,
										token: token,
										tokenIdx: tokenIdx,
										item: item,
										itemIdx: itemIdx,
										checked: e.target.checked
									});
								}}
							/>
						{/if}

=======
					<li>
>>>>>>> dfef03c8e (同步远程)
						<svelte:self
							id={`${id}-${tokenIdx}-${itemIdx}`}
							tokens={item.tokens}
							top={token.loose}
<<<<<<< HEAD
							{onTaskClick}
							{onSourceClick}
=======
>>>>>>> dfef03c8e (同步远程)
						/>
					</li>
				{/each}
			</ol>
		{:else}
			<ul>
				{#each token.items as item, itemIdx}
<<<<<<< HEAD
					<li dir="auto" class="text-start">
						{#if item?.task}
							<input
								class=" translate-y-[1px] -translate-x-1"
								type="checkbox"
								checked={item.checked}
								on:change={(e) => {
									onTaskClick({
										id: id,
										token: token,
										tokenIdx: tokenIdx,
										item: item,
										itemIdx: itemIdx,
										checked: e.target.checked
									});
								}}
							/>
						{/if}

=======
					<li>
>>>>>>> dfef03c8e (同步远程)
						<svelte:self
							id={`${id}-${tokenIdx}-${itemIdx}`}
							tokens={item.tokens}
							top={token.loose}
<<<<<<< HEAD
							{onTaskClick}
							{onSourceClick}
=======
>>>>>>> dfef03c8e (同步远程)
						/>
					</li>
				{/each}
			</ul>
		{/if}
	{:else if token.type === 'details'}
<<<<<<< HEAD
		<Collapsible
			title={token.summary}
			attributes={token?.attributes}
			className="w-full space-y-1"
			dir="auto"
		>
			<div class=" mb-1.5" slot="content">
				<svelte:self
					id={`${id}-${tokenIdx}-d`}
					tokens={marked.lexer(token.text)}
					attributes={token?.attributes}
					{onTaskClick}
					{onSourceClick}
				/>
=======
		<Collapsible title={token.summary} className="w-fit space-y-1">
			<div class=" mb-1.5" slot="content">
				<svelte:self id={`${id}-${tokenIdx}-d`} tokens={marked.lexer(token.text)} />
>>>>>>> dfef03c8e (同步远程)
			</div>
		</Collapsible>
	{:else if token.type === 'html'}
		{@const html = DOMPurify.sanitize(token.text)}
		{#if html && html.includes('<video')}
			{@html html}
		{:else if token.text.includes(`<iframe src="${WEBUI_BASE_URL}/api/v1/files/`)}
			{@html `${token.text}`}
		{:else}
			{token.text}
		{/if}
	{:else if token.type === 'iframe'}
		<iframe
			src="{WEBUI_BASE_URL}/api/v1/files/{token.fileId}/content"
			title={token.fileId}
			width="100%"
			frameborder="0"
			onload="this.style.height=(this.contentWindow.document.body.scrollHeight+20)+'px';"
		></iframe>
	{:else if token.type === 'paragraph'}
<<<<<<< HEAD
		<p dir="auto">
=======
		<p>
>>>>>>> dfef03c8e (同步远程)
			<MarkdownInlineTokens
				id={`${id}-${tokenIdx}-p`}
				tokens={token.tokens ?? []}
				{onSourceClick}
			/>
		</p>
	{:else if token.type === 'text'}
		{#if top}
<<<<<<< HEAD
			<p dir="auto">
=======
			<p>
>>>>>>> dfef03c8e (同步远程)
				{#if token.tokens}
					<MarkdownInlineTokens id={`${id}-${tokenIdx}-t`} tokens={token.tokens} {onSourceClick} />
				{:else}
					{unescapeHtml(token.text)}
				{/if}
			</p>
		{:else if token.tokens}
			<MarkdownInlineTokens
				id={`${id}-${tokenIdx}-p`}
				tokens={token.tokens ?? []}
				{onSourceClick}
			/>
		{:else}
			{unescapeHtml(token.text)}
		{/if}
	{:else if token.type === 'inlineKatex'}
		{#if token.text}
<<<<<<< HEAD
			<KatexRenderer content={token.text} displayMode={token?.displayMode ?? false} />
		{/if}
	{:else if token.type === 'blockKatex'}
		{#if token.text}
			<KatexRenderer content={token.text} displayMode={token?.displayMode ?? false} />
=======
			<KatexRenderer
				content={revertSanitizedResponseContent(token.text)}
				displayMode={token?.displayMode ?? false}
			/>
		{/if}
	{:else if token.type === 'blockKatex'}
		{#if token.text}
			<KatexRenderer
				content={revertSanitizedResponseContent(token.text)}
				displayMode={token?.displayMode ?? false}
			/>
>>>>>>> dfef03c8e (同步远程)
		{/if}
	{:else if token.type === 'space'}
		<div class="my-2" />
	{:else}
		{console.log('Unknown token', token)}
	{/if}
{/each}
