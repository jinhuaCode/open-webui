// Helper function to find matching closing tag
<<<<<<< HEAD
function findMatchingClosingTag(src: string, openTag: string, closeTag: string): number {
=======
function findMatchingClosingTag(src, openTag, closeTag) {
>>>>>>> dfef03c8e (同步远程)
	let depth = 1;
	let index = openTag.length;
	while (depth > 0 && index < src.length) {
		if (src.startsWith(openTag, index)) {
			depth++;
		} else if (src.startsWith(closeTag, index)) {
			depth--;
		}
		if (depth > 0) {
			index++;
		}
	}
	return depth === 0 ? index + closeTag.length : -1;
}

<<<<<<< HEAD
// Function to parse attributes from tag
function parseAttributes(tag: string): { [key: string]: string } {
	const attributes: { [key: string]: string } = {};
	const attrRegex = /(\w+)="(.*?)"/g;
	let match;
	while ((match = attrRegex.exec(tag)) !== null) {
		attributes[match[1]] = match[2];
	}
	return attributes;
}

function detailsTokenizer(src: string) {
	// Updated regex to capture attributes inside <details>
	const detailsRegex = /^<details(\s+[^>]*)?>\n/;
	const summaryRegex = /^<summary>(.*?)<\/summary>\n/;

	const detailsMatch = detailsRegex.exec(src);
	if (detailsMatch) {
		const endIndex = findMatchingClosingTag(src, '<details', '</details>');
		if (endIndex === -1) return;

		const fullMatch = src.slice(0, endIndex);
		const detailsTag = detailsMatch[0];
		const attributes = parseAttributes(detailsTag); // Parse attributes from <details>

		let content = fullMatch.slice(detailsTag.length, -10).trim(); // Remove <details> and </details>
		let summary = '';

=======
function detailsTokenizer(src) {
	const detailsRegex = /^<details>\n/;
	const summaryRegex = /^<summary>(.*?)<\/summary>\n/;

	if (detailsRegex.test(src)) {
		const endIndex = findMatchingClosingTag(src, '<details>', '</details>');
		if (endIndex === -1) return;

		const fullMatch = src.slice(0, endIndex);
		let content = fullMatch.slice(10, -10).trim(); // Remove <details> and </details>

		let summary = '';
>>>>>>> dfef03c8e (同步远程)
		const summaryMatch = summaryRegex.exec(content);
		if (summaryMatch) {
			summary = summaryMatch[1].trim();
			content = content.slice(summaryMatch[0].length).trim();
		}

		return {
			type: 'details',
			raw: fullMatch,
			summary: summary,
<<<<<<< HEAD
			text: content,
			attributes: attributes // Include extracted attributes from <details>
=======
			text: content
>>>>>>> dfef03c8e (同步远程)
		};
	}
}

<<<<<<< HEAD
function detailsStart(src: string) {
	return src.match(/^<details>/) ? 0 : -1;
}

function detailsRenderer(token: any) {
	const attributesString = token.attributes
		? Object.entries(token.attributes)
				.map(([key, value]) => `${key}="${value}"`)
				.join(' ')
		: '';

	return `<details ${attributesString}>
=======
function detailsStart(src) {
	return src.match(/^<details>/) ? 0 : -1;
}

function detailsRenderer(token) {
	return `<details>
>>>>>>> dfef03c8e (同步远程)
  ${token.summary ? `<summary>${token.summary}</summary>` : ''}
  ${token.text}
  </details>`;
}

<<<<<<< HEAD
// Extension wrapper function
=======
>>>>>>> dfef03c8e (同步远程)
function detailsExtension() {
	return {
		name: 'details',
		level: 'block',
		start: detailsStart,
		tokenizer: detailsTokenizer,
		renderer: detailsRenderer
	};
}

export default function (options = {}) {
	return {
		extensions: [detailsExtension(options)]
	};
}
