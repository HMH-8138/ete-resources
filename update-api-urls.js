#!/usr/bin/env node

/**
 * Script to update API URLs in all HTML files
 * Usage: node update-api-urls.js <new_api_url>
 * Examples:
 *   node update-api-urls.js https://myusername.pythonanywhere.com
 *   node update-api-urls.js https://ete-resource-backend.onrender.com
 *   node update-api-urls.js http://localhost:3000
 */

const fs = require('fs');
const path = require('path');

const apiUrl = process.argv[2];

if (!apiUrl) {
    console.error('❌ Error: Please provide the new API URL');
    console.error('Usage: node update-api-urls.js <new_api_url>');
    console.error('\nExamples:');
    console.error('  node update-api-urls.js https://myusername.pythonanywhere.com');
    console.error('  node update-api-urls.js https://ete-resource-backend.onrender.com');
    console.error('  node update-api-urls.js http://localhost:3000');
    process.exit(1);
}

// Normalize URL (remove trailing slash)
const normalizedUrl = apiUrl.replace(/\/$/, '');
const apiRoute = `${normalizedUrl}/api`;
const uploadRoute = `${normalizedUrl}/uploads`;

// HTML files to update
const htmlFiles = [
    'admin_login.html',
    'admin_new.html',
    'login.html',
    'materials.html',
    'my-uploads.html',
    'register.html',
    'student_login.html',
    'upload.html'
];

const frontendDir = path.join(__dirname, 'ETE_resourse_sharing_website');

let updateCount = 0;
let fileCount = 0;

htmlFiles.forEach(file => {
    const filePath = path.join(frontendDir, file);
    
    if (!fs.existsSync(filePath)) {
        console.warn(`⚠️  File not found: ${file}`);
        return;
    }

    let content = fs.readFileSync(filePath, 'utf8');
    let fileUpdates = 0;

    // Replace API URL - matches both localhost and remote URLs
    const apiUrlRegex = /const API_URL = ['"]https?:\/\/[^'"]+\/api['"]/g;
    const apiMatches = content.match(apiUrlRegex);
    if (apiMatches) {
        content = content.replace(apiUrlRegex, `const API_URL = '${apiRoute}'`);
        fileUpdates += apiMatches.length;
    }

    // Replace upload URLs in links - matches both localhost and remote URLs
    const uploadUrlRegex = /https?:\/\/[^/]+\/uploads\//g;
    const uploadMatches = content.match(uploadUrlRegex);
    if (uploadMatches) {
        content = content.replace(uploadUrlRegex, `${uploadRoute}/`);
        fileUpdates += uploadMatches.length;
    }

    if (fileUpdates > 0) {
        fs.writeFileSync(filePath, content, 'utf8');
        console.log(`✅ ${file} - Updated ${fileUpdates} URL(s)`);
        updateCount += fileUpdates;
        fileCount++;
    } else {
        console.log(`⏭️  ${file} - No updates needed`);
    }
});

console.log(`\n📊 Summary:`);
console.log(`   Files updated: ${fileCount}`);
console.log(`   Total URLs replaced: ${updateCount}`);
console.log(`\n✨ All API URLs have been updated to: ${apiRoute}`);
console.log(`📤 All upload URLs have been updated to: ${uploadRoute}`);
