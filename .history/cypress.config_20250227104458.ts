import { defineConfig } from 'cypress';

export default defineConfig({
	e2e: {
		baseUrl: 'http://localhost:8080'

		// baseUrl: 'http://143.64.120.39:8080'
	},
	video: true
});
