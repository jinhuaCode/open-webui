<script lang="ts">
	import hljs from 'highlight.js';
	import { loadPyodide } from 'pyodide';
	import mermaid from 'mermaid';

	import { v4 as uuidv4 } from 'uuid';

<<<<<<< HEAD
	import {
		getContext,
		getAllContexts,
		onMount,
		tick,
		createEventDispatcher,
		onDestroy
	} from 'svelte';
=======
	import { getContext, getAllContexts, onMount, tick, createEventDispatcher } from 'svelte';
>>>>>>> dfef03c8e (同步远程)
	import { copyToClipboard } from '$lib/utils';

	import 'highlight.js/styles/github-dark.min.css';

	import PyodideWorker from '$lib/workers/pyodide.worker?worker';
	import CodeEditor from '$lib/components/common/CodeEditor.svelte';
	import SvgPanZoom from '$lib/components/common/SVGPanZoom.svelte';
<<<<<<< HEAD
	import { config } from '$lib/stores';
	import { executeCode } from '$lib/apis/utils';
	import { toast } from 'svelte-sonner';
=======
>>>>>>> dfef03c8e (同步远程)

	const i18n = getContext('i18n');
	const dispatch = createEventDispatcher();

	export let id = '';

	export let save = false;
	export let run = true;

	export let token;
	export let lang = '';
	export let code = '';
<<<<<<< HEAD
	export let attributes = {};
=======
>>>>>>> dfef03c8e (同步远程)

	export let className = 'my-2';
	export let editorClassName = '';
	export let stickyButtonsClassName = 'top-8';

<<<<<<< HEAD
	let pyodideWorker = null;

=======
>>>>>>> dfef03c8e (同步远程)
	let _code = '';
	$: if (code) {
		updateCode();
	}

	const updateCode = () => {
		_code = code;
	};

	let _token = null;

	let mermaidHtml = null;

	let highlightedCode = null;
	let executing = false;

	let stdout = null;
	let stderr = null;
	let result = null;
<<<<<<< HEAD
	let files = null;
