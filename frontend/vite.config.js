import {fileURLToPath, URL} from 'node:url'
import {defineConfig} from 'vite'
import tailwindcss from '@tailwindcss/vite'
import {resolve} from 'path'

export default defineConfig({
    plugins: [
        tailwindcss(),
    ],

    base: '/static/',
    server: {
        port: 3000,
        host: 'localhost',
        cors: true,
    },
    build: {
        outDir: '../backend/static/',
        assetsDir: 'assets',
        emptyOutDir: true,
        manifest: 'manifest.json',
        rollupOptions: {
            input: {
                // eslint-disable-next-line no-undef
                main: resolve(__dirname, 'js/main.js'),
            },
            output: {
                entryFileNames: 'assets/[name]-[hash].js',
                chunkFileNames: 'assets/[name]-[hash].js',
                assetFileNames: 'assets/[name]-[hash].[ext]'
            }
        },
    },
})