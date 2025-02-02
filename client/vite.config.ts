import { sveltekit } from '@sveltejs/kit/vite';
import { defineConfig } from 'vite';

export default defineConfig({
	plugins: [sveltekit()],
	server: {
		allowedHosts: ['calyps.io'],
		fs: {
		  allow: [
			'/usr/src/app/static', // Add this line to allow access to the static directory
			// other allowed directories can stay here if needed
		  ]
		},
	}
});