=======
>>>>>>> dfef03c8e (同步远程)

	let copied = false;
	let saved = false;

	const saveCode = () => {
		saved = true;

		code = _code;
		dispatch('save', code);

		setTimeout(() => {
			saved = false;
		}, 1000);
	};

	const copyCode = async () => {
		copied = true;
		await copyToClipboard(code);

		setTimeout(() => {
			copied = false;
		}, 1000);
	};

	const checkPythonCode = (str) => {
		// Check if the string contains typical Python syntax characters
		const pythonSyntax = [
			'def ',
			'else:',
			'elif ',
			'try:',
			'except:',
			'finally:',
			'yield ',
			'lambda ',
			'assert ',
			'nonlocal ',
			'del ',
			'True',
			'False',
			'None',
			' and ',
			' or ',
			' not ',
			' in ',
			' is ',
			' with '
		];

		for (let syntax of pythonSyntax) {
			if (str.includes(syntax)) {
				return true;
			}
		}

		// If none of the above conditions met, it's probably not Python code
		return false;
	};

	const executePython = async (code) => {
<<<<<<< HEAD
=======
		if (!code.includes('input') && !code.includes('matplotlib')) {
			executePythonAsWorker(code);
		} else {
			result = null;
			stdout = null;
			stderr = null;

			executing = true;

			document.pyodideMplTarget = document.getElementById(`plt-canvas-${id}`);

			let pyodide = await loadPyodide({
				indexURL: '/pyodide/',
				stdout: (text) => {
					console.log('Python output:', text);

					if (stdout) {
						stdout += `${text}\n`;
					} else {
						stdout = `${text}\n`;
					}
				},
				stderr: (text) => {
					console.log('An error occurred:', text);
					if (stderr) {
						stderr += `${text}\n`;
					} else {
						stderr = `${text}\n`;
					}
				},
				packages: ['micropip']
			});

			try {
				const micropip = pyodide.pyimport('micropip');

				// await micropip.set_index_urls('https://pypi.org/pypi/{package_name}/json');

				let packages = [
					code.includes('requests') ? 'requests' : null,
					code.includes('bs4') ? 'beautifulsoup4' : null,
					code.includes('numpy') ? 'numpy' : null,
					code.includes('pandas') ? 'pandas' : null,
					code.includes('matplotlib') ? 'matplotlib' : null,
					code.includes('sklearn') ? 'scikit-learn' : null,
					code.includes('scipy') ? 'scipy' : null,
					code.includes('re') ? 'regex' : null,
					code.includes('seaborn') ? 'seaborn' : null
				].filter(Boolean);

				console.log(packages);
				await micropip.install(packages);

				result = await pyodide.runPythonAsync(`from js import prompt
def input(p):
    return prompt(p)
__builtins__.input = input`);

				result = await pyodide.runPython(code);

				if (!result) {
					result = '[NO OUTPUT]';
				}

				console.log(result);
				console.log(stdout);
				console.log(stderr);

				const pltCanvasElement = document.getElementById(`plt-canvas-${id}`);

				if (pltCanvasElement?.innerHTML !== '') {
					pltCanvasElement.classList.add('pt-4');
				}
			} catch (error) {
				console.error('Error:', error);
				stderr = error;
			}

			executing = false;
		}
	};

	const executePythonAsWorker = async (code) => {
>>>>>>> dfef03c8e (同步远程)
		result = null;
		stdout = null;
		stderr = null;

		executing = true;

<<<<<<< HEAD
		if ($config?.code?.engine === 'jupyter') {
			const output = await executeCode(localStorage.token, code).catch((error) => {
				toast.error(`${error}`);
				return null;
			});

			if (output) {
				if (output['stdout']) {
					stdout = output['stdout'];
					const stdoutLines = stdout.split('\n');

					for (const [idx, line] of stdoutLines.entries()) {
						if (line.startsWith('data:image/png;base64')) {
							if (files) {
								files.push({
									type: 'image/png',
									data: line
								});
							} else {
								files = [
									{
										type: 'image/png',
										data: line
									}
								];
							}

							if (stdout.startsWith(`${line}\n`)) {
								stdout = stdout.replace(`${line}\n`, ``);
							} else if (stdout.startsWith(`${line}`)) {
								stdout = stdout.replace(`${line}`, ``);
							}
						}
					}
				}

				if (output['result']) {
					result = output['result'];
					const resultLines = result.split('\n');

					for (const [idx, line] of resultLines.entries()) {
						if (line.startsWith('data:image/png;base64')) {
							if (files) {
								files.push({
									type: 'image/png',
									data: line
								});
							} else {
								files = [
									{
										type: 'image/png',
										data: line
									}
								];
							}

							if (result.startsWith(`${line}\n`)) {
								result = result.replace(`${line}\n`, ``);
							} else if (result.startsWith(`${line}`)) {
								result = result.replace(`${line}`, ``);
							}
						}
					}
				}

				output['stderr'] && (stderr = output['stderr']);
			}

			executing = false;
		} else {
			executePythonAsWorker(code);
		}
	};

	const executePythonAsWorker = async (code) => {
=======
>>>>>>> dfef03c8e (同步远程)
		let packages = [
			code.includes('requests') ? 'requests' : null,
			code.includes('bs4') ? 'beautifulsoup4' : null,
			code.includes('numpy') ? 'numpy' : null,
			code.includes('pandas') ? 'pandas' : null,
			code.includes('sklearn') ? 'scikit-learn' : null,
			code.includes('scipy') ? 'scipy' : null,
			code.includes('re') ? 'regex' : null,
<<<<<<< HEAD
			code.includes('seaborn') ? 'seaborn' : null,
			code.includes('sympy') ? 'sympy' : null,
			code.includes('tiktoken') ? 'tiktoken' : null,
			code.includes('matplotlib') ? 'matplotlib' : null,
			code.includes('pytz') ? 'pytz' : null
=======
			code.includes('seaborn') ? 'seaborn' : null
>>>>>>> dfef03c8e (同步远程)
		].filter(Boolean);

		console.log(packages);

<<<<<<< HEAD
		pyodideWorker = new PyodideWorker();
=======
		const pyodideWorker = new PyodideWorker();
>>>>>>> dfef03c8e (同步远程)

		pyodideWorker.postMessage({
			id: id,
			code: code,
			packages: packages
		});

		setTimeout(() => {
			if (executing) {
				executing = false;
				stderr = 'Execution Time Limit Exceeded';
				pyodideWorker.terminate();
			}
		}, 60000);

		pyodideWorker.onmessage = (event) => {
			console.log('pyodideWorker.onmessage', event);
			const { id, ...data } = event.data;

			console.log(id, data);

<<<<<<< HEAD
			if (data['stdout']) {
				stdout = data['stdout'];
				const stdoutLines = stdout.split('\n');

				for (const [idx, line] of stdoutLines.entries()) {
					if (line.startsWith('data:image/png;base64')) {
						if (files) {
							files.push({
								type: 'image/png',
								data: line
							});
						} else {
							files = [
								{
									type: 'image/png',
									data: line
								}
							];
						}

						if (stdout.startsWith(`${line}\n`)) {
							stdout = stdout.replace(`${line}\n`, ``);
						} else if (stdout.startsWith(`${line}`)) {
							stdout = stdout.replace(`${line}`, ``);
						}
					}
				}
			}

			if (data['result']) {
				result = data['result'];
				const resultLines = result.split('\n');

				for (const [idx, line] of resultLines.entries()) {
					if (line.startsWith('data:image/png;base64')) {
						if (files) {
							files.push({
								type: 'image/png',
								data: line
							});
						} else {
							files = [
								{
									type: 'image/png',
									data: line
								}
							];
						}

						if (result.startsWith(`${line}\n`)) {
							result = result.replace(`${line}\n`, ``);
						} else if (result.startsWith(`${line}`)) {
							result = result.replace(`${line}`, ``);
						}
					}
				}
			}

=======
			data['stdout'] && (stdout = data['stdout']);
>>>>>>> dfef03c8e (同步远程)
			data['stderr'] && (stderr = data['stderr']);
			data['result'] && (result = data['result']);

			executing = false;
		};

		pyodideWorker.onerror = (event) => {
			console.log('pyodideWorker.onerror', event);
			executing = false;
		};
	};

	let debounceTimeout;

	const drawMermaidDiagram = async () => {
		try {
			if (await mermaid.parse(code)) {
				const { svg } = await mermaid.render(`mermaid-${uuidv4()}`, code);
				mermaidHtml = svg;
			}
		} catch (error) {
			console.log('Error:', error);
		}
	};

	const render = async () => {
		if (lang === 'mermaid' && (token?.raw ?? '').slice(-4).includes('```')) {
			(async () => {
				await drawMermaidDiagram();
			})();
		}
	};

	$: if (token) {
		if (JSON.stringify(token) !== JSON.stringify(_token)) {
			_token = token;
		}
	}

	$: if (_token) {
		render();
	}

	$: dispatch('code', { lang, code });

