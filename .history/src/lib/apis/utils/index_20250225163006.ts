import { WEBUI_API_BASE_URL } from '$lib/constants';

<<<<<<< HEAD
export const getGravatarUrl = async (token: string, email: string) => {
=======
export const getGravatarUrl = async (email: string) => {
>>>>>>> dfef03c8e (同步远程)
	let error = null;

	const res = await fetch(`${WEBUI_API_BASE_URL}/utils/gravatar?email=${email}`, {
		method: 'GET',
		headers: {
<<<<<<< HEAD
			'Content-Type': 'application/json',
			Authorization: `Bearer ${token}`
=======
			'Content-Type': 'application/json'
>>>>>>> dfef03c8e (同步远程)
		}
	})
		.then(async (res) => {
			if (!res.ok) throw await res.json();
			return res.json();
		})
		.catch((err) => {
			console.log(err);
			error = err;
			return null;
		});

	return res;
};

<<<<<<< HEAD
export const executeCode = async (token: string, code: string) => {
	let error = null;

	const res = await fetch(`${WEBUI_API_BASE_URL}/utils/code/execute`, {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json',
			Authorization: `Bearer ${token}`
		},
		body: JSON.stringify({
			code: code
		})
	})
		.then(async (res) => {
			if (!res.ok) throw await res.json();
			return res.json();
		})
		.catch((err) => {
			console.log(err);

			error = err;
			if (err.detail) {
				error = err.detail;
			}
			return null;
		});

	if (error) {
		throw error;
	}

	return res;
};

export const formatPythonCode = async (token: string, code: string) => {
=======
export const formatPythonCode = async (code: string) => {
>>>>>>> dfef03c8e (同步远程)
	let error = null;

	const res = await fetch(`${WEBUI_API_BASE_URL}/utils/code/format`, {
		method: 'POST',
		headers: {
<<<<<<< HEAD
			'Content-Type': 'application/json',
			Authorization: `Bearer ${token}`
=======
			'Content-Type': 'application/json'
>>>>>>> dfef03c8e (同步远程)
		},
		body: JSON.stringify({
			code: code
		})
	})
		.then(async (res) => {
			if (!res.ok) throw await res.json();
			return res.json();
		})
		.catch((err) => {
			console.log(err);

			error = err;
			if (err.detail) {
				error = err.detail;
			}
			return null;
		});

	if (error) {
		throw error;
	}

	return res;
};

<<<<<<< HEAD
export const downloadChatAsPDF = async (token: string, title: string, messages: object[]) => {
=======
export const downloadChatAsPDF = async (title: string, messages: object[]) => {
>>>>>>> dfef03c8e (同步远程)
	let error = null;

	const blob = await fetch(`${WEBUI_API_BASE_URL}/utils/pdf`, {
		method: 'POST',
		headers: {
<<<<<<< HEAD
			'Content-Type': 'application/json',
			Authorization: `Bearer ${token}`
=======
			'Content-Type': 'application/json'
>>>>>>> dfef03c8e (同步远程)
		},
		body: JSON.stringify({
			title: title,
			messages: messages
		})
	})
		.then(async (res) => {
			if (!res.ok) throw await res.json();
			return res.blob();
		})
		.catch((err) => {
			console.log(err);
			error = err;
			return null;
		});

	return blob;
};

<<<<<<< HEAD
export const getHTMLFromMarkdown = async (token: string, md: string) => {
=======
export const getHTMLFromMarkdown = async (md: string) => {
>>>>>>> dfef03c8e (同步远程)
	let error = null;

	const res = await fetch(`${WEBUI_API_BASE_URL}/utils/markdown`, {
		method: 'POST',
		headers: {
<<<<<<< HEAD
			'Content-Type': 'application/json',
			Authorization: `Bearer ${token}`
=======
			'Content-Type': 'application/json'
>>>>>>> dfef03c8e (同步远程)
		},
		body: JSON.stringify({
			md: md
		})
	})
		.then(async (res) => {
			if (!res.ok) throw await res.json();
			return res.json();
		})
		.catch((err) => {
			console.log(err);
			error = err;
			return null;
		});

	return res.html;
};

export const downloadDatabase = async (token: string) => {
	let error = null;

	const res = await fetch(`${WEBUI_API_BASE_URL}/utils/db/download`, {
		method: 'GET',
		headers: {
			'Content-Type': 'application/json',
			Authorization: `Bearer ${token}`
		}
	})
		.then(async (response) => {
			if (!response.ok) {
				throw await response.json();
			}
			return response.blob();
		})
		.then((blob) => {
			const url = window.URL.createObjectURL(blob);
			const a = document.createElement('a');
			a.href = url;
			a.download = 'webui.db';
			document.body.appendChild(a);
			a.click();
			window.URL.revokeObjectURL(url);
		})
		.catch((err) => {
			console.log(err);
			error = err.detail;
			return null;
		});

	if (error) {
		throw error;
	}
};

export const downloadLiteLLMConfig = async (token: string) => {
	let error = null;

	const res = await fetch(`${WEBUI_API_BASE_URL}/utils/litellm/config`, {
		method: 'GET',
		headers: {
			'Content-Type': 'application/json',
			Authorization: `Bearer ${token}`
		}
	})
		.then(async (response) => {
			if (!response.ok) {
				throw await response.json();
			}
			return response.blob();
		})
		.then((blob) => {
			const url = window.URL.createObjectURL(blob);
			const a = document.createElement('a');
			a.href = url;
			a.download = 'config.yaml';
			document.body.appendChild(a);
			a.click();
			window.URL.revokeObjectURL(url);
		})
		.catch((err) => {
			console.log(err);
			error = err.detail;
			return null;
		});

	if (error) {
		throw error;
	}
};