<<<<<<< HEAD
	$: if (attributes) {
		onAttributesUpdate();
	}

	const onAttributesUpdate = () => {
		if (attributes?.output) {
			// Create a helper function to unescape HTML entities
			const unescapeHtml = (html) => {
				const textArea = document.createElement('textarea');
				textArea.innerHTML = html;
				return textArea.value;
			};

			try {
				// Unescape the HTML-encoded string
				const unescapedOutput = unescapeHtml(attributes.output);

				// Parse the unescaped string into JSON
				const output = JSON.parse(unescapedOutput);

				// Assign the parsed values to variables
				stdout = output.stdout;
				stderr = output.stderr;
				result = output.result;
			} catch (error) {
				console.error('Error:', error);
			}
		}
	};

=======
>>>>>>> dfef03c8e (同步远程)
	onMount(async () => {
		console.log('codeblock', lang, code);

		if (lang) {
			dispatch('code', { lang, code });
		}
		if (document.documentElement.classList.contains('dark')) {
			mermaid.initialize({
				startOnLoad: true,
				theme: 'dark',
				securityLevel: 'loose'
			});
		} else {
			mermaid.initialize({
				startOnLoad: true,
				theme: 'default',
				securityLevel: 'loose'
			});
		}
	});
<<<<<<< HEAD

	onDestroy(() => {
		if (pyodideWorker) {
			pyodideWorker.terminate();
		}
	});
=======
>>>>>>> dfef03c8e (同步远程)
</script>

<div>
	<div class="relative {className} flex flex-col rounded-lg" dir="ltr">
		{#if lang === 'mermaid'}
			{#if mermaidHtml}
				<SvgPanZoom
<<<<<<< HEAD
					className=" border border-gray-100 dark:border-gray-850 rounded-lg max-h-fit overflow-hidden"
=======
					className=" border border-gray-50 dark:border-gray-850 rounded-lg max-h-fit overflow-hidden"
>>>>>>> dfef03c8e (同步远程)
					svg={mermaidHtml}
					content={_token.text}
				/>
			{:else}
				<pre class="mermaid">{code}</pre>
			{/if}
		{:else}
			<div class="text-text-300 absolute pl-4 py-1.5 text-xs font-medium dark:text-white">
				{lang}
			</div>

			<div
				class="sticky {stickyButtonsClassName} mb-1 py-1 pr-2.5 flex items-center justify-end z-10 text-xs text-black dark:text-white"
			>
				<div class="flex items-center gap-0.5 translate-y-[1px]">
					{#if lang.toLowerCase() === 'python' || lang.toLowerCase() === 'py' || (lang === '' && checkPythonCode(code))}
						{#if executing}
							<div class="run-code-button bg-none border-none p-1 cursor-not-allowed">Running</div>
						{:else if run}
							<button
								class="run-code-button bg-none border-none bg-gray-50 hover:bg-gray-100 dark:bg-gray-850 dark:hover:bg-gray-800 transition rounded-md px-1.5 py-0.5"
								on:click={async () => {
									code = _code;
									await tick();
									executePython(code);
								}}>{$i18n.t('Run')}</button
							>
						{/if}
					{/if}

					{#if save}
						<button
							class="save-code-button bg-none border-none bg-gray-50 hover:bg-gray-100 dark:bg-gray-850 dark:hover:bg-gray-800 transition rounded-md px-1.5 py-0.5"
							on:click={saveCode}
						>
							{saved ? $i18n.t('Saved') : $i18n.t('Save')}
						</button>
					{/if}

					<button
						class="copy-code-button bg-none border-none bg-gray-50 hover:bg-gray-100 dark:bg-gray-850 dark:hover:bg-gray-800 transition rounded-md px-1.5 py-0.5"
						on:click={copyCode}>{copied ? $i18n.t('Copied') : $i18n.t('Copy')}</button
					>
				</div>
			</div>

			<div
				class="language-{lang} rounded-t-lg -mt-8 {editorClassName
					? editorClassName
					: executing || stdout || stderr || result
						? ''
						: 'rounded-b-lg'} overflow-hidden"
			>
				<div class=" pt-7 bg-gray-50 dark:bg-gray-850"></div>
				<CodeEditor
					value={code}
					{id}
					{lang}
					on:save={() => {
						saveCode();
					}}
					on:change={(e) => {
						_code = e.detail.value;
					}}
				/>
			</div>

			<div
				id="plt-canvas-{id}"
<<<<<<< HEAD
				class="bg-gray-50 dark:bg-[#202123] dark:text-white max-w-full overflow-x-auto scrollbar-hidden"
			/>

			{#if executing || stdout || stderr || result || files}
				<div
					class="bg-gray-50 dark:bg-[#202123] dark:text-white rounded-b-lg! py-4 px-4 flex flex-col gap-2"
				>
					{#if executing}
						<div class=" ">
							<div class=" text-gray-500 text-xs mb-1">STDOUT/STDERR</div>
							<div class="text-sm">Running...</div>
						</div>
					{:else}
						{#if stdout || stderr}
							<div class=" ">
								<div class=" text-gray-500 text-xs mb-1">STDOUT/STDERR</div>
								<div
									class="text-sm {stdout?.split('\n')?.length > 100
										? `max-h-96`
										: ''}  overflow-y-auto"
								>
									{stdout || stderr}
								</div>
							</div>
						{/if}
						{#if result || files}
							<div class=" ">
								<div class=" text-gray-500 text-xs mb-1">RESULT</div>
								{#if result}
									<div class="text-sm">{`${JSON.stringify(result)}`}</div>
								{/if}
								{#if files}
									<div class="flex flex-col gap-2">
										{#each files as file}
											{#if file.type.startsWith('image')}
												<img src={file.data} alt="Output" />
											{/if}
										{/each}
									</div>
								{/if}
							</div>
						{/if}
					{/if}
=======
				class="bg-[#202123] text-white max-w-full overflow-x-auto scrollbar-hidden"
			/>

			{#if executing}
				<div class="bg-[#202123] text-white px-4 py-4 rounded-b-lg">
					<div class=" text-gray-500 text-xs mb-1">STDOUT/STDERR</div>
					<div class="text-sm">Running...</div>
				</div>
			{:else if stdout || stderr || result}
				<div class="bg-[#202123] text-white px-4 py-4 rounded-b-lg">
					<div class=" text-gray-500 text-xs mb-1">STDOUT/STDERR</div>
					<div class="text-sm">{stdout || stderr || result}</div>
>>>>>>> dfef03c8e (同步远程)
				</div>
			{/if}
		{/if}
	</div>
</div>
